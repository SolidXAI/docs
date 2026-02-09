---
sidebar_position: 14
title: SMS Providers
description: Learn how to create and configure custom SMS providers in SolidX.
summary: Introduction to creating and configuring custom SMS providers in SolidX for sending text messages via third-party services. Implementation details pending future documentation updates.
keywords: [backend, sms providers, customization]
solidx_concerns: [new_sms_provider]
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<!-- # 📲 SMS Providers -->

## Overview

SolidX ships with an SMS provider that uses **Msg91** for sending messages. It supports both **synchronous** sending and **asynchronous** (queued/background) delivery.
It includes flows for **transactional** SMS and **OTP** SMS (Msg91 offers distinct APIs for each).

Configure your Msg91 credentials in your `.env` to use the built‑in provider.

If you prefer another provider, SolidX exposes **clean abstractions** so you can implement your own provider without coupling business logic to a specific vendor.

:::note
While you can store SMS templates in SolidX, most providers (including Msg91) require you to **register and pre‑approve** transactional templates on their platform before you can use them.
:::

---

## ⚙️ Steps to Create a Custom SMS Provider

### 1) Implement a Custom SMS Service

Below is a sample implementation of a custom SMS provider using a hypothetical API‑based service.
It implements the `ISMS` interface, uses `SmsTemplateService` for template handling, and `PublisherFactory` for queueing.

All your custom SMS I/O (API calls, provider SDKs, etc.) should be coded inside **`sendSMSSynchronously()`**.
The rest (template rendering, queueing) is reusable across providers.

<details>
<summary><strong>Show code: <code>custom-sms.service.ts</code></strong></summary>

```ts title="custom-sms.service.ts"
import { Logger } from "@nestjs/common";
import { ConfigType } from "@nestjs/config";
import Handlebars from "handlebars";
import commonConfig from "src/config/common.config";
import { QueueMessage } from "src/interfaces/mq";
import { SmsTemplateService } from "../sms-template.service";
import { ISMS } from "../../interfaces";
import { PublisherFactory } from "../queues/publisher-factory.service";

/**
 * Example Custom SMS Service
 *
 * Replace the dummy implementation in `sendSMSSynchronously()` with your provider logic.
 */
export class CustomSMSService implements ISMS {
  protected readonly logger = new Logger(CustomSMSService.name);

  constructor(
    protected readonly commonConfiguration: ConfigType<typeof commonConfig>,
    protected readonly smsPublisher: string,
    protected readonly publisherFactory: PublisherFactory<any>,
    protected readonly smsTemplateService: SmsTemplateService
  ) {}

  /** Intentionally not supported to encourage template-based messages */
  sendSMS(_to: string, _body: string, _shouldQueueSms: boolean): Promise<void> {
    throw new Error(
      "CustomSMSService does not support sending plain text messages. Use a registered template instead."
    );
  }

  async sendSMSUsingTemplate(
    to: string,
    templateName: string,
    templateParams: any,
    shouldQueueSms = false
  ): Promise<any> {
    // Load and validate template
    const smsTemplate = await this.smsTemplateService.findOneByName(templateName);
    if (!smsTemplate) {
      throw new Error(`Invalid template name ${templateName}`);
    }

    // Render body (if present) and/or use provider templateId
    let body: string | null = null;
    let templateId: string | null = null;

    if (smsTemplate.body) {
      const bodyTemplate = Handlebars.compile(smsTemplate.body);
      body = bodyTemplate(templateParams);
    }
    if (smsTemplate.smsProviderTemplateId) {
      templateId = smsTemplate.smsProviderTemplateId;
    }

    if (!body && !templateId) {
      throw new Error(
        `Invalid template: neither "body" nor "smsProviderTemplateId" specified for ${templateName}`
      );
    }

    const message = {
      payload: {
        ...templateParams,
        to,
        templateId,
        // body, // optionally include if your provider accepts raw bodies
      },
    };

    // Send using queue if explicitly requested OR if globally configured
    if (shouldQueueSms === true) {
      await this.sendSMSAsynchronously(message);
    } else if (
      shouldQueueSms === false &&
      this.commonConfiguration.shouldQueueSms === true
    ) {
      await this.sendSMSAsynchronously(message);
    } else {
      await this.sendSMSSynchronously(message);
    }
  }

  async sendSMSAsynchronously(message) {
    const { to } = message.payload;
    this.publisherFactory.publish(message, this.smsPublisher);
    this.logger.debug(`Queueing SMS to ${to} with message ${JSON.stringify(message)}`);
  }

  async sendSMSSynchronously(message: QueueMessage<any>): Promise<any> {
    // 🧩 TODO: Add your custom SMS provider integration here.
    // e.g., call Twilio/Nexmo/your in‑house gateway API.
    this.logger.log(
      `Sending SMS synchronously to ${message.payload.to} using custom provider...`
    );

    // Example (pseudo):
    // const res = await this.httpService.post("https://api.example.com/sms", {
    //   to: message.payload.to,
    //   templateId: message.payload.templateId,
    //   variables: { ...message.payload },
    // });
    // return res.data;

    return { success: true, message: "Custom SMS sent (dummy implementation)" };
  }
}
```
</details>

---

### 2) Register Your Custom Provider

<details>
<summary><strong>Show code: <code>app.module.ts</code></strong></summary>

```ts title="app.module.ts"
import { Module } from "@nestjs/common";
import { CustomSMSService } from "./custom-sms.service";

@Module({
  providers: [CustomSMSService], // register your custom provider
  exports: [CustomSMSService],
})
export class AppModule {}
```
</details>

---

### 3) Use the <code>SmsServiceFactory</code> to Send SMS

You can now use `SmsServiceFactory` to send SMS via **templates** (recommended).

<details>
<summary><strong>Show code: <code>usage-example.ts</code></strong></summary>

```ts title="usage-example.ts"
import { SmsServiceFactory } from "@solidxai/core";

export class SomeService {
  constructor(private readonly smsServiceFactory: SmsServiceFactory) {}

  async sendOtp(user: { mobile: string; username: string; fullName?: string; mobileVerificationTokenOnLogin: string; }) {
    const smsService = this.smsServiceFactory.getSmsService();

    await smsService.sendSMSUsingTemplate(
      user.mobile,
      "otp-on-login",
      {
        solidAppName: process.env.SOLID_APP_NAME,
        mobileVerificationTokenOnLogin: user.mobileVerificationTokenOnLogin,
        firstName: user.username,
        fullName: user.fullName ? user.fullName : user.username,
      }
    );
  }
}
```
</details>

---

## 🧠 Interface Definition

Your custom service must implement the `ISMS` interface:

<details>
<summary><strong>Show code: <code>interfaces.ts</code></strong></summary>

```ts title="interfaces.ts"
export interface ISMS {
  sendSMS(to: string, body: string, shouldQueueSms: boolean): Promise<any>;

  sendSMSUsingTemplate(
    to: string,
    templateName: string,
    templateParams: any,
    shouldQueueSms: boolean
  ): Promise<any>;
}
```
</details>

---

## ✅ Summary

| Step | What you do |
|---|---|
| 1️⃣ | Implement `CustomSMSService` (implements `ISMS`) |
| 2️⃣ | Register it in your module |
| 3️⃣ | Use `SmsServiceFactory` to send template-based SMS |

> With this setup, you keep provider specifics isolated, while reusing SolidX’s queueing, templating, and configuration patterns.

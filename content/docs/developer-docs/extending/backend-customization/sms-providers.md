---
title: SMS Providers
icon: "smartphone"
description: Learn how to create and configure custom SMS providers in SolidX.
summary: Overview of the built-in SMS providers shipped with SolidX (Twilio, Msg91 transactional, Msg91 OTP) and how to implement a custom SMS provider using the ISMS interface.
keywords: [backend, sms providers, customization]
solidx_concerns: [new_sms_provider]
---



## Overview

SolidX ships with three built-in SMS providers: **TwilioSMSService**, **Msg91SMSService**, and **Msg91OTPService**. All support both **synchronous** sending and **asynchronous** (queued/background) delivery.

If you prefer a different provider, SolidX exposes **clean abstractions** so you can implement your own without coupling business logic to a specific vendor.

'> **Note**

''> While you can store SMS templates in SolidX, most providers (including Msg91) require you to **register and pre‑approve** transactional templates on their platform before you can use them.
'

---

## 📦 Default SMS Providers

SolidX includes three providers out of the box. Each is decorated with `@SmsProvider()`, which registers it for auto-discovery by `SmsServiceFactory`.

| Provider | Class | Use case |
|---|---|---|
| Twilio | `TwilioSMSService` | General-purpose SMS via Twilio API |
| Msg91 Transactional | `Msg91SMSService` | Transactional SMS via Msg91 flow API |
| Msg91 OTP | `Msg91OTPService` | OTP delivery via Msg91 OTP API |

---

### `TwilioSMSService`

Sends SMS via the [Twilio](https://www.twilio.com/) SDK. It is the only built-in provider that supports **plain text messages** via `sendSMS()` in addition to template-based messages.

**Supports:**
- `sendSMS()` — sends a raw text body directly
- `sendSMSUsingTemplate()` — renders a Handlebars template and sends the result
- Comma-separated recipients in the `to` field
- Synchronous and queued async delivery

**Required settings:**

| Setting key | Description |
|---|---|
| `twilioAccountSid` | Your Twilio Account SID |
| `twilioAuthToken` | Your Twilio Auth Token |
| `twilioNumber` | The Twilio phone number to send from |

**Example:**

```ts
import { TwilioSMSService } from "@solidxai/core";

export class NotificationService {
  constructor(private readonly smsService: TwilioSMSService) {}

  async sendWelcome(mobile: string, firstName: string) {
    // Raw text — supported only by Twilio
    await this.smsService.sendSMS(mobile, `Welcome, ${firstName}!`, false);

    // Or using a pre-configured template
    await this.smsService.sendSMSUsingTemplate(
      mobile,
      "welcome-sms",
      { firstName, appName: process.env.SOLID_APP_NAME },
      false
    );
  }
}
```

---

### `Msg91SMSService`

Sends transactional SMS via [Msg91's](https://msg91.com/) `/flow` API endpoint.

> **Caution**

> `sendSMS()` is **not supported** — calling it throws an error. You must use `sendSMSUsingTemplate()` with a template that has a `smsProviderTemplateId` matching a pre-approved Msg91 template.

**Supports:**
- `sendSMSUsingTemplate()` — posts template params as `recipients` to the Msg91 flow endpoint
- Synchronous and queued async delivery

**Required settings:**

| Setting key | Description |
|---|---|
| `msg91SmsApiKey` | Your Msg91 API auth key |
| `msg91SmsUrl` | Base URL for the Msg91 API |

**Example:**

```ts
import { Msg91SMSService } from "@solidxai/core";

export class OrderService {
  constructor(private readonly smsService: Msg91SMSService) {}

  async sendOrderConfirmation(mobile: string, orderId: string, customerName: string) {
    await this.smsService.sendSMSUsingTemplate(
      mobile,
      "order-confirmation",
      { orderId, customerName },
      false
    );
  }
}
```

'> **Note**

''> The template named `"order-confirmation"` must exist in SolidX and its `smsProviderTemplateId` must match a pre-approved template on the Msg91 platform.
'

---

### `Msg91OTPService`

Sends OTP SMS via [Msg91's](https://msg91.com/) dedicated `/otp` endpoint. Intended for one-time password delivery flows.

> **Caution**

> `sendSMS()` is **not supported** — calling it throws an error. You must use `sendSMSUsingTemplate()` with a template that includes an `otp` parameter and a valid `smsProviderTemplateId`.

**Supports:**
- `sendSMSUsingTemplate()` — passes `otp`, `template_id`, `mobile`, and `authkey` as URL query params to the Msg91 OTP endpoint
- Synchronous and queued async delivery

**Required settings:**

| Setting key | Description |
|---|---|
| `msg91SmsApiKey` | Your Msg91 API auth key |
| `msg91SmsUrl` | Base URL for the Msg91 API |

**Example:**

The usage pattern is identical to `Msg91SMSService` — inject the service and call `sendSMSUsingTemplate()`. The key difference is that your template params must include an `otp` field, which gets forwarded as a query parameter to Msg91's OTP endpoint.

```ts
import { Msg91OTPService } from "@solidxai/core";

export class AuthService {
  constructor(private readonly smsService: Msg91OTPService) {}

  async sendLoginOtp(mobile: string, otp: string) {
    await this.smsService.sendSMSUsingTemplate(
      mobile,
      "otp-on-login",
      { otp },
      false
    );
  }
}
```

---

## ⚙️ Steps to Create a Custom SMS Provider

### 1) Implement a Custom SMS Service

Below is a sample implementation of a custom SMS provider using a hypothetical API‑based service.
It implements the `ISMS` interface, uses `SmsTemplateService` for template handling, and `PublisherFactory` for queueing.

All your custom SMS I/O (API calls, provider SDKs, etc.) should be coded inside **`sendSMSSynchronously()`**.
The rest (template rendering, queueing) is reusable across providers.

<details open>
<summary><strong>Show code: <code>custom-sms.service.ts</code></strong></summary>

```ts
import { Injectable, Logger } from "@nestjs/common";
import Handlebars from "handlebars";
import { QueueMessage } from "@solidxai/core";
import { SmsTemplateService } from "@solidxai/core";
import { ISMS } from "@solidxai/core";
import { PublisherFactory } from "@solidxai/core";
import { SettingService } from "@solidxai/core";
import { SmsProvider } from "@solidxai/core";
import type { SolidCoreSetting } from "@solidxai/core";

/**
 * Example Custom SMS Service
 *
 * Replace the dummy implementation in `sendSMSSynchronously()` with your provider logic.
 */
@Injectable()
@SmsProvider()
export class CustomSMSService implements ISMS {
  protected readonly logger = new Logger(CustomSMSService.name);

  constructor(
    protected readonly settingService: SettingService,
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
      this.settingService.getConfigValue<SolidCoreSetting>("shouldQueueSms") === true
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

Your service must be decorated with `@SmsProvider()` (shown above) — this is what `SmsServiceFactory` uses to auto-discover the active provider. You also need to register it as a NestJS provider in your module.

<details open>
<summary><strong>Show code: <code>app.module.ts</code></strong></summary>

```ts
import { Module } from "@nestjs/common";
import { CustomSMSService } from "./custom-sms.service";

@Module({
  providers: [CustomSMSService],
  exports: [CustomSMSService],
})
export class AppModule {}
```
</details>

---

### 3) Use the `SmsServiceFactory` to Send SMS

You can now use `SmsServiceFactory` to send SMS via **templates** (recommended).

<details open>
<summary><strong>Show code: <code>usage-example.ts</code></strong></summary>

```ts
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
      },
      false
    );
  }
}
```
</details>

---

## 🧠 Interface Definition

Your custom service must implement the `ISMS` interface:

<details open>
<summary><strong>Show code: <code>interfaces.ts</code></strong></summary>

```ts
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
| 1️⃣ | Implement `CustomSMSService` (implements `ISMS`, decorated with `@SmsProvider()`) |
| 2️⃣ | Register it in your module |
| 3️⃣ | Use `SmsServiceFactory` to send template-based SMS |

> With this setup, you keep provider specifics isolated, while reusing SolidX's queueing, templating, and configuration patterns.

---
sidebar_position: 15
title: Email Providers
description: Learn how to create and configure custom email providers in SolidX.
summary: Guide to creating custom email providers beyond the built-in SMTP provider. Covers implementing the `IMail` interface with `@MailProvider()` decorator, using `EmailTemplateService` for templates, `PublisherFactory` for background job queuing, methods for synchronous/asynchronous sending with and without templates, handling attachments, API-based service integration (e.g., third-party email APIs), and proper error handling for email delivery.
keywords: [backend, email providers, customization]
solidx_concerns: [new_email_provider]
---

# 📧 Email Providers

## 🧩 Overview

SolidX provides an `SMTP` email provider out of the box, which supports sending emails **both synchronously** and **asynchronously** (via background jobs).  
However, there may be cases where you need to create your own provider — for example, to send emails using a **third‑party API service**.

To make this easy, SolidX offers abstractions that help you implement your own provider while keeping the code **clean, testable, and decoupled**.



## ⚙️ Steps to Create a Custom Email Provider

### 1. Implement a Custom Email Service

Below is a sample implementation of a custom email provider using a hypothetical API‑based service.

It implements the `IMail` interface and is decorated with `@MailProvider()`. 

It uses `EmailTemplateService` for handling email templates and `PublisherFactory` for queuing emails.

This class provies implementation for sending email with and without templates, both synchronously and asynchronously.

All the custom email sending logic (e.g., API calls) should be placed in the `sendEmailSynchronously` method. Rest of the code handles queuing and template rendering, which can be reused across different providers.

```ts
import { HttpService } from "@nestjs/axios";
import { Inject, Injectable, Logger } from "@nestjs/common";
import { ConfigType } from "@nestjs/config";
import { 
  commonConfig, 
  EmailTemplateService, 
  IMail, 
  MailAttachment, 
  MailProvider, 
  PublisherFactory, 
  QueueMessage 
} from "@solidstarters/solid-core";
import * as Handlebars from "handlebars";

@Injectable()
@MailProvider()
export class CustomNotifyApiEmailService implements IMail {
  private readonly logger = new Logger(this.constructor.name);
  private readonly EMAIL_NOTIFICATION_TYPE = "email";
  private readonly DEFAULT_REQUEST_SERVICE = "custom"; 

  constructor(
    @Inject(commonConfig.KEY)
    private readonly commonConfiguration: ConfigType<typeof commonConfig>,
    private readonly publisherFactory: PublisherFactory<any>,
    private readonly emailTemplateService: EmailTemplateService,
    private readonly httpService: HttpService
  ) {}

  async sendEmailUsingTemplate(
    to: string,
    templateName: string,
    templateParams: any,
    shouldQueueEmails: boolean,
    wrapperAttachments?: any[],
    attachments?: MailAttachment[],
    parentEntity?: any,
    parentEntityId?: any
  ): Promise<void> {
    const emailTemplate = await this.emailTemplateService.findOneByName(templateName);
    if (!emailTemplate) {
      throw new Error(`Invalid template name ${templateName}`);
    }

    const bodyTemplate = Handlebars.compile(emailTemplate.body);
    const body = bodyTemplate(templateParams);

    const subjectTemplate = Handlebars.compile(emailTemplate.subject);
    const subject = subjectTemplate(templateParams);

    await this.sendEmail(to, subject, body, shouldQueueEmails, parentEntity, parentEntityId, attachments);
  }

  async sendEmail(
    to: string,
    subject: string,
    body: string,
    shouldQueueEmails: boolean,
    wrapperAttachments?: any[],
    attachments?: MailAttachment[],
    parentEntity?: any,
    parentEntityId?: any
  ): Promise<void> {
    const message = {
      payload: {
        from: this.commonConfiguration.apiMail.from,
        to,
        subject,
        body,
        attachments,
      },
    };

    if (shouldQueueEmails === true) {
      this.sendEmailAsynchronously(message);
    } else if (shouldQueueEmails == false && this.commonConfiguration.shouldQueueEmails === true) {
      this.sendEmailAsynchronously(message);
    } else {
      await this.sendEmailSynchronously(message);
    }
  }

  async sendEmailAsynchronously(message: QueueMessage<any>): Promise<void> {
    const { to, subject, body } = message.payload;

    this.publisherFactory.publish(message, "CustomNotifyApiEmailQueuePublisher");

    this.logger.verbose(`Queueing email to ${to} with subject ${subject} and body ${body}`);
  }

  async sendEmailSynchronously(message: QueueMessage<any>): Promise<void> {
    const { from, to, subject, body } = message.payload;

    this.logger.debug(`Pretending to send email synchronously via external API...`);
    this.logger.debug(`From: ${from}, To: ${to}, Subject: ${subject}`);
    this.logger.debug(`Body: ${body}`);

    // Example: simulate API call
    // await this.httpService.axiosRef.post("https://dummy-email-api.com/send", {
    //   sender: from,
    //   receiver: [to],
    //   subject,
    //   body,
    //   notification_type: this.EMAIL_NOTIFICATION_TYPE,
    //   request_service: this.DEFAULT_REQUEST_SERVICE,
    // });
  }
}
```



### 2. Register Your Custom Provider

```ts title="app.module.ts"
import { Module } from "@nestjs/common";
import { CustomNotifyApiEmailService } from "./custom-notify-api-email.service";

@Module({
  providers: [CustomNotifyApiEmailService], // register your custom provider
})
export class AppModule {}
```



### 3. Use the `MailFactory` to Send Emails

You can now use `MailFactory` to send emails either **via templates** or **manually**.

#### ✅ Example: Using an Email Template

```ts
import { MailFactory } from "@solidstarters/solid-core";   
...
constructor(private readonly mailFactory: MailFactory) {}
...
const mailService = this.mailFactory.getMailService();
await mailService.sendEmailUsingTemplate(
  user.email,
  "forgot-password",
  {
    solidAppName: process.env.SOLID_APP_NAME,
    firstName: user.firstName,
  },
  this.commonConfiguration.shouldQueueEmails,
  null,
  null,
  "user",
  user.id
);
```

#### ✉️ Example: Sending a Manual Email (Without Template)

```ts
import { MailFactory } from "@solidstarters/solid-core";   
...
constructor(private readonly mailFactory: MailFactory) {}
...
const mailService = this.mailFactory.getMailService();
await mailService.sendEmail(
  user.email, // to
  "Welcome to SolidX!", // subject
  "Hello John, your account has been successfully created!", // body
  false // send synchronously
);
```



## 🧠 Interface Definition

The `IMail` interface defines two main methods your provider must implement.

```ts
export interface IMail<TResponse = unknown> {
  sendEmail(
    to: string,
    subject: string,
    body: string,
    shouldQueueEmails: boolean,
    wrapperAttachments?: MailAttachmentWrapper[],
    attachments?: MailAttachment[],
    parentEntity?: any,
    parentEntityId?: any,
    cc?: string[],
    bcc?: string[],
    from?: string,
  ): Promise<TResponse>;

  sendEmailUsingTemplate(
    to: string,
    templateName: string,
    templateParams: any,
    shouldQueueEmails: boolean,
    wrapperAttachments?: MailAttachmentWrapper[],
    attachments?: MailAttachment[],
    parentEntity?: any,
    parentEntityId?: any,
    cc?: string[],
    bcc?: string[],
    from?: string,
  ): Promise<TResponse>;
}
```

> 💡 **Recommendation:** Use email templates for better separation of content and logic. It allows you to modify templates without changing your backend code.



## ✅ Summary

| Step | Description |
|------|--------------|
| 1️⃣ | Create a class implementing `IMail` |
| 2️⃣ | Decorate it with `@MailProvider()` |
| 3️⃣ | Register it in your module |
| 4️⃣ | Use `MailFactory` to send emails (template or manual) |



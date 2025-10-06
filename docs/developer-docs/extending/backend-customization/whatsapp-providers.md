---
sidebar_position: 16
# title: WhatsApp Providers
description: Learn how to create and configure custom WhatsApp providers in SolidX.
keywords: [backend, whatsapp providers, customization]
---

# 📧 WhatsApp Providers

## 🧩 Overview

SolidX provides a `Msg91` WhatsApp provider out of the box, which supports sending WhatsApp messages **both synchronously** and **asynchronously** (via background jobs).

However, there may be cases where you need to create your own provider — for example, to send WhatsApp messages using a **third‑party API service**.

To make this easy, SolidX offers abstractions that help you implement your own provider while keeping the code **clean, testable, and decoupled**.

:::note
For whatsapp messages, there is no need to keep a separate template management in SolidX, since most whatsapp providers (e.g., Twilio, Msg91, etc) have their own template management system. 

So SolidX allows you to send whatsapp messages using the `templateId` and `parameters` as configured in your whatsapp provider platform. Here the templateId is the external templateId from your whatsapp provider platform.
:::


## ⚙️ Steps to Create a Custom WhatsApp Provider

### 1. Implement a Custom WhatsApp Service

Below is a sample implementation of a custom WhatsApp provider using a hypothetical API‑based service.

It implements the `IWhatsAppTransport` interface and is decorated with `@WhatsAppProvider()`.

The IWhatsAppTransport interface currently supports only 1 method `sendWhatsAppMessage` which takes the `to` phone number, `templateId` and `parameters` as input.

Below is a sample implementation of a custom WhatsApp provider using a hypothetical API‑based service, which sends all messages asynchronously (queued). In case you want to send some messages synchronously, you can modify the logic in `sendWhatsAppMessage` and call the sendWhatsAppMessageSynchronously directly instead of queuing it.

```ts
import { HttpService } from '@nestjs/axios';
import { Inject, Injectable, Logger } from '@nestjs/common';
import { ConfigType } from '@nestjs/config';
import commonConfig from 'src/config/common.config';
import { QueueMessage } from 'src/interfaces/mq';
import { IWhatsAppTransport } from "../../interfaces";
import { PublisherFactory } from '../queues/publisher-factory.service';
import { WhatsAppProvider } from 'src/decorators/whatsapp-provider.decorator';

@Injectable()
@WhatsAppProvider()
export class CustomWhatsAppService implements IWhatsAppTransport {
  readonly logger = new Logger(CustomWhatsAppService.name);

  constructor(
    @Inject(commonConfig.KEY)
    private readonly commonConfiguration: ConfigType<typeof commonConfig>,
    private readonly publisherFactory: PublisherFactory<any>,
    private readonly httpService: HttpService,
  ) { }

  async sendWhatsAppMessage(
    to: string,
    templateId: string,
    parameters: any,
    parentEntity?: any,
    parentEntityId?: any
  ): Promise<any> {
    const message = {
      payload: {
        to,
        templateId,
        ...parameters,
      },
      parentEntity,
      parentEntityId,
    };

    // All messages are always queued as per requirement
    return this.sendWhatsAppMessageAsynchronously(message);
  }

  private async sendWhatsAppMessageAsynchronously(message: any): Promise<any> {
    const { to, templateId } = message.payload;
    this.logger.debug(`Queueing WhatsApp message to ${to} with template ${templateId}`);
    return this.publisherFactory.publish(message, 'CustomWhatsAppQueuePublisher');
  }

  async sendWhatsAppMessageSynchronously(message: QueueMessage<any>): Promise<void> {
    // Example: simulate API call to send WhatsApp message from your custom whatsapp platform provider
    this.logger.debug(`Sending WhatsApp message synchronously to ${message.payload.to} with template ${message.payload.templateId}`);
  }
}

```



### 2. Register Your Custom Provider

```ts title="app.module.ts"
import { Module } from "@nestjs/common";
import { CustomWhatsAppService } from "./custom-whatsapp.service";

@Module({
  providers: [CustomWhatsAppService], // register your custom provider
})
export class AppModule {}
```


<!-- FIXME: Need to create this abstraction -->
### 3. Use the `WhatsAppFactory` to Send WhatsApp Messages 

You can now use `WhatsAppFactory` to send WhatsApp messages either **via templates** or **manually**.

#### ✅ Example: Sending a WhatsApp Message 

```ts
import { WhatsAppFactory } from "@solidstarters/solid-core";   
...
constructor(private readonly whatsappFactory: WhatsAppFactory) {}
...
const whatsappService = this.whatsappFactory.getWhatsAppService();
await whatsappService.sendWhatsAppMessage(
  user.phoneNumber, // to
  "welcome_template", // templateId (as configured in your whatsapp provider platform)
  { name: "John" } // parameters (as configured in your whatsapp provider platform)
);
```

## 🧠 Interface Definition

The `IWhatsAppTransport` interface defines the contract for sending WhatsApp messages.

```ts
export interface IWhatsAppTransport {
  sendWhatsAppMessage(
    to: string,
    templateId: string,
    parameters: any,
    parentEntity?: any,
    parentEntityId?: any
  ): Promise<any>;
}
```


## ✅ Summary

| Step | Description |
|------|--------------|
    | 1️⃣ | Implement your custom WhatsApp provider by implementing the `IWhatsAppTransport` interface |
    | 2️⃣ | Decorate it with `@WhatsAppProvider()` |
    | 3️⃣ | Register it in your module |
    | 4️⃣ | Use `WhatsAppFactory` to send WhatsApp messages |


---
sidebar_position: 1
title: Background Jobs
description: Learn how to set up and manage background jobs in SolidX, including configuration for different brokers like Database and RabbitMQ.
keywords:
  [
    background jobs,
    SolidX,
    asynchronous processing,
    job queues,
    RabbitMQ,
    database broker,
  ]
---
import { FaTag, FaDatabase, FaCode, FaProjectDiagram } from "react-icons/fa";
import { IoIosArrowForward } from "react-icons/io";

Background jobs in SolidX enable asynchronous task processing, making it easy to offload work that doesn’t need to run immediately. Common use cases include:
	-	Sending emails or notifications
	-	Deferring non-urgent tasks
	-	Handling heavy computations in the background

SolidX implements this using a message queue system based on the Work Queue / Competing Consumers pattern:
	-	Publishers push jobs into a queue
	-	Subscribers pick up and process jobs asynchronously

Job execution is fully tracked with support for status updates, retries, and failures:
	-	ss_mq_message → stores individual queue messages
	-	ss_mq_message_queue → stores job queue definitions

SolidX supports both:
	- Database-backed queues – simple, lightweight, no external dependencies
	- RabbitMQ – robust, production-ready, and recommended for high-throughput systems

## Setting Up a Background Job

### 1. Define Queue Options

Specify the queue name and broker type in an options object.
Below is an example configuration for a database-backed queue for sending emails.

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
     <code>email-queue-options-database.ts</code>
  </summary>

```ts
import { BrokerType } from "src/interfaces";

const MAIL_QUEUE_NAME = "solidx.email.db"; 
//const MAIL_QUEUE_NAME = "solidx.email.rabbitmq"; //For RabbitMQ

export default {
  name: "solidEmailInstance",
  type: BrokerType.Database,
  //type: BrokerType.Rabbitmq //For RabbitMQ
  queueName: MAIL_QUEUE_NAME,
};
```
</details>



### 2. Configure a Publisher

We need to create a publisher class which extends the appropriate base publisher class based on the broker type and specify the queue options.

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>email-queue-publisher-database.ts</code>  
</summary>

```ts
import { Injectable } from "@nestjs/common";
import mailQueueOptions from "./email-queue-options-database";
import { MqMessageQueueService } from "src/services/mq-message-queue.service";
import { MqMessageService } from "src/services/mq-message.service";
import { QueuesModuleOptions } from "src/interfaces";
import { DatabasePublisher } from "src/services/queues/database-publisher.service";

@Injectable()
export class EmailQueuePublisherDatabase extends DatabasePublisher<any> {
  constructor(
    protected readonly mqMessageService: MqMessageService,
    protected readonly mqMessageQueueService: MqMessageQueueService
  ) {
    super(mqMessageService, mqMessageQueueService);
  }

  options(): QueuesModuleOptions {
    return {
      ...mailQueueOptions,
    };
  }
}
```

</details>

<!-- //FIXME: -->
:::info  
In the near future, you need not create a publisher. Only subscriber needs to be created.
:::

### 3. Configure a Subscriber

Subscribers process messages from the queue. They house the actual job processing logic.
Below is an example subscriber that sends emails using the SMTP service.

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>email-queue-subscriber-database.ts</code>  
</summary>

```ts
import { Injectable } from "@nestjs/common";
import mailQueueOptions from "./email-queue-options-database";
import { QueueMessage } from "src/interfaces/mq";
import { MqMessageService } from "src/services/mq-message.service";
import { MqMessageQueueService } from "src/services/mq-message-queue.service";
import { DatabaseSubscriber } from "src/services/queues/database-subscriber.service";
import { SMTPEMailService } from "src/services/mail/SMTPEmailService";
import { QueuesModuleOptions } from "src/interfaces";

@Injectable()
export class EmailQueueSubscriberDatabase extends DatabaseSubscriber<any> {
  constructor(
    private readonly mailFactory: MailServiceFactory,
    readonly mqMessageService: MqMessageService,
    readonly mqMessageQueueService: MqMessageQueueService
  ) {
    super(mqMessageService, mqMessageQueueService);
  }

  options(): QueuesModuleOptions {
    return {
      ...mailQueueOptions,
    };
  }

  subscribe(message: QueueMessage<any>) {
    const mailService = this.mailFactory.getMailService();
    return mailService.sendEmailSynchronously(message);
  }
}
```

</details>
:::tip
Keep your subscribe method clean and simple. Keep the actual logic in a separate service and call it from the subscribe method.
::: 

:::info
The above examples use a database broker. For RabbitMQ, simply switch the base classes to `RabbitmqPublisher` and `RabbitmqSubscriber`, and update the queue options accordingly.
:::


<h4 className="card-title card-headear-wrapper">
  <FaTag size={19} style={{ marginRight: "10px" }} />

## Naming Convention
</h4>

The publisher and subscriber names should follow a convention based on the broker type:

- `NameDatabase` for database broker
- `NameRabbitmq` for RabbitMQ broker

They are standard NestJS providers and must be registered in their respective modules.


<h4 className="card-title card-headear-wrapper">
  <FaDatabase size={20} style={{ marginRight: "10px" }} />

## Database Tables
</h4>

- `ss_mq_message_queue`: Queue names registry
- `ss_mq_message`: Stores message details including status, retries, payload



<h4 className="card-title card-headear-wrapper">
  <FaCode size={20} style={{ marginRight: "10px" }} />

## Environment Variable
</h4>
### 📨 Broker
- **`QUEUES_DEFAULT_BROKER`**  
  Choose the broker for background jobs:  
  - `"database"` → Database broker (**default**)  
  - `"rabbitmq"` → RabbitMQ broker  

- **`QUEUES_RABBIT_MQ_URL`** *(RabbitMQ only)*  
  RabbitMQ connection string, e.g.:  
  `amqp://guest:guest@127.0.0.1:5672`


### 🖥 Service Role
- **`QUEUES_SERVICE_ROLE`**  
  Defines how this service instance participates:  
  - `"subscriber"` → Only processes jobs  
  - `"both"` → Publishes **and** processes jobs  
    _(useful for distributed job handling)_
:::info
In a distributed setup, you can have some instances only processing jobs while others handle both publishing and processing. This is useful for load balancing and scaling for e.g (you can set the `QUEUES_SERVICE_ROLE` to `subscriber` on multiple instances to only process jobs, while having one instance set to `both` to handle publishing/subscribing).
:::

### 📧 Email Jobs
- **`COMMON_EMAIL_SHOULD_QUEUE`**  
  - `true` → Send emails via background jobs  
  - `false` → Send emails synchronously (**default**)  


### 📱 SMS Jobs
- **`COMMON_SMS_SHOULD_QUEUE`**  
  - `true` → Send SMS via background jobs  
  - `false` → Send SMS synchronously (**default**)  



<h4 className="card-title card-headear-wrapper">
  <FaProjectDiagram size={20} style={{ marginRight: "10px" }} />

## Supported Brokers
</h4>


### 1 Database Broker

- Jobs are stored in `ss_mq_message`
- Uses polling to fetch and process jobs every second
- Best for lightweight or dependency-free setups

### 2 RabbitMQ Broker

- Jobs processed via RabbitMQ queues
- Uses `amqplib` for message handling
- Best for larger-scale systems requiring reliability and routing
- Management UI: [http://localhost:15672](http://localhost:15672)
- Default login: `guest / guest`
- Set `QUEUES_RABBIT_MQ_URL` to connect to your RabbitMQ instance

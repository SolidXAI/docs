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

# Background Jobs in SolidX

Background jobs in SolidX allow asynchronous task processing, for e.g :

- Sending emails or notifications
- Deferred tasks that don’t require immediate execution
- Heavy computations that can be processed in the background



## Setting Up a Background Job

### 1. Define Queue Options

Specify the queue name and broker type in an options object.

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
     <code>email-queue-options-database.ts</code>
  </summary>

```ts
import { BrokerType } from "src/interfaces";

const MAIL_QUEUE_NAME = "solid_email_db_queue_v3";

export default {
  name: "solidEmailInstance",
  type: BrokerType.Database,
  queueName: MAIL_QUEUE_NAME,
};
```

</details>



### 2. Configure a Publisher

Send jobs to the queue using a publisher.

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



### 3. Configure a Subscriber

Subscribers process messages from the queue.

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
    private readonly emailService: SMTPEMailService,
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
    return this.emailService.sendEmailSynchronously(message);
  }
}
```

</details>
















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


- `QUEUE_SERVICE_ROLE`
  - `"subscriber"`: Only processes jobs
  - `"both"`: Processes and publishes jobs  
    Useful for distributed job handling.



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
- Set `QUEUES_RABBIT_MQ_URL`, e.g. `amqp://guest:guest@127.0.0.1:5672`

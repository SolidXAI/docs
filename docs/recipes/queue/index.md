---
sidebar_position: 4
---

# SolidX Queue 

In SolidX, you can configure queues to use either:

🗄️ Database (default for simple jobs and local dev)

🐇 RabbitMQ (for high-performance distributed tasks)

### 🏗️ Smart Broker Selection using FactoryPublisher

SolidX internally uses a FactoryPublisher mechanism that automatically selects the appropriate broker (Database or RabbitMQ) based on your .env configuration.

This means:

No changes required in your business logic.

Just update the .env file to switch brokers.

Both publishers and subscribers are designed to work dynamically with this setup.

Example

```
# Choose the broker

QUEUES_DEFAULT_BROKER=database   # or rabbitmq

```

Once the correct broker is selected, SolidX picks the correct publisher (DatabasePublisher or RabbitMqPublisher) and routes messages accordingly.

📦 Setup Options

Now that you understand how SolidX intelligently chooses the queue backend, let’s explore both options:

### 🗄️ Sending Email Using Database Queue

Sending Email Using Database Queue, To send emails, SMS, or any messages via database queue, SolidX defines three key components:

Publisher – publishes the message to the queue

Queue Options – defines the queue's configuration

Subscriber – listens for and processes the messages

Let’s walk through an example using a test queue.

1️⃣ test-queue-publisher-database.service.ts
This file defines the publisher logic. It extends SolidX’s DatabasePublisher and provides configuration via options().

```
import { Injectable } from '@nestjs/common';
import testQueueConfig from './test-queue-options-database';
import { MqMessageQueueService } from '../../services/mq-message-queue.service';
import { MqMessageService } from '../../services/mq-message.service';
import { QueuesModuleOptions } from '../../interfaces';
import { DatabasePublisher } from 'src/services/queues/database-publisher.service';

@Injectable()
export class TestQueuePublisherDatabase extends DatabasePublisher<any> {
    constructor(
        protected readonly mqMessageService: MqMessageService,
        protected readonly mqMessageQueueService: MqMessageQueueService,
    ) {
        super(mqMessageService, mqMessageQueueService);
    }

    options(): QueuesModuleOptions {
        return {
            ...testQueueConfig
        };
    }
}

```

2️⃣ test-queue-options-database.ts

This defines the queue metadata such as name and type (here, it’s a database queue):

```
import { BrokerType } from '../../interfaces';

const QUEUE_NAME = 'test_queue_db';

export default {
    name: 'queueTestDb',
    type: BrokerType.Database,
    queueName: QUEUE_NAME,
};

```

3️⃣ sms-subscriber-database.service.ts

This defines the subscriber which listens to messages and executes logic (e.g., sending Email):

```
import { Injectable, Logger } from '@nestjs/common';
import { QueueMessage } from 'src/interfaces/mq';
import testQueueConfig from './test-queue-options-database';
import { MqMessageService } from '../../services/mq-message.service';
import { MqMessageQueueService } from '../../services/mq-message-queue.service';
import { QueuesModuleOptions } from "../../interfaces";
import { DatabaseSubscriber } from 'src/services/queues/database-subscriber.service';

@Injectable()
export class TestQueueSubscriberDatabase extends DatabaseSubscriber<any> {
    private readonly testQueueLogger = new Logger(TestQueueSubscriberDatabase.name);
    constructor(
        readonly mqMessageService: MqMessageService,
        readonly mqMessageQueueService: MqMessageQueueService,
    ) {
        super(mqMessageService, mqMessageQueueService);
    }

    options(): QueuesModuleOptions {
        return {
            ...testQueueConfig
        }
    }

    subscribe(message: QueueMessage<any>) {
        // console.log(`Received message ${JSON.stringify(message)}`);
        this.testQueueLogger.debug(`Received message: ${JSON.stringify(message)}`);

        return new Promise((resolve, reject) => {
            // Simulate some processing time
            setTimeout(() => {
                this.testQueueLogger.debug(`Processed message: ${JSON.stringify(message)}`);
                resolve({ status: 'success', messageId: message.messageId, message: `Processed message` });
            }, 10000); // Simulate 1 second processing time
        });
    }
}

```

✅ Configure .env for Database Queue

To enable asynchronous email sending using the database queue, add the following variables to your API’s .env file:

```
# SMTP Email Setup
COMMON_EMAIL_SHOULD_QUEUE=true
COMMON_SMTP_EMAIL_SMTP_HOST=
COMMON_SMTP_EMAIL_SMTP_PORT=
COMMON_SMTP_EMAIL_USERNAME=
COMMON_SMTP_EMAIL_PASSWORD=
COMMON_SMTP_EMAIL_FROM=

# Queue Configuration
QUEUES_DEFAULT_BROKER=databases
QUEUES_SERVICE_ROLE=both
QUEUES_RABBIT_MQ_URL=

```

COMMON_EMAIL_SHOULD_QUEUE=true
This flag tells SolidX to use the queue system for sending emails asynchronously.

QUEUES_DEFAULT_BROKER=databases
SolidX will use Database as the queue backend.

QUEUES_SERVICE_ROLE=both
Enables both publishing and subscribing of jobs in the same service.


🎉 With the above setup, SolidX will send emails asynchronously using the database queue — no extra infrastructure required!

## 🐇 Sending Email Using RabbitMQ Queue
SolidX also supports RabbitMQ as a high-performance queue broker. RabbitMQ is ideal for distributed, scalable, and real-time background job processing.

Just like with the database queue, SolidX uses a well-structured approach for RabbitMQ queues, with:

Publisher – sends messages to the queue

Queue Options – defines the RabbitMQ queue

Subscriber – listens and processes messages from the queue

🧠 Note: RabbitMQ should be running locally (default: amqp://localhost:5672).

1️⃣ test-queue-publisher.service.ts
This defines a publisher that uses RabbitMQ. It extends SolidX’s RabbitMqPublisher and provides queue configuration.

```
import { Injectable } from '@nestjs/common';
import { RabbitMqPublisher } from 'src/services/queues/rabbitmq-publisher.service';
import testQueueConfig from './test-queue-options';
import { MqMessageQueueService } from '../services/mq-message-queue.service';
import { MqMessageService } from '../services/mq-message.service';
import { QueuesModuleOptions } from "../interfaces";

@Injectable()
export class TestQueuePublisher extends RabbitMqPublisher<any> {
    constructor(
        protected readonly mqMessageService: MqMessageService,
        protected readonly mqMessageQueueService: MqMessageQueueService,
    ) {
        super(mqMessageService, mqMessageQueueService);
    }

    options(): QueuesModuleOptions {
        return {
            ...testQueueConfig
        };
    }
}

```
2️⃣ test-queue-subscriber.service.ts

This is the subscriber that receives and processes messages from the RabbitMQ queue.

```
import { Injectable, Logger } from '@nestjs/common';
import { RabbitMqSubscriber } from 'src/services/queues/rabbitmq-subscriber.service';
import { QueueMessage } from 'src/interfaces/mq';
import testQueueConfig from './test-queue-options';
import { MqMessageService } from '../services/mq-message.service';
import { MqMessageQueueService } from '../services/mq-message-queue.service';
import { QueuesModuleOptions } from "../interfaces";

@Injectable()
export class TestQueueSubscriber extends RabbitMqSubscriber<any> {
    private readonly testQueueLogger = new Logger(TestQueueSubscriber.name);

    constructor(
        readonly mqMessageService: MqMessageService,
        readonly mqMessageQueueService: MqMessageQueueService,
    ) {
        super(mqMessageService, mqMessageQueueService);
    }

    options(): QueuesModuleOptions {
        return {
            ...testQueueConfig
        };
    }

    subscribe(message: QueueMessage<any>) {
        this.testQueueLogger.debug(`Received message: ${JSON.stringify(message)}`);

        return new Promise((resolve, reject) => {
            setTimeout(() => {
                this.testQueueLogger.debug(`Processed message: ${JSON.stringify(message)}`);
                resolve({ status: 'success', messageId: message.messageId, message: `Processed message` });
            }, 10000); // Simulate 10 seconds processing time
        });
    }
}

```

3️⃣ test-queue-options.ts

This file defines the metadata for the queue such as the broker type and queue name:

```
import { BrokerType } from "../interfaces";

const QUEUE_NAME = 'test_queue';

export default {
    name: 'queueTest',
    type: BrokerType.RabbitMQ,
    queueName: QUEUE_NAME,
};

```

This allows switching between queue brokers without changing the business logic or implementation.

✅ Configure .env for RabbitMQ Queue

To enable asynchronous job processing using RabbitMQ, you need to update your API .env file:

```
# SMTP
COMMON_EMAIL_SHOULD_QUEUE=true
COMMON_SMTP_EMAIL_SMTP_HOST=
COMMON_SMTP_EMAIL_SMTP_PORT=587
COMMON_SMTP_EMAIL_USERNAME=
COMMON_SMTP_EMAIL_PASSWORD=
COMMON_SMTP_EMAIL_FROM=

# Queues configuration
QUEUES_DEFAULT_BROKER=rabbitmq
QUEUES_SERVICE_ROLE=both
QUEUES_RABBIT_MQ_URL=a

```

COMMON_EMAIL_SHOULD_QUEUE=true

This enables the queue-based (asynchronous) job processing.

QUEUES_DEFAULT_BROKER=rabbitmq

Instructs SolidX to use RabbitMQ instead of the database.

QUEUES_RABBIT_MQ_URL=...

RabbitMQ connection string (host, port, credentials, etc.)

🎉 With this setup, SolidX will send emails, SMS, or any job asynchronously using RabbitMQ as the queue broker.

You can now build high-performance, scalable messaging and task systems with minimal configuration using SolidX!
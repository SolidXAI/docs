---
title: Queues
icon: "list-ordered"
---

Queues allow any enterprise system to implement scalability allowing long running tasks to be done as background jobs. Queues being a commonly seen pattern in high performance enterprise applications SolidX has an inbuilt abstraction around queues. 
SolidX uses the following brokers to enable queues 

- Database 
- RabbitMQ 
- Redis 

## Environment Variables

| Variable Name              | Description                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| `QUEUES_DEFAULT_BROKER`          | This variable tells SolidX to use which broker(database, RabbitMq)                |
| `QUEUES_SERVICE_ROLE`             | This variable allows us to control when a service has to be run in subscriber role, publisher role or both            |
| `QUEUES_RABBIT_MQ_URL`          | This variable is used for rabbitmq url, will only be required to be specified if broker is rabbitmq        |
| `COMMON_EMAIL_SHOULD_QUEUE` | This variable tells SolidX to use the queue system for sending emails asynchronously.|

env

## How To Configure Jobs
In SolidX a task which has to be run as a background job requires the following components. We will explain all 3 components using a dummy example representing a long running background job.

 ### Job Options

First we create a config object to represent our job, we are essentially only giving a name, specifying which type of broker to use to run this job & most importantly the queue name that will be used. 

Eg. 

```tsx
import { BrokerType } from '../../interfaces';

const QUEUE_NAME = 'test_queue_db';

export default {
    name: 'queueTestDb',
    type: BrokerType.Database,
    queueName: QUEUE_NAME,
};

```

 ### Publisher

The Publisher is responsible for sending messages to the queue. In this example, we create a custom publisher by extending SolidX’s built-in DatabasePublisher class. 

Eg. 

```tsx
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

 ### Subscriber

The Subscriber listens to a specific queue and processes incoming messages. In this example, we extend SolidX’s DatabaseSubscriber class.

Eg. 

```tsx
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

## Publishing Jobs 

SolidX internally uses a FactoryPublisher mechanism that automatically selects the appropriate broker (Database or RabbitMQ) based on your .env configuration trigger a background job.

Eg.

```tsx
import { Logger } from '@nestjs/common';
import { Injectable } from '@nestjs/common';
import { QueueMessage, QueuePublisher } from 'src/interfaces/mq';
import { classify } from '@angular-devkit/core/src/utils/strings';
import { SolidIntrospectService } from '../solid-introspect.service';

@Injectable()
export class PublisherFactory<T> {
    private readonly logger = new Logger(PublisherFactory.name);

    constructor(
        private readonly solidIntrospectionService: SolidIntrospectService
    ) {
    }

    async publish(message: QueueMessage<T>, publisherName: string, brokerToUse?: string): Promise<string> {
        let defaultBrokerToUse = brokerToUse || process.env.QUEUES_DEFAULT_BROKER;
        let resolvedPublisherName = `${publisherName}${classify(defaultBrokerToUse)}`;

        // Register all ISolidDatabaseModules implementations
        let actualPublisherToUse = this.solidIntrospectionService.getProvider(resolvedPublisherName);
        if (!actualPublisherToUse) {

            // Extra check in place to make sure we do not have to refactor old publishers which have been created earlier. 
            if (defaultBrokerToUse === 'rabbitmq') {
                actualPublisherToUse = this.solidIntrospectionService.getProvider(publisherName);
                if (!actualPublisherToUse) {
                    throw new Error(`Unable to locate publisher with name ${resolvedPublisherName}`);
                }
            }
        }

        const typedActualPublisher: QueuePublisher<T> = actualPublisherToUse.instance;
        this.logger.error(`Resolved publisher with name ${actualPublisherToUse.name}, and with options ${typedActualPublisher.options()}`);
        return typedActualPublisher.publish(message);
    }
}
```

## Admin Interface 

SolidX comes with a very useful interface where all background jobs are tracked 
TODO: Explain each field of the 2 entities viz. Queues & Messages


---
sidebar_position: 6
title: Background Jobs
description: Learn how to set up and manage background jobs in SolidX using database and RabbitMQ brokers.
summary: Comprehensive guide to asynchronous processing in SolidX with the Work Queue/Competing Consumers pattern. Covers typed queue payloads, queue options, publishers/subscribers, environment setup, and broker-specific examples for Database and RabbitMQ. Includes a dedicated RabbitMQ section for `prefetch` and parallel consumption behavior.
keywords:
  [
    background jobs,
    SolidX,
    asynchronous processing,
    job queues,
    RabbitMQ,
    database broker,
    prefetch,
  ]
solidx_concerns: [backend.background_jobs, new_background_job, new_sms_provider, new_email_provider, new_whatsapp_provider, add_custom_service_method, add_scheduled_job]
---

import { InfoBox } from '@site/src/common/InfoBox';

Background jobs in SolidX let you offload non-blocking work from request/response flows.

Common use cases:

- Notification delivery (email/SMS/WhatsApp)
- External API callbacks/webhooks
- OCR/LLM processing and other long-running tasks
- Retryable integrations

SolidX uses a Work Queue / Competing Consumers model:

- Publishers enqueue jobs
- Subscribers consume jobs asynchronously

Job execution state is tracked in:

- `ss_mq_message_queue` (queue definitions)
- `ss_mq_message` (message payload/status/retries)

## Core Building Blocks

Every background job setup usually contains:

1. Queue options file (broker type, queue name, etc.)
2. Publisher class
3. Subscriber class
4. Module provider wiring

Typed payloads are recommended for safer publish/subscribe contracts.

## 1) Queue Options + Payload Contract

```ts
import { ActiveUserData, BrokerType } from "@solidxai/core";

const OCR_REQUEST_QUEUE_NAME = "ocr_request_queue";

export interface OcrRequestPayload {
  ocrRequestId: number;
  loggedInUser?: ActiveUserData;
}

export default {
  name: "ocrRequestQueueRabbitmq",
  type: BrokerType.RabbitMQ,
  queueName: OCR_REQUEST_QUEUE_NAME,
  prefetch: 5,
};
```

`prefetch` is only applicable to RabbitMQ (details below).

## 2) Publisher Example (RabbitMQ)

```ts
import { Injectable } from "@nestjs/common";
import {
  MqMessageService,
  MqMessageQueueService,
  QueuesModuleOptions,
  RabbitMqPublisher,
} from "@solidxai/core";
import ocrRequestQueueOptions, { OcrRequestPayload } from "../ocr-request-queue-options";

@Injectable()
export class OcrRequestPublisherRabbitmq extends RabbitMqPublisher<OcrRequestPayload> {
  constructor(
    protected readonly mqMessageService: MqMessageService,
    protected readonly mqMessageQueueService: MqMessageQueueService
  ) {
    super(mqMessageService, mqMessageQueueService);
  }

  options(): QueuesModuleOptions {
    return {
      ...ocrRequestQueueOptions,
    };
  }
}
```

## 3) Subscriber Example (RabbitMQ, OCR Workflow)

```ts
import { Injectable, Logger } from "@nestjs/common";
import { InjectEntityManager } from "@nestjs/typeorm";
import { EntityManager } from "typeorm";
import {
  MqMessageService,
  MqMessageQueueService,
  QueueMessage,
  QueuesModuleOptions,
  RabbitMqSubscriber,
  S3FileService,
  SettingService,
  SolidMicroserviceAdapter,
} from "@solidxai/core";
import ocrRequestQueueOptions, { OcrRequestPayload } from "../ocr-request-queue-options";

@Injectable()
export class OcrRequestSubscriberRabbitmq extends RabbitMqSubscriber<OcrRequestPayload> {
  private readonly logger = new Logger(OcrRequestSubscriberRabbitmq.name);

  constructor(
    readonly mqMessageService: MqMessageService,
    readonly mqMessageQueueService: MqMessageQueueService,
    @InjectEntityManager() readonly entityManager: EntityManager,
    private readonly settingService: SettingService,
    private readonly solidMicroserviceAdapter: SolidMicroserviceAdapter,
    private readonly s3FileService: S3FileService
  ) {
    super(mqMessageService, mqMessageQueueService);
  }

  options(): QueuesModuleOptions {
    return {
      ...ocrRequestQueueOptions,
    };
  }

  async subscribe(message: QueueMessage<OcrRequestPayload>) {
    const { ocrRequestId } = message.payload;
    this.logger.log(`Processing OCR request ${ocrRequestId}`);

    // 1) Load request data from DB
    // 2) Update status -> Started
    // 3) Fetch signed S3 URL
    // 4) Invoke OCR/LLM pipeline
    // 5) Persist output/status
    // 6) Invoke callback URL
    // 7) Handle failure status + callback failure separately

    return { success: true };
  }
}
```

The subscriber above is intentionally condensed. Keep the heavy business logic in dedicated services and call them from `subscribe(...)`.

## RabbitMQ-Specific: `prefetch` (Important)

`prefetch` controls how many unacknowledged messages a subscriber can process concurrently per channel.

Example:

- `prefetch: 1` -> strict one-by-one processing
- `prefetch: 5` -> up to 5 in-flight messages
- higher values -> higher throughput, but also higher concurrent load on DB/API dependencies

Use `prefetch` to tune parallelism for your workload.

<InfoBox>
  `prefetch` is a RabbitMQ concept and is not used by the Database broker implementation.
</InfoBox>

## Database Broker Example (Reference)

For lightweight setups without RabbitMQ, use database-backed queues.

### Queue options (Database)

```ts
import { BrokerType } from "@solidxai/core";

const MAIL_QUEUE_NAME = "solidx.email.db";

export default {
  name: "solidEmailInstance",
  type: BrokerType.Database,
  queueName: MAIL_QUEUE_NAME,
};
```

### Publisher (Database)

```ts
import { Injectable } from "@nestjs/common";
import {
  DatabasePublisher,
  MqMessageQueueService,
  MqMessageService,
  QueuesModuleOptions,
} from "@solidxai/core";
import mailQueueOptions from "./email-queue-options-database";

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

### Subscriber (Database)

```ts
import { Injectable } from "@nestjs/common";
import {
  DatabaseSubscriber,
  MqMessageQueueService,
  MqMessageService,
  QueueMessage,
  QueuesModuleOptions,
} from "@solidxai/core";
import mailQueueOptions from "./email-queue-options-database";

@Injectable()
export class EmailQueueSubscriberDatabase extends DatabaseSubscriber<any> {
  constructor(
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
    // Delegate to application service
    return { success: true };
  }
}
```

## Naming Convention

Use clear broker-specific class names:

- `NamePublisherDatabase`, `NameSubscriberDatabase`
- `NamePublisherRabbitmq`, `NameSubscriberRabbitmq`

Register them as standard Nest providers in the relevant module.

## Environment Variables

### Broker selection

- `QUEUES_DEFAULT_BROKER`
  - `database` (default)
  - `rabbitmq`

- `QUEUES_RABBIT_MQ_URL` (RabbitMQ only)
  - example: `amqp://guest:guest@127.0.0.1:5672`

### Service role

- `QUEUES_SERVICE_ROLE`
  - `subscriber` -> only consumes
  - `both` -> publishes and consumes

### Queue enablement filter

- `QUEUES_QUEUE_NAME_REGEX_TO_ENABLE`
  - Regex used at subscriber startup to decide whether a subscriber should start for a queue.
  - `all` (or empty) means no queue-name filtering.
  - Examples:
    - `^solid_` -> only queues starting with `solid_`
    - `^(?!solid_).+` -> queues not starting with `solid_`

### Startup guards used by subscribers

- `SOLID_CLI_RUNNING`
  - Subscribers skip startup when this is `"true"`.
- `QUEUES_DEFAULT_BROKER`
  - Database subscribers start only when broker is `database`.
  - RabbitMQ subscribers start only when broker is `rabbitmq`.

### Notification queue toggles

- `COMMON_EMAIL_SHOULD_QUEUE`
- `COMMON_SMS_SHOULD_QUEUE`

## Scaling and Workload Isolation

SolidX background jobs can be scaled using the same codebase by combining:

1. Role-based startup (`QUEUES_SERVICE_ROLE`)
2. Queue-name filtering (`QUEUES_QUEUE_NAME_REGEX_TO_ENABLE`)
3. RabbitMQ concurrency tuning (`prefetch`)
4. Horizontal replicas (multiple worker processes/containers)

### 1) Role-based process split

- Keep API nodes as `both` when load is small.
- For higher load, run dedicated worker nodes with:
  - `QUEUES_SERVICE_ROLE=subscriber`
- This isolates queue processing from HTTP request traffic.

### 2) Queue-based workload split

Use queue-name regex to route different queue groups to different worker pools.

Examples:

- Worker pool A: `QUEUES_QUEUE_NAME_REGEX_TO_ENABLE=^solid_`
- Worker pool B: `QUEUES_QUEUE_NAME_REGEX_TO_ENABLE=^(?!solid_).+`

This lets you scale specific business workloads independently.

### 3) RabbitMQ throughput tuning with `prefetch`

`prefetch` (RabbitMQ only) controls in-flight messages per subscriber instance.

- Increase `prefetch` to improve parallelism per process.
- Keep it aligned with downstream capacity (DB, external APIs, CPU/memory).
- Combine with multiple process replicas for horizontal scaling.

### 4) Horizontal replicas

Run multiple instances of the same subscriber service (PM2, ECS tasks, Kubernetes pods, etc.).

- Same queue + multiple replicas -> competing consumers distribution.
- Different regex filters + dedicated replicas -> isolated queue domains.

## Deployment Note

A practical deployment pattern is to run:

1. Main backend service (API + optional publisher role)
2. One or more dedicated subscriber services
3. Optional subscriber pools per queue regex group

### PM2 example: main backend

```js
module.exports = {
  apps: [
    {
      name: "erp_solid_backend",
      script: "npm",
      args: "run start",
    },
  ],
};
```

### PM2 example: solid_* subscriber pool

```js
module.exports = {
  apps: [
    {
      name: "solid_subscribers",
      script: "npm",
      args: "run start",
      env: {
        PORT: "5000",
        QUEUES_SERVICE_ROLE: "subscriber",
        QUEUES_QUEUE_NAME_REGEX_TO_ENABLE: "^solid_",
        SOLID_SCHEDULER_ENABLED: "false",
      },
    },
  ],
};
```

### PM2 example: non-solid subscriber pool

```js
module.exports = {
  apps: [
    {
      name: "app_subscribers",
      script: "npm",
      args: "run start",
      env: {
        PORT: "4000",
        QUEUES_SERVICE_ROLE: "subscriber",
        QUEUES_QUEUE_NAME_REGEX_TO_ENABLE: "^(?!solid_).+",
        SOLID_SCHEDULER_ENABLED: "false",
      },
    },
  ],
};
```

The same model maps directly to ECS:

- Build one container image from the same codebase.
- Create separate ECS task definitions/services with different environment variables.
- Scale task count independently per subscriber service based on queue pressure.

## Broker Selection Guidance

Use Database broker when:

- You want zero external queue infrastructure
- Throughput is moderate
- Simplicity is preferred

Use RabbitMQ when:

- Throughput is high
- You need stronger queueing characteristics
- You want fine-grained concurrency control using `prefetch`

RabbitMQ management UI (default local setup): `http://localhost:15672` (`guest/guest`).

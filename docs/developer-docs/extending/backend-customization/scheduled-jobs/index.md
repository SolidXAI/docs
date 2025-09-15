---
sidebar_position: 2
title: Scheduled Jobs
description: Learn how to write the scheduled jobs in your SolidX application.
keywords: [backend, scheduled jobs, customization]
---

#  Creating Scheduled Jobs

Scheduled jobs in SolidX allow you to run recurring tasks such as sending notifications, cleaning up records, syncing data, or performing regular maintenance.

This section walks you through how to create and integrate custom scheduled jobs into your application.

---

##  Adding a New Scheduled Job

Follow these steps to define and use a custom scheduled job:

### 1 Create a Job Service

Create a new service class that implements the `IScheduledJob` interface.

<details>
<summary>Example: HelloWorld Scheduled Job</summary>

```ts
import { Injectable, Logger } from '@nestjs/common';
import { IScheduledJob, ScheduledJob, ScheduledJobProvider } from '@solidstarters/solid-core';

@Injectable()
@ScheduledJobProvider()
export class HelloWorldJobService implements IScheduledJob {
  private readonly logger = new Logger(HelloWorldJobService.name);

  async execute(reminder: ScheduledJob): Promise<void> {
    this.logger.log(`Hello from job: ${reminder.job}`);
    this.logger.log(`Reminder Name: ${reminder.scheduleName}, ID: ${reminder.id}`);
  }
}
```
</details>

### 2 Register the Service

Ensure the job service is registered in the appropriate module under the providers array.

### 3 Define the Job in Metadata

Add the job definition in your metadata.json or job configuration file.

<details>
<summary>Example Metadata Configuration</summary>

```json
{
  "scheduledJobs": [
    {
      "scheduleName": "Fees Due Email",
      "isActive": false,
      "frequency": "Daily",
      "startTime": null,
      "endTime": null,
      "startDate": null,
      "endDate": null,
      "dayOfMonth": null,
      "lastRunAt": null,
      "nextRunAt": null,
      "dayOfWeek": ["Thursday", "Friday"],
      "job": "SendEmailScheduleJobs",
      "moduleUserKey": "fees-portal"
    }
  ]
}
```
</details>

⸻

###  How It Works (TODO)
	- How job schedules are evaluated
	-	Triggering mechanism and intervals

⸻

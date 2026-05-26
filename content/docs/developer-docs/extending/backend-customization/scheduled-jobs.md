---
title: Scheduled Jobs
description: Learn how to write the scheduled jobs in your SolidX application.
summary: Explains creating scheduled jobs in SolidX for recurring tasks like notifications, cleanup, syncing, or maintenance. Covers implementing `IScheduledJob` interface with `@ScheduledJobProvider()` decorator, registering job services in modules, defining job metadata with schedule name, frequency, days of week, job class name, and module reference. Includes examples like `HelloWorldJobService` and late fee calculation jobs.
keywords: [backend, scheduled jobs, customization]
solidx_concerns: [add_scheduled_job]
---

#  Creating Scheduled Jobs

Scheduled jobs in SolidX allow you to run recurring tasks such as sending notifications, cleaning up records, syncing data, or performing regular maintenance.

This section walks you through how to create and integrate custom scheduled jobs into your application.

##  Adding a New Scheduled Job

Follow these steps to define and use a custom scheduled job:

### 1 Create a Job Service

Create a new service class that implements the `IScheduledJob` interface.

<details>
 <summary>
    
    Example: HelloWorld Scheduled Job
</summary>

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
 <summary>
    
    Example Metadata Configuration
</summary>

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

### Supported Frequencies
- Every Minute
- Hourly
- Daily
- Weekly
- Monthly

###  How It Works
	- How job schedules are evaluated
    - The SchedulerServiceImpl in @solidstarters/solid-core is responsible for evaluating and executing scheduled jobs.
    - Job Execution Flow:
      1. Fetch Active Jobs: The service retrieves all active scheduled jobs from the database.
      2. Determine Due Jobs: It checks each job's nextRunAt against the current time to identify jobs that are due for execution.
      3. Execute Jobs: For each due job, it invokes the corresponding job service's execute method.
      4. Update Job Metadata: After execution, it updates the job's lastRunAt and nextRunAt fields based on the defined frequency.  
	-	Triggering mechanism and intervals

---
title: Scheduled Jobs Configuration
description: Guide for configuring and managing scheduled jobs in SolidX
---

## Scheduled Jobs Configuration

### Overview

SolidX provides a declarative scheduled jobs system that allows you to configure recurring tasks using JSON metadata. Jobs are automatically registered by the platform and can be managed through the admin interface.

### Configuration Location

Scheduled jobs are defined in your module's metadata file:
- **File:** `solid-api/module-metadata/{module-name}/{module-name}-metadata.json`
- **Section:** `scheduledJobs` array

### Configuration Properties

| Property | Description | Possible Values |
|----------|-------------|-----------------|
| **scheduleName** | Human-readable name for the job | Any string |
| **isActive** | Whether the job is enabled | `true`, `false` |
| **frequency** | How often the job runs | "Hourly", "Daily", "Weekly", "Monthly" |
| **startTime** | Time of day to start (optional) | `null`, "HH:MM:SS" format |
| **endTime** | Time of day to stop (optional) | `null`, "HH:MM:SS" format |
| **startDate** | Date to begin running job (optional) | `null`, ISO date string |
| **endDate** | Date to stop running job (optional) | `null`, ISO date string |
| **dayOfMonth** | Day of month for monthly jobs | `0` (not used), `1-31` |
| **dayOfWeek** | JSON array of days to run | `"[\"Monday\",\"Tuesday\",...]"` |
| **job** | Class name of the job implementation | Must match TypeScript class name |
| **moduleUserKey** | Module identifier | Your module's user key |

### Example Configuration

**Hourly Job:**
```json
{
  "scheduleName": "Late Fee Calculation",
  "isActive": true,
  "frequency": "Hourly",
  "startTime": null,
  "endTime": null,
  "startDate": null,
  "endDate": null,
  "dayOfMonth": 0,
  "dayOfWeek": "[\"Monday\",\"Tuesday\",\"Wednesday\",\"Thursday\",\"Friday\",\"Saturday\",\"Sunday\"]",
  "job": "LateFeePaymentCalculatorScheduledJob",
  "moduleUserKey": "fees-portal"
}
```

**Daily Job:**
```json
{
  "scheduleName": "Fees Due Email",
  "isActive": true,
  "frequency": "Daily",
  "startTime": null,
  "endTime": null,
  "startDate": null,
  "endDate": null,
  "dayOfMonth": 0,
  "dayOfWeek": "[\"Monday\",\"Tuesday\",\"Wednesday\",\"Thursday\",\"Friday\",\"Saturday\",\"Sunday\"]",
  "job": "SendEmailScheduleJobs",
  "moduleUserKey": "fees-portal"
}
```

**Weekly Job (Specific Days):**
```json
{
  "scheduleName": "Weekly Report Generation",
  "isActive": true,
  "frequency": "Weekly",
  "startTime": "09:00:00",
  "endTime": null,
  "startDate": null,
  "endDate": null,
  "dayOfMonth": 0,
  "dayOfWeek": "[\"Monday\",\"Friday\"]",
  "job": "WeeklyReportScheduledJob",
  "moduleUserKey": "fees-portal"
}
```

**Monthly Job:**
```json
{
  "scheduleName": "Monthly Invoice Generation",
  "isActive": true,
  "frequency": "Monthly",
  "startTime": "00:00:00",
  "endTime": null,
  "startDate": null,
  "endDate": null,
  "dayOfMonth": 1,
  "dayOfWeek": "[\"Monday\",\"Tuesday\",\"Wednesday\",\"Thursday\",\"Friday\",\"Saturday\",\"Sunday\"]",
  "job": "MonthlyInvoiceScheduledJob",
  "moduleUserKey": "fees-portal"
}
```

### Implementation Structure

Each scheduled job requires a corresponding TypeScript class:

**File Location:** `solid-api/src/{module-name}/scheduled-jobs/{job-name}.service.ts`

**Basic Template:**
```typescript
import { Injectable } from '@nestjs/common';
import { ScheduledJob } from 'src/decorators/scheduled-job.decorator';

@Injectable()
@ScheduledJob()
export class YourScheduledJobClassName {
  constructor(
    // Inject required services
  ) {}

  async execute() {
    // Your job logic here
    console.log('Job executed at:', new Date());

    // Example: Query database
    // const items = await this.yourService.find({ ... });

    // Example: Process items
    // for (const item of items) {
    //   await this.processItem(item);
    // }
  }
}
```

### How to Modify Job Schedules

#### 1. Change Frequency
Update the `frequency` field in the metadata JSON:
```json
"frequency": "Daily"  // Change from "Hourly" to "Daily"
```

#### 2. Restrict to Specific Days
Modify the `dayOfWeek` array:
```json
"dayOfWeek": "[\"Monday\",\"Wednesday\",\"Friday\"]"  // Run only on specific weekdays
```

#### 3. Add Time Windows
Set `startTime` and `endTime` for business hours only:
```json
"startTime": "09:00:00",
"endTime": "17:00:00"
```

#### 4. Enable/Disable Jobs
Toggle the `isActive` flag:
```json
"isActive": false  // Temporarily disable without removing configuration
```

#### 5. Set Date Ranges
Use `startDate` and `endDate` for seasonal or time-limited jobs:
```json
"startDate": "2024-01-01",
"endDate": "2024-12-31"
```

#### 6. Schedule Monthly Jobs
Set the `dayOfMonth` field:
```json
"frequency": "Monthly",
"dayOfMonth": 15  // Run on the 15th of each month
```

### Common Use Cases

#### Late Fee Calculation
- **Frequency:** Hourly or Daily
- **Purpose:** Calculate and apply late fees for overdue payments
- **Best Practice:** Run hourly during business hours to ensure timely updates

#### Email Reminders
- **Frequency:** Daily or Weekly
- **Purpose:** Send reminder emails to users
- **Best Practice:** Run early morning (before business hours) to ensure emails are ready

#### Report Generation
- **Frequency:** Daily, Weekly, or Monthly
- **Purpose:** Generate and distribute reports
- **Best Practice:** Run during off-peak hours (e.g., midnight or early morning)

#### Data Cleanup
- **Frequency:** Daily or Weekly
- **Purpose:** Clean up old or temporary data
- **Best Practice:** Run during off-peak hours to minimize database load

### Benefits of SolidX Scheduled Jobs

- **Declarative Configuration:** No need to write cron expressions manually
- **UI Management:** Jobs can be managed through SolidX admin interface
- **Centralized Definition:** All job configurations in one place (metadata JSON)
- **Easy Debugging:** Clear visibility of job schedules and status
- **Automatic Registration:** Jobs are automatically registered when module loads
- **Flexible Scheduling:** Multiple options for controlling when jobs run
- **Type Safety:** TypeScript classes ensure compile-time checking
- **Dependency Injection:** Full access to NestJS dependency injection

### Best Practices

1. **Use Descriptive Names:** Choose clear `scheduleName` values that explain what the job does
2. **Start with Inactive:** Set `isActive: false` when first creating a job to test it manually
3. **Log Execution:** Include logging in your job implementation for debugging
4. **Handle Errors:** Wrap job logic in try-catch blocks to prevent job failures from stopping execution
5. **Optimize Frequency:** Don't run jobs more frequently than needed to reduce server load
6. **Use Time Windows:** Restrict jobs to business hours when appropriate
7. **Monitor Performance:** Track how long jobs take to execute and optimize as needed
8. **Test Thoroughly:** Test jobs in a development environment before enabling in production

### Troubleshooting

**Job Not Running:**
- Check `isActive` is set to `true`
- Verify the `job` class name matches exactly (case-sensitive)
- Ensure the job class is properly decorated with `@ScheduledJob()`
- Check server logs for registration errors

**Job Running Too Often:**
- Review `frequency` setting
- Check `dayOfWeek` configuration
- Verify `startTime` and `endTime` if set

**Job Not Running on Expected Days:**
- Ensure `dayOfWeek` array includes the correct day names
- Day names must be capitalized: "Monday", "Tuesday", etc.
- Verify the array is properly JSON-encoded as a string

**Job Failing:**
- Check server logs for error messages
- Verify all required dependencies are injected
- Ensure database connections and external services are available
- Add error handling to catch and log failures

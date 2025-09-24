---
title: Scheduled Jobs
description: Metadata schema for defining scheduled jobs in SolidX applications.
sidebar_position: 12
---

## Overview
Scheduled jobs in SolidX allow you to run recurring tasks such as sending notifications, cleaning up records, syncing data, or performing regular maintenance.

For a guide on how to create and manage scheduled jobs in SolidX, refer to the [Creating Scheduled Jobs](../../developer-docs/extending/backend-customization/scheduled-jobs/index.md).

## Example: Scheduled Jobs Metadata
<details>
<summary> Scheduled Jobs Schema </summary>
``` json
{
  "scheduledJobs": [
    {
      "scheduleName": "Late Fee Calculation",
      "isActive": true,
      "frequency": "Every Minute",
      "dayOfWeek": "[\"Tuesday\",\"Wednesday\",\"Thursday\",\"Monday\",\"Friday\",\"Saturday\",\"Sunday\"]",
      "job": "LateFeePaymentCalculatorScheduledJob",
      "moduleUserKey": "fees-portal"
    }
  ]
}
```
</details>
## Scheduled Jobs Metadata Attributes

### `scheduleName` *(string, required, unique)*
Name of the scheduled job.

### `isActive` *(boolean, optional)*
Indicates whether the scheduled job is active and should run according to its schedule.
**Default**: `false`

### `frequency` *(string, required)*
Frequency at which the job should run. Supported values include:
- `Every Minute`
- `Hourly`
- `Daily`
- `Weekly`
- `Monthly`

### `dayOfWeek` *(string, mandatory for Weekly frequency)*
Days of the week on which the job should run (applicable for weekly frequency). This should be a JSON array of day names. Please ensure that the value is a valid JSON array string in stringified format.

**Example:** `["Monday", "Wednesday", "Friday"]`  
**Applies to:** `Weekly` frequency
:::note
Currently the configuration expects json configuration in stringified format. In future releases, we may support direct array input.
:::


### `moduleUserKey` *(string, required)*
The user key of the module to which this scheduled job belongs. This helps in organizing and managing jobs by module.

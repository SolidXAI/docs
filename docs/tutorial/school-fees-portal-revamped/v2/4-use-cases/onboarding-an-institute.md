---
sidebar_position: 1
---

# Onboarding an Institute

### Foundation for Multi-Tenant School Fees Management

### Overview

Onboarding an Institute enables platform-level Super Admins (or Partner Admins) to register and configure multiple institutes inside a multi-tenant fees management platform.

Each institute operates as an independent tenant with its own:

- Admin users
- Payment gateway credentials
- Fee types & fee rules
- Student records & mapping
- Branding assets (logo, brochure, video, etc.)
- Settlement & transaction logs
- Notification/webhook flows

### Once created, the institute becomes a fully isolated logical tenant, ensuring no cross-institute data leakage.

## Why a Multi-Tenant Architecture?

The School Fees Portal is designed to onboard **N number of institutes**, each working independently.  
This architecture provides:

| Benefit | Explanation |
|--------|-------------|
| **Scalability** | Any number of institutes can be added without affecting others. |
| **Data Isolation** | Record rules ensure one institute cannot access another’s data. |
| **Customisation** | Each institute has its own fees, admins, branding, and PG setup. |
| **Operational Independence** | If one institute faces issues, others remain unaffected. |
| **Centralised Governance** | Super Admin retains global visibility and control. |

---

## Onboarding Workflow (Step-by-Step)

The onboarding flow is intentionally modular. An institute can start with basic configuration and progressively enable:

- Institute Profile & Branding
- Admin Users
- Academic Structure
- Fee Types & Fee Rules
- Student Imports
- Payment Gateway Setup
- Late Fee Rules
- Notifications & Webhooks
- Scheduled Automation Jobs

## Subscribers — Background Processing on Uploads
Subscribers allow you to respond to specific database events asynchronously, without blocking user actions.

Real Use-Case:
When an institute uploads a student data Excel file or payment mapping file, the system uses a subscriber to parse and import the file in the background.

### Why Subscribers?

-  Excel parsing is time-consuming
-  Avoid UI blocking
-  Allow progress logs
-  Automate import without manual triggers

```typescript
@EventSubscriber()
export class MediaTransactionSubscriber implements EntitySubscriberInterface<Media> {
  constructor(private readonly excelParserService: ExcelParserService) {}

  listenTo() {
    return Media;
  }

  async afterInsert(event: InsertEvent<Media>) {
    const media = event.entity;

    if (media.modelName === 'paymentCollection' && media.fieldName === 'paymentFile') {
      console.log(`Processing payment file: ${media.fileName}`);
      this.excelParserService.processStudentFeeFile(media);
    }
  }
}
```


## Computed Fields — Automatic Calculations

Computed fields allow the system to calculate values automatically instead of manually storing and updating them.

### Why Computed Fields?

- Prevents accidental inconsistencies
- Guarantees latest values every time
- Reduces repetitive logic
- Perfect for payment-related calculations

### Example: Auto-updating Fee Payment Status

Every time a payment is recorded, the item’s amountPaid, amountPending, and paymentStatus are recalculated automatically.

```typescript
@ComputedFieldProvider()
@Injectable()
export class PaymentCollectionItemAmountProvider implements IEntityPostComputeFieldProvider<PaymentCollectionItemDetail, any> {
  constructor(
    @InjectEntityManager()
    private readonly entityManager: EntityManager,
  ) { }

  async postComputeAndSaveValue(
    triggerEntity: PaymentCollectionItemDetail,
    computedFieldMetadata: ComputedFieldMetadata<any>,
  ): Promise<void> {
    if (!triggerEntity?.paymentCollectionItem?.id) {
      console.error('Payment Collection Item Id Missing');
    }
    const paymentCollectionItemDetailId = triggerEntity?.id;

    const { amountPaid, totalAmountToBePaid, amountPending, status } = await this.getPaymentCollectionItemAmounts(triggerEntity?.paymentCollectionItem?.id);

    const result = await this.entityManager.update(
      PaymentCollectionItem,
      { id: triggerEntity?.paymentCollectionItem?.id },
      {
        amountPaid: String(amountPaid),
        amountPending: String(amountPending),
        totalAmountToBePaid: String(totalAmountToBePaid),
        status: status,
      },
    );
  }
```

## Composite Indexes — Multi-Column Uniqueness & Speed

Composite indexes guarantee data integrity and provide massive performance improvements on institute-scoped queries.

### Why Composite Indexes?

Prevent duplicate records within a tenant

- Improve query performance
- Enforce unique constraints per institute
- Example: Student ID Must Be Unique Within an Institute

```typescript
@Entity('fees_portal_student')
@Index(['institute', 'studentId'], { unique: true })
export class Student extends BaseEntity {
  @Column()
  studentId: string;
}
```

## Scheduled Jobs — Nightly Automation

SolidX provides a powerful built-in scheduler that allows modules to run automated background tasks at configurable intervals.
These jobs ensure that data remains consistent, fee cycles stay updated, and time-bound processes (such as late fee calculation or reminders) run without manual intervention.

Scheduled jobs can be configured per-institute (tenant-level) or globally at the module level.

### SolidX allows two mechanisms for configuring scheduled jobs:

### 1. Through the SolidX Admin UI (Preferred)

Admins can enable or disable jobs, adjust frequency, and set execution windows directly in the SolidX Admin Panel.
The UI validates values and helps ensure safe, tenant-compatible configurations.

### 2. Through Module Metadata (Developer Mode)

Developers can register scheduled jobs inside the module metadata JSON file.

`/solid-api/module-metadata/fees-portal/fees-portal-metadata.json`

### Example Definition 

```typescript
"scheduledJobs": [
  {
    "scheduleName": "Late Fee Calculation",
    "isActive": true,
    "frequency": "Hourly",
    "startTime": null,
    "endTime": null,
    "startDate": null,
    "endDate": null,
    "dayOfMonth": 0,
    "lastRunAt": "2025-09-05T07:09:00.009Z",
    "nextRunAt": "2025-09-05T07:10:00.009Z",
    "dayOfWeek": [
      "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
    ],
    "job": "LateFeePaymentCalculatorScheduledJob",
    "moduleUserKey": "fees-portal"
  }
]
```

### Important Fields

| Key                     | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `scheduleName`          | Label shown in UI and logs.                               |
| `frequency`             | One of: `Hourly`, `Daily`, `Weekly`, `Monthly`, `Yearly`. |
| `dayOfWeek`             | Days applicable (for weekly schedules).                   |
| `startTime` / `endTime` | Optional execution window.                                |
| `job`                   | The TypeScript class implementing the job.                |
| `moduleUserKey`         | SolidX module owner of the job.                           |

### Example: Late Fee Calculation Job

```typescript
@Injectable()
@ScheduledJobProvider()
export class LateFeePaymentCalculatorScheduledJob implements IScheduledJob {
  private readonly logger = new Logger(LateFeePaymentCalculatorScheduledJob.name);

  constructor(
    @InjectEntityManager()
    private readonly entityManager: EntityManager,
  ) {}

  async execute(reminder: ScheduledJob): Promise<void> {
    this.logger.debug(`Executing job: ${reminder.job}`);
    this.logger.debug(`Schedule: ${reminder.scheduleName} | ID: ${reminder.id}`);

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Fetch overdue items
    const items = await this.entityManager.find(PaymentCollectionItem, {
      where: {
        dueDate: LessThan(today),
        status: Not(In(['Cancelled', 'Fully Paid'])),
      },
      relations: ['feeType', 'institute'],
    });

    this.logger.debug(`Found ${items.length} overdue payment collection items.`);

    const filteredItems = items.filter(
      item =>
        item.feeType?.latePaymentFeesType &&
        item.feeType.latePaymentFeesType !== 'None',
    );

    for (const item of filteredItems) {
      const dueDate = new Date(item.dueDate);
      dueDate.setHours(0, 0, 0, 0);

      const now = new Date();
      now.setHours(0, 0, 0, 0);

      const overdueByDays = Math.floor(
        (now.getTime() - dueDate.getTime()) / 86400000,
      );

      const amountToBePaid = Number(item.amountToBePaid || 0);
      const amountPaid = Number(item.amountPaid || 0);
      const basePending = amountToBePaid - amountPaid;

      let lateAmountToBePaid = 0;

      if (item.feeType.latePaymentFeesType === 'Percent') {
        lateAmountToBePaid =
          (basePending * Number(item.feeType.latePaymentFees || 0)) / 100;
      } else if (item.feeType.latePaymentFeesType === 'Absolute') {
        lateAmountToBePaid = Number(item.feeType.latePaymentFees || 0);
      }

      lateAmountToBePaid = Math.round(lateAmountToBePaid * 100) / 100;

      const totalAmountToBePaid = amountToBePaid + lateAmountToBePaid;
      const amountPending = totalAmountToBePaid - amountPaid;

      await this.entityManager.update(
        PaymentCollectionItem,
        { id: item.id },
        {
          lateAmountToBePaid,
          overdueByDays,
          amountPending: String(amountPending),
          totalAmountToBePaid: String(totalAmountToBePaid),
        },
      );
    }

    this.logger.debug(`Late fee calculation completed for ${filteredItems.length} items.`);
  }
}
```
:::tip Multi-Frequency Scheduler
SolidX allows each institute to configure reminder and automation jobs in multiple frequencies:
Daily, Weekly, Monthly, Yearly, or even Hourly for internal calculations like late fees.

This provides tenant-level flexibility so each institute can align automation with their internal fee policies.
:::
---
sidebar_position: 1
---

# 1. Onboarding an Institute

## Business Reason

The **Onboarding an Institute** use-case enables the platform’s **Super Admin** (or a Third-Party Admin) to register and manage multiple institutes inside a **multi-tenant fees management platform**.

This is the **core foundation** of the system, because each institute behaves as a completely independent tenant with its own:

- Dedicated institute admins  
- Individual payment gateway credentials  
- Custom fee types and fee rules  
- Student records and fee mappings  
- Branding (Institutes Logo, Institutes Brochure, Intro Video etc.)  
- Transaction & settlement history  
- Custom webhooks and email flows  

Once an institute is created, it becomes a *logically isolated tenant*—ensuring that all data, actions, and workflows within that institute remain fully isolated from all others.

---

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


The onboarding process is deliberately modular, allowing each institute to onboard at its own pace — starting with basic settings, and later configuring deeper features like customized fee types, late-fee rules, and payment workflows.

## Technical Deep-Dive: Advanced SolidX Concepts
Below are the core SolidX features used during Institute Onboarding. These govern data automation, validation, indexing, and asynchronous flows across the system.

## 1. Subscribers — Background Processing on Uploads
Subscribers allow you to respond to specific database events asynchronously, without blocking user actions.

Real Use-Case:
When an institute uploads a student data Excel file or payment mapping file, the system uses a subscriber to parse and import the file in the background.

Why Subscribers?

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


## 2. Computed Fields — Automatic Calculations

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

## 3. Composite Indexes — Multi-Column Uniqueness & Speed

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

## 4. Scheduled Jobs — Nightly Automation

Scheduled jobs keep the system clean and proactive without manual admin effort.

## Common Jobs During Onboarding Phase

- Pre-calculate late fees
- Send overdue payment reminders
- Cleanup temporary media files
- Generate institute reports
- Example: Nightly Overdue Reminder Job

```typescript
@Cron(CronExpression.EVERY_DAY_AT_8AM)
async handleOverduePaymentReminders() {
  const overdueItems = await this.findOverdueItems();

  for (const item of overdueItems) {
    await this.emailService.send({
      to: item.student.parentEmailAddress,
      subject: `Payment Reminder: ${item.feeType.name} overdue`,
      template: 'overdue-reminder',
      context: {
        studentName: item.student.studentName,
        amount: item.amountPending,
        dueDate: item.dueDate,
      },
    });
  }
}
```
:::tip Multi-Frequency Scheduler
The platform supports flexible reminder scheduling for each institute.  
You can configure reminders to run **Daily**, **Weekly**, **Monthly**, or **Yearly**, giving institutes full control over how often parents receive fee notifications.  
This ensures every tenant can align the reminder cycle with their internal policies.
:::
---
sidebar_position: 1
---

# 1. Onboarding an Institute

## Business Reason

The "Onboarding an Institute" use case is the foundational step in the school fees portal. It allows a super administrator to register a new educational institution onto the platform. This process is crucial because it captures all the essential details about the institute, including its name, contact information, payment gateway credentials, and branding assets. A well-defined onboarding process ensures that each institute is set up correctly and can operate independently within the multi-tenant environment of the portal.

## Onboarding Workflow

The onboarding process involves the Super Admin creating the institute, setting up its users, defining fee structures, and configuring technical details. The UI is broken down into logical tabs to make this manageable.

```mermaid
graph TD
    A[Super Admin logs in] --> B{Go to <br/> 'fees-portal' -> Institute};
    B --> C[Clicks 'Add Institute'];
    C --> D[Fills in Institute Details & Branding];
    D --> E[Fills in Payment Gateway Credentials];
    E --> F[Saves Institute Record];
    F --> G{Create Institute <br/> Admin User};
    G --> H[Go to 'Solid Core' -> Users];
    H --> I[Add New User (email, name)];
    I --> J{Link User to Institute};
    J --> K[In User form, go to 'Institute User' tab];
    K --> L[Select Institute and User Type];
    L --> M[Save User];
    M --> N((Institute Onboarded));
    N --> O[Institute Admin receives credentials <br/> and can now log in];

```

---

## Technical Deep-Dive: Advanced SolidX Concepts

This workflow leverages several powerful, advanced features of SolidX. Here’s how they work, with code examples.

### 1. Subscribers (for Bulk Data Upload)

**Concept:** Subscribers are services that listen for specific database events (like `afterInsert`, `afterUpdate`) and execute custom logic. This is perfect for automation. The `MediaTransactionSubscriber` is a key example for processing bulk student uploads.

**Example:** When an admin uploads an Excel file to a `PaymentCollection`, this subscriber can automatically parse it.

```typescript
// school-fees-portal/solid-api/src/fees-portal/subscribers/media-transaction.subscriber.ts

import { EventSubscriber, EntitySubscriberInterface, InsertEvent } from 'typeorm';
import { Media } from '@solid-softworks/solid-core';
import { ExcelParserService } from '../services/excel-parser.service';

@EventSubscriber()
export class MediaTransactionSubscriber implements EntitySubscriberInterface<Media> {
  constructor(private readonly excelParserService: ExcelParserService) {}

  listenTo() {
    return Media;
  }

  /**
   * Called after a Media entity is inserted.
   */
  async afterInsert(event: InsertEvent<Media>) {
    const media = event.entity;

    // Check if the uploaded file is for a PaymentCollection
    if (media.modelName === 'paymentCollection' && media.fieldName === 'paymentFile') {
      console.log(`New payment file uploaded: ${media.fileName}. Starting processing...`);
      
      // Don't await this; let it run in the background
      this.excelParserService.processStudentFeeFile(media);
    }
  }
}
```

### 2. Computed Fields (for Automatic Calculations)

**Concept:** Computed fields dynamically calculate their values based on other data, often triggered by events on related models. This saves you from writing repetitive calculation logic.

**Example:** The `PaymentCollectionItemAmountProvider` automatically calculates the `amountPaid` and `amountPending` on a `PaymentCollectionItem` whenever a new `PaymentCollectionItemDetail` (a payment) is added.

```typescript
// school-fees-portal/solid-api/src/fees-portal/providers/payment-collection-item-amount.provider.ts

import { Injectable } from '@nestjs/common';
import { IComputedFieldProvider } from '@solid-softworks/solid-core';

@Injectable()
export class PaymentCollectionItemAmountProvider implements IComputedFieldProvider {
  
  // This method is automatically called by SolidX when a trigger event occurs
  async computeValue(context: any, ...args: any[]): Promise<any> {
    const { paymentCollectionItem } = context;

    // 1. Find all related payment details
    const details = await this.itemDetailRepo.find({
      where: { paymentCollectionItem: { id: paymentCollectionItem.id }, paymentStatus: 'Succeeded' },
    });

    // 2. Calculate the total amount paid
    const amountPaid = details.reduce((sum, detail) => sum + Number(detail.amountPaid), 0);

    // 3. Update the parent item's fields
    paymentCollectionItem.amountPaid = amountPaid;
    paymentCollectionItem.amountPending = paymentCollectionItem.amountToBePaid - amountPaid;

    // 4. Update the status
    if (paymentCollectionItem.amountPending <= 0) {
      paymentCollectionItem.status = 'Fully Paid';
    } else {
      paymentCollectionItem.status = 'Partially Paid';
    }

    await this.itemRepo.save(paymentCollectionItem);

    return amountPaid;
  }
}
```

### 3. Composite Indexes (for Data Integrity)

**Concept:** A composite index spans multiple columns. It's used to speed up queries that filter on those columns and, critically, to enforce multi-column uniqueness.

**Example:** To ensure a `studentId` is unique *per institute* (but can be duplicated across different institutes), you would add a composite index to the `Student` entity.

```typescript
// school-fees-portal/solid-api/src/fees-portal/entities/student.entity.ts

import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '@solid-softworks/solid-core';

@Entity('fees_portal_student')
@Index(['institute', 'studentId'], { unique: true }) // <-- COMPOSITE INDEX
export class Student extends BaseEntity {
  
  @Column()
  studentId: string;

  // ... other columns and relations
}
```

### 4. Scheduled Jobs (for Automation)

**Concept:** SolidX uses the NestJS Schedule package to allow you to run tasks automatically at specific intervals (e.g., every night at 2 AM). This is ideal for maintenance, reminders, and report generation.

**Example:** A scheduled job to find overdue payments and send email reminders.

```typescript
// school-fees-portal/solid-api/src/fees-portal/services/reminder.service.ts

import { Injectable } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { EmailService } from '@solid-softworks/solid-core';

@Injectable()
export class ReminderService {
  constructor(private readonly emailService: EmailService) {}

  @Cron(CronExpression.EVERY_DAY_AT_8AM)
  async handleOverduePaymentReminders() {
    console.log('Running daily check for overdue payments...');

    // 1. Find all payment items that are past their due date and not fully paid
    const overdueItems = await this.findOverdueItems();

    // 2. Loop through and send an email for each
    for (const item of overdueItems) {
      await this.emailService.send({
        to: item.student.parentEmailAddress,
        subject: `Payment Reminder: Your fee for ${item.feeType.name} is overdue`,
        template: 'overdue-reminder', // Uses a pre-defined email template
        context: {
          studentName: item.student.studentName,
          amount: item.amountPending,
          dueDate: item.dueDate,
        },
      });
    }
  }
}
```

---
sidebar_position: 2
title: Initiate Payment Collection
description: Learn how to create and manage payment collections for students in the Fees Portal.
summary: TODO
keywords: [TODO]
concerns: TODO
---

### Overview
Below are the key features related to initiating payment collections within the Fees Portal Platform:
- Bulk payment collection creation via Excel upload
- Automatic student record creation and updates
- Support for multiple fee types in a single collection
- Flexible payment modes (Cash and Payment Gateway)
- Automated email notifications to parents/guardians
- Due date management with late fee calculations
- Payment status tracking (Pending, Partially Paid, Fully Paid)
- Excel template generation based on institute's configured fee types

### Roles Involved
- Institute Admin

You can refer to the [User Roles & Responsibilities](./fees_portal_product_overview#user-roles--responsibilities) in the Product Overview for more details on this role.

### Data Models Involved

This section describes the data models you need to implement this feature.

#### 1. Student Model

**What it represents:** Individual students enrolled at your institution whose parents/guardians will receive payment collection requests.

##### Basic Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Student Name** | Yes | Full name of the student | "Rahul Sharma" |
| **Student ID** | Yes | Unique identifier for the student (roll number, admission number) | "STU2024001" |
| **Student Email Address** | No | Student's personal email address | rahul.sharma@example.com |
| **Student Mobile Number** | No | Student's contact number | 9876543210 |
| **Student Login ID** | Computed (Auto-generated) | System-generated unique alphanumeric identifier for portal access based on student name | "RAHUL-A1B2C" |

##### Parent/Guardian Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Parent/Guardian Name** | Yes | Name of parent or guardian | "Mr. Rajesh Sharma" |
| **Parent/Guardian Email** | Yes | Email where payment notifications will be sent | rajesh.sharma@example.com |
| **Parent/Guardian Mobile** | Yes | Contact number for SMS notifications | 9123456789 |

##### Authentication Fields

| Field | Required? | Description |
|-------|-----------|-------------|
| **OTP** | Auto-managed | One-time password for portal login |
| **OTP Expires At** | Auto-managed | Expiration timestamp for OTP |
| **Token** | Auto-managed | Authentication token after successful login |

##### What you can do with this model:
- Students are automatically created when you upload a payment collection Excel file
- If a student already exists (matched by Student ID), their information is updated
- Each student belongs to one institute
- Students receive payment notifications via parent/guardian email
- Students can log in to the portal to view and pay their dues

#### 2. Payment Collection Model

**What it represents:** A batch of fee collection requests sent to multiple students at once (e.g., "Q1 2024 Fees", "Annual Sports Fees 2024").

##### Basic Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Name** | Yes | Descriptive name for this collection batch | "Quarter 1 Tuition Fees 2024" |
| **Description** | No | Additional details about the collection | "First quarter fees including tuition and lab charges" |
| **Payment Collection ID** | Computed (Auto-generated) | Unique alphanumeric identifier for this collection based on collection name | "QUART-X7Y8Z" |
| **Due Date** | Yes | Default due date for all items in this collection | 2024-04-30 |
| **Payment File** | Yes | Excel file containing student and payment details | Upload .xlsx file (max 5MB) |
| **Institute** | Yes | Which institute this collection belongs to | Auto-filled based on logged-in user |

##### What you can do with this model:
- Create multiple payment collections throughout the year
- Each collection can include multiple students and multiple fee types
- Upload an Excel file to create all payment collection items at once
- Track which collections have been sent and when
- When you delete a collection, all associated payment collection items are removed

#### 3. Payment Collection Item Model

**What it represents:** An individual payment request for one student for one fee type within a collection (e.g., "Rahul Sharma needs to pay ₹10,000 for Tuition Fees").

##### Payment Details

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Amount To Be Paid** | Yes | Base fee amount (without late fees) | 10000.00 |
| **Due Date** | Yes | When this payment is due | 2024-04-30 |
| **Part Payment Allowed** | Yes | Can student pay in installments? | true/false (copied from Fee Type) |
| **Payment Mode** | Yes | How payment should be made | "PG" (Payment Gateway) or "CASH" |

##### Status Tracking

| Field | Required? | Description | Values |
|-------|-----------|-------------|--------|
| **Status** | Auto-managed | Current payment status | "Pending", "Partially Paid", "Fully Paid", "Cancelled" |
| **Amount Paid** | Computed (Auto-calculated) | Total amount paid so far, calculated from payment collection item details | 5000.00 |
| **Amount Pending** | Computed (Auto-calculated) | Remaining amount to be paid (total - paid) | 5000.00 |

##### Late Payment Tracking

| Field | Required? | Description | How It's Calculated |
|-------|-----------|-------------|---------------------|
| **Is Overdue** | Auto-managed | Is payment past due date? | true if today > due date |
| **Overdue By Days** | Auto-calculated | Number of days overdue | today - due date |
| **Late Amount To Be Paid** | Auto-calculated | Late fee penalty | Based on Fee Type's late fee configuration |
| **Total Amount To Be Paid** | Computed (Auto-calculated) | Base amount + late fees | amountToBePaid + lateAmountToBePaid |

##### Relationships

| Relationship | Description |
|--------------|-------------|
| **Student** | Which student owes this payment |
| **Fee Type** | What type of fee this is (Tuition, Bus, etc.) |
| **Payment Collection** | Which batch this item belongs to |
| **Institute** | Which institute is collecting this fee |

##### Understanding Payment Modes:

**Payment Gateway (PG)** - Choose this when:
- Parents/guardians will pay online through the portal
- Initial status: "Pending"
- Students receive email with payment link
- Payment processed through configured payment gateway
- Status updates automatically when payment succeeds

**Cash (CASH)** - Choose this when:
- Payment has already been collected offline (at school counter, bank deposit)
- Initial status: "Fully Paid"
- Amount paid = full amount
- Students receive payment confirmation email
- No further action needed from parent/guardian

##### What you can do with this model:
- Track individual payment obligations for each student
- Monitor payment status in real-time
- Calculate late fees automatically when due date passes
- View payment history through related Payment Collection Item Details
- Send reminder emails for pending payments

#### 4. Payment Collection Item Detail Model

**What it represents:** Individual payment transactions recorded against a payment collection item (tracks each installment or payment attempt).

##### Transaction Details

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Payment Date** | Yes | When the payment was made | 2024-03-15 14:30:00 |
| **Amount Paid** | Yes | Amount received in this transaction | 5000.00 |
| **Payment Status** | Yes | Status of this transaction | "Success", "Pending", "Failed" |

##### Relationships

| Relationship | Description |
|--------------|-------------|
| **Payment Collection Item** | Which payment request this transaction is for |
| **Student** | Which student made this payment |
| **Institute** | Which institute received this payment |
| **Payment** | Link to payment gateway transaction record |

##### What you can do with this model:
- Track partial payments and installments
- View complete payment history for each item
- Reconcile with payment gateway transactions
- Calculate total amount paid across multiple transactions

#### How These Models Connect

Understanding the relationships between your data:

```
Payment Collection (Batch: "Q1 2024 Fees")
  │
  ├── Contains multiple Payment Collection Items
  │   │
  │   ├── Item 1: Rahul Sharma - Tuition Fees - ₹10,000
  │   │   ├── Links to: Student (Rahul Sharma)
  │   │   ├── Links to: Fee Type (Tuition Fees)
  │   │   └── Has multiple Payment Collection Item Details
  │   │       ├── Detail 1: Paid ₹5,000 on 2024-03-15
  │   │       └── Detail 2: Paid ₹5,000 on 2024-04-10
  │   │
  │   ├── Item 2: Rahul Sharma - Bus Fees - ₹3,000
  │   │   └── Links to: Fee Type (Bus Fees)
  │   │
  │   └── Item 3: Priya Patel - Tuition Fees - ₹10,000
  │       └── Links to: Student (Priya Patel)
  │
  └── All items share same Payment Collection

Student (Rahul Sharma)
  ├── Has multiple Payment Collection Items across different collections
  │   ├── From "Q1 2024 Fees" collection
  │   ├── From "Annual Sports Fees" collection
  │   └── From "Library Fees" collection
  │
  └── Belongs to one Institute

Fee Type (Tuition Fees)
  ├── Used in multiple Payment Collection Items
  │   └── Different students, different collections
  │
  ├── Defines: Part payment allowed?
  └── Defines: Late fee calculation rules
```

#### Important Concepts

**Automatic Student Management:**
- When you upload an Excel file, the system checks if each student already exists (by Student ID)
- If the student exists: Updates their information with latest data from Excel
- If the student is new: Creates a new student record automatically
- You don't need to manually create students before uploading payment collections

**Status Flow for Payment Gateway Items:**
```
Upload Excel (PG mode) → Status: "Pending"
                              ↓
                     Student pays 50%
                              ↓
                    Status: "Partially Paid"
                              ↓
                     Student pays remaining
                              ↓
                    Status: "Fully Paid"
```

**Status Flow for Cash Items:**
```
Upload Excel (CASH mode) → Status: "Fully Paid"
                                 ↓
                         No further action needed
```

**Late Fee Calculation:**
- Runs automatically via scheduled job
- Only applies to items with status "Pending" or "Partially Paid"
- Calculation method comes from Fee Type configuration:
  - **Percent**: `(pending amount × late fee %) ÷ 100`
  - **Absolute**: Fixed late fee amount
  - **None**: No late fees applied
- Updates total amount to be paid automatically

### Building the Data Models

This section provides step-by-step instructions for creating the Student, Payment Collection, Payment Collection Item, and Payment Collection Item Detail models using SolidX. Follow these instructions to implement the data models discussed in the previous section.

#### 1. Creating the Student Model

Navigate to the model creation interface in SolidX and configure as follows:

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | student |
| **Plural Name** | students |
| **Display Name** | Student |
| **Description** | Model to capture student information |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_student |
| **Enable Audit Tracking** | Yes |
| **Enable Soft Delete** | No |
| **Draft Publish Workflow** | No |
| **Internationalization** | No |
| **Is Child Model** | No |

##### Field Definitions

Create the following fields in the order listed:

**Field 1: Student Name**

| Attribute | Value |
|-----------|-------|
| **Name** | studentName |
| **Display Name** | Student Name |
| **Type** | Short Text |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 2: Student Email Address**

| Attribute | Value |
|-----------|-------|
| **Name** | studentEmailAddress |
| **Display Name** | Student Email Address |
| **Type** | Short Text |
| **Required** | No |
| **Enable Audit Tracking** | Yes |

**Field 3: Student Mobile Number**

| Attribute | Value |
|-----------|-------|
| **Name** | studentMobileNumber |
| **Display Name** | Student Mobile Number |
| **Type** | Short Text |
| **Required** | No |
| **Enable Audit Tracking** | Yes |

**Field 4: Parent/Guardian Name**

| Attribute | Value |
|-----------|-------|
| **Name** | parentName |
| **Display Name** | Parent/Guardian Name |
| **Type** | Short Text |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 5: Parent/Guardian Mobile Number**

| Attribute | Value |
|-----------|-------|
| **Name** | parentMobileNumber |
| **Display Name** | Parent/Guardian Mobile Number |
| **Type** | Short Text |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 6: Parent/Guardian Email Address**

| Attribute | Value |
|-----------|-------|
| **Name** | parentEmailAddress |
| **Display Name** | Parent/Guardian Email Address |
| **Type** | Short Text |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 7: Student ID**

| Attribute | Value |
|-----------|-------|
| **Name** | studentId |
| **Display Name** | Student Id |
| **Type** | Short Text |
| **Required** | Yes |
| **Is User Key** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 8: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 9: Student Login ID (Computed Field)**

| Attribute | Value |
|-----------|-------|
| **Name** | studentLoginId |
| **Display Name** | Student Login Id |
| **Description** | This is the unique login id for the student. This is used to login to the student portal. |
| **Type** | Computed |
| **Computed Field Value Type** | String |
| **Computed Field Value Provider** | AlphaNumExternalIdComputationProvider |
| **Computed Field Value Provider Context** | `{"dynamicFieldPrefix": "studentName", "length": 5}` |
| **Computed Field Trigger Config** | Model: student, Operation: before-insert |
| **Required** | Yes |
| **Unique** | Yes |
| **Index** | No |
| **Enable Audit Tracking** | Yes |

**Note:** This field is automatically generated when a student is created, using an alphanumeric ID based on the student's name with a length of 5 characters.

**Field 10: OTP**

| Attribute | Value |
|-----------|-------|
| **Name** | otp |
| **Display Name** | OTP |
| **Type** | Short Text |
| **Required** | No |

**Field 11: OTP Expires At**

| Attribute | Value |
|-----------|-------|
| **Name** | otpExpiresAt |
| **Display Name** | OTP Expires At |
| **Type** | Datetime |
| **Required** | No |

**Field 12: Token**

| Attribute | Value |
|-----------|-------|
| **Name** | token |
| **Display Name** | Token |
| **Type** | Long Text |
| **Required** | No |

**Field 13: Payments Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | payments |
| **Display Name** | Payments |
| **Type** | Relation |
| **Relation Type** | One-to-Many |
| **Related Model** | payment |
| **Related Module** | fees-portal |
| **Related Field** | student |
| **Create Inverse** | Yes |
| **Cascade** | cascade |
| **Enable Audit Tracking** | No |

#### 2. Creating the Payment Collection Model

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | paymentCollection |
| **Plural Name** | paymentCollections |
| **Display Name** | Payment Collection |
| **Description** | Model used to capture information about a payment collection. A payment collection is a batch of payments that are collected together. |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_payment_collection |
| **Enable Audit Tracking** | Yes |
| **Enable Soft Delete** | No |
| **Draft Publish Workflow** | No |
| **Internationalization** | No |
| **Is Child Model** | No |

##### Field Definitions

**Field 1: Name**

| Attribute | Value |
|-----------|-------|
| **Name** | name |
| **Display Name** | Name |
| **Type** | Short Text |
| **Required** | Yes |
| **Index** | Yes |
| **Is User Key** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 2: Description**

| Attribute | Value |
|-----------|-------|
| **Name** | description |
| **Display Name** | Description |
| **Type** | Long Text |
| **Required** | No |

**Field 3: Due Date**

| Attribute | Value |
|-----------|-------|
| **Name** | dueDate |
| **Display Name** | Due Date |
| **Type** | Datetime |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 4: Payment Collection ID (Computed Field)**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentCollectionId |
| **Display Name** | Payment Collection ID |
| **Type** | Computed |
| **Computed Field Value Type** | String |
| **Computed Field Value Provider** | AlphaNumExternalIdComputationProvider |
| **Computed Field Value Provider Context** | `{"dynamicFieldPrefix": "name", "length": 5}` |
| **Computed Field Trigger Config** | Model: paymentCollection, Operation: before-insert |
| **Required** | Yes |
| **Unique** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Note:** This field is automatically generated when a payment collection is created, using an alphanumeric ID based on the collection's name with a length of 5 characters.

**Field 5: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 6: Payment File**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentFile |
| **Display Name** | Payment File |
| **Description** | The payment file that is uploaded by the institute admin |
| **Type** | Media (Single) |
| **Media Types** | file |
| **Media Max Size (KB)** | 5120 |
| **Required** | Yes |
| **Storage Provider** | default-filesystem |

**Field 7: Payment Collection Items Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentCollectionItems |
| **Display Name** | Payment Collection Items |
| **Type** | Relation |
| **Relation Type** | One-to-Many |
| **Related Model** | paymentCollectionItem |
| **Related Module** | fees-portal |
| **Related Field** | paymentCollection |
| **Create Inverse** | Yes |
| **Cascade** | cascade |
| **Enable Audit Tracking** | No |

#### 3. Creating the Payment Collection Item Model

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | paymentCollectionItem |
| **Plural Name** | paymentCollectionItems |
| **Display Name** | Payment Collection Item |
| **Description** | Model used to capture information about a payment collection item. A payment collection item is a single payment within a payment collection. |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_payment_collection_item |
| **Enable Audit Tracking** | Yes |
| **Enable Soft Delete** | No |
| **Draft Publish Workflow** | No |
| **Internationalization** | No |
| **Is Child Model** | No |

##### Field Definitions

**Field 1: Due Date**

| Attribute | Value |
|-----------|-------|
| **Name** | dueDate |
| **Display Name** | Due Date |
| **Type** | Datetime |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 2: Part Payment Allowed**

| Attribute | Value |
|-----------|-------|
| **Name** | partPaymentAllowed |
| **Display Name** | Part Payment Allowed |
| **Type** | Boolean |
| **Default Value** | false |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 3: Status**

| Attribute | Value |
|-----------|-------|
| **Name** | status |
| **Display Name** | Status |
| **Type** | Short Text |
| **Default Value** | Pending |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 4: Amount Paid (Computed Field)**

| Attribute | Value |
|-----------|-------|
| **Name** | amountPaid |
| **Display Name** | Amount Paid |
| **Type** | Computed |
| **Computed Field Value Type** | Decimal |
| **Computed Field Value Provider** | PaymentCollectionItemAmountProvider |
| **Computed Field Value Provider Context** | `{}` |
| **Computed Field Trigger Config** | Model: paymentCollectionItemDetail, Operation: after-update |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Note:** This field is automatically calculated when payment collection item details are updated. It sums all successful payments made for this item.

**Field 5: Amount Pending (Computed Field)**

| Attribute | Value |
|-----------|-------|
| **Name** | amountPending |
| **Display Name** | Amount Pending |
| **Type** | Computed |
| **Computed Field Value Type** | Decimal |
| **Computed Field Value Provider** | NoopsEntityComputedFieldProviderService |
| **Computed Field Value Provider Context** | `{}` |
| **Computed Field Trigger Config** | Model: paymentCollectionItemDetail, Operation: before-insert |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Note:** This field uses a no-op provider as a placeholder. The actual value is calculated based on the difference between the total amount to be paid and the amount already paid.

**Field 6: Is Overdue**

| Attribute | Value |
|-----------|-------|
| **Name** | isOverdue |
| **Display Name** | Is Overdue |
| **Type** | Boolean |
| **Default Value** | false |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 7: Overdue By Days**

| Attribute | Value |
|-----------|-------|
| **Name** | overdueByDays |
| **Display Name** | Overdue By Days |
| **Type** | Integer |
| **Required** | No |
| **Enable Audit Tracking** | Yes |

**Field 8: Late Amount To Be Paid**

| Attribute | Value |
|-----------|-------|
| **Name** | lateAmountToBePaid |
| **Display Name** | Late Amount To Be Paid |
| **Type** | Decimal |
| **Default Value** | 0 |
| **Required** | No |
| **Enable Audit Tracking** | Yes |

**Field 9: Total Amount To Be Paid (Computed Field)**

| Attribute | Value |
|-----------|-------|
| **Name** | totalAmountToBePaid |
| **Display Name** | Total Amount To Be Paid |
| **Type** | Computed |
| **Computed Field Value Type** | Decimal |
| **Computed Field Value Provider** | NoopsEntityComputedFieldProviderService |
| **Computed Field Value Provider Context** | `{}` |
| **Computed Field Trigger Config** | Model: paymentCollectionItemDetail, Operation: before-insert |
| **Required** | No |
| **Enable Audit Tracking** | Yes |

**Note:** This field uses a no-op provider as a placeholder. The actual value represents the sum of the base amount and any late fees (amountToBePaid + lateAmountToBePaid).

**Field 10: Amount To Be Paid**

| Attribute | Value |
|-----------|-------|
| **Name** | amountToBePaid |
| **Display Name** | Amount To Be Paid |
| **Type** | Decimal |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 11: Payment Mode**

| Attribute | Value |
|-----------|-------|
| **Name** | mode |
| **Display Name** | Mode |
| **Description** | Mode of payment. Can be CASH or PG (Payment Gateway) |
| **Type** | Short Text |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 12: Student Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | student |
| **Display Name** | Student |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | student |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 13: Payment Collection Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentCollection |
| **Display Name** | Payment Collection |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | paymentCollection |
| **Related Module** | fees-portal |
| **Related Field** | paymentCollectionItems |
| **Create Inverse** | Yes |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 14: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 15: Fee Type Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | feeType |
| **Display Name** | Fee Type |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | feeType |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 16: Payment Collection Item Details Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentCollectionItemDetails |
| **Display Name** | Payment Collection Item Details |
| **Type** | Relation |
| **Relation Type** | One-to-Many |
| **Related Model** | paymentCollectionItemDetail |
| **Related Module** | fees-portal |
| **Related Field** | paymentCollectionItem |
| **Create Inverse** | Yes |
| **Cascade** | cascade |
| **Enable Audit Tracking** | No |

#### 4. Creating the Payment Collection Item Detail Model

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | paymentCollectionItemDetail |
| **Plural Name** | paymentCollectionItemDetails |
| **Display Name** | Payment Collection Item Detail |
| **Description** | Model used to capture individual payment transactions for a payment collection item |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_payment_collection_item_detail |
| **Enable Audit Tracking** | Yes |
| **Enable Soft Delete** | No |
| **Draft Publish Workflow** | No |
| **Internationalization** | No |
| **Is Child Model** | No |

##### Field Definitions

**Field 1: Payment Date**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentDate |
| **Display Name** | Payment Date |
| **Type** | Datetime |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 2: Payment Status**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentStatus |
| **Display Name** | Payment Status |
| **Type** | Short Text |
| **Default Value** | Pending |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 3: Amount Paid**

| Attribute | Value |
|-----------|-------|
| **Name** | amountPaid |
| **Display Name** | Amount Paid |
| **Type** | Decimal |
| **Required** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 4: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 5: Student Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | student |
| **Display Name** | Student |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | student |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 6: Payment Collection Item Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentCollectionItem |
| **Display Name** | Payment Collection Item |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | paymentCollectionItem |
| **Related Module** | fees-portal |
| **Related Field** | paymentCollectionItemDetails |
| **Create Inverse** | Yes |
| **Cascade** | cascade |
| **Required** | Yes |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

**Field 7: Payment Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | payment |
| **Display Name** | Payment |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | payment |
| **Related Module** | fees-portal |
| **Create Inverse** | No |
| **Cascade** | cascade |
| **Required** | No |
| **Index** | Yes |
| **Enable Audit Tracking** | Yes |

:::tip Reference Documentation
For detailed information about field types and configuration best practices, refer to these common reference documents:
- 📚 [Field Type Reference](../common/field-types.md) - Complete guide to all available field types
- ⚙️ [Configuration Notes](../common/configuration-notes.md) - Important guidelines for relations, cascading, audit tracking, and more
:::

### Generating APIs and UI Components

Once you've created the data models, you'll need to generate the REST APIs and UI components.

:::tip Reference Documentation
📋 For detailed step-by-step instructions, see [Generating APIs and UI Components](../common/code-generation.md)
:::

### Implementing Custom Business Logic

While SolidX auto-generates basic CRUD operations, the payment collection feature requires custom business logic for Excel processing, student management, and email notifications. This section explains the key customizations needed.

#### 1. Excel Upload Validation

Before processing the uploaded Excel file, validation ensures data quality and prevents errors.

**Implementation Location:** Payment Collection Service
- **File:** `solid-api/src/fees-portal/services/payment-collection.service.ts`
- **Method:** `feeTypeValidation()`

**What It Does:**
1. **Excel Structure Validation**
   - Reads the uploaded Excel file using the ExcelService's `readExcelFromStreamNonStreaming()` method
   - Identifies header row and extracts column names
   - Known columns: Student Name, Student Id, Parent/Guardian Name/Email/Mobile, Payment Mode
   - Fee type columns: Any column not in known fields and not containing "Due Date"

2. **Fee Type Validation**
   - Extracts unique fee types from Excel headers
   - Queries the database for institute's configured Fee Types
   - Throws error if any fee type in Excel is not configured
   - Error message example: "Fee type 'Lab Fees' is not configured for your institute"

3. **Due Date Validation**
   - Ensures all due dates are today or in the future
   - Rejects past due dates with detailed error messages
   - Supports both string format (yyyy-mm-dd) and Excel date types
   - Example error: "Row 5: Due date for 'Tuition Fees' cannot be in the past"

4. **Payment Mode Validation**
   - Only "CASH" or "PG" (Payment Gateway) allowed
   - Defaults to "PG" if empty
   - Case-insensitive validation
   - Example error: "Row 3: Invalid payment mode 'CHECK'. Use 'CASH' or 'PG'"

5. **Email Validation**
   - Parent/Guardian email must be lowercase
   - Email is mandatory
   - Basic format validation

**Key Code Pattern:**

```typescript
import { ExcelService } from 'src/services/excel.service';
import { createReadStream } from 'fs';

@Injectable()
export class PaymentCollectionService {
  constructor(
    private readonly excelService: ExcelService,
    // ... other dependencies
  ) {}

  async feeTypeValidation(filePath: string, instituteId: number) {
    // Create a readable stream from the file path
    const fileStream = createReadStream(filePath);

    // Read the entire Excel file using ExcelService
    const { headers, rows } = await this.excelService.readExcelFromStreamNonStreaming(
      fileStream,
      {
        hasHeaderRow: true,
        worksheetIndex: 0
      }
    );

    // Extract fee type columns from headers
    const knownColumns = [
      'Student Name', 'Student Id',
      'Parent/Guardian Name', 'Parent/Guardian Email', 'Parent/Guardian Mobile',
      'Payment Mode'
    ];

    const feeTypeColumns = headers.filter(header =>
      !knownColumns.includes(header) &&
      !header.includes('Due Date')
    );

    const excelFeeTypes = [...new Set(feeTypeColumns)]; // Get unique fee types

    // Validate fee types against database
    const instituteFeeTypes = await this.getFeeTypesForInstitute(instituteId);
    const invalidFeeTypes = excelFeeTypes.filter(
      ft => !instituteFeeTypes.map(f => f.feeType).includes(ft)
    );

    if (invalidFeeTypes.length > 0) {
      throw new Error(`Fee types not configured: ${invalidFeeTypes.join(', ')}`);
    }

    // Validate each row
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      const rowNumber = i + 2; // +2 because Excel rows start at 1 and row 1 is headers

      // Validate due dates for each fee type
      for (const feeType of excelFeeTypes) {
        const dueDateColumn = `${feeType} Due Date`;
        const amountColumn = `${feeType} Amount`;

        const amount = row[amountColumn];
        const dueDate = row[dueDateColumn];

        // Only validate if amount is provided
        if (amount && parseFloat(amount) > 0) {
          if (!dueDate) {
            throw new Error(
              `Row ${rowNumber}: Due date is required for '${feeType}' when amount is specified`
            );
          }

          const dueDateObj = new Date(dueDate);
          if (dueDateObj < today) {
            throw new Error(
              `Row ${rowNumber}: Due date for '${feeType}' cannot be in the past`
            );
          }
        }
      }

      // Validate payment mode
      const paymentMode = row['Payment Mode']?.toString().toUpperCase() || 'PG';
      if (!['CASH', 'PG'].includes(paymentMode)) {
        throw new Error(
          `Row ${rowNumber}: Invalid payment mode '${row['Payment Mode']}'. Use 'CASH' or 'PG'`
        );
      }

      // Validate required fields
      if (!row['Parent/Guardian Email']) {
        throw new Error(`Row ${rowNumber}: Parent/Guardian Email is required`);
      }
    }

    return { headers, rows };
  }
}
```

#### 2. Excel Template Generation

To help users format their Excel correctly, SolidX provides template generation.

**Implementation Location:** Generate Fee Collection Report Service
- **File:** `solid-api/src/fees-portal/services/generate-fee-collection-report.service.ts`
- **Endpoint:** `GET /api/generate-fee-reports?id={instituteId}`

**What It Does:**
1. Fetches institute's configured fee types from database
2. Generates Excel with dynamic headers based on fee types
3. Headers format:
   - Fixed columns: Student Name, Student Id, Parent/Guardian Name, Parent/Guardian Email, Parent/Guardian Mobile
   - Dynamic columns: For each fee type: `{FeeType} Amount`, `{FeeType} Due Date`
   - Last column: Payment Mode
4. Includes sample row with today's date
5. Returns downloadable Excel file

**Template Structure Example:**

| Student Name | Student Id | Parent/Guardian Name | Parent/Guardian Email | Parent/Guardian Mobile | Tuition Fees Amount | Tuition Fees Due Date | Bus Fees Amount | Bus Fees Due Date | Payment Mode |
|-------------|-----------|---------------------|----------------------|----------------------|--------------------|--------------------|----------------|-----------------|--------------|
| Rahul Sharma | STU001 | Mr. Rajesh Sharma | rajesh@example.com | 9123456789 | 10000 | 2024-04-30 | 3000 | 2024-04-30 | PG |

#### 3. Background Processing with Event Subscriber

The core processing logic uses TypeORM's Event Subscriber pattern to automatically process Excel files after upload.

**Implementation Location:** Media Transaction Subscriber
- **File:** `solid-api/src/fees-portal/subscriber/media-transaction.subscriber.ts`
- **Event:** `afterInsert` on Media entity

**How It Works:**

When a file is uploaded for the Payment Collection model:
1. TypeORM fires `afterInsert` event after Media record is saved
2. Subscriber checks if media belongs to `paymentCollection` model
3. If yes, triggers `paymentCollectionTransaction()` method
4. Processing happens synchronously within the database transaction

**Processing Flow:**

```
Excel Upload
    ↓
Media Entity Insert
    ↓
afterInsert Event Fired
    ↓
Read Excel using ExcelService
    ↓
For Each Row in Excel:
    ↓
    ├── Find or Create Student
    │   ├── Search by Student ID + Institute
    │   ├── If found: Update details
    │   └── If not found: Create new
    ↓
    ├── Create Payment Collection Items
    │   └── For each Fee Type with amount > 0:
    │       ├── Read amount, due date, mode
    │       ├── If mode = CASH:
    │       │   └── Status = "Fully Paid"
    │       └── If mode = PG:
    │           └── Status = "Pending"
    ↓
    └── Send Email Notification
        ├── If all items CASH (Fully Paid):
        │   └── Send payment success email
        └── If any items PG (Pending):
            └── Send due fees email with payment link
```

**Key Code Pattern:**

```typescript
import { ExcelService } from 'src/services/excel.service';
import { createReadStream } from 'fs';

@EventSubscriber()
export class MediaTransactionSubscriber implements EntitySubscriberInterface<Media> {
  constructor(
    private readonly excelService: ExcelService,
    // ... other dependencies
  ) {}

  async afterInsert(event: InsertEvent<Media>) {
    const media = event.entity;

    if (media.modelName === 'paymentCollection') {
      await this.paymentCollectionTransaction(media, event.manager);
    }
  }

  async paymentCollectionTransaction(media: Media, entityManager: EntityManager) {
    // Get file path from media entity
    const filePath = media.filePath; // Adjust based on your Media entity structure

    // Create a readable stream from the file path
    const fileStream = createReadStream(filePath);

    // Read the entire Excel file using ExcelService
    const { headers, rows } = await this.excelService.readExcelFromStreamNonStreaming(
      fileStream,
      {
        hasHeaderRow: true,
        worksheetIndex: 0
      }
    );

    // Process each row
    for (const row of rows) {
      await this.processRow(row, headers, entityManager);
    }
  }

  async processRow(
    row: Record<string, any>,
    headers: string[],
    entityManager: EntityManager
  ) {
    // Extract student data from row using header keys
    const studentData = {
      studentId: row['Student Id'],
      studentName: row['Student Name'],
      parentName: row['Parent/Guardian Name'],
      parentEmailAddress: row['Parent/Guardian Email']?.toLowerCase(),
      parentMobileNumber: row['Parent/Guardian Mobile'],
      // ... other fields
    };

    // Process student and payment items
    // ... (see next section for details)
  }
}
```

#### 4. Student Management Logic

**Method:** `processRow()` in Media Transaction Subscriber

**Student Creation/Update Logic:**

```typescript
async processRow(
  row: Record<string, any>,
  headers: string[],
  entityManager: EntityManager
) {
  // Extract student data from the row object
  // The ExcelService returns rows as objects with header keys
  const studentData = {
    studentId: row['Student Id'],
    studentName: row['Student Name'],
    parentName: row['Parent/Guardian Name'],
    parentEmailAddress: row['Parent/Guardian Email']?.toLowerCase(),
    parentMobileNumber: row['Parent/Guardian Mobile'],
    institute: { id: instituteId }
  };

  // Find existing student
  let student = await entityManager.findOne(Student, {
    where: {
      studentId: studentData.studentId,
      institute: { id: instituteId }
    }
  });

  if (student) {
    // Update existing student
    student.studentName = studentData.studentName;
    student.parentName = studentData.parentName;
    student.parentEmailAddress = studentData.parentEmailAddress;
    student.parentMobileNumber = studentData.parentMobileNumber;
  } else {
    // Create new student
    student = entityManager.create(Student, studentData);
  }

  await entityManager.save(Student, student);

  // Continue processing payment items for this student
  await this.createPaymentItems(row, headers, student, entityManager);
}
```

**Important Notes:**
- Student uniqueness is determined by: Student ID + Institute
- Updates overwrite existing data (name, parent info, contact details)
- Student Login ID is generated separately (not from Excel)
- Institute is always set from logged-in user's context
- The ExcelService's `readExcelFromStreamNonStreaming()` returns rows as objects with column headers as keys, making data access simpler and more readable

#### 5. Payment Collection Item Creation

**For Each Fee Type in Excel:**

```typescript
async createPaymentItems(
  row: Record<string, any>,
  headers: string[],
  student: Student,
  entityManager: EntityManager
) {
  // Get fee types for this institute
  const instituteFeeTypes = await entityManager.find(FeeType, {
    where: { institute: { id: instituteId } }
  });

  // Extract fee type columns from headers
  const feeTypeColumns = headers.filter(
    header => !['Student Name', 'Student Id', 'Parent/Guardian Name',
                'Parent/Guardian Email', 'Parent/Guardian Mobile',
                'Payment Mode'].includes(header) &&
                !header.includes('Due Date')
  );

  // Process each fee type
  for (const feeType of instituteFeeTypes) {
    const amountColumnName = `${feeType.feeType} Amount`;
    const dueDateColumnName = `${feeType.feeType} Due Date`;

    // Access data using the column names as object keys
    const amount = row[amountColumnName];
    const dueDate = row[dueDateColumnName];
    const paymentMode = row['Payment Mode'] || 'PG';

    // Skip if no amount
    if (!amount || parseFloat(amount) <= 0) continue;

    // Determine status based on payment mode
    let status, amountPaid, amountPending;

    if (paymentMode.toString().toUpperCase() === 'CASH') {
      status = 'Fully Paid';
      amountPaid = parseFloat(amount);
      amountPending = 0;
    } else {
      status = 'Pending';
      amountPaid = 0;
      amountPending = parseFloat(amount);
    }

    // Create payment collection item
    const item = entityManager.create(PaymentCollectionItem, {
      student: student,
      feeType: feeType,
      paymentCollection: paymentCollection,
      institute: { id: instituteId },
      amountToBePaid: parseFloat(amount),
      dueDate: new Date(dueDate),
      partPaymentAllowed: feeType.partPaymentAllowed,
      status: status,
      amountPaid: amountPaid,
      amountPending: amountPending,
      totalAmountToBePaid: parseFloat(amount),
      mode: paymentMode.toString().toUpperCase()
    });

    await entityManager.save(PaymentCollectionItem, item);
  }
}
```

**Benefits of Using ExcelService:**
- Clean object-based access to cell values using column headers as keys
- Automatic handling of different Excel cell types (numbers, dates, strings)
- Built-in support for rich text, formulas, and hyperlinks
- No need to manage cell indices or column mappings manually
- Consistent data normalization across the application

#### 6. Email Notification Logic

**Method:** `sendEmailNotification()` in Media Transaction Subscriber

**Decision Logic:**

```typescript
// Fetch all items for this student + payment collection
const items = await entityManager.find(PaymentCollectionItem, {
  where: {
    student: { id: student.id },
    paymentCollection: { id: paymentCollection.id }
  },
  relations: ['feeType', 'institute']
});

// Check if all items are fully paid (CASH mode)
const allFullyPaid = items.every(item => item.status === 'Fully Paid');

if (allFullyPaid) {
  // Send payment success email
  await mailFactory.sendEmailUsingTemplate(
    student.parentEmailAddress, //to
    'fees-portal-payment-success', //template name
    { // templateParams
      student: student,
      paymentDetails: {
        totalAmount: items.reduce((sum, item) => sum + item.amountPaid, 0),
        feeTypes: items.map(item => item.feeType.feeType).join(', '),
        status: 'Fully Paid',
        createdDate: new Date()
      },
      instituteLogo: institute.logo,
    },
    true //shouldQueueEmails
  );
} else {
  // Send due fees email with payment link
  const redirectUrl = `https://${institute.hostedPagePrefix}-${EDU_BASE_DOMAIN}/?id=${student.studentLoginId}`;

  await mailFactory.sendEmailUsingTemplate(
    student.parentEmailAddress, //to
    'new-payment-or-payment-reminder', //template name
    { // templateParams
      student: student,
      dueDetails: {
        totalAmount: items.reduce((sum, item) => sum + item.amountPending, 0),
        feeTypes: items.map(item => item.feeType.feeType).join(', '),
        status: 'Pending',
        redirectUrl: redirectUrl,
        createdDate: new Date()
      },
      instituteLogo: institute.logo,
    },
    true //shouldQueueEmails
  );
}
```

**Email Templates:**

1. **Payment Success Email** (`fees-portal-payment-success.handlebars.html`)
   - Triggered when: All items have status "Fully Paid" (CASH mode)
   - Shows: Confirmation of payment received, total amount, fee types
   - No action needed from parent

2. **Due Fees Email** (`fees-portal-new-payment-or-payment-reminder.handlebars.html`)
   - Triggered when: Any item has status "Pending" (PG mode)
   - Shows: Amount due, fee types, due dates, payment link
   - Call to action: "Pay Now" button linking to student portal

**Template Location:** `solid-api/module-metadata/fees-portal/email-templates/`

#### 7. Computed Field for Amount Calculations

When payments are made through the payment gateway, amounts need to be recalculated.

**Implementation Location:** Payment Collection Item Amount Provider
- **File:** `solid-api/src/fees-portal/computed-providers/payment-collection-item-amount-provider.ts`
- **Trigger:** After Payment Collection Item Detail save

**What It Does:**

```typescript
// Triggered when payment detail is saved
async computeFieldValue(entity: PaymentCollectionItemDetail) {
  const item = entity.paymentCollectionItem;

  // Sum all successful payment details
  const totalPaid = await this.sumSuccessfulPayments(item.id);

  // Calculate pending amount
  const totalAmount = item.amountToBePaid + (item.lateAmountToBePaid || 0);
  const pending = totalAmount - totalPaid;

  // Determine status
  let status;
  if (pending <= 0) {
    status = 'Fully Paid';
  } else if (totalPaid > 0) {
    status = 'Partially Paid';
  } else {
    status = 'Pending';
  }

  // Update item
  await this.update(item.id, {
    amountPaid: totalPaid,
    amountPending: pending,
    totalAmountToBePaid: totalAmount,
    status: status
  });
}
```

#### 8. Scheduled Jobs

The payment collection feature uses two scheduled jobs to automate late fee calculation and email reminders.

:::tip Reference Documentation
📋 For detailed information about scheduled jobs configuration, properties, and best practices, see [Scheduled Jobs Configuration](../common/scheduled-jobs.md)
:::

**Job 1: Late Fee Calculator**

- **File:** `solid-api/src/fees-portal/scheduled-jobs/late-fee-payment-calculator-scheduled-job.service.ts`
- **Class Name:** `LateFeePaymentCalculatorScheduledJob`
- **Frequency:** Hourly (runs every hour, all days of the week)
- **Purpose:** Calculate and apply late fees for overdue payments

**Configuration in metadata JSON:**
```json
{
  "scheduleName": "Late Fee Calculation",
  "isActive": true,
  "frequency": "Hourly",
  "job": "LateFeePaymentCalculatorScheduledJob",
  "moduleUserKey": "fees-portal"
}
```

**What It Does:**
```typescript
// Find overdue items
const overdueItems = await this.find({
  where: {
    dueDate: LessThan(new Date()),
    status: Not(In(['Cancelled', 'Fully Paid']))
  },
  relations: ['feeType']
});

// Calculate late fees
for (const item of overdueItems) {
  const overdueDays = Math.floor((today - item.dueDate) / (1000 * 60 * 60 * 24));
  const pendingAmount = parseFloat(item.amountPending);

  let lateFee = 0;
  if (item.feeType.latePaymentFeesType === 'Percent') {
    lateFee = (pendingAmount * item.feeType.latePaymentFees) / 100;
  } else if (item.feeType.latePaymentFeesType === 'Absolute') {
    lateFee = item.feeType.latePaymentFees;
  }

  await this.update(item.id, {
    isOverdue: true,
    overdueByDays: overdueDays,
    lateAmountToBePaid: lateFee,
    totalAmountToBePaid: pendingAmount + lateFee
  });
}
```

**Job 2: Fees Due Email Reminder**

- **File:** `solid-api/src/fees-portal/scheduled-jobs/send-email-schedule-jobs.service.ts`
- **Class Name:** `SendEmailScheduleJobs`
- **Frequency:** Daily (runs once per day, all days of the week)
- **Purpose:** Send payment reminders to parents with pending fees

**Configuration in metadata JSON:**
```json
{
  "scheduleName": "Fees Due Email",
  "isActive": true,
  "frequency": "Daily",
  "job": "SendEmailScheduleJobs",
  "moduleUserKey": "fees-portal"
}
```

**What It Does:**
```typescript
// Find pending items
const pendingItems = await this.find({
  where: {
    status: In(['Pending', 'Partially Paid'])
  },
  relations: ['student', 'feeType', 'institute']
});

// Group by student
const groupedByStudent = this.groupBy(pendingItems, 'student.id');

// Send reminders
for (const [studentId, items] of Object.entries(groupedByStudent)) {
  const student = items[0].student;
  const institute = items[0].institute;

  await mailFactory.sendEmailUsingTemplate(
    student.parentEmailAddress,
    'new-payment-or-payment-reminder',
    {
      student: student,
      dueDetails: {
        totalAmount: items.reduce((sum, item) => sum + parseFloat(item.amountPending), 0),
        feeTypes: items.map(item => item.feeType.feeType).join(', '),
        redirectUrl: `https://${institute.hostedPagePrefix}-${EDU_BASE_DOMAIN}/?id=${student.studentLoginId}`
      },
      instituteLogo: institute.logo,
    },
    true
  );
}
```

:::tip Implementation Order
Follow this sequence when implementing custom business logic:
1. Create validation service method (`feeTypeValidation`)
2. Implement template generation service
3. Create event subscriber for Excel processing
4. Implement student creation/update logic
5. Implement payment item creation logic
6. Implement email notification logic
7. Create computed field provider for amount calculations
8. Set up scheduled jobs for late fees and reminders
9. Test end-to-end flow with sample Excel file
:::

:::info Excel Service Integration
All Excel file operations in this feature use the centralized `ExcelService` for consistency:

**Key Methods Used:**
- **`readExcelFromStreamNonStreaming()`**: For validation and processing Excel files
  - Returns `{ headers: string[], rows: Record<string, any>[] }`
  - Handles complex cell types (rich text, formulas, dates)
  - Provides clean object-based access using column headers as keys

- **`createExcelStream()`**: For generating templates
  - Accepts custom headers array
  - Creates downloadable Excel files with proper formatting

**Benefits:**
- Consistent data normalization across the application
- Automatic handling of Excel-specific data types
- Built-in support for streaming large files
- Clean, maintainable code without low-level ExcelJS complexity
- Reusable service for all import/export operations

**Alternative Approach:**
For very large files that may cause memory issues, consider using `readExcelInPagesFromStream()` which returns an async generator for processing rows in chunks. However, for typical payment collection files (hundreds to thousands of rows), `readExcelFromStreamNonStreaming()` provides better performance and simpler code.
:::

### Customizing the UI

After generating the code using SolidX, default list and form views are automatically created for each model. However, these default views need customization to provide a streamlined payment collection workflow. This section explains how to customize these views using layout JSON configuration and UI extensions.

#### Payment Collection Form View Customizations

<!-- Image placeholder: payment_collection_form_view.png -->
*The customized Payment Collection Form View with template download functionality.*

**1. Simplified Field Layout**

The Payment Collection form displays only essential fields in a single-column layout:

| Field | Purpose | Visibility |
|-------|---------|-----------|
| **Name** | Identify this collection batch | Always visible |
| **Description** | Additional context (optional) | Always visible |
| **Due Date** | Default due date for all items | Always visible |
| **Institute** | Which institute (auto-filled for Institute Admin) | Hidden for new records, visible when editing |
| **Payment File** | Excel upload | Disabled when editing existing records |

**Layout JSON Snippet:**

```json
{
  "type": "column",
  "attrs": {
    "name": "group-1",
    "label": "Payment Collection Details",
    "className": "col-12"
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "name"
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "description"
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "dueDate"
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute"
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentFile"
      }
    }
  ]
}
```

**Benefits:**
- Simple, focused interface for primary task
- No overwhelming options or tabs
- Clear workflow: Select Institute → Select Due Date → Upload

**2. Form Load Handler for Conditional Field Behavior and Pre-filling**

**Extension:** `paymentCollectionOnFormLoadHandler.ts`

This unified handler controls field behavior and pre-fills data based on context:

```typescript
export function paymentCollectionOnFormLoadHandler(formContext) {
  const { formData, userData, userRole, isEditMode } = formContext;

  // Disable fields when editing existing record
  if (isEditMode) {
    formContext.setFieldProperty('name', 'disabled', true);
    formContext.setFieldProperty('institute', 'disabled', true);
    formContext.setFieldProperty('paymentFile', 'disabled', true);
  }

  // Auto-fill institute for Institute Admin users on new records
  if (!isEditMode && userRole === 'Institute Admin' && userData.institute) {
    formContext.setFieldValue('institute', userData.institute.id);
  }
}
```

**Rationale:**
- **Disable name when editing**: Payment collection name identifies the batch; changing it after processing would cause confusion
- **Disable institute when editing**: Institute cannot change after items are created
- **Disable payment file when editing**: Excel is processed on upload; re-uploading would create duplicate items
- **Auto-fill institute**: Institute Admins only manage their own institute
- **Unified handler**: Combines layout and data loading logic in a single handler for better maintainability

**Benefits:**
- Single handler for all form initialization logic
- Reduces data entry for Institute Admins
- Prevents accidental cross-institute data creation
- Maintains data integrity
- Follows current best practices

**4. Excel Template Download Button**

Add a button directly in the form header using the `formButtons` configuration. This button will trigger a custom action to download the Excel template.

**Step 1: Configure Form Button in Layout JSON**

```json
{
  "name": "paymentCollection-form-view",
  "displayName": "Initiate Payments",
  "type": "form",
  "context": "{}",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "paymentCollection",
  "layout": {
    "type": "form",
    "attrs": {
      "name": "form-1",
      "label": "Initiate Payments",
      "className": "grid",
      "showCogWheelFormButton": false,
      "formButtons": [
        {
          "attrs": {
            "className": "p-button p-component p-button-sm",
            "icon": "pi pi-download",
            "label": "Download Sample Excel",
            "action": "GenerateTemplateFormat",
            "customComponentIsSystem": true,
            "actionInContextMenu": false,
            "openInPopup": true
          }
        }
      ]
    },
    "onFormLoad": "paymentCollectionOnFormLoadHandler",
    "children": [
      // ... rest of form layout
    ]
  }
}
```

This configuration adds a "Download Sample Excel" button in the form header that:
- Displays the download icon (`pi pi-download`)
- Triggers the `GenerateTemplateFormat` action when clicked
- Opens in a popup for better user experience
- Appears alongside other form action buttons

**Step 2: Implement the Custom Action Component**

Create the action handler that will be triggered when the button is clicked. SolidX automatically maps the `action` name from the form button configuration to the corresponding component file.

**File:** `generate-template-format.tsx`

```tsx
import React from 'react';
import { Button } from 'primereact/button';

export function GenerateTemplateFormat({ instituteId }) {
  const handleDownload = async () => {
    const url = `/api/generate-fee-reports?id=${instituteId}`;
    window.open(url, '_blank');
  };

  return (
    <div className="template-download-section">
      <h3>Step 1: Download Excel Template</h3>
      <p>Download the template with your institute's configured fee types</p>
      <Button
        label="Download Template"
        icon="pi pi-download"
        onClick={handleDownload}
        className="p-button-success"
      />
      <hr />
      <h3>Step 2: Upload Completed Excel</h3>
      <p>Fill the template with student and payment details, then upload below</p>
    </div>
  );
}
```

**Benefits:**
- Seamless integration with form header actions
- Guides users through workflow (Download → Fill → Upload)
- Template matches institute's fee types dynamically
- Reduces formatting errors
- Improves user experience with clear step-by-step instructions

#### Complete Payment Collection Form Layout JSON

Below is the complete form layout JSON for the Payment Collection model, including the formButtons configuration:

<details>
<summary>Click to expand the complete JSON layout</summary>

```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Payment Collection",
    "className": "grid",
    "showCogWheelFormButton": false,
    "formButtons": [
      {
        "attrs": {
          "className": "p-button p-component p-button-sm",
          "icon": "pi pi-download",
          "label": "Download Sample Excel",
          "action": "GenerateTemplateFormat",
          "customComponentIsSystem": true,
          "actionInContextMenu": false,
          "openInPopup": true
        }
      }
    ]
  },
  "onFormLoad": "paymentCollectionOnFormLoadHandler",
  "children": [
    {
      "type": "sheet",
      "attrs": {
        "name": "sheet-1"
      },
      "children": [
        {
          "type": "row",
          "attrs": {
            "name": "row-1"
          },
          "children": [
            {
              "type": "column",
              "attrs": {
                "name": "group-1",
                "label": "Payment Collection Details",
                "className": "col-12"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "name"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "description"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "dueDate"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "institute",
                    "visible": true
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "paymentFile"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```
</details>

#### Payment Collection List View Customizations

**1. Key Columns Display**

The list view shows essential information for managing collections:

| Column | Purpose | Sortable | Filterable |
|--------|---------|----------|------------|
| **Name** | Collection identifier | Yes | Yes |
| **Due Date** | When payments are due | Yes | Yes |
| **Institute** | Which institute (Platform Admin view) | Yes | Yes |
| **Created Date** | When collection was created | Yes | Yes |
| **Created By** | Who created the collection | No | Yes |

**2. Role-Based Action Permissions**

```json
"configureViewActions": {
  "create": { "roles": ["Admin", "Institute Admin"] },
  "edit": { "roles": ["Admin", "Institute Admin"] },
  "delete": { "roles": ["Admin"] },
  "import": { "roles": [] },
  "export": { "roles": ["Admin", "Institute Admin"] },
  "customizeLayout": { "roles": ["Admin", "Institute Admin"] }
}
```

**Benefits:**
- Institute Admins can create and edit collections
- Only Platform Admins can delete collections (data integrity)
- Import disabled (use Excel upload instead)
- Export enabled for reporting

#### Payment Collection Item List View Columns

Shows all critical information for tracking payments:

| Column | Purpose | Widget/Format |
|--------|---------|---------------|
| **Student** | Who owes the fee | Link to student record |
| **Fee Type** | What fee is owed | Text |
| **Amount To Be Paid** | Base amount | Currency |
| **Amount Paid** | Paid so far | Currency (green if > 0) |
| **Amount Pending** | Still owed | Currency (red if > 0) |
| **Late Amount** | Late fee penalty | Currency (highlighted if > 0) |
| **Total Amount** | Base + Late fees | Currency (bold) |
| **Status** | Current status | Badge (colored by status) |
| **Due Date** | Payment deadline | Date (red if overdue) |
| **Is Overdue** | Past due? | Boolean icon |
| **Overdue By Days** | Days past due | Number (red if > 0) |
| **Payment Mode** | CASH or PG | Badge |
| **Payment Collection** | Which batch | Link to collection |

#### Student List View Customizations

**1. Key Columns**

| Column | Purpose |
|--------|---------|
| **Student Name** | Full name |
| **Student ID** | Unique identifier |
| **Parent/Guardian Name** | Primary contact |
| **Parent/Guardian Email** | Email for notifications |
| **Parent/Guardian Mobile** | Phone contact |
| **Institute** | Which institute |

**2. Role-Based Column Visibility**

Column visibility is controlled by adding a `roles` key to individual field configurations in the list view layout JSON.

**Example: Hiding Institute Column from Institute Admins**

**View:** `student-list-view`

**List View Layout Configuration:**

```json
{
  "name": "student-list-view",
  "displayName": "Students",
  "type": "list",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "student",
  "layout": {
    "type": "list",
    "attrs": {
      // ... list configuration
    },
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "studentName"
        }
      },
      {
        "type": "field",
        "attrs": {
          "name": "institute",
          "roles": ["Admin"]  // ← Add roles key here
        }
      }
      // ... other fields
    ]
  }
}
```

**Key Points:**
- Add the `roles` property inside the field's `attrs` object
- The `roles` array specifies which user roles can see this column
- Only users with "Admin" role will see the institute column
- Institute Admins (without "Admin" role) will not see this column
- If `roles` is not specified, the column is visible to all users

**Benefits:**
- Platform Admins see institute column (multi-institute view)
- Institute Admins don't see institute column (single institute context)
- Cleaner, role-appropriate interface for each user type

#### General Design Principles

The customizations follow these principles:

1. **Task-Oriented Workflow**: Form guides users through clear steps (Download → Upload)
2. **Progressive Disclosure**: Only show fields relevant to current context
3. **Role-Appropriate Views**: Show only what each role needs to see
4. **Error Prevention**: Disable fields that shouldn't be changed after processing
5. **Clarity**: Clear labels and helper text guide users

These customizations transform the auto-generated UI into an intuitive payment collection workflow that minimizes errors and maximizes efficiency.

### Excel File Format and Requirements

This section provides detailed specifications for the Excel file format required for payment collection upload.

#### File Format Specifications

| Specification | Requirement |
|--------------|-------------|
| **File Type** | .xlsx (Excel 2007 or later) |
| **Maximum File Size** | 5 MB |
| **Sheet Name** | Any (first sheet is processed) |
| **Header Row** | Row 1 must contain column headers |
| **Data Rows** | Start from Row 2 onwards |
| **Maximum Rows** | No hard limit (practical limit based on processing time) |

#### Required Columns

These columns must be present in your Excel file:

| Column Name | Data Type | Required | Format/Validation | Example |
|------------|-----------|----------|-------------------|---------|
| **Student Name** | Text | Yes | Any text | "Rahul Sharma" |
| **Student Id** | Text | Yes | Must be unique per institute | "STU2024001" |
| **Parent/Guardian Name** | Text | Yes | Any text | "Mr. Rajesh Sharma" |
| **Parent/Guardian Email** | Email | Yes | Valid email format, lowercase | "rajesh.sharma@example.com" |
| **Parent/Guardian Mobile** | Text | Yes | 10-digit number | "9123456789" |

#### Dynamic Fee Type Columns

For each fee type configured in your institute, add TWO columns:

**Pattern:** `{Fee Type Name} Amount` and `{Fee Type Name} Due Date`

**Example:** If your institute has "Tuition Fees" and "Bus Fees" configured:

| Column Name | Data Type | Required | Format | Example |
|------------|-----------|----------|--------|---------|
| **Tuition Fees Amount** | Number | No* | Decimal number, no commas | 10000 or 10000.50 |
| **Tuition Fees Due Date** | Date | No* | yyyy-mm-dd or Excel date | "2024-04-30" or Excel date |
| **Bus Fees Amount** | Number | No* | Decimal number, no commas | 3000 |
| **Bus Fees Due Date** | Date | No* | yyyy-mm-dd or Excel date | "2024-04-30" |

**Important Notes:**
- Fee type names must exactly match those configured in your institute's Fee Type master data
- Column names are case-sensitive
- If amount is 0 or empty for a fee type, no payment item will be created for that fee type
- Due date is required if amount > 0

#### Payment Mode Column

| Column Name | Data Type | Required | Format | Example |
|------------|-----------|----------|--------|---------|
| **Payment Mode** | Text | No (defaults to "PG") | "CASH" or "PG" (case-insensitive) | "PG" |

**Values:**
- **PG** (Payment Gateway): Student will receive email with payment link; status will be "Pending"
- **CASH**: Payment already collected offline; status will be "Fully Paid"; student receives confirmation

#### Sample Excel Structure

Here's how a complete Excel file should look:

| Student Name | Student Id | Parent/Guardian Name | Parent/Guardian Email | Parent/Guardian Mobile | Tuition Fees Amount | Tuition Fees Due Date | Bus Fees Amount | Bus Fees Due Date | Lab Fees Amount | Lab Fees Due Date | Payment Mode |
|-------------|-----------|---------------------|----------------------|----------------------|--------------------|--------------------|----------------|-----------------|----------------|-----------------|-------------|
| Rahul Sharma | STU001 | Mr. Rajesh Sharma | rajesh.sharma@example.com | 9123456789 | 10000 | 2024-04-30 | 3000 | 2024-04-30 | 0 | | PG |
| Priya Patel | STU002 | Mrs. Meena Patel | meena.patel@example.com | 9876543210 | 10000 | 2024-04-30 | | | 1500 | 2024-05-15 | PG |
| Amit Kumar | STU003 | Mr. Suresh Kumar | suresh.kumar@example.com | 9988776655 | 10000 | 2024-04-30 | 3000 | 2024-04-30 | 1500 | 2024-05-15 | CASH |

**Analysis of Sample Data:**

**Row 2 (Rahul Sharma):**
- Will create 2 payment items: Tuition Fees (₹10,000) and Bus Fees (₹3,000)
- Lab Fees has amount 0, so no item created
- Both items will have status "Pending" (PG mode)
- Student will receive email with payment link

**Row 3 (Priya Patel):**
- Will create 2 payment items: Tuition Fees (₹10,000) and Lab Fees (₹1,500)
- Bus Fees has no amount, so no item created
- Lab Fees has different due date (2024-05-15)
- Both items status "Pending"
- Student will receive email with payment link

**Row 4 (Amit Kumar):**
- Will create 3 payment items: All three fee types
- All items will have status "Fully Paid" (CASH mode)
- Student will receive payment confirmation email
- No payment link needed
- Student receives payment confirmation email

#### Common Validation Errors and Solutions

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Fee type 'XYZ' is not configured" | Excel contains fee type not in institute's master data | Add fee type to institute configuration first, or remove column from Excel |
| "Due date cannot be in the past" | Due date is before today | Change due date to today or future date |
| "Invalid payment mode" | Payment Mode is not "CASH" or "PG" | Use only "CASH" or "PG" (case doesn't matter) |
| "Parent/Guardian Email is required" | Email column is empty | Fill in email address for all students |
| "Invalid email format" | Email is malformed | Check email format (must contain @) |
| "Student Id is required" | Student Id column is empty | Provide unique student ID for each row |
| "Amount must be greater than 0" | Negative or invalid amount | Enter positive numbers only |

#### Best Practices

**Data Entry:**
1. **Use the generated template**: Download template from the form to ensure correct structure
2. **Check fee type names**: Copy fee type names exactly as configured in your institute
3. **Consistent date format**: Use yyyy-mm-dd format for dates (e.g., 2024-04-30)
4. **No special formatting**: Don't use currency symbols (₹, $), commas, or colors
5. **One row per student**: Each student should appear only once in the file
6. **Complete all required fields**: Don't leave required columns empty

**Before Upload:**
1. **Remove extra rows/columns**: Delete any template instructions or extra headers
2. **Verify student IDs**: Ensure student IDs are unique
3. **Check due dates**: Confirm all dates are today or in the future
4. **Validate amounts**: All amounts should be positive numbers
5. **Review payment modes**: Use only "CASH" or "PG"
6. **Test with small batch**: Upload 5-10 students first to verify format

**After Upload:**
1. **Check processing status**: Verify no error messages appear
2. **Review created items**: Check Payment Collection Items list
3. **Verify student emails**: Confirm parents received notification emails
4. **Spot check amounts**: Verify amounts match your Excel

#### Troubleshooting

**Upload fails immediately:**
- Check file size (must be < 5 MB)
- Verify file format (.xlsx only)
- Ensure first row contains headers

**Upload succeeds but no items created:**
- Check if amounts are > 0
- Verify fee type names match exactly
- Review validation error messages

**Some students missing:**
- Check for empty required fields
- Verify email format
- Check Student ID for duplicates in Excel

**Wrong number of items created:**
- Count non-zero amounts in Excel
- Each non-zero amount creates one item
- Zero or empty amounts are skipped

:::tip Testing Recommendation
Before uploading payment collections for all students:
1. Create a test Excel with 2-3 students
2. Use different scenarios: PG mode, CASH mode, multiple fee types
3. Upload and verify results
4. Check emails were sent correctly
5. Once verified, proceed with full batch
:::

### Payment Collection Workflow

This section provides a comprehensive step-by-step guide for Institute Admins to create and manage payment collections.

#### Prerequisites

Before initiating a payment collection, ensure:

- [ ] Institute is activated (status = "Active")
- [ ] Fee Types are configured for your institute
- [ ] Late payment rules are set for each fee type (if applicable)
- [ ] Payment gateway credentials are configured
- [ ] Email templates are configured

#### Phase 1: Prepare Payment Collection Data

**Step 1: Gather Student Information**

Collect the following information for all students:
- Student Name
- Student ID (roll number, admission number)
- Parent/Guardian Name
- Parent/Guardian Email (for notifications)
- Parent/Guardian Mobile Number

**Step 2: Determine Fee Amounts and Due Dates**

For each student and each fee type:
- Calculate fee amount (based on your fee structure)
- Determine due date (can be same for all or different by fee type)
- Decide payment mode:
  - **PG**: Student will pay online through portal
  - **CASH**: Payment already collected offline

**Step 3: Prepare Collection Name and Description**

Choose a clear, descriptive name for this batch:
- Good examples:
  - "Q1 2024 Tuition and Bus Fees"
  - "Annual Sports Fees 2024"
  - "January 2024 Monthly Fees"
- Add description (optional):
  - "First quarter fees including tuition, lab, and bus charges"
  - "Annual sports fees for academic year 2024-25"

#### Phase 2: Download and Fill Excel Template

**Step 4: Login to Fees Portal**

- Navigate to the Fees Portal admin interface
- Login using Institute Admin credentials
- You will see only your institute's data

**Step 5: Navigate to Payment Collections**

- Click on "Fees Portal" module in the sidebar
- Select "Payment Collections" from the menu
- Click "Create New" button

**Step 6: Download Excel Template**

- In the form, locate the "Download Template" section at the top
- Click "Download Template" button
- Save the Excel file to your computer

**The template will contain:**
- Fixed columns: Student Name, Student Id, Parent/Guardian details
- Dynamic columns: For each fee type configured in your institute
- Example: If you have "Tuition Fees", "Bus Fees", "Lab Fees" configured:
  - Tuition Fees Amount
  - Tuition Fees Due Date
  - Bus Fees Amount
  - Bus Fees Due Date
  - Lab Fees Amount
  - Lab Fees Due Date
- Last column: Payment Mode

**Step 7: Fill the Excel Template**

Open the downloaded template and fill in the data:

**For each student (one row per student):**

1. **Enter student details:**
   - Student Name: Full name
   - Student Id: Unique identifier (must be consistent across collections)
   - Parent/Guardian Name: Primary contact person
   - Parent/Guardian Email: Email where notifications will be sent (lowercase)
   - Parent/Guardian Mobile: 10-digit mobile number

2. **Enter fee amounts and due dates:**
   - For each fee type, enter the amount in the `Fee Type Amount` column
   - Enter the due date in the `Fee Type Due Date` column (format: yyyy-mm-dd)
   - If a student doesn't need to pay a particular fee type, leave the amount as 0 or empty
   - Example:
     ```
     Tuition Fees Amount: 10000
     Tuition Fees Due Date: 2024-04-30
     Bus Fees Amount: 3000
     Bus Fees Due Date: 2024-04-30
     Lab Fees Amount: 0  (or leave empty - no item will be created)
     ```

3. **Enter payment mode:**
   - Use "PG" if student will pay online through payment gateway
   - Use "CASH" if payment has already been collected offline
   - Leave empty to default to "PG"

**Important Notes:**
- Don't change column names
- Don't add or remove columns
- Don't use currency symbols (₹, $) or commas in amounts
- Use numbers only for amounts (e.g., 10000.50)
- Use yyyy-mm-dd format for dates (e.g., 2024-04-30)
- Ensure all due dates are today or in the future
- Each student should appear only once in the file

**Step 8: Save and Validate Excel**

Before uploading:
- [ ] Double-check all required fields are filled
- [ ] Verify student IDs are unique
- [ ] Confirm due dates are not in the past
- [ ] Check email addresses are valid
- [ ] Verify amounts are positive numbers
- [ ] Confirm payment modes are "PG" or "CASH"

#### Phase 3: Upload Payment Collection

**Step 9: Fill Form Details**

Return to the Payment Collection form in the portal:

| Field | What to Enter | Example |
|-------|--------------|---------|
| **Name** | Descriptive name for this collection | "Q1 2024 Tuition and Bus Fees" |
| **Description** | Additional context (optional) | "First quarter fees for all students" |
| **Due Date** | Default due date (can be overridden in Excel) | 2024-04-30 |
| **Institute** | Auto-filled (Institute Admin) | Your institute |

**Step 10: Upload Excel File**

- Click "Choose File" in the "Payment File" field
- Select your completed Excel file
- Verify file name appears

**Step 11: Submit Form**

- Click "Save" button
- System will validate the Excel file
- If validation fails, error messages will appear:
  - Read error messages carefully
  - Fix issues in Excel
  - Upload again
- If validation succeeds, form will be saved

**Step 12: Wait for Processing**

After successful upload:
- System processes Excel file in the background
- For each row in Excel:
  - Student record is created or updated
  - Payment Collection Items are created for each fee type
  - Email notifications are queued
- Processing time depends on number of students (typically 1-2 minutes for 100 students)

#### Phase 4: Verify Results

**Step 13: Check Payment Collection Items**

- Navigate to "Payment Collection Items" menu
- Filter by your payment collection name
- Verify correct number of items created:
  - Count = (Number of students) × (Number of fee types with amount > 0 per student)
  - Example: 50 students, each paying 3 fee types = 150 items

**Step 14: Verify Item Details**

For a few sample students, check:
- [ ] Student name and ID are correct
- [ ] Fee type is correct
- [ ] Amount to be paid matches Excel
- [ ] Due date is correct
- [ ] Payment mode (CASH or PG) is correct
- [ ] Status is correct:
  - "Fully Paid" for CASH mode
  - "Pending" for PG mode

**Step 15: Check Email Notifications**

Verify emails were sent:

**For PG mode items:**
- Parents should receive "New Payment Request" email
- Email contains:
  - Student name and details
  - Total amount due
  - List of fee types
  - Payment link to student portal
  - Due date

**For CASH mode items:**
- Parents should receive "Payment Confirmation" email
- Email contains:
  - Student name and details
  - Total amount paid
  - List of fee types
  - Payment confirmation message

#### Phase 5: Monitor and Manage

**Step 16: Track Payment Status**

Regularly check Payment Collection Items list:
- Filter by "Pending" or "Partially Paid" status
- Monitor overdue items (Is Overdue = true)
- Check late fees being applied (Late Amount To Be Paid > 0)

**Step 17: Handle Common Scenarios**

**Scenario 1: Student Made Partial Payment**
- Status will automatically change to "Partially Paid"
- Amount Paid and Amount Pending will update
- Student can see remaining balance in portal

**Scenario 2: Payment is Overdue**
- Late fee calculator job runs daily
- Is Overdue flag set to true
- Late Amount To Be Paid calculated based on Fee Type configuration
- Total Amount To Be Paid = Base Amount + Late Fee
- Student sees updated amount in portal

#### Phase 6: Ongoing Management

**Step 18: Send Payment Reminders**

The system automatically sends reminder emails on a schedule (typically weekly):
- Targets students with "Pending" or "Partially Paid" status
- Email contains:
  - Updated amount (including late fees if overdue)
  - Days overdue (if applicable)
  - Payment link

##### TODO
You can also manually trigger reminders if needed.

**Step 19: Generate Reports**

Use the export feature to download payment collection data:
- Navigate to Payment Collection Items list
- Apply filters (e.g., "Pending", "Overdue")
- Click "Export" button
- Download Excel file with current data
- Use for analysis, reporting, or record-keeping

**Step 20: Reconcile Payments**

Periodically reconcile payment records:
- Check Payment Collection Item Details for transaction history
- Verify amounts match payment gateway records
- Investigate any discrepancies
- Update records if needed

#### Common Tasks Quick Reference

| Task | Steps |
|------|-------|
| **Create payment collection for all students** | Phase 1 → Phase 2 → Phase 3 |
| **Add payment collection for specific students** | Create new collection with subset of students in Excel |
| **Check payment status for a student** | Payment Collection Items → Filter by Student Name |
| **View overdue payments** | Payment Collection Items → Filter by "Is Overdue = true" |
| **Download payment report** | Payment Collection Items → Apply filters → Export |

#### Troubleshooting Guide

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| **Excel upload fails** | Invalid file format, size too large, or structural issues | Check file type (.xlsx), size < 5MB, verify headers |
| **No items created** | All amounts are 0 or empty | Ensure at least one fee type has amount > 0 |
| **Wrong number of items** | Zero amounts in Excel | Only non-zero amounts create items |
| **Validation error** | Fee type not configured, past due dates, invalid emails | Read error message, fix Excel, re-upload |
| **No email sent** | Invalid email address, email service issue | Verify email in Student record, check email logs |
| **Payment link doesn't work** | Student Login ID not generated | Check Student record for studentLoginId field |
| **Status not updating** | Payment gateway webhook not configured | Contact technical team to verify webhook setup |
| **Late fees not calculated** | Scheduled job not running | Contact technical team to verify job configuration |

:::tip Best Practices
1. **Start small**: For your first collection, upload 5-10 students to test the workflow
2. **Consistent Student IDs**: Always use the same Student ID format across all collections
3. **Regular monitoring**: Check payment status at least weekly
4. **Timely reminders**: Don't wait too long to follow up on pending payments
5. **Clear communication**: Send reminder to parents a week before due date
6. **Documentation**: Keep a copy of each uploaded Excel file for your records
7. **Reconciliation**: Match payment records with your accounting system regularly
:::

#### Success Criteria

You've successfully initiated a payment collection when:

- [ ] Excel template downloads with your fee types
- [ ] Excel validates without errors
- [ ] Payment Collection is created
- [ ] Correct number of Payment Collection Items created
- [ ] Students appear in system with correct details
- [ ] Email notifications sent to all parents
- [ ] Payment links work for PG mode students
- [ ] CASH mode students show "Fully Paid" status
- [ ] Payment status updates when students pay online (We will cover this in the next section)

Congratulations! You've successfully initiated a payment collection. Students can now view and pay their fees through the student portal, and you can monitor payment status in real-time.
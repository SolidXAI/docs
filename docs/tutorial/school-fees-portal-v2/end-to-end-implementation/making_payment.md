# Making Payment (Student Portal)

## Overview

This document provides comprehensive documentation for the **Student Payment Flow** in the school fees portal. This use case enables students and parents to view pending fees, make online payments through an integrated payment gateway, and track payment history through a dedicated student portal.

### Key Features

- **Custom Authentication**: OTP-based authentication for students without traditional user accounts
- **Payment Dashboard**: View all pending fees with detailed breakdowns
- **Flexible Payment Options**: Support for full and partial payments (where allowed)
- **Integrated Payment Gateway**: Seamless Mswipe payment gateway integration
- **Payment Tracking**: Complete payment history with transaction details
- **Automated Calculations**: Computed fields for amount tracking and late fee calculations
- **Email Notifications**: OTP delivery, payment confirmations, and reminders
- **Scheduled Processing**: Automated late fee application and payment reminders

### Architecture

```
┌─────────────────────────────────────────┐
│      Student Portal (Frontend)          │
│   Separate Application on Different     │
│            Port/Domain                  │
└──────────────┬──────────────────────────┘
               │ REST API Calls
               │ Bearer Token Auth
               ↓
┌─────────────────────────────────────────┐
│         SolidX Backend APIs             │
│    /api/student/* (Authentication)      │
│    /api/payment/* (Payment Flow)        │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴───────┐
        ↓              ↓
┌─────────────┐  ┌──────────────┐
│   Mswipe    │  │   Email      │
│   Gateway   │  │   Service    │
└─────────────┘  └──────────────┘
```

### User Roles and Access

| Role | Access Level | Interface |
|------|-------------|-----------|
| **Student/Parent** | Public access via custom authentication | Student Portal (separate frontend) |
| **System** | Automated processing | Scheduled jobs, webhooks, computed fields |

### What This Documentation Covers

1. **Student Authentication Flow** - OTP-based login system
2. **Payment Dashboard** - Viewing pending and completed payments
3. **Payment Initiation** - Generating payment gateway links
4. **Payment Processing** - Webhook handling and status updates
5. **Payment History** - Transaction tracking and reporting
6. **Automated Systems** - Computed fields and scheduled jobs
7. **Technical Implementation** - API endpoints, request/response formats
8. **Complete Workflow** - Step-by-step process from login to payment

---

## Roles Involved

### Student/Parent (Primary User)

**Responsibilities:**
- Log in using student login ID and OTP
- View pending fee collections
- Make payments through payment gateway
- Track payment history
- Download payment reports

**Access:**
- Student Portal (separate frontend application)
- Public endpoints with custom authentication

**Typical Workflow:**
1. Enter student login ID
2. Receive and verify OTP via email
3. View dashboard with pending fees
4. Select fees to pay
5. Complete payment via gateway
6. Receive payment confirmation

### System (Automated)

**Responsibilities:**
- Generate and validate OTPs
- Calculate late fees for overdue payments
- Send payment reminders
- Update payment statuses
- Process webhook callbacks from payment gateway

---

## Data Models Involved

### 1. Student Model

**What it represents:** A student enrolled in an institute who needs to make fee payments through the student portal.

#### Authentication & Access

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Student Login ID** | Computed (Auto-generated) | Unique identifier for portal login | "JOHND-A1B2C" |
| **OTP** | System-managed | One-time password for authentication (valid 5 minutes) | "123456" |
| **OTP Expires At** | System-managed | OTP expiration timestamp | 2024-01-15T10:35:00Z |
| **Token** | System-managed | JWT authentication token (valid 12 hours) | "eyJhbGciOiJIUzI1NiIsInR..." |

#### Basic Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Student Name** | Yes | Full name of the student | "John Doe" |
| **Student ID** | Yes | Institute-specific student identifier | "STU2024001" |
| **Student Email Address** | No | Student's personal email | john.doe@example.com |
| **Student Mobile Number** | No | Student's contact number | 9876543210 |

#### Parent/Guardian Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Parent Name** | Yes | Name of parent or guardian | "Mr. Robert Doe" |
| **Parent Email Address** | Yes | Email for OTPs and payment notifications | robert.doe@example.com |
| **Parent Mobile Number** | Yes | Contact number for notifications | 9123456789 |

#### Relationships

| Relationship | Description |
|--------------|-------------|
| **Institute** | Which institute the student belongs to |
| **Payment Collection Items** | All fee items assigned to this student |
| **Payments** | Payment transactions made by this student |

### 2. Payment Collection Item Model

**What it represents:** A specific fee item assigned to a student (e.g., "Tuition Fee for Q1 2024"). This is what students see and pay in the portal.

#### Fee Details

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Fee Type** | Yes | Type of fee (Tuition, Bus, Lab, etc.) | "Tuition Fee" |
| **Amount To Be Paid** | Yes | Base fee amount before late fees | 30000.00 |
| **Due Date** | Yes | Payment deadline | 2024-02-15 |
| **Part Payment Allowed** | Yes | Can student pay in installments? | true/false |
| **Payment Mode** | Yes | How payment should be made | "PG" (Payment Gateway) or "CASH" |

#### Status Tracking

| Field | Required? | Description | Values |
|-------|-----------|-------------|--------|
| **Status** | Auto-managed | Current payment status | "Pending", "Partially Paid", "Fully Paid", "Cancelled" |
| **Amount Paid** | Computed (Auto-calculated) | Total amount paid so far | 15000.00 |
| **Amount Pending** | Computed (Auto-calculated) | Remaining amount to be paid | 15000.00 |

#### Late Payment Tracking

| Field | Required? | Description | How It's Calculated |
|-------|-----------|-------------|---------------------|
| **Is Overdue** | Auto-managed | Is payment past due date? | true if today > due date AND status != "Fully Paid" |
| **Overdue By Days** | Auto-calculated | Number of days overdue | floor((today - dueDate) / 86400000) |
| **Late Amount To Be Paid** | Auto-calculated | Late fee penalty | Based on Fee Type's late fee configuration |
| **Total Amount To Be Paid** | Computed (Auto-calculated) | Base amount + late fees | amountToBePaid + lateAmountToBePaid |

#### Relationships

| Relationship | Description |
|--------------|-------------|
| **Student** | Which student owes this payment |
| **Fee Type** | What type of fee this is |
| **Payment Collection** | Which batch this item belongs to |
| **Institute** | Which institute this belongs to |
| **Payment Collection Item Details** | Individual payment transactions for this item |

### 3. Payment Model

**What it represents:** A single payment transaction initiated by a student through the payment gateway.

#### Payment Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Amount** | Yes | Total amount in this payment | 50000.00 |
| **Payment Status** | Auto-managed | Current status | "Pending", "Succeeded", "Failed" |
| **Is Refunded** | Auto-managed | Has this payment been refunded? | true/false |

#### Payment Gateway Details (Mswipe)

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **MSwipe IPG Order ID** | Auto-generated | Internal order identifier | "ABC School_P1705329600000" |
| **MSwipe IPG Invoice ID** | Auto-generated | Invoice identifier sent to gateway | "ABC School_P1705329600000" |
| **MSwipe IPG Trans ID** | From gateway | Transaction ID from Mswipe | "TXN123456789" |
| **MSwipe IPG Payment ID** | From gateway | Payment ID from Mswipe | "PAY987654321" |
| **MSwipe Encoded IPG ID** | From gateway | Encoded transaction ID | "ENC_ABC123..." |
| **MSwipe IPG Status** | From gateway | Gateway status response | "success", "failed" |

#### Relationships

| Relationship | Description |
|--------------|-------------|
| **Student** | Which student made this payment |
| **Institute** | Which institute this payment is for |
| **Payment Collection Item Details** | Fee items included in this payment |

### 4. Payment Collection Item Detail Model

**What it represents:** A link between a Payment transaction and a specific Payment Collection Item, tracking how much of a particular fee was paid in a specific transaction.

#### Transaction Details

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Amount Paid** | Yes | Amount paid for this specific fee item in this transaction | 30000.00 |
| **Payment Date** | Yes | When this payment was made | 2024-01-15T10:30:00Z |
| **Payment Status** | Auto-managed | Status of this payment | "Pending", "Succeeded", "Failed" |
| **Is Refunded** | Auto-managed | Has this been refunded? | true/false |

#### Relationships

| Relationship | Description |
|--------------|-------------|
| **Payment** | Which payment transaction this belongs to |
| **Payment Collection Item** | Which fee item this payment is for |
| **Student** | Which student made this payment |
| **Institute** | Which institute this is for |

#### What you can do with this model:
- Track multiple payments for the same fee item (partial payments)
- View complete payment history for each fee
- Calculate total amounts paid across all transactions
- Support refund processing

---

## Prerequisites for Making Payments

Before students can make payments through the portal, ensure the following prerequisites are met:

### 1. Institute Configuration

- [ ] **Institute is Activated** (status = "Active")
  - Institute must have completed activation workflow
  - Subdomain configured (e.g., `stmary-edu.antpay.live`)

- [ ] **Payment Gateway Credentials Configured**
  - Mswipe merchant credentials set up
  - `paymentGatewayAccessKey` configured
  - `paymentGatewayAccessSecret` configured
  - `paymentGatewayMerchantId` configured
  - `paymentGatewayUserId` configured

- [ ] **Email Configuration**
  - Email templates configured for:
    - OTP verification
    - Payment confirmation
    - Payment failure
    - Payment reminders
  - SMTP settings configured

### 2. Student Setup

- [ ] **Student Record Created**
  - Student exists in the system
  - Student Login ID has been generated (computed field)
  - Parent email address configured
  - Parent mobile number configured

- [ ] **Payment Collections Assigned**
  - At least one Payment Collection Item assigned to student
  - Payment mode set to "PG" (Payment Gateway)
  - Due dates configured

### 3. Environment Configuration

- [ ] **Environment Variables Set**
  ```bash
  IAM_JWT_SECRET=<jwt_secret_key>
  MSWIPE_LOGIN_URL=<mswipe_login_endpoint>
  MSWIPE_PAYMENT_GATEWAY_URL=<mswipe_gateway_endpoint>
  BASE_URL=<backend_api_base_url>
  EDU_BASE_DOMAIN=<student_portal_base_domain>
  ```

### 4. Student Portal Deployment

- [ ] **Frontend Application Deployed**
  - Separate frontend application running
  - Configured to call backend APIs
  - CORS settings allow cross-origin requests
  - Hosted on separate port/domain

---

## Student Payment Workflow

This section provides a comprehensive step-by-step guide for students/parents to authenticate and make payments through the student portal.

### Phase 1: Authentication (Login with OTP)

#### Step 1: Navigate to Student Portal

**Student Action:**
- Open student portal URL: `https://{institute.hostedPagePrefix}-{EDU_BASE_DOMAIN}`
- Example: `https://stmary-edu.antpay.live`

#### Step 2: Enter Student Login ID

**Student Action:**
- Enter student login ID (provided by school)
- Example: `JOHND-A1B2C`

**Frontend Action:**
```
GET /api/student/login/initiate/:id
```

**API Request:**
```http
GET /api/student/login/initiate/JOHND-A1B2C
```

**API Response (Success):**
```json
{
  "isValid": true,
  "maskedEmail": "ro****@example.com",
  "maskedPhone": "91******89",
  "studentLoginId": "JOHND-A1B2C",
  "id": 123,
  "message": "Student ID is valid"
}
```

**API Response (Failure):**
```json
{
  "isValid": false,
  "maskedEmail": null,
  "maskedPhone": null,
  "studentLoginId": null,
  "id": null,
  "message": "Student ID is invalid"
}
```

**What to verify:**
- Student sees masked email and phone
- Confirms these match their records
- Proceeds to OTP generation

#### Step 3: Request OTP

**Student Action:**
- Click "Send OTP" button

**Frontend Action:**
```
POST /api/student/initiate-otp
```

**API Request:**
```http
POST /api/student/initiate-otp
Content-Type: application/json

{
  "studentLoginId": "JOHND-A1B2C"
}
```

**API Response:**
```json
{
  "success": true,
  "id": 123,
  "message": "OTP sent to registered email"
}
```

**Backend Processing:**
1. Generates 6-digit OTP (e.g., `123456`)
2. Sets OTP expiration to 5 minutes from now
3. Generates JWT token (valid for 12 hours)
4. Stores OTP, expiration, and token in Student record
5. Sends email to parent email address

**Email Sent:**
- **Template:** `otp-verification`
- **To:** Parent email address
- **Subject:** "Your OTP for School Fees Portal Login"
- **Content:**
  - OTP: `123456`
  - Validity: 5 minutes
  - Institute logo and support contact

**What to verify:**
- Student/parent receives OTP email within 1-2 minutes
- Email shows correct OTP digits
- Email shows institute branding

#### Step 4: Verify OTP

**Student Action:**
- Check email for OTP
- Enter OTP in portal (e.g., `123456`)
- Click "Verify" button

**Frontend Action:**
```
POST /api/student/verify-otp
```

**API Request:**
```http
POST /api/student/verify-otp
Content-Type: application/json

{
  "studentLoginId": "JOHND-A1B2C",
  "otp": "123456"
}
```

**API Response (Success):**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "studentId": "STU2024001",
  "studentLoginId": "JOHND-A1B2C",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**API Response (Invalid OTP):**
```json
{
  "success": false,
  "message": "Invalid OTP"
}
```

**API Response (Expired OTP):**
```json
{
  "success": false,
  "message": "OTP has expired"
}
```

**Frontend Processing:**
- Stores JWT token in browser (localStorage or sessionStorage)
- Redirects to dashboard
- Includes token in all subsequent API calls as `Authorization: Bearer {token}`

**What to verify:**
- OTP verification succeeds
- Student is redirected to dashboard
- Token is stored for future requests

---

### Phase 2: View Pending Payments (Dashboard)

#### Step 5: Load Student Profile and Institute Data

**Frontend Action (on dashboard load):**
```
GET /api/student/get-student-record?id={studentId}
GET /api/student/get-institute-record?userId={studentId}
```

**API Request 1 (Student Record):**
```http
GET /api/student/get-student-record?id=123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**API Response:**
```json
{
  "id": 123,
  "studentName": "John Doe",
  "studentEmailAddress": "john@example.com",
  "studentMobileNumber": "9876543210",
  "parentName": "Robert Doe",
  "parentMobileNumber": "9123456789",
  "parentEmailAddress": "robert.doe@example.com",
  "studentId": "STU2024001",
  "studentLoginId": "JOHND-A1B2C",
  "institute": {
    "instituteName": "St. Mary's School",
    "supportEmail": "support@stmary.edu",
    "supportMobile": "+919876543210",
    "tnC": "Terms and conditions content...",
    "privacyPolicy": "Privacy policy content...",
    "faqs": "Frequently asked questions...",
    "_media": {
      "logo": [
        {
          "_full_url": "https://s3.amazonaws.com/school-logos/stmary.png"
        }
      ]
    }
  }
}
```

**Frontend Display:**
- Show student name and details
- Display institute logo and branding
- Show support contact information

#### Step 6: Fetch Pending Payment Collections

**Frontend Action:**
```
Call PaymentCollectionService.getPaymentCollectionsForStudent(studentLoginId, isPaid=false)
```

**Backend Query (via custom service method):**
```typescript
// Find all payment collections with pending items for this student
const collections = await find(PaymentCollection, {
  where: {
    paymentCollectionItems: {
      student: { studentLoginId: studentLoginId },
      status: In(['Pending', 'Partially Paid'])
    }
  },
  relations: ['paymentCollectionItems', 'paymentCollectionItems.feeType', 'institute']
})
```

**API Response:**
```json
[
  {
    "id": 1,
    "name": "Quarter 1 2024 Fees",
    "createdOn": "15 Jan 2024",
    "description": "Q1 fees including tuition and lab charges",
    "institute": {
      "id": 1,
      "instituteName": "St. Mary's School"
    },
    "totalAmountToBePaid": 50000,
    "paymentCollectionItems": [
      {
        "id": 101,
        "feeType": {
          "id": 1,
          "feeType": "Tuition Fee"
        },
        "dueDate": "2024-02-15",
        "amountToBePaid": 30000,
        "amountPaid": 0,
        "amountPending": 30000,
        "status": "Pending",
        "partPaymentAllowed": true,
        "isOverdue": false,
        "totalAmountToBePaid": 30000,
        "lateAmountToBePaid": 0,
        "mode": "PG"
      },
      {
        "id": 102,
        "feeType": {
          "id": 2,
          "feeType": "Lab Fee"
        },
        "dueDate": "2024-02-15",
        "amountToBePaid": 20000,
        "amountPaid": 0,
        "amountPending": 20000,
        "status": "Pending",
        "partPaymentAllowed": false,
        "isOverdue": false,
        "totalAmountToBePaid": 20000,
        "lateAmountToBePaid": 0,
        "mode": "PG"
      }
    ]
  }
]
```

**Dashboard Display:**

For each payment collection, show:
- **Collection Name:** "Quarter 1 2024 Fees"
- **Description:** "Q1 fees including tuition and lab charges"
- **Created On:** "15 Jan 2024"
- **Total Amount:** ₹50,000

For each payment collection item within the collection:

| Fee Type | Due Date | Amount | Late Fee | Total | Status | Can Pay Partially? |
|----------|----------|--------|----------|-------|--------|--------------------|
| Tuition Fee | 15 Feb 2024 | ₹30,000 | ₹0 | ₹30,000 | Pending | Yes |
| Lab Fee | 15 Feb 2024 | ₹20,000 | ₹0 | ₹20,000 | Pending | No |

**Overdue Items Display:**

If `isOverdue = true`, show:
- Red "OVERDUE" badge
- Days overdue: "Overdue by 5 days"
- Late fee amount highlighted in red
- Total amount includes late fee

Example:
```
Tuition Fee - OVERDUE
Due Date: 10 Jan 2024 (overdue by 5 days)
Base Amount: ₹30,000
Late Fee (5%): ₹1,500
Total Amount: ₹31,500
Status: Pending
```

**What to verify:**
- All pending payment collections are displayed
- Fee items show correct amounts
- Overdue items are highlighted
- Late fees are calculated and displayed
- Part payment option is clearly indicated

---

### Phase 3: Initiate Payment

#### Step 7: Select Fees to Pay

**Student Action:**
- Review pending fees
- Select which fees to pay (can select multiple from same or different collections)
- For partial payment allowed items, can choose to pay partial amount
- Click "Proceed to Pay" button

**Frontend Preparation:**

Build payment request with selected items:

```javascript
// Example: Student selects to pay both items in full
const paymentRequest = {
  studentLoginId: "JOHND-A1B2C",
  amountMap: {
    "101": 30000,  // Tuition Fee
    "102": 20000   // Lab Fee
  },
  totalAmount: 50000
}

// Example: Student pays partial amount for Tuition Fee
const partialPaymentRequest = {
  studentLoginId: "JOHND-A1B2C",
  amountMap: {
    "101": 15000  // Paying half of Tuition Fee
  },
  totalAmount: 15000
}
```

**Validation Rules:**
- If `partPaymentAllowed = false`, must pay full `totalAmountToBePaid`
- If `partPaymentAllowed = true`, can pay any amount from ₹1 to `amountPending`
- Cannot pay more than `amountPending` for any item
- Total amount must equal sum of all amounts in amountMap

#### Step 8: Generate Payment Gateway Link

**Frontend Action:**
```
POST /api/payment/payment-gateway
```

**API Request:**
```http
POST /api/payment/payment-gateway
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "studentLoginId": "JOHND-A1B2C",
  "amountMap": {
    "101": 30000,
    "102": 20000
  },
  "totalAmount": 50000
}
```

**Backend Processing:**

**Step 8a: Create Payment Record**
```sql
INSERT INTO payment (
  institute_id,
  student_id,
  amount,
  mSwipeIpgOrderId,
  mSwipeIpgInvoiceId,
  paymentStatus,
  createdAt
) VALUES (
  1,
  123,
  50000,
  'St. Mary\'s School_P1705329600000',
  'St. Mary\'s School_P1705329600000',
  'Pending',
  NOW()
)
-- Returns payment.id = 1001
```

**Step 8b: Create Payment Collection Item Details**
```sql
-- For Tuition Fee (item 101)
INSERT INTO payment_collection_item_detail (
  payment_id,
  student_id,
  institute_id,
  paymentCollectionItem_id,
  paymentDate,
  amountPaid,
  paymentStatus
) VALUES (
  1001,
  123,
  1,
  101,
  NOW(),
  30000,
  'Pending'
)

-- For Lab Fee (item 102)
INSERT INTO payment_collection_item_detail (
  payment_id,
  student_id,
  institute_id,
  paymentCollectionItem_id,
  paymentDate,
  amountPaid,
  paymentStatus
) VALUES (
  1001,
  123,
  1,
  102,
  NOW(),
  20000,
  'Pending'
)
```

**Step 8c: Call Mswipe Gateway**

**Mswipe Authentication:**
```http
POST https://mswipe.api/login
Content-Type: application/json

{
  "clientId": "merchant_username",
  "password": "merchant_password",
  "applId": "api",
  "channelId": "pbl"
}
```

**Mswipe Response:**
```json
{
  "status": true,
  "token": "MSWIPE_AUTH_TOKEN_123..."
}
```

**Mswipe Payment Link Request:**
```http
POST https://mswipe.api/payment/createlink
Content-Type: application/json

{
  "amount": "50000",
  "mobileno": "9123456789",
  "custcode": "MERCHANT_ID",
  "user_id": "INST_USER_ID",
  "sessiontoken": "MSWIPE_AUTH_TOKEN_123...",
  "versionno": "VER4.0.0",
  "email_id": "robert.doe@example.com",
  "invoice_id": "St. Mary's School_P1705329600000",
  "request_id": "1705329600000",
  "ApplicationId": "api",
  "ChannelId": "pbl",
  "ClientId": "merchant_username",
  "redirect_url": "https://api.school-portal.com/api/payment/payment-callback",
  "IsSendSMS": true
}
```

**Mswipe Response:**
```json
{
  "status": "True",
  "smslink": "https://upi.mswipe.com/pay/ABC123?key=value",
  "txn_id": "TXN987654321",
  "orderId": "St. Mary's School_P1705329600000"
}
```

**Step 8d: Update Payment Record with Transaction ID**
```sql
UPDATE payment
SET mSwipeIpgTransId = 'TXN987654321'
WHERE id = 1001
```

**API Response:**
```json
{
  "url": "https://upi.mswipe.com/pay/ABC123?key=value"
}
```

**What to verify:**
- Payment record created with status "Pending"
- Payment Collection Item Details created for all selected items
- Mswipe payment link generated successfully
- Transaction ID stored in Payment record

#### Step 9: Redirect to Payment Gateway

**Frontend Action:**
- Redirect student to payment gateway URL
- Student leaves student portal and goes to Mswipe payment page

**Payment Gateway (Mswipe) Page:**
- Student sees payment details:
  - Amount: ₹50,000
  - Merchant: St. Mary's School
  - Invoice ID: St. Mary's School_P1705329600000
- Student selects payment method:
  - UPI (Google Pay, PhonePe, Paytm, etc.)
  - Credit/Debit Card
  - Net Banking
- Student completes payment

---

### Phase 4: Payment Processing (Webhook Callback)

#### Step 10: Payment Gateway Callback

**After Payment Completion:**

Mswipe sends callback to backend (both GET and POST supported)

**Callback Format (GET):**
```http
GET /api/payment/payment-callback?status=success&ipgid=TXN987654321&encIpgId=ENC_ABC123&invoiceID=St.%20Mary's%20School_P1705329600000
```

**Callback Format (POST):**
```http
POST /api/payment/payment-callback
Content-Type: application/json

{
  "Status": "success",
  "TransID": "TXN987654321",
  "EncID": "ENC_ABC123",
  "InvoiceID": "St. Mary's School_P1705329600000",
  "PaymentID": "PAY123456"
}
```

**Backend Processing:**

**Step 10a: Find Payment Record**
```typescript
const payment = await find(Payment, {
  where: { mSwipeIpgInvoiceId: "St. Mary's School_P1705329600000" },
  relations: ['student', 'institute']
})
```

**Step 10b: Update Payment Status (Success Case)**
```sql
UPDATE payment
SET
  mSwipeIpgStatus = 'success',
  mSwipeIpgTransId = 'TXN987654321',
  mSwipeEncodedIpgId = 'ENC_ABC123',
  mSwipeIpgPaymentId = 'PAY123456',
  paymentStatus = 'Succeeded',
  updatedAt = NOW()
WHERE mSwipeIpgInvoiceId = 'St. Mary''s School_P1705329600000'
```

**Step 10c: Update Payment Collection Item Details**
```sql
UPDATE payment_collection_item_detail
SET
  paymentStatus = 'Succeeded',
  updatedAt = NOW()
WHERE payment_id = 1001
```

**Step 10d: Trigger Computed Field Provider**

When PaymentCollectionItemDetail is updated, the `PaymentCollectionItemAmountProvider` is automatically triggered:

**Computed Field Logic:**
```typescript
// For each PaymentCollectionItem (101, 102)
// Find all succeeded payment details
const succeededDetails = await find(PaymentCollectionItemDetail, {
  where: {
    paymentCollectionItem: { id: itemId },
    paymentStatus: 'Succeeded'
  }
})

// Calculate totals
const amountPaid = sum(succeededDetails.map(d => d.amountPaid))
const totalAmountToBePaid = item.amountToBePaid + item.lateAmountToBePaid
const amountPending = totalAmountToBePaid - amountPaid

// Determine status
const status = (amountPending <= 0) ? 'Fully Paid' :
               (amountPaid > 0) ? 'Partially Paid' : 'Pending'

// Update PaymentCollectionItem
await update(PaymentCollectionItem, itemId, {
  amountPaid: amountPaid.toString(),
  amountPending: amountPending.toString(),
  totalAmountToBePaid: totalAmountToBePaid.toString(),
  status: status
})
```

**Example Calculation for Tuition Fee (item 101):**
```
Before Payment:
  amountToBePaid: 30000
  lateAmountToBePaid: 0
  amountPaid: 0
  amountPending: 30000
  totalAmountToBePaid: 30000
  status: "Pending"

After Payment (₹30,000):
  Succeeded details: [{ amountPaid: 30000 }]
  amountPaid: 30000 (sum of succeeded)
  totalAmountToBePaid: 30000 + 0 = 30000
  amountPending: 30000 - 30000 = 0
  status: "Fully Paid"

After Payment Updates:
  amountToBePaid: 30000
  lateAmountToBePaid: 0
  amountPaid: 30000
  amountPending: 0
  totalAmountToBePaid: 30000
  status: "Fully Paid"
```

**Step 10e: Send Payment Confirmation Email**

**Email Template:** `confirm-payment`
**To:** Parent email address
**Subject:** "Payment Confirmation - St. Mary's School"

**Email Context:**
```json
{
  "paymentDetails": {
    "paymentCollection": "Quarter 1 2024 Fees",
    "txnId": "TXN987654321",
    "totalAmountDue": 50000,
    "createdAt": "2024-01-15T10:30:00Z",
    "feeTypes": ["Tuition Fee", "Lab Fee"],
    "totalAmount": 50000,
    "status": "Paid"
  },
  "student": {
    "studentName": "John Doe",
    "studentLoginId": "JOHND-A1B2C",
    "institute": {
      "instituteName": "St. Mary's School",
      "supportEmail": "support@stmary.edu",
      "supportMobile": "+919876543210"
    }
  },
  "instituteLogo": "https://s3.amazonaws.com/school-logos/stmary.png"
}
```

**Email Content:**
```
Dear Robert Doe,

Payment Confirmed!

Your payment for John Doe (Login ID: JOHND-A1B2C) has been successfully processed.

Payment Details:
- Collection: Quarter 1 2024 Fees
- Fee Types: Tuition Fee, Lab Fee
- Amount Paid: ₹50,000
- Transaction ID: TXN987654321
- Date: 15 Jan 2024, 10:30 AM
- Status: Paid

Thank you for your payment.

For any queries, contact:
Email: support@stmary.edu
Phone: +919876543210

---
St. Mary's School
```

**Step 10f: Redirect Student Back to Portal**

**Redirect URL (Success):**
```
https://stmary-edu.antpay.live/dashboard?paymentStatus=success&txnId=TXN987654321
```

**Redirect URL (Failure):**
```
https://stmary-edu.antpay.live/dashboard?paymentStatus=failed&txnId=TXN987654321
```

**Frontend Processing:**
- Parse query parameters
- Show success/failure message
- Refresh dashboard to show updated payment status
- Display transaction ID

**What to verify:**
- Payment status updated to "Succeeded"
- Payment Collection Item Details updated to "Succeeded"
- PaymentCollectionItem amounts recalculated correctly
- PaymentCollectionItem status changed to "Fully Paid" or "Partially Paid"
- Confirmation email sent to parent
- Student redirected back to portal with success message

#### Step 11: Payment Failure Handling

**If Payment Fails:**

**Callback Parameters:**
```
status=failed
ipgid=TXN987654321
invoiceID=St. Mary's School_P1705329600000
```

**Backend Processing:**

**Update Payment Status:**
```sql
UPDATE payment
SET
  mSwipeIpgStatus = 'failed',
  paymentStatus = 'Failed',
  updatedAt = NOW()
WHERE mSwipeIpgInvoiceId = 'St. Mary''s School_P1705329600000'
```

**Update Payment Collection Item Details:**
```sql
UPDATE payment_collection_item_detail
SET
  paymentStatus = 'Failed',
  updatedAt = NOW()
WHERE payment_id = 1001
```

**Send Failure Email:**
- Template: `confirm-payment` (with status: "Failed")
- To: Parent email address
- Content: Payment failed message with retry instructions

**Redirect:**
```
https://stmary-edu.antpay.live/dashboard?paymentStatus=failed&txnId=TXN987654321
```

**Frontend Display:**
- Show error message: "Payment failed. Please try again."
- Original fees remain in pending status
- Student can retry payment

**What to verify:**
- Failed payment doesn't update fee amounts
- Original fees still show as "Pending"
- Student receives failure notification
- Student can initiate new payment for same fees

---

### Phase 5: View Payment History

#### Step 12: Access Payment History

**Student Action:**
- Navigate to "Payment History" section in dashboard

**Frontend Action:**
```
GET /api/payment/payment-transaction-history?studentLoginId={studentLoginId}
```

**API Request:**
```http
GET /api/payment/payment-transaction-history?studentLoginId=JOHND-A1B2C
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**API Response:**
```json
[
  {
    "id": 1001,
    "student": {
      "id": 123,
      "studentLoginId": "JOHND-A1B2C"
    },
    "institute": {
      "id": 1,
      "instituteName": "St. Mary's School"
    },
    "amount": 50000,
    "mSwipeIpgOrderId": "St. Mary's School_P1705329600000",
    "mSwipeIpgTransId": "TXN987654321",
    "mSwipeIpgInvoiceId": "St. Mary's School_P1705329600000",
    "mSwipeIpgStatus": "success",
    "paymentStatus": "Succeeded",
    "isRefunded": false,
    "createdAt": "2024-01-15T10:30:00Z"
  },
  {
    "id": 1002,
    "student": {
      "id": 123,
      "studentLoginId": "JOHND-A1B2C"
    },
    "institute": {
      "id": 1,
      "instituteName": "St. Mary's School"
    },
    "amount": 15000,
    "mSwipeIpgOrderId": "St. Mary's School_P1705329700000",
    "mSwipeIpgTransId": "TXN987654322",
    "mSwipeIpgInvoiceId": "St. Mary's School_P1705329700000",
    "mSwipeIpgStatus": "success",
    "paymentStatus": "Succeeded",
    "isRefunded": false,
    "createdAt": "2024-01-10T14:20:00Z"
  }
]
```

**Frontend Display:**

| Date | Transaction ID | Amount | Status | Invoice ID |
|------|---------------|--------|--------|------------|
| 15 Jan 2024, 10:30 AM | TXN987654321 | ₹50,000 | Succeeded | St. Mary's School_P1705329600000 |
| 10 Jan 2024, 02:20 PM | TXN987654322 | ₹15,000 | Succeeded | St. Mary's School_P1705329700000 |

**Status Indicators:**
- ✅ Succeeded (green)
- ❌ Failed (red)
- ⏳ Pending (yellow)
- 🔄 Refunded (blue)

**What to verify:**
- All payment transactions are displayed
- Latest payments appear first
- Transaction details are accurate
- Status is clearly indicated

#### Step 13: Download Payment Report

**Student Action:**
- Click "Download Report" button in Payment History section

**Frontend Action:**
```
POST /api/payment/download-student-fee-report?studentLoginId={studentLoginId}
```

**API Request:**
```http
POST /api/payment/download-student-fee-report?studentLoginId=JOHND-A1B2C
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**API Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Content-Disposition: `attachment; filename="payment-history-JOHND-A1B2C.xlsx"`
- Body: Binary Excel file

**Excel File Structure:**

| Ref No | Institute | Created On | Description | Fee Type | Due Date | Amount Paid | Status | Payment Mode |
|--------|-----------|------------|-------------|----------|----------|-------------|--------|--------------|
| Quarter 1 2024 Fees | St. Mary's School | 15 Jan 2024 | Q1 fees including tuition and lab charges | Tuition Fee | 15 Feb 2024 | ₹30,000 | Fully Paid | PG |
| Quarter 1 2024 Fees | St. Mary's School | 15 Jan 2024 | Q1 fees including tuition and lab charges | Lab Fee | 15 Feb 2024 | ₹20,000 | Fully Paid | PG |

**What to verify:**
- Excel file downloads successfully
- All payment collection items included
- Data is accurate and complete
- File can be opened in Excel/Google Sheets

---

## Automated Systems

### 1. Computed Field Providers

#### PaymentCollectionItemAmountProvider

**Purpose:** Automatically recalculate payment amounts when payment details are created or updated.

**Configuration:**
```json
{
  "name": "amountPaid",
  "type": "computed",
  "computedFieldValueType": "decimal",
  "computedFieldValueProvider": "PaymentCollectionItemAmountProvider",
  "computedFieldTriggerConfig": [
    {
      "modelName": "paymentCollectionItemDetail",
      "operations": ["after-update"]
    }
  ]
}
```

**Trigger:** When PaymentCollectionItemDetail record is created or updated

**Logic:**
```typescript
async computeValue(context: ComputedFieldContext): Promise<string> {
  const itemId = context.entity.paymentCollectionItem.id

  // Find all succeeded payment details for this item
  const succeededDetails = await this.detailRepo.find({
    where: {
      paymentCollectionItem: { id: itemId },
      paymentStatus: 'Succeeded'
    }
  })

  // Calculate total amount paid
  const amountPaid = succeededDetails.reduce(
    (sum, detail) => sum + parseFloat(detail.amountPaid),
    0
  )

  // Get payment collection item
  const item = await this.itemRepo.findOne({
    where: { id: itemId }
  })

  // Calculate totals
  const totalAmountToBePaid = parseFloat(item.amountToBePaid) +
                               parseFloat(item.lateAmountToBePaid || '0')
  const amountPending = totalAmountToBePaid - amountPaid

  // Determine status
  let status = 'Pending'
  if (amountPending <= 0) {
    status = 'Fully Paid'
  } else if (amountPaid > 0) {
    status = 'Partially Paid'
  }

  // Update payment collection item
  await this.itemRepo.update(itemId, {
    amountPaid: amountPaid.toString(),
    amountPending: amountPending.toString(),
    totalAmountToBePaid: totalAmountToBePaid.toString(),
    status: status
  })

  return amountPaid.toString()
}
```

**Updates:**
- `amountPaid`: Sum of all succeeded payment details
- `amountPending`: Total to be paid minus amount paid
- `totalAmountToBePaid`: Base amount plus late fees
- `status`: "Pending" → "Partially Paid" → "Fully Paid"

**Example Scenarios:**

**Scenario 1: Full Payment**
```
Initial State:
  amountToBePaid: 30000
  lateAmountToBePaid: 0
  amountPaid: 0
  amountPending: 30000
  status: "Pending"

Payment Detail Created (₹30,000, status: "Succeeded"):
  Trigger: PaymentCollectionItemAmountProvider

Computed Updates:
  amountPaid: 30000
  totalAmountToBePaid: 30000
  amountPending: 0
  status: "Fully Paid"
```

**Scenario 2: Partial Payment**
```
Initial State:
  amountToBePaid: 30000
  lateAmountToBePaid: 0
  amountPaid: 0
  amountPending: 30000
  status: "Pending"

Payment Detail Created (₹15,000, status: "Succeeded"):
  Trigger: PaymentCollectionItemAmountProvider

Computed Updates:
  amountPaid: 15000
  totalAmountToBePaid: 30000
  amountPending: 15000
  status: "Partially Paid"
```

**Scenario 3: Multiple Partial Payments**
```
Initial State:
  amountToBePaid: 30000
  lateAmountToBePaid: 1500
  amountPaid: 15000
  amountPending: 16500
  status: "Partially Paid"

Payment Detail Created (₹10,000, status: "Succeeded"):
  Trigger: PaymentCollectionItemAmountProvider

Succeeded Details: [
  { amountPaid: 15000 },
  { amountPaid: 10000 }
]

Computed Updates:
  amountPaid: 25000 (sum)
  totalAmountToBePaid: 31500 (30000 + 1500)
  amountPending: 6500 (31500 - 25000)
  status: "Partially Paid"
```

**Location:** [solid-api/src/fees-portal/computed-providers/payment-collection-item-amount-provider.ts](../solid-api/src/fees-portal/computed-providers/payment-collection-item-amount-provider.ts)

---

### 2. Scheduled Jobs

#### Job 1: Late Fee Payment Calculator

**Purpose:** Calculate and apply late fees for overdue payments.

**Configuration:**
```json
{
  "scheduleName": "Late Fee Calculation",
  "isActive": true,
  "frequency": "Daily",
  "job": "LateFeePaymentCalculatorScheduledJob",
  "moduleUserKey": "fees-portal"
}
```

**Frequency:** Daily (runs once per day)

**Logic:**

**Step 1: Find Overdue Items**
```typescript
const today = new Date()
const overdueItems = await this.itemRepo.find({
  where: {
    dueDate: LessThan(today),
    status: Not(In(['Cancelled', 'Fully Paid'])),
    feeType: {
      latePaymentFeesType: Not('None')
    }
  },
  relations: ['feeType']
})
```

**Step 2: Calculate Late Fees**
```typescript
for (const item of overdueItems) {
  // Calculate overdue days
  const dueDate = new Date(item.dueDate)
  const overdueByDays = Math.floor((today.getTime() - dueDate.getTime()) / 86400000)

  // Calculate base pending amount
  const basePending = parseFloat(item.amountToBePaid) - parseFloat(item.amountPaid || '0')

  // Calculate late fee based on fee type configuration
  let lateFee = 0
  if (item.feeType.latePaymentFeesType === 'Percent') {
    lateFee = (basePending * parseFloat(item.feeType.latePaymentFees)) / 100
  } else if (item.feeType.latePaymentFeesType === 'Absolute') {
    lateFee = parseFloat(item.feeType.latePaymentFees)
  }

  // Calculate total amounts
  const totalAmountToBePaid = parseFloat(item.amountToBePaid) + lateFee
  const amountPending = totalAmountToBePaid - parseFloat(item.amountPaid || '0')

  // Update payment collection item
  await this.itemRepo.update(item.id, {
    isOverdue: true,
    overdueByDays: overdueByDays,
    lateAmountToBePaid: lateFee.toString(),
    totalAmountToBePaid: totalAmountToBePaid.toString(),
    amountPending: amountPending.toString()
  })
}
```

**Example Calculation:**

**Fee Type Configuration:**
```
Tuition Fee:
  latePaymentFeesType: "Percent"
  latePaymentFees: 5
```

**Payment Collection Item:**
```
Initial State (on due date):
  dueDate: 2024-01-15
  amountToBePaid: 30000
  amountPaid: 0
  lateAmountToBePaid: 0
  totalAmountToBePaid: 30000
  amountPending: 30000
  isOverdue: false
  overdueByDays: 0
  status: "Pending"

After 10 days (2024-01-25, job runs):
  today: 2024-01-25
  overdueByDays: floor((2024-01-25 - 2024-01-15) / 86400000) = 10
  basePending: 30000 - 0 = 30000
  lateFee: (30000 * 5) / 100 = 1500
  totalAmountToBePaid: 30000 + 1500 = 31500
  amountPending: 31500 - 0 = 31500

Updated State:
  dueDate: 2024-01-15
  amountToBePaid: 30000
  amountPaid: 0
  lateAmountToBePaid: 1500
  totalAmountToBePaid: 31500
  amountPending: 31500
  isOverdue: true
  overdueByDays: 10
  status: "Pending"
```

**What This Job Does:**
- Runs daily at configured time
- Finds all overdue payment items
- Calculates late fees based on fee type configuration
- Updates payment amounts and overdue status
- Affects what students see on their dashboard

**Location:** [solid-api/src/fees-portal/scheduled-jobs/late-fee-payment-calculator-scheduled-job.service.ts](../solid-api/src/fees-portal/scheduled-jobs/late-fee-payment-calculator-scheduled-job.service.ts)

#### Job 2: Send Email Reminders

**Purpose:** Send payment reminder emails to students with pending fees.

**Configuration:**
```json
{
  "scheduleName": "Fees Due Email",
  "isActive": true,
  "frequency": "Daily",
  "job": "SendEmailScheduleJobs",
  "moduleUserKey": "fees-portal"
}
```

**Frequency:** Daily (runs once per day)

**Logic:**

**Step 1: Find Pending Items**
```typescript
const pendingItems = await this.itemRepo.find({
  where: {
    status: In(['Pending', 'Partially Paid'])
  },
  relations: ['student', 'feeType', 'institute', 'paymentCollection']
})
```

**Step 2: Group by Student**
```typescript
const groupedByStudent = {}
for (const item of pendingItems) {
  const studentId = item.student.id
  if (!groupedByStudent[studentId]) {
    groupedByStudent[studentId] = []
  }
  groupedByStudent[studentId].push(item)
}
```

**Step 3: Send Reminder Email for Each Student**
```typescript
for (const [studentId, items] of Object.entries(groupedByStudent)) {
  const student = items[0].student
  const institute = items[0].institute

  // Calculate totals
  const totalAmountDue = items.reduce(
    (sum, item) => sum + parseFloat(item.amountPending),
    0
  )

  // Get unique fee types and collections
  const feeTypes = [...new Set(items.map(item => item.feeType.feeType))].join(', ')
  const paymentCollections = [...new Set(items.map(item => item.paymentCollection.name))].join(', ')

  // Send email
  await this.mailService.sendEmail('new-payment-or-payment-reminder', {
    dueDetails: {
      totalAmountDue: totalAmountDue,
      feeTypes: feeTypes,
      status: 'Pending',
      redirectUrl: `https://${institute.hostedPagePrefix}-${process.env.EDU_BASE_DOMAIN}/?id=${student.studentLoginId}`,
      createdAt: new Date().toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      }).toUpperCase(),
      paymentCollections: paymentCollections
    },
    student: {
      studentName: student.studentName,
      studentId: student.studentId,
      studentLoginId: student.studentLoginId
    },
    instituteLogo: institute._media?.logo?.[0]?._full_url,
    supportEmail: institute.supportEmail,
    supportMobile: institute.supportMobile
  }, student.parentEmailAddress)
}
```

**Email Template Context:**
```json
{
  "dueDetails": {
    "totalAmountDue": 35000,
    "feeTypes": "Tuition Fee, Lab Fee",
    "status": "Pending",
    "redirectUrl": "https://stmary-edu.antpay.live/?id=JOHND-A1B2C",
    "createdAt": "25-JAN-2024",
    "paymentCollections": "Quarter 1 2024 Fees"
  },
  "student": {
    "studentName": "John Doe",
    "studentId": "STU2024001",
    "studentLoginId": "JOHND-A1B2C"
  },
  "instituteLogo": "https://s3.amazonaws.com/school-logos/stmary.png",
  "supportEmail": "support@stmary.edu",
  "supportMobile": "+919876543210"
}
```

**Email Content:**
```
Dear Parent/Guardian,

Payment Reminder - Pending Fees

This is a reminder that the following fees for John Doe (STU2024001) are pending:

Payment Collections: Quarter 1 2024 Fees
Fee Types: Tuition Fee, Lab Fee
Total Amount Due: ₹35,000
Status: Pending

Please log in to the student portal to make the payment:
https://stmary-edu.antpay.live/?id=JOHND-A1B2C

For any queries, contact:
Email: support@stmary.edu
Phone: +919876543210

---
St. Mary's School
```

**What This Job Does:**
- Runs daily at configured time
- Finds all students with pending/partially paid fees
- Groups fees by student
- Sends single reminder email per student (not per fee)
- Includes direct login link to student portal

**Location:** [solid-api/src/fees-portal/scheduled-jobs/send-email-schedule-jobs.service.ts](../solid-api/src/fees-portal/scheduled-jobs/send-email-schedule-jobs.service.ts)

---

## Technical Implementation Details

### API Endpoints Summary

#### Student Authentication

| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/api/student/login/initiate/:id` | GET | Public | Validate student login ID |
| `/api/student/initiate-otp` | POST | Public | Generate and send OTP |
| `/api/student/verify-otp` | POST | Public | Verify OTP and return JWT token |
| `/api/student/s1` | POST | Public | Validate JWT token |

#### Student Profile & Institute

| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/api/student/get-student-record` | GET | @StudentAuth | Get student profile data |
| `/api/student/get-institute-record` | GET | @StudentAuth | Get institute details |

#### Payment Dashboard

| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `PaymentCollectionService.getPaymentCollectionsForStudent()` | Service | @StudentAuth | Get pending/paid payment collections |

#### Payment Processing

| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/api/payment/payment-gateway` | POST | @StudentAuth | Generate payment gateway link |
| `/api/payment/payment-callback` | GET/POST | Public | Handle payment gateway webhook |

#### Payment History

| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/api/payment/payment-transaction-history` | GET | @StudentAuth | Get student payment history |
| `/api/payment/download-student-fee-report` | POST | @StudentAuth | Download payment report as Excel |

### Authentication Guard

**Guard:** `StudentAuthGuard`

**Purpose:** Validate JWT token for student portal requests

**Implementation:**
```typescript
@Injectable()
export class StudentAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest()
    const authHeader = request.headers['authorization']

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new BadRequestException('Missing or invalid authorization header')
    }

    const token = authHeader.substring(7)

    try {
      // Verify JWT signature
      const decoded = jwt.verify(token, process.env.IAM_JWT_SECRET)

      // Check if token exists in Student table
      const student = await this.studentRepo.findOne({
        where: { token: token }
      })

      if (!student) {
        throw new BadRequestException('Invalid token')
      }

      // Attach student to request
      request.student = student

      return true
    } catch (error) {
      throw new BadRequestException('Invalid or expired token')
    }
  }
}
```

**Usage:**
```typescript
@Controller('api/student')
export class StudentController {

  @Get('get-student-record')
  @StudentAuth()  // Applies StudentAuthGuard
  async getStudentRecord(@Query('id') id: number) {
    // Only accessible with valid JWT token
    return this.studentService.getStudentRecord(id)
  }
}
```

**Token Flow:**
1. Student verifies OTP
2. Backend generates JWT token (valid 12 hours)
3. Backend stores token in Student record
4. Frontend stores token in browser
5. Frontend sends token in Authorization header for all subsequent requests
6. Guard validates token on each request

### Request/Response Formats

#### Authentication Responses

**Success:**
```json
{
  "success": true,
  "message": "Operation successful",
  "studentId": "STU2024001",
  "studentLoginId": "JOHND-A1B2C",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Failure:**
```json
{
  "success": false,
  "message": "Error message describing what went wrong"
}
```

**Validation Error:**
```json
{
  "isValid": false,
  "message": "Student ID is invalid"
}
```

#### Payment Gateway Link Response

**Success:**
```json
{
  "url": "https://upi.mswipe.com/pay/ABC123?key=value"
}
```

**Error:**
```json
{
  "statusCode": 400,
  "message": "Error message",
  "error": "Bad Request"
}
```

#### Payment Callback Parameters

**GET Request:**
```
/api/payment/payment-callback?status=success&ipgid=TXN123&encIpgId=ENC_ABC&invoiceID=School_P123
```

**POST Request:**
```json
{
  "Status": "success",
  "TransID": "TXN123",
  "EncID": "ENC_ABC",
  "InvoiceID": "School_P123",
  "PaymentID": "PAY456"
}
```

### Error Handling

#### Authentication Errors

| Error | HTTP Status | Response |
|-------|-------------|----------|
| Missing Authorization header | 400 | `{ "message": "Missing or invalid authorization header" }` |
| Invalid JWT signature | 400 | `{ "message": "Invalid or expired token" }` |
| Token not in database | 400 | `{ "message": "Invalid token" }` |
| Student not found | 404 | `{ "message": "Student not found" }` |

#### Payment Errors

| Error | HTTP Status | Response |
|-------|-------------|----------|
| Payment not found (callback) | 404 | `{ "message": "Payment not found" }` |
| Student not found | 404 | `{ "message": "Student not found with ID {id}" }` |
| Invalid amount | 400 | `{ "message": "Amount cannot be negative or zero" }` |
| Gateway error | 500 | `{ "message": "Payment gateway error: {details}" }` |

#### OTP Errors

| Error | Response |
|-------|----------|
| Invalid OTP | `{ "success": false, "message": "Invalid OTP" }` |
| Expired OTP | `{ "success": false, "message": "OTP has expired" }` |
| OTP not generated | `{ "success": false, "message": "Invalid OTP" }` |

### Environment Variables

```bash
# JWT Authentication
IAM_JWT_SECRET=your_jwt_secret_key_here

# Mswipe Payment Gateway
MSWIPE_LOGIN_URL=https://api.mswipe.com/login
MSWIPE_PAYMENT_GATEWAY_URL=https://api.mswipe.com/payment/createlink
MSWIPE_PAYMENT_TRANSACTION_URL=https://api.mswipe.com/transaction/status

# Application URLs
BASE_URL=https://api.school-fees-portal.com
EDU_BASE_DOMAIN=edu.antpay.live
STUDENT_PORTAL_FRONTEND_BASE_URL=https://student.edu.antpay.live

# Email Service
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@school.com
SMTP_PASSWORD=smtp_password

# AWS S3 (for media files)
S3_AWS_REGION_NAME=ap-south-1
S3_AWS_ACCESS_KEY=your_access_key
S3_AWS_SECRET_KEY=your_secret_key
```

### Database Schema Changes

**Payment Table:**
```sql
ALTER TABLE payment
ADD COLUMN mSwipeIpgTransId VARCHAR(255),
ADD COLUMN mSwipeIpgPaymentId VARCHAR(255),
ADD COLUMN mSwipeEncodedIpgId VARCHAR(255),
ADD COLUMN mSwipeIpgStatus VARCHAR(50);
```

**Student Table:**
```sql
ALTER TABLE student
ADD COLUMN otp VARCHAR(6),
ADD COLUMN otpExpiresAt TIMESTAMP,
ADD COLUMN token TEXT;
```

---

## Security Considerations

### 1. Authentication Security

**OTP Security:**
- OTP valid for only 5 minutes
- 6-digit numeric code (1 million combinations)
- Sent to registered parent email only
- Single-use (verified OTP cannot be reused)
- Not stored in plain text in logs

**JWT Token Security:**
- Signed with `IAM_JWT_SECRET`
- Valid for 12 hours only
- Stored in Student record for validation
- Verified on every protected endpoint
- Includes student login ID in payload

**Best Practices:**
```typescript
// Generate secure OTP
const otp = Math.floor(100000 + Math.random() * 900000).toString()

// Set short expiration
const otpExpiresAt = new Date(Date.now() + 5 * 60 * 1000) // 5 minutes

// Generate JWT with expiration
const token = jwt.sign(
  { studentLoginId: student.studentLoginId },
  process.env.IAM_JWT_SECRET,
  { expiresIn: '12h' }
)
```

### 2. Payment Security

**Payment Gateway Integration:**
- No payment card data stored on backend
- All card transactions handled by PCI-compliant Mswipe
- Redirect to gateway for payment processing
- Webhook validation to prevent tampering

**Invoice ID Generation:**
```typescript
// Unique invoice ID format
const invoiceId = `${instituteName}_P${Date.now()}`
// Example: "St. Mary's School_P1705329600000"
```

**Webhook Security:**
- Accept callbacks only from Mswipe IP ranges
- Validate invoice ID matches existing payment
- Verify transaction ID from gateway
- Check payment amount matches original request

### 3. Authorization

**Student Data Access:**
- Students can only access their own data
- Token validation ensures student identity
- No cross-student data leakage
- Institute isolation maintained

**Endpoint Protection:**
```typescript
// Protected endpoint example
@Get('get-student-record')
@StudentAuth()  // Requires valid JWT token
async getStudentRecord(@Query('id') id: number) {
  // Additional check: ensure id matches token student
  const tokenStudent = request.student
  if (tokenStudent.id !== id) {
    throw new ForbiddenException('Cannot access other student data')
  }
  return this.studentService.getStudentRecord(id)
}
```

### 4. Data Privacy

**Personal Information:**
- Student email masked in login initiation
- Phone number masked in login initiation
- Payment history shows only student's own transactions
- No exposure of other students' data

**Email Security:**
- OTPs sent only to registered parent email
- Payment confirmations sent only to parent email
- No sensitive payment data in email body
- Use secure SMTP with TLS

### 5. Rate Limiting

**Recommendations:**
```typescript
// Implement rate limiting for OTP generation
// Maximum 3 OTP requests per student per hour
@Throttle(3, 3600)
@Post('initiate-otp')
async initiateOtp(@Body() dto: InitiateOtpDto) {
  // ...
}

// Rate limit login attempts
// Maximum 5 failed attempts per student per 15 minutes
@Throttle(5, 900)
@Post('verify-otp')
async verifyOtp(@Body() dto: VerifyOtpDto) {
  // ...
}
```

---

## Best Practices

### For Institute Admins

1. **Payment Gateway Configuration**
   - Test payment gateway credentials in staging before production
   - Keep gateway credentials secure (use environment variables)
   - Monitor webhook callback success rates
   - Set up alerts for failed payment callbacks

2. **Email Template Configuration**
   - Test all email templates before going live
   - Ensure institute branding is consistent
   - Include support contact in all emails
   - Use clear, simple language for parents

3. **Late Fee Configuration**
   - Clearly communicate late fee policy to parents
   - Set reasonable late fee percentages/amounts
   - Consider grace periods before applying late fees
   - Review late fee calculations regularly

4. **Monitoring and Reporting**
   - Check payment reconciliation daily
   - Monitor failed payments and follow up
   - Review scheduled job execution logs
   - Track email delivery success rates

### For Developers

1. **Error Handling**
   - Always validate student login ID before processing
   - Handle payment gateway timeouts gracefully
   - Log all payment callback parameters
   - Return user-friendly error messages

2. **Testing**
   - Test complete payment flow in staging
   - Test payment failure scenarios
   - Test OTP expiration handling
   - Test partial payment scenarios

3. **Code Organization**
```typescript
// Good: Separate concerns
class StudentAuthService {
  generateOtp() { /* ... */ }
  verifyOtp() { /* ... */ }
  generateToken() { /* ... */ }
}

class PaymentService {
  initiatePayment() { /* ... */ }
  handleCallback() { /* ... */ }
  getHistory() { /* ... */ }
}

// Bad: Everything in one service
class StudentService {
  generateOtp() { /* ... */ }
  initiatePayment() { /* ... */ }
  sendEmail() { /* ... */ }
  // Too many responsibilities
}
```

4. **Logging**
```typescript
// Log important events
logger.info('OTP generated for student', { studentLoginId, expiresAt })
logger.info('Payment initiated', { paymentId, amount, studentId })
logger.info('Payment callback received', { status, txnId, invoiceId })
logger.warn('OTP verification failed', { studentLoginId, reason })
logger.error('Payment gateway error', { error, paymentId })
```

### For Frontend Developers

1. **Token Management**
   - Store JWT token securely (sessionStorage or localStorage)
   - Clear token on logout
   - Handle token expiration gracefully
   - Redirect to login if token invalid

2. **User Experience**
   - Show loading states during payment processing
   - Display clear error messages
   - Provide payment status updates
   - Show payment history clearly

3. **Payment Flow UX**
```javascript
// Good: Clear flow with confirmation
1. Show payment summary
2. Ask for confirmation
3. Show loading indicator
4. Redirect to payment gateway
5. Handle return with status message

// Bad: Abrupt redirect
1. Click "Pay Now"
2. Immediately redirect to gateway (no confirmation)
```

4. **Error Handling**
```javascript
// Good: User-friendly error messages
if (error.message === 'Invalid OTP') {
  showError('The OTP you entered is incorrect. Please try again.')
} else if (error.message === 'OTP has expired') {
  showError('Your OTP has expired. Please request a new one.')
}

// Bad: Technical error messages
showError(error.message) // "Token validation failed at line 42"
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. OTP Not Received

**Issue:** Student doesn't receive OTP email

**Possible Causes:**
- Email in spam folder
- Incorrect parent email in student record
- SMTP service down
- Email template not configured

**Diagnostic Steps:**
```bash
# Check student email address
curl -X GET "http://localhost:3000/api/student/login/initiate/JOHND-A1B2C"

# Check email service logs
docker logs solid-api | grep "OTP email"

# Verify SMTP configuration
env | grep SMTP
```

**Solution:**
- Verify parent email is correct
- Check spam folder
- Verify SMTP credentials
- Test email template manually

#### 2. OTP Expired

**Issue:** Student gets "OTP has expired" message

**Possible Causes:**
- More than 5 minutes elapsed since OTP generation
- System clock incorrect

**Solution:**
- Request new OTP
- Verify system time is correct

#### 3. Payment Gateway Link Not Generated

**Issue:** "Generate payment link" fails

**Possible Causes:**
- Mswipe credentials incorrect
- Mswipe service down
- Network connectivity issue
- Invalid payment amount

**Diagnostic Steps:**
```bash
# Check Mswipe credentials
env | grep MSWIPE

# Test Mswipe login
curl -X POST "https://api.mswipe.com/login" \
  -H "Content-Type: application/json" \
  -d '{"clientId":"username","password":"password","applId":"api","channelId":"pbl"}'

# Check backend logs
docker logs solid-api | grep "Mswipe"
```

**Solution:**
- Verify Mswipe credentials in environment
- Test Mswipe API connectivity
- Contact Mswipe support if service is down

#### 4. Payment Callback Not Received

**Issue:** Payment completed but status not updated

**Possible Causes:**
- Callback URL incorrect in Mswipe config
- Firewall blocking Mswipe IP
- Backend service down during callback
- Callback endpoint error

**Diagnostic Steps:**
```bash
# Check callback endpoint logs
docker logs solid-api | grep "payment-callback"

# Verify callback URL configuration
echo $BASE_URL/api/payment/payment-callback

# Check if callback endpoint is accessible
curl -X GET "http://localhost:3000/api/payment/payment-callback?status=success&ipgid=TEST&invoiceID=TEST_P123"
```

**Solution:**
- Verify BASE_URL environment variable
- Check firewall allows Mswipe IPs
- Contact Mswipe to resend webhook
- Manually update payment status if needed

#### 5. Computed Fields Not Updating

**Issue:** Payment successful but amounts not recalculated

**Possible Causes:**
- Computed field provider not registered
- Database trigger not firing
- Transaction rollback

**Diagnostic Steps:**
```bash
# Check if PaymentCollectionItemAmountProvider is registered
docker logs solid-api | grep "PaymentCollectionItemAmountProvider"

# Query payment collection item directly
psql -U postgres -d school_fees -c \
  "SELECT id, amountPaid, amountPending, status FROM payment_collection_item WHERE id = 101"
```

**Solution:**
- Verify computed field provider is in metadata
- Restart application to reload providers
- Manually trigger computed field calculation

#### 6. Late Fees Not Applied

**Issue:** Overdue payments don't show late fees

**Possible Causes:**
- Scheduled job not running
- Fee type late payment configuration missing
- Job frequency too low

**Diagnostic Steps:**
```bash
# Check if scheduled job is active
psql -U postgres -d school_fees -c \
  "SELECT * FROM scheduled_job WHERE job = 'LateFeePaymentCalculatorScheduledJob'"

# Check fee type configuration
psql -U postgres -d school_fees -c \
  "SELECT id, feeType, latePaymentFeesType, latePaymentFees FROM fee_type WHERE id = 1"

# Check job execution logs
docker logs solid-api | grep "LateFeePaymentCalculatorScheduledJob"
```

**Solution:**
- Verify scheduled job is active in metadata
- Check fee type has late payment configuration
- Manually run scheduled job
- Increase job frequency if needed

#### 7. Token Validation Failed

**Issue:** Student gets "Invalid token" error

**Possible Causes:**
- Token expired (> 12 hours)
- Token not stored in Student record
- JWT_SECRET changed

**Diagnostic Steps:**
```bash
# Verify token in database
psql -U postgres -d school_fees -c \
  "SELECT studentLoginId, token FROM student WHERE studentLoginId = 'JOHND-A1B2C'"

# Check JWT secret
env | grep IAM_JWT_SECRET
```

**Solution:**
- Student should log in again to get new token
- Verify IAM_JWT_SECRET hasn't changed
- Clear browser cache and re-login

### Diagnostic Commands

**Check Student Record:**
```sql
SELECT
  id, studentName, studentLoginId,
  parentEmailAddress, otp, otpExpiresAt,
  LEFT(token, 20) as token_preview
FROM student
WHERE studentLoginId = 'JOHND-A1B2C';
```

**Check Payment Status:**
```sql
SELECT
  p.id, p.amount, p.paymentStatus,
  p.mSwipeIpgTransId, p.createdAt
FROM payment p
WHERE p.student_id = 123
ORDER BY p.createdAt DESC;
```

**Check Payment Collection Item Status:**
```sql
SELECT
  pci.id, ft.feeType, pci.amountToBePaid,
  pci.amountPaid, pci.amountPending,
  pci.lateAmountToBePaid, pci.totalAmountToBePaid,
  pci.status, pci.isOverdue, pci.overdueByDays
FROM payment_collection_item pci
JOIN fee_type ft ON pci.feeType_id = ft.id
WHERE pci.student_id = 123
ORDER BY pci.dueDate;
```

**Check Payment Details:**
```sql
SELECT
  pcid.id, pcid.amountPaid, pcid.paymentStatus,
  pcid.paymentDate, p.mSwipeIpgTransId
FROM payment_collection_item_detail pcid
JOIN payment p ON pcid.payment_id = p.id
WHERE pcid.paymentCollectionItem_id = 101
ORDER BY pcid.paymentDate DESC;
```

**Check Scheduled Job Status:**
```sql
SELECT * FROM scheduled_job
WHERE moduleUserKey = 'fees-portal';
```

**Check Email Logs:**
```bash
docker logs solid-api | grep "sendEmail" | tail -20
```

**Check Mswipe Integration:**
```bash
docker logs solid-api | grep "Mswipe" | tail -20
```

---

## FAQ

### General Questions

**Q: Can students make payments without OTP?**
A: No, OTP verification is mandatory for authentication. This ensures only authorized parents/students can make payments.

**Q: How long is the OTP valid?**
A: OTPs are valid for 5 minutes from generation. After expiration, students need to request a new OTP.

**Q: Can students use multiple devices?**
A: Yes, students can use any device. The JWT token is valid across devices as long as it hasn't expired (12 hours).

**Q: What happens if payment is made after due date?**
A: Late fees will be automatically calculated and added to the total amount based on the fee type's late payment configuration.

### Payment Questions

**Q: Can students make partial payments?**
A: Yes, if the fee type allows partial payments (`partPaymentAllowed = true`). Otherwise, the full amount must be paid.

**Q: What payment methods are supported?**
A: Mswipe gateway supports UPI, Credit/Debit cards, and Net Banking. The specific methods available depend on the institute's Mswipe configuration.

**Q: How long does payment processing take?**
A: Most payments are processed instantly. The webhook callback typically arrives within seconds of payment completion.

**Q: What if payment fails?**
A: If payment fails, the student will be redirected back to the portal with a failure message. The payment record will be marked as "Failed" and the student can retry.

**Q: Can students get refunds?**
A: Refunds must be initiated by the institute admin through the Mswipe merchant dashboard. The `isRefunded` flag will be updated accordingly.

### Technical Questions

**Q: Can the student portal run on a different domain?**
A: Yes, the student portal is a separate frontend application and can run on any domain. CORS must be configured on the backend to allow requests from the frontend domain.

**Q: How is payment security ensured?**
A: Payments are processed through PCI-compliant Mswipe gateway. No card data is stored on the backend. JWT tokens ensure only authenticated students can initiate payments.

**Q: What happens if webhook is missed?**
A: If the webhook is missed (e.g., backend down), the payment status won't update automatically. Admins can manually verify the payment status through Mswipe merchant dashboard and update records.

**Q: Can computed fields be triggered manually?**
A: Computed fields are triggered automatically on configured database operations. For manual recalculation, you can update the triggering entity (e.g., update PaymentCollectionItemDetail to trigger amount recalculation).

### Troubleshooting Questions

**Q: Student can't log in - what to check?**
A:
1. Verify student login ID is correct
2. Check parent email is correct in student record
3. Verify SMTP configuration for OTP delivery
4. Check spam folder for OTP email
5. Ensure OTP hasn't expired (5 minutes)

**Q: Payment shows as pending but was completed - what to do?**
A:
1. Check backend logs for webhook callback
2. Verify callback URL is accessible from Mswipe
3. Contact Mswipe to resend webhook
4. Manually verify payment in Mswipe dashboard
5. Update payment status manually if needed

**Q: Late fees not showing - what to check?**
A:
1. Verify fee type has late payment configuration
2. Check if scheduled job is active
3. Check job execution logs
4. Verify payment is past due date
5. Manually run late fee calculator job

---

## Summary

This documentation covers the complete **Making Payment** use case for the student portal, including:

### Key Components

1. **Custom Authentication**
   - OTP-based login (no traditional user accounts)
   - JWT token management
   - Secure email verification

2. **Payment Dashboard**
   - View pending fees with detailed breakdowns
   - See overdue items with late fees
   - Track payment history

3. **Payment Processing**
   - Integrated Mswipe payment gateway
   - Support for full and partial payments
   - Webhook-based status updates

4. **Automated Systems**
   - Computed fields for amount calculations
   - Scheduled late fee application
   - Automated payment reminders

5. **Complete API Integration**
   - RESTful endpoints for all operations
   - Secure Bearer token authentication
   - Comprehensive error handling

### Success Criteria

You've successfully implemented the student payment flow when:

- [ ] Students can authenticate using OTP
- [ ] Students can view all pending fees
- [ ] Payment gateway links generate successfully
- [ ] Payments process and update status correctly
- [ ] Payment history displays accurately
- [ ] Late fees calculate automatically for overdue payments
- [ ] Email notifications are sent at all key points
- [ ] Computed fields update payment amounts correctly
- [ ] Students can download payment reports

This use case enables a seamless, secure payment experience for students and parents while automating fee management for institute admins.

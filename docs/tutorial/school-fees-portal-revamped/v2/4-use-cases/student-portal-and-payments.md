---
sidebar_position: 3
---

# 3. Student Portal & Payments

This section details the student and parent-facing portal, covering everything from logging in to making payments and receiving notifications.

## Getting the Frontend Code

To build the student portal, we will use a separate frontend application built with Next.js. A starter repository is provided to give you the basic structure, UI components, and API service helpers.

:::info
**Action Required: Clone the Starter Repository**

[➡️ TODO: Insert Git repository link here](https://github.com/solidstarters/school-fees-portal-frontend-starter)

Clone this repository to your local machine.
:::

## Student/Parent Login Flow

The portal uses a secure, passwordless OTP (One-Time Password) login system.

### Login Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend API
    participant Mail/SMS Service

    User->>Frontend: Enters email/mobile and clicks 'Login'
    Frontend->>Backend API: POST /api/auth/request-otp (email)
    Backend API->>Backend API: Generate 4-digit OTP and expiry
    Backend API->>Backend API: Save OTP hash and expiry on Student record
    Backend API->>Mail/SMS Service: Send OTP to user's email/mobile
    Mail/SMS Service-->>User: Delivers OTP
    User->>Frontend: Enters the received OTP
    Frontend->>Backend API: POST /api/auth/verify-otp (email, otp)
    Backend API->>Backend API: 1. Find Student by email <br> 2. Verify OTP hash <br> 3. Check expiry
    alt OTP is valid
        Backend API->>Backend API: Generate JWT Session Token
        Backend API-->>Frontend: Return JWT Token and User data
        Frontend->>Frontend: Store JWT in localStorage
        Frontend->>User: Redirect to Dashboard
    else OTP is invalid
        Backend API-->>Frontend: Return 401 Unauthorized Error
        Frontend->>User: Show "Invalid OTP" message
    end

```

## The Student Dashboard

Once logged in, the parent is presented with a clear, concise dashboard showing:
-   **Student's Name and ID**
-   **Outstanding Fees:** A list of all fees that are `Pending` or `Partially Paid`, with amounts and due dates. Each item has a "Pay Now" button.
-   **Payment History:** A table showing all previous payments, their status (`Succeeded`, `Failed`), and dates.

## The Payment Flow

When a user clicks "Pay Now", it initiates a multi-step process involving the frontend, the SolidX backend, and the Stripe payment gateway.

### Payment Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant SolidX Backend
    participant Stripe API

    User->>Frontend: Clicks "Pay Now" for one or more fee items
    Frontend->>SolidX Backend: POST /api/payment/initiate (itemIds, amounts)
    SolidX Backend->>SolidX Backend: 1. Create 'Payment' record (status: Pending) <br> 2. Create 'PaymentCollectionItemDetail' records
    SolidX Backend->>Stripe API: Create Stripe Checkout Session (with amounts, success/cancel URLs, metadata)
    Stripe API-->>SolidX Backend: Return Checkout Session with unique payment URL
    SolidX Backend-->>Frontend: Return the unique payment URL from Stripe
    Frontend->>User: Redirect browser to Stripe's payment page
    User->>Stripe API: Enters card details and completes payment
    Stripe API-->>User: Shows success/failure message and redirects back to Frontend
    
    %% --- The Webhook (Asynchronous) ---
    Stripe API-->>SolidX Backend: POST /api/payment/webhook (payment success/failure event)
    SolidX Backend->>SolidX Backend: **Verify Stripe Signature**
    alt Signature is valid
        SolidX Backend->>SolidX Backend: 1. Update 'Payment' record status <br> 2. Update 'PaymentCollectionItemDetail' status
        SolidX Backend->>SolidX Backend: Trigger 'amountPaid' computed field on 'PaymentCollectionItem'
        SolidX Backend->>SolidX Backend: Send "Payment Confirmation" email
        SolidX Backend-->>Stripe API: Return 200 OK
    else Signature is invalid
        SolidX Backend-->>Stripe API: Return 400 Bad Request
    end
```

### Consuming Webhooks Securely

A critical step in payment processing is handling the webhook from the payment gateway. You **must** verify that the webhook request actually came from Stripe.

**Example: Stripe Webhook Verification in a NestJS Controller**
```typescript
// school-fees-portal/solid-api/src/fees-portal/controllers/payment.controller.ts
import { Headers, Controller, Post, Req, RawBodyRequest } from '@nestjs/common';
import Stripe from 'stripe';

@Controller('payment')
export class PaymentController {
  private readonly stripe: Stripe;
  private readonly webhookSecret: string = process.env.STRIPE_WEBHOOK_SECRET;

  // ... constructor
  
  @Post('webhook')
  async handleStripeWebhook(@Headers('stripe-signature') signature: string, @Req() req: RawBodyRequest<Request>) {
    let event: Stripe.Event;

    try {
      // Use the raw body to construct the event
      event = this.stripe.webhooks.constructEvent(
        req.rawBody,
        signature,
        this.webhookSecret,
      );
    } catch (err) {
      console.error(`Webhook signature verification failed.`);
      // On error, return a 400
      return { error: `Webhook Error: ${err.message}` };
    }

    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object;
        // Payment was successful, find the Payment record via metadata
        // and update its status in your database.
        await this.paymentService.processSuccessfulPayment(session);
        break;
      // ... handle other event types
      default:
        console.log(`Unhandled event type ${event.type}`);
    }

    // Return a 200 to acknowledge receipt of the event
    return { received: true };
  }
}
```

## Automated Processes

The student-facing experience is supported by automated backend processes built on SolidX's core features.

-   **Late Fee Calculation:** This is handled by a **Scheduled Job** (e.g., a `Cron` job) that runs nightly. The job queries for `PaymentCollectionItem` records that are past their `dueDate` and not `Fully Paid`. It then applies late fees according to the logic defined in the `FeeType`.
-   **Email Notifications:** All emails (OTP, payment confirmation, late fee reminders) are sent via the core `EmailService`. This service uses predefined templates, allowing you to manage your email content easily without changing the application code.

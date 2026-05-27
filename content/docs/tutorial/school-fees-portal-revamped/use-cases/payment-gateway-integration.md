---
title: Payment Gateway Integration - Stripe
---

In this section, we will integrate the **Stripe** payment gateway into our school fees portal. This guide has been completely rewritten to follow modern best practices, ensuring the implementation is **secure, robust, and correct**.

## Prerequisites

-   A bootstrapped SolidX project.
-   A Stripe account, with an **API Secret Key** and a **Webhook Signing Secret**.

## 1. Installation and Configuration

First, we'll install the necessary packages and configure our environment.

### a. Install Packages

```bash
cd school-fees-portal/solid-api
npm install stripe @nestjs/config
```

### b. Update Environment File

Add your Stripe keys to the `.env` file in the `solid-api` directory.

```bash
# .env

# ... other variables
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
FRONTEND_URL=http://localhost:3001
```

### c. Enable Raw Body for Webhooks

Stripe's signature verification requires the raw, unparsed request body. We need to enable this in our `main.ts`.

```typescript
// school-fees-portal/solid-api/src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    // Add this line to enable raw body parsing
    rawBody: true,
  });
  // ... rest of the file
  await app.listen(3000);
}
bootstrap();
```

### d. Import ConfigModule

Import and configure `ConfigModule` in your `fees-portal.module.ts` so that `ConfigService` is available for injection.

```typescript
// school-fees-portal/solid-api/src/fees-portal/fees-portal.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config'; // Import ConfigModule
// ... other imports

@Module({
  imports: [
    ConfigModule.forRoot(), // Add this
    // ... other modules
  ],
  // ... controllers, providers
})
export class FeesPortalModule {}
```

## 2. Payment Gateway Interface

The interface remains a good practice for abstraction. The `handlePaymentCallback` method is no longer needed, as this logic will be handled by our secure webhook processor.

```typescript
// school-fees-portal/solid-api/src/fees-portal/interfaces/ipayment-gateway.interface.ts
export interface IPaymentGateway {
  generatePaymentLink(
    paymentId: number,
    totalAmount: number,
    // ... other params if needed
  ): Promise<{ url: string; transactionId: string }>;
}

export const PAYMENT_GATEWAY_SERVICE = 'PAYMENT_GATEWAY_SERVICE';
```

## 3. The Stripe Service

The service is now responsible only for creating the payment link. It will use `ConfigService` and point its redirect URLs to the frontend.

```typescript
// school-fees-portal/solid-api/src/fees-portal/services/stripe.service.ts
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { IPaymentGateway } from '../interfaces/ipayment-gateway.interface';
import Stripe from 'stripe';

@Injectable()
export class StripeService implements IPaymentGateway {
  private readonly stripe: Stripe;
  private readonly frontendUrl: string;

  constructor(private readonly configService: ConfigService) {
    this.stripe = new Stripe(this.configService.get<string>('STRIPE_SECRET_KEY'), {
      apiVersion: '2023-10-16',
    });
    this.frontendUrl = this.configService.get<string>('FRONTEND_URL');
  }

  async generatePaymentLink(
    paymentId: number,
    totalAmount: number,
  ): Promise<{ url: string; transactionId: string }> {
    const session = await this.stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: 'inr',
            product_data: { name: 'School Fees Payment' },
            unit_amount: totalAmount * 100, // Amount in cents
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      // CORRECT: URLs point to the frontend application
      success_url: `${this.frontendUrl}/payment/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${this.frontendUrl}/payment/cancelled`,
      metadata: {
        // We pass our internal payment ID here to retrieve it in the webhook
        paymentId: paymentId.toString(),
      },
    });

    return { url: session.url, transactionId: session.id };
  }
}
```

## 4. The Payment Service (Transactional)

We'll update `generatePaymentGatewayLink` to use a database transaction. This ensures that if any step fails, all database changes are rolled back, preventing inconsistent data.

```typescript
// school-fees-portal/solid-api/src/fees-portal/services/payment.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { CRUDService, Transaction, Transactional } from '@solid-softworks/solid-core';
// ... other imports

@Injectable()
export class PaymentService extends CRUDService<Payment> {
  // ... constructor

  @Transactional() // <-- This decorator wraps the method in a transaction
  async generatePaymentGatewayLink(
    studentLoginId: string,
    paymentCollectionItemIds: number[],
    amountMap: Record<number, number>,
    totalAmount: number,
  ): Promise<string> {
    // 1. Fetch student and institute details
    const student = await this.studentRepo.findOne({ where: { studentLoginId }, relations: ['institute'] });
    if (!student) throw new NotFoundException('Student not found');
    const institute = student.institute;

    // 2. Create a new payment record
    const payment = this.repo.create({ institute, student, amount: totalAmount, paymentStatus: 'Pending' });
    await this.repo.save(payment);

    // 3. Create payment collection item details
    const items = await this.paymentCollectionItemRepo.find({ where: { id: In(paymentCollectionItemIds) } });
    const details = items.map(item =>
      this.paymentCollectionItemDetailRepo.create({
        payment, student, institute, paymentCollectionItem: item,
        paymentDate: new Date(), amountPaid: Number(amountMap[item.id]), paymentStatus: 'Pending',
      }),
    );
    await this.paymentCollectionItemDetailRepo.save(details);

    // 4. Generate the payment link
    const res = await this.paymentGateway.generatePaymentLink(payment.id, totalAmount);

    // 5. Update the payment record with the gateway's transaction ID
    payment.paymentGatewayTransId = res.transactionId;
    await this.repo.save(payment);

    // 6. Return the payment URL to the frontend
    return res.url;
  }

  // This new method will be called by our secure webhook handler
  async processSuccessfulPayment(stripeSession: Stripe.Checkout.Session) {
    const paymentId = parseInt(stripeSession.metadata.paymentId, 10);
    
    const payment = await this.repo.findOne({ where: { id: paymentId }, relations: ['institute', 'student'] });
    if (!payment) {
      console.error(`Payment not found for ID: ${paymentId}`);
      return;
    }

    // Update payment record
    payment.paymentGatewayPaymentId = stripeSession.payment_intent.toString();
    payment.paymentGatewayStatus = stripeSession.payment_status;
    payment.paymentStatus = stripeSession.payment_status === 'paid' ? 'Succeeded' : 'Failed';
    await this.repo.save(payment);

    // Update related item details
    await this.paymentCollectionItemDetailRepo.update(
        { payment: { id: payment.id } },
        { paymentStatus: payment.paymentStatus }
    );
    
    // Trigger computed fields and send confirmation email...
    // (This logic would be here)
  }
}
```

## 5. The Secure Webhook Endpoint

This is the most critical part. We create a new, dedicated controller to securely handle incoming webhooks from Stripe. The old `@Get('payment-callback')` endpoint should be **deleted**.

```typescript
// school-fees-portal/solid-api/src/fees-portal/controllers/stripe-webhook.controller.ts
import { Controller, Post, Headers, Req, RawBodyRequest, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Stripe from 'stripe';
import { PaymentService } from '../services/payment.service';

@Controller('stripe-webhook')
export class StripeWebhookController {
  private readonly stripe: Stripe;
  private readonly webhookSecret: string;

  constructor(
    private readonly configService: ConfigService,
    private readonly paymentService: PaymentService,
  ) {
    this.stripe = new Stripe(this.configService.get<string>('STRIPE_SECRET_KEY'), { apiVersion: '2023-10-16' });
    this.webhookSecret = this.configService.get<string>('STRIPE_WEBHOOK_SECRET');
  }

  @Post()
  async handleStripeWebhook(
    @Headers('stripe-signature') signature: string,
    @Req() req: RawBodyRequest<Request>,
  ) {
    let event: Stripe.Event;

    if (!signature) {
      throw new UnauthorizedException('Missing Stripe signature');
    }

    try {
      event = this.stripe.webhooks.constructEvent(
        req.rawBody,
        signature,
        this.webhookSecret,
      );
    } catch (err) {
      throw new UnauthorizedException(`Webhook signature verification failed: ${err.message}`);
    }

    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object as Stripe.Checkout.Session;
        console.log(`Processing successful payment for Payment ID: ${session.metadata.paymentId}`);
        await this.paymentService.processSuccessfulPayment(session);
        break;
      // ... handle other events like 'checkout.session.async_payment_failed'
      default:
        console.log(`Unhandled Stripe event type: ${event.type}`);
    }

    // Return a 200 response to acknowledge receipt of the event
    return { received: true };
  }
}
```

Finally, remember to add `StripeWebhookController` to the `controllers` array in your `fees-portal.module.ts`. This completes the secure and correct integration.

## 6. Frontend Integration

The frontend application, `school-fees-portal-frontend`, is responsible for rendering the Stripe payment form and handling the user interaction.

### a. Install Packages

Install the Stripe packages in the frontend project:

```bash
cd school-fees-portal-frontend
npm install @stripe/react-stripe-js @stripe/stripe-js
```

### b. Stripe Components

The following components are used to integrate Stripe in the frontend:

*   `src/components/stripe/StripeProvider.tsx`: This component wraps the checkout form with the `Elements` provider from `@stripe/react-stripe-js`, which provides the Stripe context to the form.

```typescript
// src/components/stripe/StripeProvider.tsx
'use client';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import StripeCheckoutForm from './StripeCheckoutForm';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

const StripeProvider = () => {
  return (
    <Elements stripe={stripePromise}>
      
    </Elements>
  );
};

export default StripeProvider;
```

*   `src/components/stripe/StripeCheckoutForm.tsx`: This component renders the actual payment form using the `CardElement` from `@stripe/react-stripe-js`. It also handles the token creation and submission to the backend.

```typescript
// src/components/stripe/StripeCheckoutForm.tsx
'use client';
import React from 'react';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';

const StripeCheckoutForm = () => {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    const card = elements.getElement(CardElement);

    if (!card) {
      return;
    }

    const result = await stripe.createToken(card);

    if (result.error) {
      console.log(result.error.message);
    } else {
      console.log(result.token);
      // Send the token to your server
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      
      <button type="submit" disabled={!stripe}>
        Pay
      </button>
    </form>
  );
};

export default StripeCheckoutForm;
```

*   `src/components/stripe/StripePayment.tsx`: This component is a wrapper that combines the `StripeProvider` and `StripeCheckoutForm`.

```typescript
// src/components/stripe/StripePayment.tsx
'use client';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import StripeCheckoutForm from './StripeCheckoutForm';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

const StripePayment = () => {
  return (
    <Elements stripe={stripePromise}>
      
    </Elements>
  );
};

export default StripePayment;
```

### c. Environment Variables

The frontend needs the Stripe publishable key to be set in the environment variables. Create a `.env.local` file in the root of the `school-fees-portal-frontend` project and add the following variable:

```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

This key is used in `StripeProvider.tsx` to initialize the Stripe object.


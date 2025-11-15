---
sidebar_position: 5
---

# 5. Payment Gateway Integration with Stripe

In this section, we will integrate the Stripe payment gateway into our school fees portal. This will allow us to process online payments from students.

## Prerequisites

Before we begin, make sure you have the following:

*   A bootstrapped SolidX project for the school fees portal.
*   A Stripe account and API keys (secret key).

## Steps

1.  **Create a Payment Gateway Interface:** Define a contract for our payment gateway service.
2.  **Configure Payment Gateway Credentials:** We will store the Stripe API keys in the environment file.
3.  **Create a Stripe Service:** This service will handle the communication with the Stripe API.
4.  **Initiate Payment:** We will add a "Pay Now" button to the student's fee collection page.
5.  **Handle Payment Callback:** Stripe will notify our application about the payment status through a callback URL.
6.  **Update Payment Status:** We will update the payment status in our database based on the callback.

## 1. Create a Payment Gateway Interface

First, let's define an interface for our payment gateway. This will allow us to easily switch to a different payment gateway provider in the future if needed.

Create a new file `ipayment-gateway.interface.ts` in `school-fees-portal/solid-api/src/fees-portal/interfaces/`:

```typescript
export interface IPaymentGateway {
  generatePaymentLink(
    paymentId: number,
    totalAmount: number,
    custCode: string,
    userName: string,
    password,
    custUserId: string,
    options: any,
  ): Promise<any>;

  handlePaymentCallback(data: any): Promise<any>;
}

export const PAYMENT_GATEWAY_SERVICE = 'PAYMENT_GATEWAY_SERVICE';
```

## 2. Configure Payment Gateway Credentials

Store your Stripe secret key in the `.env` file in the `solid-api` directory:

```
STRIPE_SECRET_KEY=your_stripe_secret_key
```

## 3. Create a Stripe Service

Now, let's create a service that implements the `IPaymentGateway` interface. This service will contain the logic specific to Stripe.

First, install the Stripe Node.js library:

```bash
cd school-fees-portal/solid-api
npm install stripe
```

Create a new file `stripe.service.ts` in `school-fees-portal/solid-api/src/fees-portal/services/`:

```typescript
import { Injectable } from '@nestjs/common';
import { IPaymentGateway } from '../interfaces/ipayment-gateway.interface';
import Stripe from 'stripe';

@Injectable()
export class StripeService implements IPaymentGateway {
  private readonly stripe: Stripe;

  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
      apiVersion: '2023-10-16',
    });
  }

  async generatePaymentLink(
    paymentId: number,
    totalAmount: number,
    custCode: string, // Not used by Stripe
    userName: string, // Not used by Stripe
    password, // Not used by Stripe
    custUserId: string, // Not used by Stripe
    options: any,
  ): Promise<any> {
    const session = await this.stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: 'inr',
            product_data: {
              name: 'Fees',
            },
            unit_amount: totalAmount * 100,
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${process.env.BASE_URL}/api/payment/payment-callback?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.BASE_URL}/payment-failed`,
      metadata: {
        paymentId,
      },
    });

    return { url: session.url, transactionId: session.id };
  }

  async handlePaymentCallback(data: any): Promise<any> {
    const session = await this.stripe.checkout.sessions.retrieve(data.query.session_id);
    return {
        paymentGatewayInvoiceId: session.metadata.paymentId,
        paymentGatewayStatus: session.payment_status,
        paymentGatewayTransId: session.id,
    };
  }
}
```

Now, we need to provide this service in our `fees-portal.module.ts`:

```typescript
// school-fees-portal/solid-api/src/fees-portal/fees-portal.module.ts
import { Module } from '@nestjs/common';
// ... other imports
import { StripeService } from './services/stripe.service';
import { PAYMENT_GATEWAY_SERVICE } from './interfaces/ipayment-gateway.interface';

@Module({
  imports: [
    // ... other modules
  ],
  controllers: [
    // ... other controllers
  ],
  providers: [
    // ... other providers
    {
      provide: PAYMENT_GATEWAY_SERVICE,
      useClass: StripeService,
    },
  ],
})
export class FeesPortalModule {}
```

## 4. Initiate Payment

We will now update our `PaymentService` to use the `IPaymentGateway` interface to generate the payment link.

Update the `generatePaymentGatewayLink` method in `school-fees-portal/solid-api/src/fees-portal/services/payment.service.ts`:

```typescript
// school-fees-portal/solid-api/src/fees-portal/services/payment.service.ts

// ... imports

@Injectable()
export class PaymentService extends CRUDService<Payment> {
  // ... constructor and other methods

  async generatePaymentGatewayLink(
    studentLoginId: string,
    paymentCollectionItemIds: number[],
    amountMap: Record<number, number>,
    totalAmount: number,
  ) {
    // 1. Fetch student and institute details
    const student = await this.studentRepo.findOne({
      where: { studentLoginId },
      relations: ['institute'],
    });
    if (!student) throw new Error('Student not found');
    const institute = student.institute;

    // 2. Create a new payment record
    const payment = this.repo.create({
      institute,
      student,
      amount: totalAmount,
      paymentStatus: 'Pending',
    });
    await this.repo.save(payment);

    // 3. Create payment collection item details
    const items = await this.paymentCollectionItemRepo.find({
      where: { id: In(paymentCollectionItemIds) },
    });
    const details = items.map((item) =>
      this.paymentCollectionItemDetailRepo.create({
        payment,
        student,
        institute,
        paymentCollectionItem: item,
        paymentDate: new Date(),
        amountPaid: Number(amountMap[item.id]),
        paymentStatus: 'Pending',
      }),
    );
    await this.paymentCollectionItemDetailRepo.save(details);

    // 4. Generate the payment link using the payment gateway service
    const res = await this.paymentGateway.generatePaymentLink(
      payment.id,
      totalAmount,
      institute.paymentGatewayMerchantId,
      institute.paymentGatewayAccessKey,
      institute.paymentGatewayAccessSecret,
      institute.custUserId,
      {
        phone: student.parentMobileNumber,
        email: student.parentEmailAddress,
      },
    );

    // 5. Update the payment record with the transaction ID
    payment.paymentGatewayTransId = res.transactionId;
    await this.repo.save(payment);

    // 6. Return the payment link
    return res.url;
  }

  // ... other methods
}
```

## 5. Handle Payment Callback

Next, we need to create an endpoint to handle the callback from Stripe.

Add the following method to `school-fees-portal/solid-api/src/fees-portal/controllers/payment.controller.ts`:

```typescript
// school-fees-portal/solid-api/src/fees-portal/controllers/payment.controller.ts

// ... imports

@Controller('payment')
export class PaymentController {
  constructor(private readonly paymentService: PaymentService) {}

  // ... other methods

  @Get('payment-callback')
  async handlePaymentCallback(@Req() req: Request) {
    const data = {
      body: req.body,
      query: req.query,
      method: req.method,
    };
    return this.paymentService.handlePaymentCallback(data);
  }
}
```

Now, update the `handlePaymentCallback` method in `payment.service.ts`:

```typescript
// school-fees-portal/solid-api/src/fees-portal/services/payment.service.ts

// ... imports

@Injectable()
export class PaymentService extends CRUDService<Payment> {
  // ... constructor and other methods

  async handlePaymentCallback(data: any) {
    const callbackData = await this.paymentGateway.handlePaymentCallback(data);
    
    const payment = await this.repo.findOne({
        where: { id: callbackData.paymentGatewayInvoiceId },
        relations: ['institute', 'student'],
    });

    if (!payment) {
      throw new NotFoundException('Payment not found');
    }

    // Update payment record
    payment.paymentGatewayTransId = callbackData.paymentGatewayTransId;
    payment.paymentGatewayStatus = callbackData.paymentGatewayStatus;
    payment.paymentStatus = callbackData.paymentGatewayStatus === 'paid' ? 'Succeeded' : 'Failed';
    await this.repo.save(payment);

    // Update payment collection item details
    const itemDetails = await this.paymentCollectionItemDetailRepo.find({
      where: { payment: { id: payment.id } },
    });

    for (const detail of itemDetails) {
      detail.paymentStatus = payment.paymentStatus;
      await this.paymentCollectionItemDetailRepo.save(detail);
    }

    // Send payment confirmation email
    await this.sendPaymentSuccessMail(payment.institute.id, payment, itemDetails, payment.paymentStatus);

    return {
      success: true,
      message: 'Payment status updated successfully',
    };
  }

  // ... other methods
}
```

## 6. Update Payment Status

The `handlePaymentCallback` method now handles updating the payment status in the `payment` and `paymentCollectionItemDetail` models. It also triggers an email to the parent with the payment confirmation.

This completes our Stripe payment gateway integration.

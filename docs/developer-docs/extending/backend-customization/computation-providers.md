---
title: Computation Providers
description: Learn how to extend the backend with custom computation providers.
sidebar_position: 5
keywords: [backend, computation providers, customization]
solidx_concerns: [add_computed_field_provider]
---

import { NoteBoxs } from '@site/src/common/NoteBoxs';
import { IoIosArrowForward } from "react-icons/io";
import { MdSettings, MdBuildCircle } from "react-icons/md";

# Computation Providers

In **SolidX**, computed fields are fields whose values are automatically derived from other data — for example, `totalPrice`, `fullName`, or `age`. They eliminate the need to store redundant values and ensure consistency across your models.

Computed fields are powered by **computation providers**, which encapsulate the business logic required to calculate and assign values to these fields.

Providers are triggered automatically when relevant data changes, ensuring that the computed field always reflects the correct value without manual intervention.

## How to Configure a Computed Field

<h3 className="card-headear-wrapper">
  <MdSettings size={24} />
  
### Sample Metadata Configuration
</h3>

Below is an example configuration for a computed field named `amountPaid` in the `paymentCollectionItemDetail` model. The field computes the total amount paid based on related payment records.

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Example: Configuration for <code>amountPaid</code> computed field
  </summary>

```json
{
  "name": "paymentCollectionItemDetail",
  "displayName": "Payment Collection Item Detail",
  "fields": [
    {
      "name": "amountPaid",
      "displayName": "Amount Paid",
      "type": "computed",
      "ormType": "varchar",
      "computedFieldTriggerConfig": [
        {
          "modelName": "paymentCollectionItemDetail",
          "moduleName": "fees-portal",
          "operations": [
            "after-update",
            "after-insert"
          ]
        }
      ],
      "computedFieldValueProvider": "PaymentCollectionItemAmountProvider",
      "computedFieldValueProviderCtxt": "{}"
    }
  ]
}
```

</details>

- `computedFieldValueProvider` specifies the **provider class** responsible for the computation logic.  
- `computedFieldTriggerConfig` defines the **entities and operations** that trigger the computation.

Supported operations include:
- `before-update`
- `before-insert`
- `before-remove`
- `after-update`
- `after-insert`
- `after-remove`

🔸 **Before operations** trigger `preComputeValue()` of `IEntityPreComputeFieldProvider`.  
🔸 **After operations** trigger `postComputeAndSaveValue()` of `IEntityPostComputeFieldProvider`.  

> **Note:** For before operations, `modelName` must be the same as the model with the computed field. For after operations, it can be any model, related or unrelated.

You can:
- Access the triggering entity and metadata
- Set the computed value (auto-saved in `preComputeValue`)
- Execute logic and persist data in `postComputeAndSaveValue`

### Sample Provider Implementation

Here is a sample implementation of the `PaymentCollectionItemAmountProvider`:

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Example: <code>PaymentCollectionItemAmountProvider</code> Implementation
  </summary>

```ts
import { Injectable } from '@nestjs/common';
import { InjectEntityManager } from '@nestjs/typeorm';
import {
  ComputedFieldMetadata,
  ComputedFieldProvider,
  IEntityPostComputeFieldProvider
} from '@solidstarters/solid-core';
import { EntityManager } from 'typeorm';
import { PaymentCollectionItemDetail } from '../entities/payment-collection-item-detail.entity';
import { PaymentCollectionItem } from '../entities/payment-collection-item.entity';

@ComputedFieldProvider()
@Injectable()
export class PaymentCollectionItemAmountProvider implements IEntityPostComputeFieldProvider<PaymentCollectionItemDetail, any> {
  constructor(
    @InjectEntityManager()
    private readonly entityManager: EntityManager,
  ) {}

  async postComputeAndSaveValue(
    triggerEntity: PaymentCollectionItemDetail,
    computedFieldMetadata: ComputedFieldMetadata<any>,
  ): Promise<void> {
    if (!triggerEntity?.paymentCollectionItem?.id) {
      console.error('Payment Collection Item Id Missing');
    }

    const { amountPaid, totalAmountToBePaid, amountPending, status } =
      await this.getPaymentCollectionItemAmounts(triggerEntity?.paymentCollectionItem?.id);

    await this.entityManager.update(
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

  name(): string {
    return 'PaymentCollectionItemAmountProvider';
  }

  help(): string {
    return 'Provider used to compute payment collection item amounts based on related details.';
  }

  private async getPaymentCollectionItemAmounts(itemId: number): Promise<{
    amountPaid: number;
    totalAmountToBePaid: number;
    amountPending: number;
    status: string;
  }> {
    const details = await this.entityManager.find(PaymentCollectionItemDetail, {
      where: { paymentCollectionItem: { id: itemId }, paymentStatus: 'Succeeded' },
      relations: ['paymentCollectionItem'],
    });

    const amountPaid = details.reduce(
      (sum, detail) => sum + Number(detail.amountPaid || 0),
      0,
    );

    const paymentCollectionItem = details[0]?.paymentCollectionItem;

    const totalAmountToBePaid =
      Number(paymentCollectionItem?.amountToBePaid || 0) +
      Number(paymentCollectionItem?.lateAmountToBePaid || 0);

    const amountPending = totalAmountToBePaid - amountPaid;
    const status = amountPending > 0 ? 'Partially Paid' : 'Fully Paid';

    return { amountPaid, totalAmountToBePaid, amountPending, status };
  }
}
```
</details>

## Computation Provider Interfaces

To implement a custom computation provider, you need to implement one or both of the following interfaces:

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Interfaces to Implement
  </summary>

```ts
export interface IEntityPreComputeFieldProvider<TTriggerEntity, TContext, TValue=void> extends IEntityComputedFieldProvider {
  preComputeValue(triggerEntity: TTriggerEntity, computedFieldMetadata: ComputedFieldMetadata<TContext>): Promise<TValue>;
}

export interface IEntityPostComputeFieldProvider<TTriggerEntity, TContext> extends IEntityComputedFieldProvider {
  postComputeAndSaveValue(triggerEntity: TTriggerEntity, computedFieldMetadata: ComputedFieldMetadata<TContext>): Promise<void>;
}

export interface IEntityComputedFieldProvider {
  help(): string;
  name(): string;
}
```
</details>

## How It Works

<h3 className="card-headear-wrapper">
  <MdBuildCircle size={20} />
  
### Core Mechanism
</h3>

1. `ComputedEntityFieldSubscriber` listens to `insert`, `update`, and `delete` events across all entities.  
2. For **before** operations:  
   - `preComputeValue()` is called **synchronously**  
   - Value is set directly on the entity and auto-saved  
3. For **after** operations:  
   - `postComputeAndSaveValue()` is called **asynchronously** via [Background Jobs](../background-jobs/index.md)  
   - Final saving happens via `ComputedFieldEvaluationSubscriber`  

<NoteBoxs>
Computed field configurations are loaded from the database and cached in the Solid Registry at application startup. Any changes require a server restart to take effect.
</NoteBoxs>

## Related Recipes (TODO)

- [Pre-computed fields](../pre-computed-fields/index.md)  
- [Post-computed fields](../post-computed-fields/index.md)  
- [Multiple Computed Fields](../multiple-computed-fields/index.md)  

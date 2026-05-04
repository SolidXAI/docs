---
title: Computed Fields
description: Learn how to extend the backend with custom computation providers.
summary: Explains SolidX computed fields powered by computation providers for automatic value derivation (e.g., totals, full names, age). Covers metadata configuration including `computedFieldTriggerConfig` for specifying triggers (before/after insert/update/remove operations), `computedFieldValueProvider` class implementation, `IEntityPreComputeFieldProvider` and `IEntityPostComputeFieldProvider` interfaces, provider registration, and examples like `PaymentCollectionItemAmountProvider` for calculating amounts based on related records.
sidebar_position: 5
keywords: [backend, computation providers, customization]
solidx_concerns: [backend.custom_computed_fields, add_computed_field_provider, create_model_with_fields, add_field_to_a_model]
---

import { NoteBoxs } from '@site/src/common/NoteBoxs';
import { TipBox } from '@site/src/common/TipBox';
import { IoIosArrowForward } from "react-icons/io";

# Computation Providers

## Overview

In SolidX, a **computed field** is a field whose value is always derived from other data — never set manually. Common examples include `totalPrice` (summed from line items), `fullName` (concatenated from first and last name), or `amountPaid` (aggregated from child payment records).

A **computation provider** is the TypeScript class that implements the derivation logic. You register it once, and SolidX calls it automatically whenever the relevant data changes — ensuring computed values stay consistent without any manual intervention.

## Mental Model

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    Think of a computed field as a spreadsheet formula applied to a database record. You define the formula once (in the provider), declare which events should re-evaluate it (in the trigger config), and the platform handles execution automatically.
  </p>
  <ul>
    <li>The <strong>computed field</strong> in metadata is the contract — it declares <em>what</em> to compute and <em>when</em>.</li>
    <li>The <strong>computation provider</strong> is the class that contains the logic — it receives the triggering entity and computes the new value.</li>
    <li><strong>Before operations</strong> run synchronously in the same transaction and are ideal when the value depends only on the entity itself.</li>
    <li><strong>After operations</strong> run asynchronously after the save and are ideal when the value depends on related records or requires cross-entity writes.</li>
  </ul>
  <p>
    So the intuition is: <strong>declare what triggers recomputation and write the logic once — SolidX handles when and how it runs.</strong>
  </p>
</div>

### Before vs. After

The trigger timing determines which interface your provider implements and how the value gets saved:

| Timing | Operations | Method called | How it runs | When to use |
|---|---|---|---|---|
| **Before** | `before-insert`, `before-update`, `before-delete` | `preComputeValue()` | Synchronously, in the same transaction | Value depends only on the triggering entity |
| **After** | `after-insert`, `after-update`, `after-delete` | `postComputeAndSaveValue()` | Asynchronously, via a [background job](./background-jobs) | Value depends on related records or requires additional writes |

> For `before-*` triggers, `modelName` in the trigger config must match the model that owns the computed field.  
> For `after-*` triggers, `modelName` can be any model — related or otherwise.

---

## Configuration

### Step 1 — Define the field in metadata

Add the field to your model's metadata with `"type": "computed"` and specify:
- `computedFieldValueProvider` — the name of the provider class to invoke
- `computedFieldTriggerConfig` — which entity events trigger the computation
- `computedFieldValueProviderCtxt` — a JSON string passed as context to the provider

**Example scenario:** `paymentCollectionItemDetail` records represent individual payment transactions. When a detail is inserted or updated (i.e., a payment comes in), the parent `paymentCollectionItem` needs its aggregate totals recalculated — `amountPaid`, `amountPending`, `totalAmountToBePaid`, and `status`. Since this involves writing to a related parent entity, `after-*` operations are the right choice here.

<details open>
  <summary className="card-title">
    Example: <code>amountPaid</code> computed field on <code>paymentCollectionItemDetail</code>
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
          "operations": ["after-update", "after-insert"]
        }
      ],
      "computedFieldValueProvider": "PaymentCollectionItemAmountProvider",
      "computedFieldValueProviderCtxt": "{}"
    }
  ]
}
```

</details>

<NoteBoxs>
Computed field configurations are loaded from the database and cached in the Solid Registry at startup. Any changes require a server restart to take effect.
</NoteBoxs>

---

### Step 2 — Implement the provider

Implement `IEntityPreComputeFieldProvider` for before operations, or `IEntityPostComputeFieldProvider` for after operations. Decorate the class with `@ComputedFieldProvider()`.

**In this example**, `PaymentCollectionItemAmountProvider` implements `IEntityPostComputeFieldProvider` because it needs to query all related detail records and write aggregated totals back to the parent — work that can only happen after the triggering detail has been saved.

<details open>
  <summary className="card-title">
    Example: <code>PaymentCollectionItemAmountProvider</code>
  </summary>

```ts
import { Injectable } from '@nestjs/common';
import { InjectEntityManager } from '@nestjs/typeorm';
import {
  ComputedFieldMetadata,
  ComputedFieldProvider,
  IEntityPostComputeFieldProvider
} from '@solidxai/core';
import { EntityManager } from 'typeorm';
import { PaymentCollectionItemDetail } from '../entities/payment-collection-item-detail.entity';
import { PaymentCollectionItem } from '../entities/payment-collection-item.entity';

@ComputedFieldProvider()
@Injectable()
export class PaymentCollectionItemAmountProvider
  implements IEntityPostComputeFieldProvider<PaymentCollectionItemDetail, any> {

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
    return 'Computes payment collection item amounts based on related details.';
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

---

### Step 3 — Register the provider

Register the provider as a NestJS provider in the module it belongs to.

```ts
// fees-portal.module.ts
@Module({
  providers: [PaymentCollectionItemAmountProvider],
})
```

---

## Provider Interfaces

SolidX provides two interfaces for computation providers. The key difference is in **who performs the save** and **when the logic runs**.

### `IEntityPreComputeFieldProvider` — before operations

```ts
export interface IEntityPreComputeFieldProvider<TTriggerEntity, TContext, TValue = void>
  extends IEntityComputedFieldProvider {
  preComputeValue(
    triggerEntity: TTriggerEntity,
    computedFieldMetadata: ComputedFieldMetadata<TContext>
  ): Promise<TValue>;
}
```

- Runs **synchronously** before the entity is saved, inside the same database transaction.
- Your implementation sets the computed value **directly on `triggerEntity`** (e.g., `triggerEntity.fullName = ...`). Because the entity is saved immediately after, those mutations are persisted automatically — no `entityManager` call needed.
- Use this when the computation depends only on the **triggering entity's own fields**.
- The `modelName` in `computedFieldTriggerConfig` **must** be the same model that owns the computed field.

### `IEntityPostComputeFieldProvider` — after operations

```ts
export interface IEntityPostComputeFieldProvider<TTriggerEntity, TContext>
  extends IEntityComputedFieldProvider {
  postComputeAndSaveValue(
    triggerEntity: TTriggerEntity,
    computedFieldMetadata: ComputedFieldMetadata<TContext>
  ): Promise<void>;
}
```

- Runs **asynchronously** after the entity is saved, via a [background job](./background-jobs).
- Returns `void` — **you are responsible for all persistence**. The platform does not set or save any field value on your behalf.
- Use this when the computation needs to **query related records**, or when the result must be **written to a different entity** (like rolling up child totals to a parent).
- The `modelName` in `computedFieldTriggerConfig` can be **any model** — it does not need to be the model that owns the computed field.

### Shared base interface

Both interfaces extend `IEntityComputedFieldProvider`, which requires two methods:

```ts
export interface IEntityComputedFieldProvider {
  name(): string;  // Must exactly match computedFieldValueProvider in the field metadata
  help(): string;  // Human-readable description of the provider and expected context shape
}
```

---

## How It Works

1. `ComputedEntityFieldSubscriber` listens to `insert`, `update`, and `delete` events across all entities.
2. On a **before** event — `preComputeValue()` runs synchronously. The returned value is set on the entity and persisted in the same transaction.
3. On an **after** event — `postComputeAndSaveValue()` is queued as a [background job](./background-jobs) and runs asynchronously. The `ComputedFieldEvaluationSubscriber` handles persistence once the job completes.

---

## Built-in Providers

SolidX ships with several providers for common patterns — generating IDs, concatenating fields, and no-op placeholders. See [Built-in Computation Providers](../reference/built-in-computation-providers) for the full reference with configuration examples and sample outputs.

---
title: Computation Providers
description: Learn how to extend the backend with custom computation providers.
---

# 🧮 Computation Providers

Computation providers are essential for defining how **computed fields** are calculated and updated in the backend. This guide walks you through setting up and implementing them in SolidX.

---

## ⚙️ How to Configure a Computed Field

### 🧾 Sample Metadata Configuration

In the `computedFieldValueProvider`, we specify the **provider class** responsible for the computation logic.

The `computedFieldTriggerConfig` defines the **entities and operations** that trigger the computation. You need to specify:
- `modelName`
- `moduleName`
- `operations`: 

Supported operations include:
- `before-update`
- `before-insert`
- `before-remove`
- `after-update`
- `after-insert`
- `after-remove`

🔸 **Before operations** trigger `preComputeValue()` of `IEntityPreComputeFieldProvider`.

🔸 **After operations** trigger `postComputeAndSaveValue()` of `IEntityPostComputeFieldProvider`.

> For **before operations**, `modelName` must be the same as the model with the computed field.  
> For **after operations**, it can be **any model**, related or unrelated.

You can:
- Access the triggering entity and metadata
- Set the computed value (saved automatically for `preComputeValue`)
- Persist additional logic and saving in `postComputeAndSaveValue`

<details>
  <summary>📄 Example: Configuration for <code>amountPaid</code> computed field</summary>

```json
{
  "name": "paymentCollectionItemDetail",
  "displayName": "Payment Collection Item Detail",
  "description": null,
  "fields": [
    {
      "name": "amountPaid",
      "displayName": "Amount Paid",
      "description": null,
      "type": "computed",
      "ormType": "varchar",
      "isSystem": false,
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
      "computedFieldValueProviderCtxt": "{}",
      "required": false,
      "unique": false,
      "index": false,
      "private": false,
      "encrypt": false,
      "encryptionType": null,
      "decryptWhen": null,
      "columnName": null,
      "isUserKey": false
    }
  ]
}
```

</details>

---

## 🧩 Computation Provider Interfaces

To implement a custom computation provider, you need to implement either or both of the following interfaces:

<details>
  <summary>💡 Interfaces to Implement</summary>

```ts

export interface IEntityPreComputeFieldProvider<TTriggerEntity, TContext, TValue=void> extends IEntityComputedFieldProvider {
  preComputeValue(triggerEntity: TTriggerEntity, computedFieldMetadata: ComputedFieldMetadata<TContext>): Promise<TValue>;
}

export interface IEntityPostComputeFieldProvider<TTriggerEntity, TContext> extends IEntityComputedFieldProvider {
  postComputeAndSaveValue(triggerEntity: TTriggerEntity, computedFieldMetadata: ComputedFieldMetadata<TContext>): Promise<void>;
}
```

The IEntityComputedFieldProvider looks like this:
```ts
export interface IEntityComputedFieldProvider {
  help(): string;
  name(): string;
}
```

</details>

---

## ⚙️ How It Works

### 🛠 Core Mechanism

1. `ComputedEntityFieldSubscriber` listens to `insert`, `update`, and `delete` events across all entities.
2. For **before** operations:
   - `preComputeValue()` is called **synchronously**
   - Value is set directly on the entity and auto-saved
3. For **after** operations:
   - `postComputeAndSaveValue()` is called **asynchronously** via background jobs
   - Final saving happens via `ComputedFieldEvaluationSubscriber`

---

## 📚 Related Recipes 
### TODO

- 👉 [Pre-computed fields](../pre-computed-fields/index.md)  
- 👉 [Post-computed fields](../post-computed-fields/index.md)  
- 👉 [Multiple Computed Fields](../multiple-computed-fields/index.md)  

---
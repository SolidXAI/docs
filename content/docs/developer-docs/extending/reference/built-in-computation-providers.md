---
title: Built-in Computation Providers
icon: "calculator"
description: Reference for the built-in computation providers available in SolidX.
keywords: [backend, computation providers, built-in, reference]
---


# Built-in Computation Providers

SolidX ships with the following computation providers for common patterns. To use any of them, set `computedFieldValueProvider` to the provider name and pass the required context as a JSON string in `computedFieldValueProviderCtxt`.

For background on how computation providers work, see [Computation Providers](../backend-customization/computation-providers).

---

## AlphaNumExternalIdComputationProvider

Generates a random **alphanumeric code** with an optional prefix and configurable length. Useful for invoice numbers, record codes, or any short human-readable identifier.

<details open>
  <summary>
    Context interface
  </summary>

```ts
export interface AlphaNumExternalIdContext {
  prefix?: string;             // alias -> staticPrefix
  length?: number;             // default: 5
  dynamicFieldPrefix?: string; // entity field name to use as prefix
}
```

| Context Property | Type | Default | Sample Value | Description |
|---|---|---|---|---|
| `prefix` | `string` | `""` | `"INV"` | Static string prepended to the code (alias: `staticPrefix`) |
| `length` | `number` | `5` | `6` | Length of the generated alphanumeric portion |
| `dynamicFieldPrefix` | `string` | - | `"clientCode"` | Field name on the entity to use as a dynamic prefix |

</details>

<details open>
  <summary>
    Example: generating an invoice number
  </summary>

**Use case:** When a new invoice is created, a unique human-readable invoice number is needed for display and reference. This example generates a code like `INV-A3X9K2` - an `"INV"` prefix followed by 6 random alphanumeric characters - so every invoice gets a distinct, easily shareable identifier automatically on insert.

**Field metadata:**

```json
{
  "name": "invoiceNumber",
  "type": "computed",
  "ormType": "varchar",
  "computedFieldTriggerConfig": [
    {
      "modelName": "invoice",
      "moduleName": "billing",
      "operations": ["before-insert"]
    }
  ],
  "computedFieldValueProvider": "AlphaNumExternalIdComputationProvider",
  "computedFieldValueProviderCtxt": "{\"prefix\": \"INV\", \"length\": 6}"
}
```

**Computed output:**

```json
{ "invoiceNumber": "INV-A3X9K2" }
```

</details>

---

## ConcatEntityComputedFieldProvider

Concatenates **one or more fields** on the entity into a single string. Supports 1-level-deep relation paths (e.g., `"city.name"`) and optional slugification.

<details open>
  <summary>
    Context interface
  </summary>

```ts
export interface ConcatComputedFieldContext {
  separator: string;   // concatenated values separator
  fields: string[];    // supports "relation.field" for 1-level deep paths
  slugify?: boolean;   // if true, slugify each field value before concatenation
}
```

| Context Property | Type | Default | Sample Value | Description |
|---|---|---|---|---|
| `fields` | `string[]` | - | `["firstName", "lastName"]` | Fields to concatenate. Supports `"relation.field"` paths |
| `separator` | `string` | - | `" "` | String placed between each field value |
| `slugify` | `boolean` | `false` | `true` | If `true`, slugifies each field value before concatenating |

</details>

<details open>
  <summary>
    Example: full name from first and last name
  </summary>

**Use case:** A student record stores first and last name as separate fields, but the UI and search require a single `fullName` field. This example concatenates `firstName` and `lastName` with a space separator, producing a value like `"Jane Doe"` automatically on every insert or update - no manual assignment needed.

**Field metadata:**

```json
{
  "name": "fullName",
  "type": "computed",
  "ormType": "varchar",
  "computedFieldTriggerConfig": [
    {
      "modelName": "student",
      "moduleName": "school",
      "operations": ["before-insert", "before-update"]
    }
  ],
  "computedFieldValueProvider": "ConcatEntityComputedFieldProvider",
  "computedFieldValueProviderCtxt": "{\"separator\": \" \", \"fields\": [\"firstName\", \"lastName\"]}"
}
```

**Computed output:**

```json
// Entity: { "firstName": "Jane", "lastName": "Doe" }
{ "fullName": "Jane Doe" }
```

</details>

<details open>
  <summary>
    Example: slugified location code
  </summary>

**Use case:** A location record has `city` and `state` fields. A URL-safe slug is needed for routing or filtering - for example, `"new-york-ny"` instead of `"New York NY"`. Enabling `slugify` lowercases and hyphenates each value before concatenation, making the output safe to embed in URLs or use as a unique code.

**Context:**

```json
{
  "separator": "-",
  "fields": ["city", "state"],
  "slugify": true
}
```

**Computed output:**

```json
// Entity: { "city": "New York", "state": "NY" }
{ "locationCode": "new-york-ny" }
```

</details>

---

## UuidExternalIdEntityComputedFieldProvider

Generates a **UUID** with an optional static prefix. Suitable for entities that need globally unique references - especially across distributed systems.

<details open>
  <summary>
    Context interface
  </summary>

```ts
export interface UuidExternalIdContext {
  prefix?: string; // alias -> staticPrefix
}
```

| Context Property | Type | Default | Sample Value | Description |
|---|---|---|---|---|
| `prefix` | `string` | `""` | `"ORD"` | Static string prepended to the UUID (alias: `staticPrefix`) |

</details>

<details open>
  <summary>
    Example: order external ID
  </summary>

**Use case:** Orders are referenced across multiple systems - billing, fulfilment, and support. A globally unique, prefixed ID like `ORD-550e8400-e29b-41d4-a716-446655440000` ensures each order can be unambiguously identified regardless of which system is querying it. The prefix makes the entity type immediately recognisable from the ID alone, which is useful in logs and cross-system communication.

**Field metadata:**

```json
{
  "name": "externalId",
  "type": "computed",
  "ormType": "varchar",
  "computedFieldTriggerConfig": [
    {
      "modelName": "order",
      "moduleName": "sales",
      "operations": ["before-insert"]
    }
  ],
  "computedFieldValueProvider": "UuidExternalIdEntityComputedFieldProvider",
  "computedFieldValueProviderCtxt": "{\"prefix\": \"ORD\"}"
}
```

**Computed output:**

```json
{ "externalId": "ORD-550e8400-e29b-41d4-a716-446655440000" }
```

</details>

---

## NoopsEntityComputedFieldProviderService

A **no-op provider** - it runs but does not modify the field value. Use it to tag fields as `"type": "computed"` for metadata consistency when the actual computation is handled by a different provider.


This is useful when one provider handles several related computed fields in a single pass. Tag the secondary computed fields with <code>NoopsEntityComputedFieldProviderService</code> so they don't trigger redundant or conflicting logic independently.


<details open>
  <summary>
    Example: multi-field amount computation
  </summary>

**Use case:** An invoice has three computed financial fields: `amount`, `taxes`, and `totalAmount`. A single custom provider - `CalculateTotalsProvider` - computes all three values in one pass when `totalAmount` is triggered. Because `CalculateTotalsProvider` writes the `taxes` value as part of that same computation, there is no need for a separate provider to recalculate it.

To handle this, `taxes` is tagged with `NoopsEntityComputedFieldProviderService`. This marks it as a computed field (so the framework tracks it correctly and treats it as read-only on the client side), but no additional calculation logic runs for it when it is triggered - its value is already being set by `CalculateTotalsProvider` during `totalAmount`'s computation. Without the no-op provider, the framework would expect `taxes` to have its own computation logic, which would either be redundant or conflict with what `CalculateTotalsProvider` already sets.

**Field metadata for `taxes` (value computed by `CalculateTotalsProvider`, not this field's own provider):**

```json
{
  "name": "taxes",
  "type": "computed",
  "ormType": "varchar",
  "computedFieldTriggerConfig": [
    {
      "modelName": "invoice",
      "moduleName": "billing",
      "operations": ["after-insert", "after-update"]
    }
  ],
  "computedFieldValueProvider": "NoopsEntityComputedFieldProviderService",
  "computedFieldValueProviderCtxt": "{}"
}
```

The `taxes` value is written by `CalculateTotalsProvider` when it processes `totalAmount`. Assigning `NoopsEntityComputedFieldProviderService` here ensures the field is correctly typed as computed without triggering any additional - and potentially conflicting - calculation of its own.

</details>

---
title: Field Type Reference
description: Reference guide for field types when creating models in SolidX
---

## Field Type Reference

When creating fields in SolidX, use this mapping guide:

| Field Type in SolidX | When to Use | Key Attributes to Set |
|---------------------|-------------|----------------------|
| **Short Text** | Names, emails, IDs, brief content | `required`, `unique`, `min`, `max`, `isUserKey` |
| **Long Text** | Addresses, descriptions | `required` |
| **Rich Text** | Formatted content (T&C, FAQs) | `required` |
| **Boolean** | Yes/No flags | `required`, `defaultValue` |
| **Decimal** | Money amounts, percentages | `required`, `defaultValue`, `min`, `max` |
| **Integer** | Counters (overdue days) | `required`, `defaultValue` |
| **Selection (Static)** | Fixed dropdown options | `selectionStaticValues`, `defaultValue`, `isMultiSelect` |
| **Media (Single)** | File uploads | `mediaTypes`, `mediaMaxSizeKb`, `mediaStorageProviderUserKey` |
| **Relation** | Links between models | `relationType`, `relationCoModelSingularName`, `relationCoModelFieldName`, `relationCascade` |
| **Computed** | Auto-calculated fields | `computedFieldValueProvider`, `computedFieldValueProviderCtxt`, `computedFieldTriggerConfig` |
| **Datetime** | Date and time values | `required` |

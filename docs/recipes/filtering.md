---
sidebar_position: 9
title: Filtering Data
description: Learn how to use filter operators to query records via the REST API or the CRUD service.
keywords: [filters, query, operators, REST API, CRUD service]
---

# Filtering Data

SolidX provides a powerful filtering syntax that works consistently across two layers:

- **REST API** — pass filters as query-string parameters when calling the [Retrieve endpoints](/developer-docs/rest-apis/retrieve).
- **CRUD Service** — pass a `filters` object inside the DTO when calling [`find()`](/developer-docs/extending/backend-customization/crud-service#4-findfilterdto-context) or [`findOne()`](/developer-docs/extending/backend-customization/crud-service#5-findoneid-query-context) from backend code.

The syntax and available operators are identical in both cases.

---

## Syntax

Each filter targets a **field**, applies an **operator**, and compares against a **value**.

| Layer | Format |
|-------|--------|
| REST query string | `filters[field][operator]=value` |
| Service DTO (TypeScript) | `{ field: { $operator: value } }` |

When several fields are passed, they are implicitly combined with **`$and`**.

---

## Available Operators

| Operator | Description |
|-----------|-------------|
| `$eq` | Equal |
| `$eqi` | Equal (case-insensitive) |
| `$ne` | Not equal |
| `$nei` | Not equal (case-insensitive) |
| `$lt` | Less than |
| `$lte` | Less than or equal to |
| `$gt` | Greater than |
| `$gte` | Greater than or equal to |
| `$in` | Included in an array |
| `$notIn` | Not included in an array |
| `$contains` | Contains |
| `$notContains` | Does not contain |
| `$containsi` | Contains (case-insensitive) |
| `$notContainsi` | Does not contain (case-insensitive) |
| `$null` | Is null |
| `$notNull` | Is not null |
| `$between` | Is between |
| `$startsWith` | Starts with |
| `$startsWithi` | Starts with (case-insensitive) |
| `$endsWith` | Ends with |
| `$endsWithi` | Ends with (case-insensitive) |
| `$or` | Joins the filters in an "or" expression |
| `$and` | Joins the filters in an "and" expression |
| `$not` | Joins the filters in a "not" expression |

> 💡 **Tip:** `$and`, `$or`, and `$not` can be nested inside one another for complex logic.

---

## Examples

### Simple filters

**1. Equal match** — Get all active users

```ts
// Service DTO
filters: { status: { $eq: 'active' } }

// REST query string
// GET /api/users?filters[status][$eq]=active
```

**2. Greater-than & contains** — Get users with age > 25 whose name contains "John"

```ts
// Service DTO
filters: {
  age: { $gt: 25 },
  name: { $containsi: 'john' }
}

// REST query string
// GET /api/users?filters[age][$gt]=25&filters[name][$containsi]=john
```

**3. Range query** — Get all high-value paid fee transactions

```ts
// Service DTO
filters: {
  amount: { $gte: 5000 },
  status: { $eq: 'paid' }
}

// REST query string
// GET /api/fees?filters[amount][$gte]=5000&filters[status][$eq]=paid
```

### Nested filters

**4. Using `$and`** — Get users aged > 25 AND status = active

```ts
// Service DTO
filters: {
  $and: [
    { age: { $gt: 25 } },
    { status: { $eq: 'active' } }
  ]
}

// REST query string
// GET /api/users?filters[$and][0][age][$gt]=25&filters[$and][1][status][$eq]=active
```

**5. Using `$or`** — Get users whose name starts with "A" OR who have role "admin"

```ts
// Service DTO
filters: {
  $or: [
    { name: { $startsWithi: 'a' } },
    { role: { $eq: 'admin' } }
  ]
}

// REST query string
// GET /api/users?filters[$or][0][name][$startsWithi]=a&filters[$or][1][role][$eq]=admin
```

**6. Combining `$and` with `$or`** — Get active users who are either admins or have age > 30

```ts
filters: {
  $and: [
    { status: { $eq: 'active' } },
    {
      $or: [
        { role: { $eq: 'admin' } },
        { age: { $gt: 30 } }
      ]
    }
  ]
}
```

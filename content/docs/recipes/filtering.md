---
title: Filtering
icon: "search"
description: Learn how to use filter operators to query records via the REST API or the CRUD service.
keywords: [filters, query, operators, REST API, CRUD service]
---

# Filtering Data

SolidX provides a powerful filtering syntax that works consistently across two layers:

- **REST API** — pass filters as query-string parameters when calling the [Retrieve endpoints](../developer-docs/rest-apis/retrieve).
- **CRUD Service** — pass a `filters` object inside the DTO when calling [`find()`](../developer-docs/extending/backend-customization/crud-service#4-findfilterdto-context) or [`findOne()`](../developer-docs/extending/backend-customization/crud-service#5-findoneid-query-context) from backend code.

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
// REST query string
// GET /api/users?filters[$and][0][status][$eq]=active&filters[$and][1][$or][0][role][$eq]=admin&filters[$and][1][$or][1][age][$gt]=30
```

---

## Grouping & Aggregation

The `find()` method supports grouping records by one or more fields, with optional aggregation functions. This works via both REST API query strings and the CRUD service DTO.

When grouping is active, the response shape changes — instead of a flat list of records, you receive **group metadata** (and optionally the records within each group).

The relevant DTO fields are:

```ts
groupBy?: string[];          // Fields to group by
aggregates?: string[];       // Aggregate functions (e.g., "id:count")
populateGroup?: boolean;     // Fetch actual records per group
groupFilter?: BasicFilterDto; // Pagination/sorting within each group
```

> The examples below use a **PincodeMaster** model that has many-to-one `state` and `city` relations and a `createdAt` timestamp.

### Group by basics

Pass one or more field names in the `groupBy` array. If no `aggregates` are specified, `COUNT(*)` is applied automatically.

```ts
// Service DTO — group by a scalar field
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['pincode'],
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=pincode
```

The response includes `groupMeta` (one entry per group with group key + aggregate values) and `meta.totalRecords` reflecting the total number of groups.

### Grouping on relations

Group-by fields can traverse **many-to-one** relations using dot notation. The query builder automatically joins the related table.

```ts
// Service DTO — group by state and city
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['state.name', 'city.name'],
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=state.name&groupBy[1]=city.name
```

You can combine relation and scalar fields:

```ts
// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=state.name&groupBy[1]=city.name&groupBy[2]=pincode
```

Group names are ordered to match the `groupBy` array: state → city → pincode.

> Joins from filters are reused when possible; otherwise the necessary joins are created automatically.

### Date granularity

Group date/timestamp fields by a time bucket using the syntax `field:granularity`. Optionally append a format specifier: `field:granularity:format`.

**Supported granularities:** `day`, `week`, `month`, `year`

**Supported formats:** `MMM`, `MMMM`, `YYYY`, `YYYY-MM`, `YYYY-MM-DD`

```ts
// Service DTO — group by month
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['createdAt:month'],
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=createdAt:month
```

With a format specifier for short month names (Jan, Feb, …):

```ts
// Service DTO
groupBy: ['createdAt:month:MMM']

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=createdAt:month:MMM
```

For full month names use `MMMM`. Other formats: `YYYY`, `YYYY-MM`, `YYYY-MM-DD`. If no format is specified, the raw date bucket value is used.

Date grouping is database-aware and works across Postgres, SQL Server.

### Aggregates

Specify aggregate functions using the syntax `field:function` in the `aggregates` array.

**Supported functions:** `count`, `count_distinct`, `sum`, `avg`, `min`, `max`

```ts
// Service DTO — distinct pincodes per state
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['state.name'],
  aggregates: ['pincode:count_distinct'],
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=state.name&aggregates[0]=pincode:count_distinct
```

Multiple aggregates:

```ts
// Service DTO — total rows and distinct IDs per state/city group
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['state.name', 'city.name'],
  aggregates: ['id:count', 'id:count_distinct'],
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=state.name&groupBy[1]=city.name&aggregates[0]=id:count&aggregates[1]=id:count_distinct
```

Combine date granularity, relations, and aggregates:

```ts
// Distinct pincodes per state, per year
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=createdAt:year&groupBy[1]=state.name&aggregates[0]=pincode:count_distinct
```

### Group sorting & pagination

When grouping is active, `sort` and `offset`/`limit` apply to **group rows**, not individual entity rows. `meta.totalRecords` reflects the total number of groups (computed without pagination).

```ts
// Service DTO — sort groups alphabetically by state name, paginate to 50 groups
const result = await pincodeMasterService.find({
  limit: 50,
  offset: 0,
  groupBy: ['state.name'],
  sort: ['state.name:ASC'],
});

// REST query string
// GET /api/pincode-master?offset=0&limit=50&groupBy[0]=state.name&sort[0]=state.name:ASC
```

You can also sort by aggregate aliases (e.g., `id_max`).

### Populating group records

Set `populateGroup: true` to fetch the actual entity records within each group. Use `groupFilter` to control pagination and sorting of records **within** each group.

```ts
// Service DTO
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['state.name'],
  populateGroup: true,
  groupFilter: {
    limit: 10,
    offset: 0,
    sort: ['pincode:ASC'],
  },
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=state.name&populateGroup=true&groupFilter[limit]=10&groupFilter[offset]=0&groupFilter[sort][0]=pincode:ASC
```

The response includes a `groupRecords` array — each entry contains the group key, aggregate values, and a nested `records` array with pagination meta.

### Combining filters with grouping

All standard filter operators work alongside grouping. Filters are applied **before** grouping, so only matching rows are considered.

```ts
// Service DTO — groups only for state "Maharashtra"
const result = await pincodeMasterService.find({
  limit: 200,
  offset: 0,
  groupBy: ['state.name'],
  filters: {
    state: { name: { $eq: 'Maharashtra' } },
  },
});

// REST query string
// GET /api/pincode-master?offset=0&limit=200&groupBy[0]=state.name&filters[state][name][$eq]=Maharashtra
```

### Caveats

> **Warning**

> - **`populateGroup` is not supported when grouping on relation fields** (e.g., `state.name`, `city.name`). Use it only for scalar group-by fields. For relation-based groups, fetch group metadata first, then retrieve records in a separate call using the group key as a filter.
> - **Sort behavior with date bucket keys:** For date group keys with granularity/format (e.g., `createdAt:month:YYYY`), the sort parser treats the last segment as the sort order. Results may vary by database driver and may not sort as expected in all cases.

---
description: Information about the retrieve endpoint of the REST API, including usage, parameters, and responses
title: Retrieve Endpoint
summary: This document covers the retrieve endpoints of the SolidX REST API, explaining how to fetch records from the system. The endpoints support both retrieving multiple records with advanced filtering, pagination, sorting, and field selection options, as well as retrieving single records by ID. The documentation includes sample requests and responses, required headers, body content structure, and comprehensive examples of the filtering capabilities available for data retrieval operations.
solidx_concerns: [add_full_custom_ui,onlayoutload_handler_function,ondataload_handler_function,add_form_button,add_list_header_button_with,add_list_row_button_with,create_custom_form_field_widget,create_custom_list_field_widget]
---

# Overview
This section will give information about the retrieve endpoint of the REST API, including how to use it, what parameters it accepts, and what responses it returns.

The retrieve endpoints allows you to fetch one or more records from the system.

## Read API: Query string (filters) usage

Queries can accept a `filters` parameter with the following syntax:  
Each filter is expressed as `filters[field][operator]=value`.

The following operators are available:

| Operator | Description |
|-----------|-------------|
| $eq | Equal |
| $eqi | Equal (case-insensitive) |
| $ne | Not equal |
| $nei | Not equal (case-insensitive) |
| $lt | Less than |
| $lte | Less than or equal to |
| $gt | Greater than |
| $gte | Greater than or equal to |
| $in | Included in an array |
| $notIn | Not included in an array |
| $contains | Contains |
| $notContains | Does not contain |
| $containsi | Contains (case-insensitive) |
| $notContainsi | Does not contain (case-insensitive) |
| $null | Is null |
| $notNull | Is not null |
| $between | Is between |
| $startsWith | Starts with |
| $startsWithi | Starts with (case-insensitive) |
| $endsWith | Ends with |
| $endsWithi | Ends with (case-insensitive) |
| $or | Joins the filters in an "or" expression |
| $and | Joins the filters in an "and" expression |
| $not | Joins the filters in a "not" expression |

When several fields are passed in the filters object, they are implicitly combined with `$and`.  
For example:
`GET /api/fees?filters[amount][$gte]=5000&filters[status][$eq]=paid`
This query returns all fee records where the amount is at least ₹5000 and the status is “paid” — for instance, to fetch all high-value paid fee transactions.

> 💡 Tip: `$and`, `$or`, and `$not` operators can be nested inside one another for complex logic.

### Example filters

#### Simple examples
1. **Equal match:** Get all active users  
   ```ts
   filters: { status: { $eq: 'active' } }
   // → ?filters[status][$eq]=active
   ```

2. **Greater than and contains:** Get users with age > 25 and name containing "John"  
   ```ts
   filters: {
     age: { $gt: 25 },
     name: { $containsi: 'john' }
   }
   // → ?filters[age][$gt]=25&filters[name][$containsi]=john
   ```

#### Nested examples

3. **Using `$and`:** Get users aged > 25 AND status = active  
   ```ts
   filters: {
     $and: [
       { age: { $gt: 25 } },
       { status: { $eq: 'active' } }
     ]
   }
   // → ?filters[$and][0][age][$gt]=25&filters[$and][1][status][$eq]=active
   ```

4. **Using `$or`:** Get users whose name starts with "A" OR have role "admin"  
   ```ts
   filters: {
     $or: [
       { name: { $startsWithi: 'a' } },
       { role: { $eq: 'admin' } }
     ]
   }
   // → ?filters[$or][0][name][$startsWithi]=a&filters[$or][1][role][$eq]=admin
   ```
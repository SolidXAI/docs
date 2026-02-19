---
sidebar_position: 3
description: Information about the retrieve endpoint of the REST API, including usage, parameters, and responses
title: Retrieve Endpoint
summary: This document covers the retrieve endpoints of the SolidX REST API, explaining how to fetch records from the system. The endpoints support both retrieving multiple records with advanced filtering, pagination, sorting, and field selection options, as well as retrieving single records by ID. The documentation includes sample requests and responses, required headers, body content structure, and comprehensive examples of the filtering capabilities available for data retrieval operations.
solidx_concerns: [add_full_custom_ui,onlayoutload_handler_function,ondataload_handler_function,add_form_button,add_list_header_button_with,add_list_row_button_with,create_custom_form_field_widget,create_custom_list_field_widget]
---

# Retrieve Endpoints

The retrieve endpoints allow you to fetch records from the system. There are two endpoints:

- **Find** — retrieve a list of records with filtering, pagination, sorting, and field selection.
- **FindOne** — retrieve a single record by its ID.

---

## Find (List Records)

Returns a paginated list of records for a given model.

**Endpoint:** `GET /api/{model}`

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | number | Maximum number of records to return (default: 10) |
| `offset` | number | Number of records to skip for pagination (default: 0) |
| `fields` | string[] | Columns to include in the response (e.g. `fields[0]=id&fields[1]=name`) |
| `sort` | string[] | Columns to sort by (prefix with `-` for descending, e.g. `sort[0]=-createdAt`) |
| `populate` | string[] | Relations to load (e.g. `populate[0]=department&populate[1]=roles.permissions`) |
| `populateMedia` | string[] | Media fields whose URLs should be resolved (e.g. `populateMedia[0]=avatar`) |
| `filters` | object | Filter expressions — see [Filtering Data](../../../recipes/filtering) for the full syntax and operators |

### Example Request

```
GET /api/persons?limit=10&offset=0&fields[0]=id&fields[1]=name&fields[2]=email&populate[0]=department&sort[0]=name&filters[status][$eq]=active
```

### Example Response

```json
{
  "records": [
    {
      "id": 1,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "department": { "id": 3, "name": "Engineering" }
    }
  ],
  "meta": {
    "totalRecords": 42,
    "currentPage": 1,
    "totalPages": 5
  }
}
```

---

## FindOne (Single Record)

Returns a single record by its ID.

**Endpoint:** `GET /api/{model}/:id`

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fields` | string[] | Columns to include in the response |
| `populate` | string[] | Relations to load |
| `populateMedia` | string[] | Media fields whose URLs should be resolved |

### Example Request

```
GET /api/persons/12?populate[0]=department&populate[1]=manager&populateMedia[0]=avatar
```

### Example Response

```json
{
  "id": 12,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "department": { "id": 3, "name": "Engineering" },
  "manager": { "id": 5, "name": "John Smith" },
  "_media": {
    "avatar": [
      { "id": 7, "name": "profile.png", "_full_url": "https://storage.example.com/uploads/profile.png" }
    ]
  }
}
```

---

## Filtering

Both the **Find** endpoint and the backend [CRUD Service `find()` method](../../extending/backend-customization/crud-service#4-findfilterdto-context) share the same filter syntax and operators.

For the complete operators reference, examples (simple and nested), and usage from both REST and service layers, see the **[Filtering Data](../../../recipes/filtering)** recipe.

---
title: Delete Endpoint
description: Information about the delete endpoint of the REST API, including usage, parameters, and responses
summary: This document describes the delete endpoints in SolidX's REST API, covering both single record and bulk deletion operations. When soft delete is enabled on a model, records are not permanently removed but marked as deleted with deletedAt and deletedTracker fields populated. The documentation includes detailed examples of delete requests and responses, showing the HTTP headers required (Content-Type and Authorization), endpoint URLs, and the structure of returned data including soft delete metadata and tracking information.
---

#  Delete Endpoint

This section explains how to use the **delete endpoints** of the REST API in SolidX. You can remove records either individually or in bulk using these endpoints.

##  Deleting a Single Record

When soft delete is enabled on a m<summary> Example: Bulk Delete Fee Types</summary>
odel (like `fee-type`), the record is not permanently removed — instead, the `deletedAt` and `deletedTracker` fields are populated.

<details>
 <summary>
    
     Example: Delete a Fee Type Record
  </summary>

###  Headers

```http
Content-Type: application/json
Authorization: Bearer <token>
```

 ###  Request Body

```http
DELETE /api/fee-type/{id}
```

 ###  Sample Response

```json
{
  "statusCode": 200,
  "message": [],
  "error": "",
  "data": {
    "partPaymentAllowed": true,
    "id": 3,
    "createdAt": "2025-08-06T23:30:10.185Z",
    "updatedAt": "2025-08-07T00:06:18.418Z",
    "deletedAt": "2025-08-07T00:06:18.378Z",
    "deletedTracker": "Thu Aug 07 2025 11:06:18 GMT+0530 (India Standard Time)",
    "feeType": "tuition",
    "updatedBy": {
      "id": 1,
      "fullName": "Default Admin",
      "email": "admin@example.service.com",
      "active": true
    }
  }
}
```

</details>

 The above response confirms soft deletion, showing timestamps and tracker info.

##  Bulk Deletion

SolidX also supports deleting multiple records in a single request.

<details>
<summary>
    
     Example: Bulk Delete Fee Types
  </summary>

###  Headers

```http
Content-Type: application/json
Authorization: Bearer <token>
```

 ###  Request

```http
DELETE /api/fee-type/bulk
```

 ###  Body

```json
[1]  // List of record IDs to delete
```

 ###  Sample Response

```json
[
  {
    "statusCode": 200,
    "message": [],
    "error": "",
    "data": {
      "partPaymentAllowed": true,
      "id": 3,
      "createdAt": "2025-08-06T23:30:10.185Z",
      "updatedAt": "2025-08-07T00:06:18.418Z",
      "deletedAt": "2025-08-07T00:06:18.378Z",
      "deletedTracker": "Thu Aug 07 2025 11:06:18 GMT+0530 (India Standard Time)",
      "feeType": "tuition",
      "updatedBy": {
        "id": 1,
        "fullName": "Default Admin",
        "email": "admin@example.service.com",
        "active": true
      }
    }
  }
]
```

</details>

 **Summary**
- Use `DELETE /api/model/{id}` for soft-deleting a single record.
- Use `DELETE /api/model/bulk` with an array of IDs for bulk deletion.
- Responses return deleted data including soft delete metadata (`deletedAt`, `deletedTracker`).

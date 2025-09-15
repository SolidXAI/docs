---
title: Update Endpoints
description: Information about the update endpoints of the REST API, including usage, parameters, and responses.
sidebar_position: 2
---

#  Update Endpoints in SolidX

This section provides details about the **Update Endpoints** of the REST API, including usage patterns, headers, request/response formats, and examples of both **partial** and **full** updates.

---

##  Types of Updates

### 1 Partial Update
- Method: `PATCH`
- Purpose: Update specific fields of a record without affecting the rest.

<details>
<summary> Example: Update <code>feeType</code> Field</summary>

####  Headers
```http
Content-Type: application/json
Authorization: Bearer <token>
```

####  Request
```http
PATCH /api/fee-type/1
```

####  Body
```json
{
  "feeType": "tuition"
}
```

####  Response
```json
{
  "statusCode": 200,
  "message": [],
  "error": "",
  "data": {
    "feeType": "tuition",
    "partPaymentAllowed": true,
    "id": 3,
    "updatedBy": {
      "fullName": "Default Admin",
      "email": "admin@example.service.com",
      "active": true,
      "id": 1
    },
    "updatedAt": "2025-08-06T23:30:10.185Z"
  }
}
```

</details>

---

### 2 Full Update
- Method: `PUT`
- Purpose: Replace the entire model with a new object.
- Idempotent: Yes (repeated calls with the same payload have the same effect).

<details>
<summary> Example: Full Update of Fee Type</summary>

#### 📋 Headers
```http
Content-Type: application/json
Authorization: Bearer <token>
```

####  Request
```http
PUT /api/fee-type/1
```

####  Body
```json
{
  "feeType": "tuition",
  "instituteUserKey": "Don Bosco",
  "partPaymentAllowed": true
}
```

####  Response
```json
{
  "statusCode": 200,
  "message": [],
  "error": "",
  "data": {
    "feeType": "tuition",
    "partPaymentAllowed": true,
    "institute": {
      "instituteName": "Don Bosco",
      "id": 3
    },
    "updatedBy": {
      "fullName": "Default Admin",
      "email": "admin@example.service.com",
      "id": 1
    },
    "updatedAt": "2025-08-06T23:30:10.185Z"
  }
}
```

</details>

---

##  Update Without Media

Used when no files (like images or documents) are uploaded.

<details>
<summary> Example: JSON-only Update</summary>

```http
PATCH /api/institute-user/1
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{
  "userType": "Institute Admin",
  "email": "admin@institute.com"
}
```

</details>

---

##  Update With Media

Used when the request includes file uploads (e.g., profile pictures, attachments).

<details>
<summary> Example: Update with Multipart Form Data</summary>

```http
PATCH /api/institute-user/1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Authorization: Bearer <token>
```

**Form Fields**
- `updateDto` (as JSON string)
- `files` (actual file(s))

**Example Payload**
```json
updateDto: {
  "userType": "Institute Admin",
  "email": "admin@institute.com"
}
files: profile-picture.jpg
```

</details>

---

---
title: Create Endpoint
description: Information about the create endpoint of the REST API, including usage, parameters, and responses
summary: This document details the create endpoints in SolidX's REST API, covering single record creation, bulk record creation, and record creation with media files. It provides comprehensive examples including HTTP headers (Content-Type and Authorization), request body structures, and sample responses for each scenario. The create endpoints support both JSON payloads for standard data and multipart/form-data for media uploads. All endpoints require proper create permissions and JWT bearer authentication for security.
---

This section provides information about the SolidX **create REST endpoints**, including how to use them, what parameters they accept, and what responses they return.

SolidX supports both single record creation and bulk record creation.

##  Creating a Single Record

###  Headers

```http
Content-Type: application/json
Authorization: Bearer <token>
```

  ###  Request Body

`POST /api/fee-type`
<details>
 <summary>Request Body</summary>

```json
{
  "feeType": "string",
  "instituteId": 0,
  "instituteUserKey": "string",
  "partPaymentAllowed": true,
  "latePaymentFeesType": "string",
  "latePaymentFees": 0
}
```
</details>
<details>
 <summary>Sample Request</summary>

```json
{
  "feeType": "tuition",
  "instituteUserKey": "Don Bosco",
  "partPaymentAllowed": true
}
```
</details>
<details>
 <summary>Sample Response</summary>

```json
{
  "statusCode": 200,
  "message": [],
  "error": "",
  "data": {
    "partPaymentAllowed": true,
    "feeType": "test",
    "institute": {
      "id": 3,
      "instituteName": "Don Bosco",
      "hostedPagePrefix": "donbosco",
      "paymentGatewayMerchantId": "CUST123",
      "instituteAddress": "Kurla",
      "instituteContactNumber": "9833795342"
    },
    "createdBy": {
      "id": 1,
      "fullName": "Default Admin",
      "username": "admin@example.service.com",
      "email": "admin@example.service.com"
    },
    "updatedBy": {
      "id": 1,
      "fullName": "Default Admin",
      "username": "admin@example.service.com",
      "email": "admin@example.service.com"
    },
    "id": 3,
    "createdAt": "2025-08-06T23:30:10.185Z",
    "updatedAt": "2025-08-06T23:30:10.185Z"
  }
}
```
</details>

##  Bulk Record Creation

To create multiple records at once:

  ###  Request

`POST /api/fee-type/bulk`
<details>
 <summary>Sample Bulk Request</summary>

```json
[
  {
    "feeType": "tuition",
    "instituteUserKey": "Don Bosco",
    "partPaymentAllowed": true
  }
]
```
</details>

##  Creating a Record with Media

If your model includes media fields (e.g., uploading a logo), use the `multipart/form-data` content type.

  ###  Request with Media

```http
POST /api/fee-type
Content-Type: multipart/form-data
Authorization: Bearer <token>
```
<details>
 <summary>Multipart Form Data Example</summary>

```http
--boundary
Content-Disposition: form-data; name="data"

{
  "feeType": "tuition",
  "instituteUserKey": "Don Bosco",
  "partPaymentAllowed": true
}
--boundary
Content-Disposition: form-data; name="logo"; filename="tuitionLogo.png"
Content-Type: image/png

<binary data>
--boundary--
```
</details>

 Ensure the user has the appropriate **create permission** for the model.  
  Refer to the [Permissions](../../../admin-docs/iam/permissions.md) section for more information.

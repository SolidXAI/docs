---
sidebar_position: 1
title: Recover Endpoint
description: Information about the recover endpoint of the REST API, including usage, parameters, and responses
---
import {  MdHttp, MdInput,MdOutput,MdDescription } from "react-icons/md";


#  Recover Endpoint

##  Overview
The recover endpoint allows you to restore one or more records that have been soft-deleted in your application.

This documentation includes usage examples for:
- Recovering a single record by ID
- Recovering records in bulk



##  Recover a Single Record

<h3 className=" card-headear-wrapper">
    <MdHttp size={24}  />

###  Headers
</h3>

```http
Content-Type: application/json
Authorization: Bearer <token>
```


 <h3 className=" card-headear-wrapper">
    <MdInput size={18}  />

###  Sample Request
  </h3>


```http
POST /api/fee-type/recover/{id}
```


 <h3 className=" card-headear-wrapper">
    <MdOutput size={18}  />

###  Sample Response
  </h3>

```json
{
  "statusCode": 200,
  "message": [],
  "error": "",
  "data": {
    "message": "Record successfully recovered",
    "data": {
      "partPaymentAllowed": true,
      "id": 3,
      "createdAt": "2025-08-06T23:30:10.185Z",
      "updatedAt": "2025-08-07T00:06:18.418Z",
      "deletedAt": "2025-08-07T00:06:18.378Z",
      "deletedTracker": "Thu Aug 07 2025 11:06:18 GMT+0530 (India Standard Time)",
      "publishedAt": null,
      "localeName": null,
      "defaultEntityLocaleId": null,
      "feeType": "tuition",
      "latePaymentFeesType": null,
      "latePaymentFees": null
    }
  }
}
```

>  **Known Issue**: Although the record is successfully recovered in the database, the response may still contain `deletedAt` and `deletedTracker`. This is expected to be fixed in upcoming releases.



##  Bulk Recovery of Records

<h3 className=" card-headear-wrapper">
    <MdHttp size={24}  />

###  Headers
</h3>

```http
Content-Type: application/json
Authorization: Bearer <token>
```

 <h3 className=" card-headear-wrapper">
    <MdInput size={18}  />

###  Sample Request
  </h3>

```http
POST /api/fee-type/recover/bulk
```

 <h3 className=" card-headear-wrapper">
    <MdDescription size={18}  />

###  Sample Body
  </h3>

```json
[1, 2, 3]  // Array of record IDs to recover
```

 <h3 className=" card-headear-wrapper">
    <MdOutput size={18}  />

###  Sample Response
  </h3>

```json
{
  "statusCode": 200,
  "message": ["3 records successfully recovered"],
  "error": "",
  "data": [
    {
        "message": "Record successfully recovered",
        "data": {
          "partPaymentAllowed": true,
          "id": 3,
          "createdAt": "2025-08-06T23:30:10.185Z",
          "updatedAt": "2025-08-07T00:06:18.418Z",
          "deletedAt": "2025-08-07T00:06:18.378Z",
          "deletedTracker": "Thu Aug 07 2025 11:06:18 GMT+0530 (India Standard Time)",
          "publishedAt": null,
          "localeName": null,
          "defaultEntityLocaleId": null,
          "feeType": "tuition",
          "latePaymentFeesType": null,
          "latePaymentFees": null
        }
    },
    ...,
  ]
}
```


>  **Known Issue**: Similar to single record recovery, the response may still include `deletedAt` and `deletedTracker` fields for recovered records. This is expected to be resolved in future updates.

---
sidebar_position: 1
title: Delete Endpoint
description: Information about the delete endpoint of the REST API, including usage, parameters, and responses
---

import { IoIosArrowForward } from "react-icons/io";
import {  MdHttp, MdInput,MdOutput,MdDescription } from "react-icons/md";

#  Delete Endpoint

This section explains how to use the **delete endpoints** of the REST API in SolidX. You can remove records either individually or in bulk using these endpoints.



##  Deleting a Single Record

When soft delete is enabled on a m<summary> Example: Bulk Delete Fee Types</summary>
odel (like `fee-type`), the record is not permanently removed — instead, the `deletedAt` and `deletedTracker` fields are populated.

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
     Example: Delete a Fee Type Record
  </summary>

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

###  Request Body
  </h3>

```http
DELETE /api/fee-type/{id}
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
<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
     Example: Bulk Delete Fee Types
  </summary>


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

###  Request 
  </h3>

```http
DELETE /api/fee-type/bulk
```

 <h3 className=" card-headear-wrapper">
    <MdDescription size={18}  />

###  Body
  </h3>

```json
[1]  // List of record IDs to delete
```

 <h3 className=" card-headear-wrapper">
    <MdOutput size={18}  />

###  Sample Response
  </h3>

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

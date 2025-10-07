---
title: Update Endpoints
description: Information about the update endpoints of the REST API, including usage, parameters, and responses.
summary: This document explains the update endpoints in SolidX's REST API, covering both partial updates (PATCH method for updating specific fields) and full updates (PUT method for replacing entire records). It provides detailed examples of updates without media files (using JSON content type) and updates with media files (using multipart/form-data). Each section includes HTTP headers, request formats, sample payloads, and response structures. Both update methods are idempotent and require JWT bearer authentication.
sidebar_position: 2
---

import { IoIosArrowForward } from "react-icons/io";
import {  MdHttp, MdInput,MdOutput,MdDescription } from "react-icons/md";

#  Update Endpoints in SolidX

This section provides details about the **Update Endpoints** of the REST API, including usage patterns, headers, request/response formats, and examples of both **partial** and **full** updates.



##  Types of Updates

### 1 Partial Update
- Method: `PATCH`
- Purpose: Update specific fields of a record without affecting the rest.

<details>
<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
      Example: Update <code>feeType</code> Field
  </summary>

<h4 className=" card-headear-wrapper">
    <MdHttp size={24}  />

####  Headers
</h4>

```http
Content-Type: application/json
Authorization: Bearer <token>
```

 <h4 className=" card-headear-wrapper">
    <MdInput size={18}  />

####  Request 
  </h4>

```http
PATCH /api/fee-type/1
```

 <h4 className=" card-headear-wrapper">
    <MdDescription size={18}  />

####  Body
  </h4>
  
```json
{
  "feeType": "tuition"
}
```




 <h4 className=" card-headear-wrapper">
    <MdOutput size={18}  />

####   Response
  </h4>
  
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



### 2 Full Update
- Method: `PUT`
- Purpose: Replace the entire model with a new object.
- Idempotent: Yes (repeated calls with the same payload have the same effect).

<details>
<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
      Example: Full Update of Fee Type
  </summary>

<h4 className=" card-headear-wrapper">
    <MdHttp size={24}  />

####  Headers
</h4>

```http
Content-Type: application/json
Authorization: Bearer <token>
```

 <h4 className=" card-headear-wrapper">
    <MdInput size={18}  />

####  Request 
  </h4>

```http
PUT /api/fee-type/1
```

 <h4 className=" card-headear-wrapper">
    <MdDescription size={18}  />

####  Body
  </h4>

```json
{
  "feeType": "tuition",
  "instituteUserKey": "Don Bosco",
  "partPaymentAllowed": true
}
```

 <h4 className=" card-headear-wrapper">
    <MdOutput size={18}  />

####   Response
  </h4>
  
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



##  Update Without Media

Used when no files (like images or documents) are uploaded.

<details>
<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
       Example: JSON-only Update
  </summary>


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



##  Update With Media

Used when the request includes file uploads (e.g., profile pictures, attachments).

<details>
<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
       Example: Update with Multipart Form Data
</summary>

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



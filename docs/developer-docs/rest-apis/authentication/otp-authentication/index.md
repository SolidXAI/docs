---
title: OTP
description: Information about OTP-based authentication APIs
summary: Details SolidX OTP-based authentication mechanism with comprehensive API documentation. Covers two-step registration (Initiate Registration sends OTP to email/mobile with customizable validationSources, Confirm Registration verifies OTP) and two-step login (Initiate Login sends OTP, Confirm Login verifies and returns JWT tokens). Includes environment variables for OTP expiry, validation sources, request/response formats, error handling, and transactional override options.
sidebar_position: 2
---
  
import { MdOutlineSettings, MdHttp, MdInput, MdOutput } from "react-icons/md";
import { FiShare2 } from "react-icons/fi";



#  OTP Authentication

This section covers the OTP-based authentication APIs available in SolidX.



##  Implementation Overview

SolidX provides a comprehensive OTP-based authentication mechanism with the following endpoints:

1. **Register**
2. **Login**



##  1. Register

###  1.1 Initiate Registration

Allows users to register using their username, email, or mobile number through OTP verification.

The registration process is divided into two steps:

- **Initiate Registration**: Sends OTP to specified validation sources.
- **Confirm Registration**: Confirms registration with the OTP.

The `validationSources` field in the request body specifies which sources (`email`, `mobile`) should be validated. This can be customized via environment variables or overridden via the `transactional` flag in the request.


  <h3 className=" card-headear-wrapper">
    <FiShare2 size={20}  />

###  Endpoint
</h3>

```
POST /api/iam/otp/register/initiate
```


  <h3 className=" card-headear-wrapper">
    <MdOutlineSettings size={20}  />

###  Environment Variables
</h3>

- `IAM_PASSWORD_LESS_REGISTRATION`: Enables/disables OTP registration.
- `IAM_OTP_EXPIRY`: OTP expiry time (default: 5 mins).
- `IAM_PASSWORD_LESS_REGISTRATION_VALIDATE_WHAT`: Values can be `email`, `mobile`, or both.

<h3 className=" card-headear-wrapper">
    <MdHttp size={24}  />

###  Headers
</h3>


```http
Content-Type: application/json
```

  <h3 className=" card-headear-wrapper">
    <MdInput size={18}  />

###  Request Body
  </h3> 

```json
{
  "username": "string",
  "email": "[EMAIL]",
  "mobile": "string",
  "validationSources": ["email", "mobile"],
  "customPayload": {}
}
```

  <h3 className=" card-headear-wrapper">
    <MdOutput size={20}  />

###  Response Body
  </h3>

```json
{
  "message": "OTP sent successfully"
}
```



###  1.2 Confirm Registration

```
POST /api/iam/otp/register/confirm
```

<h3 className=" card-headear-wrapper">
    <MdHttp size={24}  />

###  Headers
</h3>

```http
Content-Type: application/json
```

  <h3 className=" card-headear-wrapper">
    <MdInput size={18}  />

###  Request Body
  </h3> 

```json
{
  "type": "email", 
  "identifier": "[EMAIL]",
  "otp": "string"
}
```

<h3 className=" card-headear-wrapper">
    <MdOutput size={20}  />

###  Response Body
  </h3>

```json
{
  "active": true,
  "message": "User registration verified for email"
}
```



##  2. Login

###  2.1 Initiate Login

Allows users to log in using username, email, or mobile through OTP.

Similar to registration, the `validationSources` and environment variables control OTP delivery.

  <h3 className=" card-headear-wrapper">
    <FiShare2 size={20}  />

###  Endpoint
</h3>

```
POST /api/iam/otp/login/initiate
```

###  Environment Variables

- `IAM_PASSWORD_LESS_REGISTRATION`: Enables/disables OTP login.
- `IAM_OTP_EXPIRY`: OTP expiry time (default: 5 mins).
- `IAM_PASSWORD_LESS_LOGIN_VALIDATE_WHAT`: What to validate during login.

<h3 className=" card-headear-wrapper">
    <MdHttp size={24}  />

###  Headers
</h3>


```http
Content-Type: application/json
```

  <h3 className=" card-headear-wrapper">
    <MdInput size={18}  />

###  Request Body
  </h3> 



```json
{
  "type": "email",
  "identifier": "[EMAIL]"
}
```

<h3 className=" card-headear-wrapper">
    <MdOutput size={20}  />

###  Response Body
  </h3>

```json
{
  "message": "OTP sent successfully"
}
```



###  2.2 Confirm Login

```
POST /api/iam/otp/login/confirm
```

<h3 className=" card-headear-wrapper">
    <MdHttp size={24}  />

###  Headers
</h3>


```http
Content-Type: application/json
```

  <h3 className=" card-headear-wrapper">
    <MdInput size={18}  />

###  Request Body
  </h3> 


```json
{
  "type": "email",
  "identifier": "[EMAIL]",
  "otp": "string"
}
```

<h3 className=" card-headear-wrapper">
    <MdOutput size={20}  />

###  Response Body
  </h3>


```json
{
  "accessToken": "<ACCESS_TOKEN>",
  "refreshToken": "<REFRESH_TOKEN>",
  "user": {
    "id": 1,
    "username": "[USERNAME]",
    "email": "[EMAIL]",
    "mobile": "string",
    "lastLoginProvider": "otp",
    "roles": ["User", "Admin"]
  }
}
```
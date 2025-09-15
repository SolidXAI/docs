---
title: OTP Authentication
description: Information about OTP-based authentication APIs
sidebar_position: 2
---

#  OTP Authentication

This section covers the OTP-based authentication APIs available in SolidX.

---

##  Implementation Overview

SolidX provides a comprehensive OTP-based authentication mechanism with the following endpoints:

1. **Register**
2. **Login**

---

##  1. Register

###  1.1 Initiate Registration

Allows users to register using their username, email, or mobile number through OTP verification.

The registration process is divided into two steps:

- **Initiate Registration**: Sends OTP to specified validation sources.
- **Confirm Registration**: Confirms registration with the OTP.

The `validationSources` field in the request body specifies which sources (`email`, `mobile`) should be validated. This can be customized via environment variables or overridden via the `transactional` flag in the request.

###  Endpoint

```
POST /api/iam/otp/register/initiate
```

###  Environment Variables

- `IAM_PASSWORD_LESS_REGISTRATION`: Enables/disables OTP registration.
- `IAM_OTP_EXPIRY`: OTP expiry time (default: 5 mins).
- `IAM_PASSWORD_LESS_REGISTRATION_VALIDATE_WHAT`: Values can be `email`, `mobile`, or both.

###  Headers

```http
Content-Type: application/json
```

###  Request Body

```json
{
  "username": "string",
  "email": "[EMAIL]",
  "mobile": "string",
  "validationSources": ["email", "mobile"],
  "customPayload": {}
}
```

###  Response Body

```json
{
  "message": "OTP sent successfully"
}
```

---

###  1.2 Confirm Registration

```
POST /api/iam/otp/register/confirm
```

###  Headers

```http
Content-Type: application/json
```

###  Request Body

```json
{
  "type": "email", 
  "identifier": "[EMAIL]",
  "otp": "string"
}
```

###  Response Body

```json
{
  "active": true,
  "message": "User registration verified for email"
}
```

---

##  2. Login

###  2.1 Initiate Login

Allows users to log in using username, email, or mobile through OTP.

Similar to registration, the `validationSources` and environment variables control OTP delivery.

###  Endpoint

```
POST /api/iam/otp/login/initiate
```

###  Environment Variables

- `IAM_PASSWORD_LESS_REGISTRATION`: Enables/disables OTP login.
- `IAM_OTP_EXPIRY`: OTP expiry time (default: 5 mins).
- `IAM_PASSWORD_LESS_LOGIN_VALIDATE_WHAT`: What to validate during login.

###  Headers

```http
Content-Type: application/json
```

###  Request Body

```json
{
  "type": "email",
  "identifier": "[EMAIL]"
}
```

###  Response Body

```json
{
  "message": "OTP sent successfully"
}
```

---

###  2.2 Confirm Login

```
POST /api/iam/otp/login/confirm
```

###  Headers

```http
Content-Type: application/json
```

###  Request Body

```json
{
  "type": "email",
  "identifier": "[EMAIL]",
  "otp": "string"
}
```

###  Response Body

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
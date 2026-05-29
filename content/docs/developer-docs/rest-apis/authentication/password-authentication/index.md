---
title: Password
icon: "key-round"
description: Information about password-based authentication APIs
summary: Comprehensive documentation of SolidX password-based authentication APIs. Covers seven endpoints - Register (with environment variables for enabling registration), Authenticate (login with username and password, returns JWT tokens), Refresh Tokens (obtain new tokens using refresh token), Forgot Password (password reset flow), Change Password (for authenticated users), Get User Info (retrieve current user details), and Logout. Includes HTTP headers, request and response formats, error codes, and security considerations.
---



#  Password Authentication

This section covers the password-based authentication APIs available in SolidX.



##  Implementation Overview

SolidX provides a comprehensive password-based authentication mechanism with the following endpoints:

1. **Register**
2. **Authenticate**
3. **Refresh Tokens**
4. **Forgot Password**
5. **Change Password**
6. **Get User Info**
7. **Logout**



##  1. Register

Allows users to create a new account.

  <h3 className=" ">
    

###  Environment Variables
</h3>


- `IAM_PASSWORD_REGISTRATION_ENABLED`: Enables/disables registration.
- `IAM_ALLOW_PUBLIC_REGISTRATION`: Allows public registration when set to `true`.


<h3 className=" ">
    

###  Headers
</h3>

  ```http
  Content-Type: application/json
  ```

  <h3 className=" ">
    

###  Request Body
  </h3>



```json
{
  "fullName": "string",
  "username": "string",
  "email": "[EMAIL]",
  "password": "[PASSWORD]",
  "mobile": "string",
  "roles": ["string"]
}
```

  <h3 className=" ">
    

###  Response Body
  </h3>


```json
{
  "fullName": "string",
  "username": "string",
  "email": "[EMAIL]",
  "mobile": "string",
  "forcePasswordChange": true,
  "roles": [...],
  "id": 0,
  "createdAt": "...",
  "updatedAt": "..."
}
```

>  **Note**: The response body can be optimized. It currently includes sensitive data like passwords.



##  2. Authenticate

Log in and receive access and refresh tokens.

  <h3 className=" ">
    

###  Environment Variables  
</h3>

- `IAM_JWT_ACCESS_TOKEN_TTL`: TTL for access tokens (default: 60 mins).
- `IAM_JWT_REFRESH_TOKEN_TTL`: TTL for refresh tokens (default: 1 day).

<h3 className=" ">
    

###  Headers
</h3>

```http
Content-Type: application/json
```

  <h3 className=" ">
    

###  Request Body
  </h3>

```json
{
  "email": "[EMAIL]",
  "username": "[EMAIL]",
  "password": "[PASSWORD]"
}
```

  <h3 className=" ">
    

###  Response Body
  </h3>

```json
{
  "data": {
    "user": {
      "email": "[EMAIL]",
      "username": "[EMAIL]",
      "roles": ["Admin", "Internal User"]
    },
    "accessToken": "<ACCESS_TOKEN>",
    "refreshToken": "<REFRESH_TOKEN>"
  }
}
```



##  3. Refresh Tokens

Refresh the access token using a valid refresh token.

<h3 className=" ">
    

###  Headers
</h3>

```http
Content-Type: application/json
```

<h3 className=" ">
    

###  Request Body
  </h3>

```json
{
  "refreshToken": "<REFRESH_TOKEN>"
}
```

  <h3 className=" ">
    

###  Response Body
  </h3>

```json
{
  "accessToken": "<NEW_ACCESS_TOKEN>",
  "refreshToken": "<NEW_REFRESH_TOKEN>"
}
```



##  4. Forgot Password

Initiates and confirms password reset flow.

  <h3 className=" ">
    

###  Environment Variables
</h3>

- `IAM_OTP_EXPIRY`: OTP expiry time (default: 10 mins).


  <h3 className=" ">
    

###  Initiate Request
</h3>

```http
POST /api/iam/initiate/forgot-password
```


<h3 className=" ">
    

###  Headers
</h3>


```http
Content-Type: application/json
```

#### Request Body

```json
{
  "email": "[EMAIL]",
  "username": "string"
}
```

#### Response Body

```json
{
  "status": "success",
  "message": "Password reset token sent",
  "data": {
    "user": {
      "email": "[EMAIL]",
      "username": "string"
    }
  }
}
```

###  Confirm Request

```http
POST /api/iam/confirm/forgot-password
```

#### Request Body

```json
{
  "username": "string",
  "email": "[EMAIL]",
  "verificationToken": "string",
  "password": "[NEW_PASSWORD]"
}
```



##  5. Change Password

<h3 className=" ">
    

###  Request Body
  </h3>
  
```http
POST /api/iam/change-password
```

#### Request Body

```json
{
  "id": 0,
  "email": "[EMAIL]",
  "currentPassword": "[CURRENT_PASSWORD]",
  "newPassword": "[NEW_PASSWORD]"
}
```



##  6. Get User Info

Retrieve logged-in user info.

```http
GET /api/iam/me
```

#### Headers

```http
Authorization: Bearer <ACCESS_TOKEN>
```

#### Response Body

```json
{
  "user": {
    "email": "[EMAIL]",
    "username": "[EMAIL]",
    "roles": ["Admin"]
  },
  "accessToken": "<ACCESS_TOKEN>",
  "refreshToken": "<REFRESH_TOKEN>"
}
```



##  7. Logout

Invalidate the current session.

#### Response Body

```json
{
  "message": "Logout successful"
}
```

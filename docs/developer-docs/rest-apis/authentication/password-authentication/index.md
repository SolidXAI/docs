---
sidebar_position: 1
title: Password Authentication
description: Information about password-based authentication APIs
---

# 🔑 Password Authentication

This section covers the password-based authentication APIs available in SolidX.

## 🛠️ Implementation
Below endpoints are available as part of the password authentication.
1. **Register**: Allows users to create a new account, by providing their full name, username, email, password, mobile number, and roles. This endpoint is public and does not require authentication. On successful registration, the user will receive a response containing their details.

## Environment Variables
IAM_PASSWORD_REGISTRATION_ENABLED -> This variable controls whether password-based registration is enabled or not. If set to `true`, users can register using their email and password. If set to `false`, registration will be disabled.
IAM_ALLOW_PUBLIC_REGISTRATION -> This variable controls whether public registration is allowed or not. If set to `true`, users can register using the signup API. If set to false, only an admin can register user using the admin panel.

# Request / Response form
 ### Headers
``` http
    Content-Type: application/json
```

### Request Body
``` json
{
  "fullName": "string",
  "username": "string",
  "email": "string",
  "password": "string",
  "mobile": "string",
  "roles": [
    "string"
  ]
}
```

### Response Body
```json
{
  "fullName": "string",
  "username": "string",
  "email": "string",
  "mobile": "string",
  "password": "string",
  "forcePasswordChange": true,
  "lastLoginProvider": "local",
  "accessCode": "string",
  "googleAccessToken": "string",
  "googleId": "string",
  "googleProfilePicture": "string",
  "active": true,
  "forgotPasswordConfirmedAt": "2025-08-07T07:01:49.994Z",
  "verificationTokenOnForgotPassword": "string",
  "verificationTokenOnForgotPasswordExpiresAt": "2025-08-07T07:01:49.994Z",
  "emailVerifiedOnRegistrationAt": "2025-08-07T07:01:49.994Z",
  "emailVerificationTokenOnRegistration": "string",
  "emailVerificationTokenOnRegistrationExpiresAt": "2025-08-07T07:01:49.994Z",
  "mobileVerifiedOnRegistrationAt": "2025-08-07T07:01:49.994Z",
  "mobileVerificationTokenOnRegistration": "string",
  "mobileVerificationTokenOnRegistrationExpiresAt": "2025-08-07T07:01:49.994Z",
  "emailVerifiedOnLoginAt": "2025-08-07T07:01:49.994Z",
  "emailVerificationTokenOnLogin": "string",
  "emailVerificationTokenOnLoginExpiresAt": "2025-08-07T07:01:49.994Z",
  "mobileVerifiedOnLoginAt": "2025-08-07T07:01:49.994Z",
  "mobileVerificationTokenOnLogin": "string",
  "mobileVerificationTokenOnLoginExpiresAt": "2025-08-07T07:01:49.994Z",
  "customPayload": "string",
  "roles": [
    ...
  ],
  "userViewMetadata": [
    ...
  ],
  "id": 0,
  "createdAt": "2025-08-07T07:01:49.994Z",
  "updatedAt": "2025-08-07T07:01:49.994Z",
  "deletedAt": "2025-08-07T07:01:49.994Z",
  "deletedTracker": "string",
  "publishedAt": "2025-08-07T07:01:49.994Z",
  "localeName": "string",
  "defaultEntityLocaleId": 0,
  "createdBy": "string",
  "updatedBy": "string"
}
```
*** Known Issues: The response body can be optimized further, since it is too long ***

2. **Authenticate**: Allows users to log in and receive an access token and refresh token. The access token is used for subsequent requests, while the refresh token can be used to obtain a new access token when the current one expires. Access tokens are typically short-lived, while refresh tokens are longer-lived. The default expiration for access tokens is 60 minutes, and for refresh tokens, it is 1 day. The values can be controlled via environment variables.

## Environment Variables
IAM_JWT_ACCESS_TOKEN_TTL: Defines the time-to-live (TTL) for access tokens, which is typically set to 60 minutes.
IAM_JWT_REFRESH_TOKEN_TTL: Defines the time-to-live (TTL) for refresh tokens, which is typically set to 1 day.

# Request / Response form
 ### Headers
``` http
    Content-Type: application/json
```
### Request Body
``` json
{
  "email": "admin@example.service.com",
  "username": "admin@example.service.com",
  "password": "Admin@3215$"
}
```
### Response Body
``` json
{
  "statusCode": 200,
  "message": [],
  "error": "",
  "data": {
    "user": {
      "email": "admin@example.service.com",
      "mobile": null,
      "username": "admin@example.service.com",
      "forcePasswordChange": false,
      "id": 1,
      "roles": [
        "Admin",
        "Internal User"
      ]
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiYWRtaW5AZXhhbXBsZS5zZXJ2aWNlLmNvbSIsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5zZXJ2aWNlLmNvbSIsInJvbGVzIjpbIkFkbWluIiwiSW50ZXJuYWwgVXNlciJdLCJpYXQiOjE3NTQ1NDI3ODQsImV4cCI6MTc1NDU0NjM4NCwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwIiwiaXNzIjoibXktc2Nob29sLXBvcnRhbCJ9.AaZWIlGABXsguhhXyFBNz42Ru9hXlqz-lFLE4dltpOE",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInJlZnJlc2hUb2tlbklkIjoiNzkyODk3NTktMzgyMi00ZDAxLTkxNmMtMTA4MDYwOTU0NGRmIiwiaWF0IjoxNzU0NTQyNzg0LCJleHAiOjE3NTQ2MjkxODQsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCIsImlzcyI6Im15LXNjaG9vbC1wb3J0YWwifQ.Woxi1ztpAMislfUxJ4i4v8_4SwQuavS5w_JVuhJodwE"
  }
}
```

3. **Refresh Tokens**: Allows users to refresh their access tokens. This api requires a valid refresh token to be sent in the request body. If the refresh token is valid, a new access token and refresh token are returned. This is useful for maintaining user sessions without requiring them to log in again frequently.

## Request / Response form
### Headers
``` http
    Content-Type: application/json
```     

### Request Body
POST /api/iam/refresh-tokens

``` json
{
  "refreshToken": "string"
}
```

## Response Body
``` json
{
                "accessToken": "<NEW_ACCESS_TOKEN>",
                "refreshToken": "<NEW_REFRESH_TOKEN>",
            }
          ```  
4. **Forgot Password**: Allows users to initiate and confirm a forgot password reset. On successful initiation, a password reset link is sent to the user's email address. This link contains an OTP like token that can be used to reset the password. User can click on the link to reset their password. The link is typically valid for a limited time, such as 10 minutes. You can provide either email or username in the request body to initiate the forgot password flow.

## Environment Variables
IAM_OTP_EXPIRY: Defines the time-to-live (TTL) for OTP tokens, which is typically set to 10 minutes.

## Request / Response form
POST /api/iam/initiate/forgot-password
### Headers
``` http
    Content-Type: application/json
```
### Request Body
``` json
{
  "email": "string",
  "username": "string"
}
```
### Response Body
``` json{
            status: 'success',
            message: SUCCESS_MESSAGES.FORGOT_PASSWORD_TOKEN_SENT,
            error: '',
            errorCode: '',
            data: {
                user: {
                    email: user.email,
                    mobile: user.mobile,
                    username: user.username,
                },
            }
        }
```
For Confirm Forgot Password api,
### Request / Response form
POST /api/iam/confirm/forgot-password
### Headers
``` http
    Content-Type: application/json
```
### Request Body
``` json
{
  "username": "string",
  "email": "string",
  "verificationToken": "string",
  "password": "string"
}
```

## Response Body
``` json
{
            status: 'success',
            message: SUCCESS_MESSAGES.FORGOT_PASSWORD_CONFIRMED,
            error: '',
            errorCode: '',
            data: {}
        }
        ```

5. **Change Password**: Allows users to change their password.

## Request / Response form
### Headers
``` http
    Content-Type: application/json  
```    

### Request Body
POST /api/iam/change-password
``` json
{
  "id": 0,
  "email": "string",
  "currentPassword": "string",
  "newPassword": "string"
}
```

6. **Get User Info**: Allows users to retrieve their own user information. This is useful for displaying user profile information or for checking the current user's authentication status.
GET /api/iam/me

### Headers
``` http
    Authorization: Bearer <ACCESS_TOKEN>
``` 

### Response Body
``` json
{
            user: {
                email: user.email,
                mobile: user.mobile,
                username: user.username,
                id: user.id,
                roles: Suser.roles.map((role, idx, roles) => role.name)
            },
            accessToken : ACCESS_TOKEN,
            refreshToken: REFRESH_TOKEN

        }
 ```       
7. **Logout**: Allows users to log out and invalidate their access token. It invalidates the current refresh token for the user (identified by the access token) and removes it from the cache. This cache might be an in-memory i.e default or Redis cache, depending on the configuration. After logging out, the user will need to log in again to obtain a new access token and refresh token.

## Request / Response form

### Response Body
``` json
{ message: SUCCESS_MESSAGES.LOGOUT_SUCCESS}
```
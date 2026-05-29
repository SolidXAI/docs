---
description: This section elaborates on the authentication APIs provided for the different authentication providers.
title: Authentication
icon: "lock"
summary: This document provides an overview of the authentication mechanisms supported by SolidX. The platform offers three authentication providers - Password-based authentication (the default method using username and password), OTP authentication (using One-Time Passwords for secure login), and OAuth authentication (currently supporting Google as an OAuth provider for social login integration).
---

<Callout type="info" title="Mental Model">

  Authentication providers in SolidX are different entry paths into the same platform session model. The provider changes how identity is verified, but the goal stays the same: establish a trusted user session that the rest of the platform can authorize.
  - Password is the standard username-and-password flow.
    - OTP is useful when short-lived verification is preferred.
    - OAuth is useful when identity should be delegated to an external provider.
  So the intuition is: <strong>these are alternative authentication strategies for the same secured application surface</strong>.

</Callout>

SolidX supports the below authentication providers:
- **Password**: This is the default authentication provider that uses username and password for authentication.
- **OTP**: This provider uses One-Time Passwords for authentication.
- **OAuth**: This provider uses OAuth for authentication.
 - Currently, SolidX supports Google as an OAuth provider.

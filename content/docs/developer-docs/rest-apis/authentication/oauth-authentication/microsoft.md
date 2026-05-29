---
title: Microsoft OAuth
icon: "share-2"
description: Guide to configuring Microsoft OAuth authentication
summary: This guide covers the end-to-end process of setting up Microsoft OAuth (Entra ID) for your SolidX application, including Azure Portal configuration and environment variable setup.
---


# Microsoft OAuth Authentication

## Overview

This document provides a guide on how to configure and use Microsoft OAuth authentication. The implementation uses Microsoft Entra ID (formerly Azure Active Directory) to allow users to sign in with their Microsoft accounts.

## Microsoft Entra ID Configuration (Azure Portal)

To use Microsoft OAuth, you must register an application in the Microsoft Entra admin center.

### 1. Register an Application

1.  Log in to the [Microsoft Entra admin center](https://entra.microsoft.com/) (formerly Azure Portal).
    ![Microsoft for Developers Landing Page](/img/oauth/microsoft/microsoft-entra-page.png)
2.  Click on **App registrations**.
3.  Click **New registration**.
4.  Enter a name for your application (e.g., `SolidCore-App`).
    ![Microsoft for Developers Landing Page](/img/oauth/microsoft/app-registration-page.png)
5.  Choose the **Supported account types** (e.g., "Accounts in any organizational directory and personal Microsoft accounts").
6.  In the **Redirect URI** section, select **Web** and enter your callback URL:
    - Development: `http://localhost:3000/api/iam/microsoft/connect/callback`
    - Production: `https://your-api-domain.com/api/iam/microsoft/connect/callback`
7.  Click **Register**.

### 2. Get Application and Tenant IDs

1.  After registration, you will be on the application's **Overview** page.
2.  Copy the **Application (client) ID**.
3.  Copy the **Directory (tenant) ID**.

### 3. Create a Client Secret

1.  Navigate to **Certificates & secrets** > **Client secrets**.
2.  Click **New client secret**.
3.  Add a description and set an expiration time.
4.  Click **Add**.
5.  **IMPORTANT**: Copy the secret **Value** immediately. You will not be able to see it again.

## Configuration (Environment Variables)

Add the following environment variables to your `.env` file:

```bash
# Microsoft OAuth Configuration
IAM_MICROSOFT_OAUTH_CLIENT_ID=your-application-id
IAM_MICROSOFT_OAUTH_CLIENT_SECRET=your-client-secret
IAM_MICROSOFT_OAUTH_TENANT_ID=common
IAM_MICROSOFT_OAUTH_CALLBACK_URL=http://localhost:3000/api/iam/microsoft/connect/callback
IAM_MICROSOFT_OAUTH_REDIRECT_URL=http://localhost:4200/auth/microsoft/callback
```

## Authentication Flow

1.  **User clicks the Microsoft sign-in button** in your app.
2.  **Your app redirects to Microsoft's login page** for authentication.
3.  **User logs in with their Microsoft account** and grants your app permission to access their email and profile.
4.  **Microsoft sends back a confirmation** that the user is authenticated.
5.  **Your app receives the confirmation** and creates an internal session for that user.
6.  **Your app logs the user in** and they can now access your app.

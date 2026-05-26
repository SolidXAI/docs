---
title: Facebook OAuth
description: Guide to configuring Facebook (Meta) OAuth authentication
summary: This guide covers the end-to-end process of setting up Facebook OAuth for your SolidX application, including Meta for Developers app configuration, and environment variable setup.
---

import { SiMeta } from "react-icons/si";

# <SiMeta size={32} color="#1877F2" style={{ verticalAlign: 'middle', marginRight: '12px' }} /> Facebook OAuth Authentication

## Overview

This document provides a guide on how to configure and use Facebook OAuth authentication. The implementation allows users to sign in using their Facebook (Meta) accounts.

## Facebook App Configuration (Meta for Developers)

To use Facebook OAuth, you must create and configure an app on the Meta for Developers platform.

### 1. Create a Facebook App

1.  Log in to the [Meta for Developers](https://developers.facebook.com/) portal.
    ![Meta for Developers Landing Page](/img/oauth/facebook/meta-login-page.png)
2.  Click on **My Apps** and then click **Create App**.
3.  Select an app type (e.g., "Allow people to log in with their Facebook account").
4.  Enter an app name and contact email.
    ![Meta for Developers Landing Page](/img/oauth/facebook/create-app-screen.png)
5.  Click **Create App**.
    ![Meta for Developers Landing Page](/img/oauth/facebook/final-app-screen.png)

### 2. Configure Facebook Login

1.  In the app dashboard, find **Facebook Login** and click **Set Up**.
2.  Select **Web** (WWW) as the platform.
3.  Enter your site URL (e.g., `https://localhost:3000`).
4.  Navigate to **Facebook Login** > **Settings** in the left sidebar.
5.  In the **Valid OAuth Redirect URIs** field, enter your callback URL:
    - Development: `https://localhost:3000/api/iam/facebook/connect/callback`
    - Production: `https://your-api-domain.com/api/iam/facebook/connect/callback`
6.  Click **Save Changes**.

### 3. Get App ID and App Secret

1.  Navigate to **App Settings** > **Basic**.
2.  Copy the **App ID**.
3.  Click **Show** next to **App Secret** (you may need to re-enter your password) and copy the secret.

## Configuration (Environment Variables)

Add the following environment variables to your `.env` file:

```env
# Facebook OAuth Configuration
IAM_FACEBOOK_OAUTH_CLIENT_ID=your-app-id
IAM_FACEBOOK_OAUTH_CLIENT_SECRET=your-app-secret
IAM_FACEBOOK_OAUTH_CALLBACK_URL=https://localhost:3000/api/iam/facebook/connect/callback
IAM_FACEBOOK_OAUTH_REDIRECT_URL=https://localhost:3000/auth/facebook/callback
```

## Authentication Flow

1.  **User clicks the Facebook sign-in button** in your app.
2.  **Your app redirects to Facebook's login page** for authentication.
3.  **User logs in with their Facebook account** and grants your app permission to access their email and profile.
4.  **Facebook sends back a confirmation** that the user is authenticated.
5.  **Your app receives the confirmation** and creates an internal session for that user.
6.  **Your app logs the user in** and they can now access your app.

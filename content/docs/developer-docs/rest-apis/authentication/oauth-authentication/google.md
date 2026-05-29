---
title: Google OAuth
icon: "share-2"
description: Guide to configuring Google OAuth authentication
summary: This guide covers the end-to-end process of setting up Google OAuth for your SolidX application, including Google Cloud Console configuration, environment variable setup, and understanding the authentication flow.
---


# Google OAuth Authentication

## Overview

This document provides a guide on how to configure and use Google OAuth authentication. The implementation allows users to sign in using their Google accounts.

## Google Cloud Configuration

To use Google OAuth, you must create and configure an app on the Google Cloud Console.

### 1. Create a Google Cloud Project

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Click **Select a Project** and then **New Project**.
3.  Enter a project name and click **Create**.
4.  Wait for the project to be created and select it.

### 2. Enable Google People API

1.  In the Google Cloud Console, navigate to **APIs & Services** > **Library**.
2.  Search for "Google People API".
3.  Click on it and then click **Enable**.

### 3. Create OAuth Credentials

1.  Navigate to **APIs & Services** > **Credentials**.
2.  Click **Create Credentials** and select **OAuth 2.0 Client ID**.
3.  Choose **Web application** as the application type.
4.  Add your authorized redirect URIs:
    - Development: `https://localhost:3000/api/iam/google/connect/callback`
    - Production: `https://your-api-domain.com/api/iam/google/connect/callback`
5.  Click **Create**.

### 4. Get Client ID and Client Secret

1.  After creation, a dialog will appear with your **Client ID** and **Client Secret**.
2.  Copy both values and store them securely.
3.  You can also view these at any time in the **OAuth 2.0 Client IDs** section.

## Configuration (Environment Variables)

Add the following environment variables to your `.env` file:

```bash
# Google OAuth Configuration
IAM_GOOGLE_OAUTH_CLIENT_ID=your-client-id
IAM_GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
IAM_GOOGLE_OAUTH_CALLBACK_URL=https://localhost:3000/api/iam/google/connect/callback
IAM_GOOGLE_OAUTH_REDIRECT_URL=https://localhost:4200/auth/google/callback
```

## Authentication Flow

1.  **User clicks the Google sign-in button** in your app.
2.  **Your app redirects to Google's login page** for authentication.
3.  **User logs in with their Google account** and grants your app permission to access their email and profile.
4.  **Google sends back a confirmation** that the user is authenticated.
5.  **Your app receives the confirmation** and creates an internal session for that user.
6.  **Your app logs the user in** and they can now access your app.

---
sidebar_position: 5
title: OAuth
description: Information about OAuth-based authentication methods
summary: Simple overview of OAuth authentication in SolidX, including Google, Facebook, Microsoft, LinkedIn, Twitter/X, and custom OAuth providers.
---

import { FcGoogle } from "react-icons/fc";
import { SiMeta } from "react-icons/si";
import { FaMicrosoft, FaLinkedin, FaTwitter } from "react-icons/fa";

# OAuth methods

SolidX supports several OAuth sign-in methods. You can use built-in providers or connect with other OAuth services.

## Supported OAuth methods

<div className="feature-grid">
  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FcGoogle size={20} style={{ marginRight: "10px" }} />
      Google
    </h4>
    <p className="card-desc">A popular Google sign-in option.</p>
    <p><a href="./google.md">Google OAuth guide</a></p>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <SiMeta size={20} color="#1877F2" style={{ marginRight: "10px" }} />
      Facebook
    </h4>
    <p className="card-desc">Sign in with Facebook / Meta accounts.</p>
    <p><a href="./facebook.md">Facebook OAuth guide</a></p>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaMicrosoft size={20} color="#00A4EF" style={{ marginRight: "10px" }} />
      Microsoft
    </h4>
    <p className="card-desc">Sign in with Microsoft / Entra ID accounts.</p>
    <p><a href="./microsoft.md">Microsoft OAuth guide</a></p>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaLinkedin size={20} color="#0A66C2" style={{ marginRight: "10px" }} />
      LinkedIn
    </h4>
    <p className="card-desc">Sign in with LinkedIn accounts.</p>
    <p>LinkedIn support is available as a standard OAuth method.</p>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaTwitter size={20} color="#1DA1F2" style={{ marginRight: "10px" }} />
      Twitter/X
    </h4>
    <p className="card-desc">Sign in with Twitter / X accounts.</p>
    <p>Twitter/X support is available as a standard OAuth method.</p>
  </div>
  </div>

## A friendly OAuth overview

OAuth lets users sign in through another service, like Google, Facebook, LinkedIn, or Twitter/X, without storing their password in SolidX.

### Basic flow

- User clicks a provider sign-in button.
- The app sends the user to the provider.
- The provider returns the user back to SolidX.
- SolidX finishes sign-in and opens the app.

### What you usually need

- A client ID from the provider
- A client secret or app secret
- A redirect URL for the login result
- A few provider settings in the provider console

## Want a different provider?

If you want a provider not listed here, use the custom OAuth providers option and follow the same simple pattern.

## Where to go next

- [Facebook OAuth](./facebook.md)
- [Google OAuth](./google.md)
- [Microsoft OAuth](./microsoft.md)

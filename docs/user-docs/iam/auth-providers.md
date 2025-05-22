---
sidebar_position: 5
---

# Authentication Providers

SOLID supports multiple authentication methods through its provider system, offering flexibility in how users can sign up and log in to your application.

## Supported Providers

<!-- ### Password Authentication
- Traditional username/password
- Password policies
- Password reset flow
- Account recovery

### OTP (Passwordless)
- Email-based OTP
- SMS-based OTP
- Time-based tokens
- Recovery codes 

### OAuth Providers

1. **Google**
2. **Meta/Facebook**
3. **LinkedIn**
4. **Twitter/X**
5. **Custom OAuth providers**-->

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Password Authentication</h4>
    <ul className="card-desc">
      <li>Traditional username/password</li>
      <li>Password policies</li>
      <li>Password reset flow</li>
      <li>Account recovery</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 OTP (Passwordless)</h4>
    <ul className="card-desc">
      <li>Email-based OTP</li>
      <li>SMS-based OTP</li>
      <li>Time-based tokens</li>
      <li>Recovery codes</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 OAuth Providers</h4>
   1. **Google**
2. **Meta/Facebook**
3. **LinkedIn**
4. **Twitter/X**
5. **Custom OAuth providers**
  </div>

</div>

## Authentication Flow

### Standard OAuth Flow

1. Frontend initiates auth:

```javascript
// Redirect to OAuth provider
window.location.href = "https://solid.website.com/api/iam/[provider]/connect";
```

2. Backend handles callback:

```
https://solid.website.com/api/iam/[provider]/connect/callback
```

3. Provider redirects with code:

```
http://website.com/connect/[provider]/callback?accessCode=[code]
```

4. Frontend exchanges code:

```
GET https://solid.website.com/api/iam/[provider]/auth?accessCode=[code]
```

5. Backend returns JWT:

```json
{
  "token": "eyJhbGciOiJIUzI1...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "profile": {}
  }
}
```

## Provider Configuration

### Password Provider

```json
{
  "provider": "password",
  "config": {
    "minLength": 8,
    "requireNumbers": true,
    "requireSpecialChars": true,
    "requireUppercase": true,
    "passwordHistory": 5,
    "maxAttempts": 5,
    "lockoutDuration": 300
  }
}
```

### OTP Provider

```json
{
  "provider": "otp",
  "config": {
    "type": "email",
    "codeLength": 6,
    "expiry": 300,
    "rateLimit": {
      "window": 3600,
      "max": 5
    }
  }
}
```

### OAuth Provider (Google Example)

```json
{
  "provider": "google",
  "config": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret",
    "redirectUri": "https://solid.website.com/api/iam/google/connect/callback",
    "scopes": ["email", "profile"]
  }
}
```

## Features

<!-- ### Multi-factor Authentication (MFA)
- Enable/disable per user
- Multiple MFA methods
- Backup codes
- Remember device option

### Session Management
- JWT tokens
- Refresh tokens
- Token expiry
- Session invalidation

### Account Recovery
- Email recovery
- Security questions
- Admin assistance
- Recovery codes -->

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Multi-factor Authentication (MFA)</h4>
    <ul className="card-desc">
      <li>Enable/disable per user</li>
      <li>Multiple MFA methods</li>
      <li>Backup codes</li>
      <li>Remember device option</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Session Management</h4>
    <ul className="card-desc">
      <li>JWT tokens</li>
      <li>Refresh tokens</li>
      <li>Token expiry</li>
      <li>Session invalidation</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 Account Recovery</h4>
    <ul className="card-desc">
      <li>Email recovery</li>
      <li>Security questions</li>
      <li>Admin assistance</li>
      <li>Recovery codes</li>
    </ul>
  </div>

</div>

## Security Features

  <!-- ### Password Security
  - Secure hashing (bcrypt)
  - Password policies
  - Brute force protection
  - Password history

  ### OAuth Security
  - State parameter
  - PKCE support
  - Scope validation
  - Token validation

  ### General Security
  - Rate limiting
  - IP blocking
  - Audit logging
  - Session monitoring -->

  <div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Password Security</h4>
    <ul className="card-desc">
      <li>Secure hashing (bcrypt)</li>
      <li>Password policies</li>
      <li>Brute force protection</li>
      <li>Password history</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 OAuth Security</h4>
    <ul className="card-desc">
      <li>State parameter</li>
      <li>PKCE support</li>
      <li>Scope validation</li>
      <li>Token validation</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 General Security</h4>
    <ul className="card-desc">
      <li>Rate limiting</li>
      <li>IP blocking</li>
      <li>Audit logging</li>
      <li>Session monitoring</li>
    </ul>
  </div>

</div>

## Best Practices

<!--
1. **Provider Selection**
   - Consider user base
   - Evaluate security needs
   - Plan backup methods
   - Test all flows

2. **Configuration**
   - Secure credentials
   - Set proper timeouts
   - Configure rate limits
   - Enable logging

3. **User Experience**
   - Clear error messages
   - Simple recovery flows
   - Multiple auth options
   - Remember user preferences

4. **Security**
   - Regular audits
   - Monitor failed attempts
   - Review permissions
   - Update configurations -->

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Provider Selection</h4>
    <ul className="card-desc">
      <li>Consider user base</li>
      <li>Evaluate security needs</li>
      <li>Plan backup methods</li>
      <li>Test all flows</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Configuration</h4>
    <ul className="card-desc">
      <li>Secure credentials</li>
      <li>Set proper timeouts</li>
      <li>Configure rate limits</li>
      <li>Enable logging</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 User Experience</h4>
    <ul className="card-desc">
      <li>Clear error messages</li>
      <li>Simple recovery flows</li>
      <li>Multiple auth options</li>
      <li>Remember user preferences</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4 Security</h4>
    <ul className="card-desc">
      <li>Regular audits</li>
      <li>Monitor failed attempts</li>
      <li>Review permissions</li>
      <li>Update configurations</li>
    </ul>
  </div>

</div>

## Implementation Examples

### Adding Google Authentication

1. Configure Provider:

```json
{
  "name": "google",
  "enabled": true,
  "config": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret",
    "redirectUri": "https://solid.website.com/api/iam/google/connect/callback",
    "scopes": ["email", "profile"],
    "mapping": {
      "email": "email",
      "name": "displayName",
      "picture": "photoUrl"
    }
  }
}
```

2. Frontend Integration:

```javascript
function initiateGoogleAuth() {
  window.location.href = "https://solid.website.com/api/iam/google/connect";
}

async function handleCallback(accessCode) {
  const response = await fetch(
    `https://solid.website.com/api/iam/google/auth?accessCode=${accessCode}`
  );
  const { token, user } = await response.json();
  // Store token and handle user session
}
```

### Implementing OTP Authentication

1. Configure Provider:

```json
{
  "name": "email_otp",
  "enabled": true,
  "config": {
    "type": "email",
    "template": "auth_otp",
    "codeLength": 6,
    "expiry": 300,
    "rateLimit": {
      "window": 3600,
      "max": 5
    }
  }
}
```

2. Authentication Flow:

```javascript
// Request OTP
async function requestOTP(email) {
  await fetch("/api/iam/otp/request", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

// Verify OTP
async function verifyOTP(email, code) {
  const response = await fetch("/api/iam/otp/verify", {
    method: "POST",
    body: JSON.stringify({ email, code }),
  });
  const { token, user } = await response.json();
  // Handle successful authentication
}
```

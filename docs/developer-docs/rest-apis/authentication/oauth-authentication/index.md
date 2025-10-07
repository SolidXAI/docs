---
sidebar_position: 5
title: OAuth Authentication
description: Information about OAuth-based authentication providers
summary: Comprehensive guide to OAuth authentication in SolidX supporting multiple providers (Password, OTP, Google, Meta/Facebook, LinkedIn, Twitter/X, custom OAuth). Covers standard OAuth flow (frontend redirect, backend callback), environment variable configuration per provider (client IDs, secrets, callback URLs), securing OAuth with state validation, token exchange, user profile retrieval, session management with JWT tokens, frontend implementation patterns, and examples for Google OAuth integration.
---

import { HiOutlineLockClosed, HiOutlineKey, HiOutlineGlobeAlt } from "react-icons/hi";
import { HiOutlineArrowsRightLeft,HiOutlineShieldCheck, HiOutlineClock, HiOutlineArrowPath, HiOutlineShieldExclamation  } from "react-icons/hi2"; 
import { FcGoogle } from "react-icons/fc";
import { IoIosArrowForward } from "react-icons/io";



# Authentication Providers

SOLID supports multiple authentication methods through its provider system, offering flexibility in how users can sign up and log in to your application.

## Supported Providers

<div className="feature-grid">

  <div className="feature-card">
      <h4 className="card-title card-headear-wrapper ">
        <HiOutlineLockClosed size={20} style={{ marginRight: "10px" }} />
      Section Management
    </h4>
    <ul className="card-desc">
      <li>Traditional username/password</li>
      <li>Password policies</li>
      <li>Password reset flow</li>
      <li>Account recovery</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper ">
        <HiOutlineKey size={20} style={{ marginRight: "10px" }} />
      Section Management
    </h4>
    <ul className="card-desc">
      <li>Email-based OTP</li>
      <li>SMS-based OTP</li>
      <li>Time-based tokens</li>
      <li>Recovery codes</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper ">
        <HiOutlineGlobeAlt size={20} style={{ marginRight: "10px" }} />
      Section Management
    </h4>
1. **Google**
2. **Meta/Facebook**
3. **LinkedIn**
4. **Twitter/X**
5. **Custom OAuth providers**
  </div>

</div>

## Authentication Flow


  <h3 className=" card-headear-wrapper">
    <HiOutlineArrowsRightLeft size={22}  />

### Standard OAuth Flow
</h3>


#### 1. Frontend initiates auth:

```tsx
// Redirect to OAuth provider
window.location.href = "https://solid.website.com/api/iam/[provider]/connect";
```

#### 2. Backend handles callback:

```http
https://solid.website.com/api/iam/[provider]/connect/callback
```

#### 3. Provider redirects with code:

```http
http://website.com/connect/[provider]/callback?accessCode=[code]
```

#### 4. Frontend exchanges code:

```http
GET https://solid.website.com/api/iam/[provider]/auth?accessCode=[code]
```

#### 5. Backend returns JWT:

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

  <h3 className=" card-headear-wrapper">
    <HiOutlineLockClosed size={22}  />

### Standard OAuth Flow
</h3>

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

  <h3 className=" card-headear-wrapper">
    <HiOutlineKey size={22}  />

### OTP Provider
</h3>

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

  <h3 className=" card-headear-wrapper">
    <FcGoogle size={22}  />

### OAuth Provider (Google Example)
</h3>


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
  <h4 className="card-title card-headear-wrapper">
    <HiOutlineShieldCheck size={30} style={{ marginRight: "10px" }} />
    Multi-factor Authentication (MFA)
  </h4>
  <ul className="card-desc">
    <li>Enable/disable per user</li>
    <li>Multiple MFA methods</li>
    <li>Backup codes</li>
    <li>Remember device option</li>
  </ul>
</div>

<div className="feature-card">
  <h4 className="card-title card-headear-wrapper">
    <HiOutlineClock size={20} style={{ marginRight: "10px" }} />
    Session Management
  </h4>
  <ul className="card-desc">
    <li>JWT tokens</li>
    <li>Refresh tokens</li>
    <li>Token expiry</li>
    <li>Session invalidation</li>
  </ul>
</div>

<div className="feature-card">
  <h4 className="card-title card-headear-wrapper">
    <HiOutlineArrowPath size={20} style={{ marginRight: "10px" }} />
    Account Recovery
  </h4>
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
    <h4 className="card-title card-headear-wrapper">
      <HiOutlineLockClosed size={20} style={{ marginRight: "10px" }} />
      Password Security
    </h4>
    <ul className="card-desc">
      <li>Secure hashing (bcrypt)</li>
      <li>Password policies</li>
      <li>Brute force protection</li>
      <li>Password history</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <HiOutlineKey size={20} style={{ marginRight: "10px" }} />
      OAuth Security
    </h4>
    <ul className="card-desc">
      <li>State parameter</li>
      <li>PKCE support</li>
      <li>Scope validation</li>
      <li>Token validation</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <HiOutlineShieldExclamation size={20} style={{ marginRight: "10px" }} />
      General Security
    </h4>
    <ul className="card-desc">
      <li>Rate limiting</li>
      <li>IP blocking</li>
      <li>Audit logging</li>
      <li>Session monitoring</li>
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

```typescript
@Auth(AuthType.None)
@Controller("iam/google")
@ApiTags("Iam")
export class GoogleAuthenticationController {
  constructor(
    @Inject(iamConfig.KEY)
    private iamConfiguration: ConfigType<typeof iamConfig>,
    private readonly userService: UserService,
    private readonly authService: AuthenticationService
  ) {}

  @Public()
  @UseGuards(GoogleOauthGuard)
  @Get("connect")
  async connect() {
    this.validateConfiguration();
  }

  private validateConfiguration() {
    if (!isGoogleOAuthConfigured(this.iamConfiguration)) {
      throw new InternalServerErrorException("Google OAuth is not configured");
    }
  }

  @Public()
  @Get("connect/callback")
  @UseGuards(GoogleOauthGuard)
  googleAuthCallback(@Req() req: Request, @Res() res: Response) {
    this.validateConfiguration();
    const user = req.user;

    // console.log(`Found user: ${JSON.stringify(user)}`);
    // const token = await this.authService.signIn(req.user);
    //   res.cookie('access_token', token, {
    //     maxAge: 2592000000,
    //     sameSite: true,
    //     secure: false,
    //   });
    // return req.user;
    // return res;

    return res.redirect(
      `${this.iamConfiguration.googleOauth.redirectURL}?accessCode=${user["accessCode"]}`
    );
  }

  /**
   * This is just a dummy endpoint where we are passing in the accessCode, this will be configured in the .env as an environment variable and
   * will be passed the accessCode, using the accessCode the UI code on this page will mostly invoke the /iam/google/auth endpoint which will finally generate the JWT token.
   *
   * @param accessCode
   * @returns
   */
  @Public()
  @Get("dummy-redirect")
  async dummyGoogleAuthRedirect(@Query("accessCode") accessCode) {
    this.validateConfiguration();
    const user = await this.userService.findOneByAccessCode(accessCode);

    delete user["password"];

    return user;
  }

  /**
   * Use this endpoint to authenticate using an accessCode with Google.
   *
   * @param accessCode
   * @returns
   */
  @Public()
  @Get("authenticate")
  @ApiQuery({ name: "accessCode", required: true, type: String })
  async googleAuth(@Query("accessCode") accessCode) {
    this.validateConfiguration();
    return this.authService.signInUsingGoogle(accessCode);
  }
}
```



## Best Practices

  <details>
    <summary className="card-title card-headear-wrapper">
      <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
      Provider Selection
    </summary>
    <ul className="card-desc">
      <li>Consider user base</li>
      <li>Evaluate security needs</li>
      <li>Plan backup methods</li>
      <li>Test all flows</li>
    </ul>
  </details>

  <details>
    <summary className="card-title card-headear-wrapper">
      <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
      Configuration
    </summary>
    <ul className="card-desc">
      <li>Secure credentials</li>
      <li>Set proper timeouts</li>
      <li>Configure rate limits</li>
      <li>Enable logging</li>
    </ul>
  </details>

  <details>
    <summary className="card-title card-headear-wrapper">
      <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
      User Experience
    </summary>
    <ul className="card-desc">
      <li>Clear error messages</li>
      <li>Simple recovery flows</li>
      <li>Multiple auth options</li>
      <li>Remember user preferences</li>
    </ul>
  </details>

  <details>
    <summary className="card-title card-headear-wrapper">
      <IoIosArrowForward  size={20} style={{ marginRight: "8px" }}  className="rotatable"  />
      Security
    </summary>
    <ul className="card-desc">
      <li>Regular audits</li>
      <li>Monitor failed attempts</li>
      <li>Review permissions</li>
      <li>Update configurations</li>
    </ul>
  </details>


---
sidebar_position: 5
title: IAM
---

import { FaUser, FaUsersCog, FaDatabase, FaUserShield, FaKey, FaLock, FaSignInAlt, FaRegLightbulb,FaShieldAlt,FaShieldVirus,FaUserCog } from "react-icons/fa";
import { IoIosArrowForward } from "react-icons/io";


# IAM

SOLID's IAM system provides comprehensive user, role, and permission management to secure your application.

## Overview

The IAM system consists of several key components:

- User management
- Role-based access control (RBAC)
- Permission management
- Record-level security
- Authentication providers

## Components

### [Users](./users.md)

<div className="border-box">
  <h4 className="card-title card-headear-wrapper">
      <FaUser size={15} style={{ marginRight: "10px" }} />
      Manage user accounts and profiles:
    </h4>
   - User creation and invitation
   - Profile management
   - Account settings
   - Access control
</div>

### [Roles](./roles.md)

<div className="border-box">
  <h4 className="card-title card-headear-wrapper">
      <FaUsersCog size={15} style={{ marginRight: "10px" }} />
      Define and manage user roles:
    </h4>
    - Role creation
    - Permission assignment
    - Role hierarchy
    - Access levels
</div>

### [Permissions](./permissions.md)

<div className="border-box">
    <h4 className="card-title card-headear-wrapper">
      <FaKey size={15} style={{ marginRight: "10px" }} />
      Control access to system features:
    </h4>
     - Automatic permission discovery
     - Permission grouping
     - Custom permissions
     - Permission inheritance
</div>

### [Record Rules](./record-rules.md)

<div className="border-box">
    <h4 className="card-title card-headear-wrapper">
      <FaDatabase size={15} style={{ marginRight: "10px" }} />
      Configure data-level security:
    </h4>
     - Record-level access control
     - Dynamic rules
     - User-based filters
     - Role-based filters
</div>

### [Authentication Providers](/docs/developer-docs/rest-apis/authentication/oauth-authentication/)


<div className="border-box">
    <h4 className="card-title card-headear-wrapper">
      <FaLock size={15} style={{ marginRight: "10px" }} />
      Multiple authentication methods:
    </h4>
      - Password-based
      - OTP (passwordless)
      - OAuth providers:
        - Google
        - Meta/Facebook
        - LinkedIn
        - Twitter/X
      - Custom providers 
</div>

## Key Features
<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaUserCog size={15} style={{ marginRight: "10px" }} />
      User Management  
    </h4>
    <ul className="card-desc">
      <li>User registration</li>
      <li>Profile management</li>
      <li>Password policies</li>
      <li>Account recovery</li>
      <li>Session management</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaShieldAlt size={15} style={{ marginRight: "10px" }} />
      Access Control  
    </h4>
    <ul className="card-desc">
      <li>Role-based access</li>
      <li>Permission management</li>
      <li>Record-level security</li>
      <li>API authentication</li>
      <li>Token management</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaLock size={15} style={{ marginRight: "10px" }} />
      Authentication  
    </h4>
    <ul className="card-desc">
      <li>Multiple auth methods</li>
      <li>Social login</li>
      <li>Two-factor auth</li>
      <li>Single sign-on</li>
      <li>JWT tokens</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaShieldVirus size={15} style={{ marginRight: "10px" }} />
      Security Features  
    </h4>
    <ul className="card-desc">
      <li>Password hashing</li>
      <li>Session management</li>
      <li>Token expiration</li>
      <li>Audit logging</li>
      <li>Security policies</li>
    </ul>
  </div>

</div>

## Best Practices
<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    User Management
  </summary>
  <ul className="card-desc">
    <li>Implement strong password policies</li>
    <li>Enable account recovery</li>
    <li>Monitor user activity</li>
    <li>Regular access reviews</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Role Design
  </summary>
  <ul className="card-desc">
    <li>Follow principle of least privilege</li>
    <li>Create role hierarchies</li>
    <li>Document role purposes</li>
    <li>Regular role audits</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Permissions
  </summary>
  <ul className="card-desc">
    <li>Group related permissions</li>
    <li>Regular permission reviews</li>
    <li>Document permission usage</li>
    <li>Monitor permission changes</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Security
  </summary>
  <ul className="card-desc">
    <li>Enable audit logging</li>
    <li>Monitor failed logins</li>
    <li>Regular security reviews</li>
    <li>Incident response plan</li>
  </ul>
</details>

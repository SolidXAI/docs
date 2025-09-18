---
title: Seeding and Metadata
description: Overview of how the database is initialized with metadata in SolidX.
sidebar_position: 4
---

import { 
  FaKey, FaDatabase, FaPuzzlePiece, FaUserShield, FaUsers, FaEye, FaPlayCircle, FaBars, FaEnvelope, FaSms, FaSlidersH, FaShieldAlt, FaList, FaChartBar 
} from "react-icons/fa";


#  Seeding the Database

Seeding is the process of initializing the database with the **essential metadata and data** required for the application to function correctly.

>  The result of the seeding step is a **fully functional database** with all necessary metadata populated.

---

##  Running the seed Command

To run the seeding process, execute the following command in the `solid-api` directory:

```bash
solid seed
```

This command triggers the `ModuleMetadataSeederService`, provided by the [`@solidstarters/solid-core`](https://www.npmjs.com/package/@solidstarters/solid-core) package.  
It is responsible for populating all the necessary metadata into the database.

---

## What Gets Seeded?

The following metadata is populated during the seeding process:

<h4 className="card-title card-headear-wrapper">
  <FaKey size={16} style={{ marginRight: "2px" }} />

### Permissions
</h4>

- Permission names are derived from the controller and controller method names.
- Example: `UserController.findMany`, `MenuItemMetadataController.findMany`

<h4 className="card-title card-headear-wrapper">
    <FaDatabase size={16} style={{ marginRight: "2px" }} />

### Media Storage Providers
</h4>

  - Sets up providers used for storing media files.
  - Default providers include:
    - `default-filesystem`: For local file storage.

<h4 className="card-title card-headear-wrapper">
  <FaPuzzlePiece size={16} style={{ marginRight: "2px" }} />

### System Fields Metadata
</h4>

- All the system models and fields are defined in the solid-core-metadata.json file provided by the `@solidstarters/solid-core` package.
- The above configuration gets seeded as part of this step

<h4 className="card-title card-headear-wrapper">
  <FaPuzzlePiece size={16} style={{ marginRight: "2px" }} />

### Functional Modules Metadata
</h4>

- Reads from JSON files to seed metadata per functional module (e.g. fees portal, temple portal).

<h4 className="card-title card-headear-wrapper">
  <FaUserShield size={16} style={{ marginRight: "2px" }} />

### Roles
</h4>

- Creates default roles like:
  - `Admin`: With all permissions.
  - `Internal User`: With the necessary technical permissions. All users created in SolidX are assigned this role.
- Other custom roles are created but require manual permission assignment post-login.

<h4 className="card-title card-headear-wrapper">
  <FaUsers size={16} style={{ marginRight: "2px" }} />

### Users
</h4>

- Seeds default users as specified in metadata.
- Users are prompted to **change their passwords** on first login.

<h4 className="card-title card-headear-wrapper">
  <FaEye size={16} style={{ marginRight: "2px" }} />

### Views
</h4>

- User interface components are created based on metadata.

<h4 className="card-title card-headear-wrapper">
  <FaPlayCircle size={16} style={{ marginRight: "2px" }} />

### Actions
</h4>

- Links views to functionalities using action definitions.

<h4 className="card-title card-headear-wrapper">
  <FaBars size={16} style={{ marginRight: "2px" }} />

### Menus
</h4>

- Sets up navigation menus for the app.

<h4 className="card-title card-headear-wrapper">
  <FaEnvelope size={16} style={{ marginRight: "2px" }} />

### Email Templates
</h4>

- Initializes default email templates for notifications.

<h4 className="card-title card-headear-wrapper">
  <FaSms size={16} style={{ marginRight: "2px" }} />

### SMS Templates
</h4>

- Populates SMS templates for messaging services.

<h4 className="card-title card-headear-wrapper">
  <FaSlidersH size={16} style={{ marginRight: "2px" }} />

### Settings
</h4>

- Seeds default application-level configurations.

<h4 className="card-title card-headear-wrapper">
  <FaShieldAlt size={16} style={{ marginRight: "2px" }} />

### Security Rules
</h4>

- Establishes access rules for different models and roles.

<h4 className="card-title card-headear-wrapper">
  <FaList size={16} style={{ marginRight: "2px" }} />

### List of Values
</h4>

- Predefined value lists used across the app (e.g., dropdowns).

<h4 className="card-title card-headear-wrapper">
  <FaChartBar size={16} style={{ marginRight: "2px" }} />

### Dashboards
</h4>

- Dashboard configuration providing visual summaries and KPIs

---

##  Summary

The seeding process is **essential for bootstrapping** a SolidX instance with all necessary metadata.  
Make sure to verify seeded users and assign proper permissions for any additional roles.


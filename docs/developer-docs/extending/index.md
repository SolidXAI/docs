---
title: Extending SolidX
description: Guide to extending SolidX with custom code generation and frontend/backend customization.
sidebar_position: 5
---

import { FaCode, FaDesktop, FaServer } from "react-icons/fa";

# Extending SolidX

This section outlines how to extend **SolidX** to build your own functional modules, such as a `school-fees-portal`.

SolidX offers a **powerful code generation tool** that enables rapid scaffolding of new modules with all the essential boilerplate. This accelerates your development by letting you focus directly on your specific **business logic**, without worrying about foundational setup.

In addition to scaffolding, SolidX supports **deep customization** across both frontend and backend layers. You can tailor UI components, introduce new features, or adjust the behavior of existing elements to match your application's needs.



## Customization Capabilities

SolidX provides the following extensibility features:

<div className="border-box">

<h4 className="card-title card-headear-wrapper">
  <FaCode size={18} style={{ marginRight: "2px" }} />

### Generated Code

</h4>

- Quickly scaffold new modules using the SolidX code generation tool.
- Auto-generates:
  - Controllers
  - Services
  - Entitities
  - Data Transfer Objects
  - Layout JSON files (for UI configuration)
- The default layout supports:
  - List View
  - Form View

</div>
<br/>
<div className="border-box">

<h4 className="card-title card-headear-wrapper">
  <FaDesktop size={18} style={{ marginRight: "2px" }} />

### Frontend Customization

</h4>

- Modify the generated `layout.json` to:
  - Customize list views
  - Tailor form layouts
  - Configure kanban boards
  - Add custom UI behaviors

</div>

<br/>

<div className="border-box">

<h4 className="card-title card-headear-wrapper">
  <FaServer size={18} style={{ marginRight: "2px" }} />

### Backend Customization

</h4>

- Extend the NestJS backend by adding:
  - Custom services and controllers
  - Computed providers
  - Middleware or interceptors
  - Business-specific logic

</div>

<br/>

By leveraging these capabilities, you can build modular, scalable, and highly customized applications using the SolidX framework.

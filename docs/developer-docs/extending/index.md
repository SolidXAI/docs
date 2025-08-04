---
title: Extending SolidX
description: Guide to extending SolidX with custom code generation and frontend/backend customization.
sidebar_position: 5
---

# 🧩 Extending SolidX

This section outlines how to extend **SolidX** to build your own functional modules, such as a `school-fees-portal`.

SolidX offers a **powerful code generation tool** that enables rapid scaffolding of new modules with all the essential boilerplate. This accelerates your development by letting you focus directly on your specific **business logic**, without worrying about foundational setup.

In addition to scaffolding, SolidX supports **deep customization** across both frontend and backend layers. You can tailor UI components, introduce new features, or adjust the behavior of existing elements to match your application's needs.

---

## 🔧 Customization Capabilities

SolidX provides the following extensibility features:

### ⚙️ Generated Code

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

### 🎨 Frontend Customization

- Modify the generated `layout.json` to:
  - Customize list views
  - Tailor form layouts
  - Configure kanban boards
  - Add custom UI behaviors

### 🛠 Backend Customization

- Extend the NestJS backend by adding:
  - Custom services and controllers
  - Computed providers
  - Middleware or interceptors
  - Business-specific logic

---

By leveraging these capabilities, you can build modular, scalable, and highly customized applications using the SolidX framework.

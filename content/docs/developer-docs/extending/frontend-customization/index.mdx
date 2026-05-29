---
title: Frontend
icon: "palette"
description: Catalog of frontend customization patterns in SolidX.
summary: "Entry point for metadata-driven extensions and bespoke frontend UIs in SolidX, including module-based file-location rules, manifest registration patterns, and API-call conventions."
---

## Frontend Customization Catalog

Use this section as the source of truth for where each customization type belongs and how it should be wired in the UI module system.

<Callout type="info" title="Mental Model">

  The SolidX frontend is designed so that custom UI code stays close to the module that owns the business feature.
    Instead of scattering custom screens, reducers, and extension widgets across the app, the convention keeps each feature grouped together.
  - Use metadata-driven extensions when you are augmenting generated admin screens.
    - Use bespoke UI when you need full route-level control.
    - Keep ownership module-local so discovery, registration, and maintenance stay predictable.
  So the intuition is: <strong>the UI stays flexible because SolidX combines generated structure with module-owned custom code</strong>.

</Callout>

## UI Module Convention

In the current SolidX frontend model, custom frontend code should be organized inside module folders under `solid-ui/src/<module-name>/`.

Recommended structure:

```text
solid-ui/src/
  <module-name>/
    admin-layout/
    custom-layout/
    redux/
    <module-name>.ui-module.ts
```

Use these responsibilities:

- `admin-layout/` for metadata-driven admin extensions such as buttons, event handlers, and widgets
- `custom-layout/` for bespoke route-level UIs and custom application shells
- `redux/` for module-owned RTK Query APIs, reducers, and middleware
- `<module-name>.ui-module.ts` as the manifest that registers routes, extension components, extension functions, reducers, and middleware

`AppRoutes.tsx` should live beside `App.tsx` at `solid-ui/src/AppRoutes.tsx`, and should consume aggregated module routes rather than manually registering every feature route inline.

### Core API Convention

For extension/frontend API calls, use Solid HTTP helpers from `@solidxai/core-ui`:

- `solidGet`
- `solidPost`
- `solidPut`
- `solidPatch`
- `solidDelete`
- `solidAxios`

Use endpoint paths like `/resource` and do not hardcode `/api` in request paths.

### Extension Component Types

- [Form View Buttons](./form-view-buttons.md)
- [List View Buttons](./list-view-buttons.md)
- [Extension UI Guidelines](./extension-ui-guidelines.md)
- [Custom Widgets](./custom-widgets.md)
- [Form View Field Widgets](./form-view-field-widgets.md)
- [List View Field Widgets](./list-view-field-widgets.md)
- [Kanban Card Widgets](./kanban-card-widget.md)

### Extension Function Types

- [Form View Events](./form-view-events.md)
- [List View Events](./list-view-events.md)
- [Layout Manager](./layout-manager.md)

### Bespoke UI

Use [Bespoke Frontend UI](./bespoke-frontend-ui.md) for full route-level UIs under `solid-ui/src/<module-name>/custom-layout/...`.

### Supporting APIs

- [Solid HTTP API](./solid-http-api.md)
- [Redux Module Integration](./redux-module-integration.md)
- [Solid Entity API](./solid-entity-api.md)
- [List View API](./list-view-api.md)
- [Layout Manager](./layout-manager.md)

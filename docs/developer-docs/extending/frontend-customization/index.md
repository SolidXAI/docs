---
title: Frontend Customization
description: Catalog of frontend customization patterns in SolidX.
summary: Entry point for metadata-driven extensions and bespoke frontend pages in SolidX, including file-location rules, registration patterns, and API-call conventions.
sidebar_position: 3
---

## Frontend Customization Catalog

Use this section as the source of truth for where each customization type belongs and how it should be wired.

### Core API Convention

For extension/frontend API calls, use Solid HTTP helpers from `@solidxai/core-ui`:

- `solidGet`
- `solidPost`
- `solidPut`
- `solidPatch`
- `solidDelete`
- `solidAxios`

Use endpoint paths like `/resource` and do not hardcode `/api` in request paths.

### Extension Types

- [Form View Buttons](./form-view-buttons.md)
- [Form View Events](./form-view-events.md)
- [List View Buttons](./list-view-buttons.md)
- [List View Events](./list-view-events.md)
- [Extension UI Guidelines](./extension-ui-guidelines.md)
- [Custom Widgets](./custom-widgets.md)
- [Form View Field Widgets](./form-view-field-widgets.md)
- [List View Field Widgets](./list-view-field-widgets.md)
- [Kanban Field Widgets](./kanban-field-widgets.md)

### Bespoke UI

Use [Bespoke Frontend UI](./bespoke-frontend-ui.md) for full route-level pages under `solid-ui/src/pages/<layout-reference>/...`.

### Supporting APIs

- [Solid HTTP API](./solid-http-api.md)
- [Solid Entity API](./solid-entity-api.md)
- [List View API](./list-view-api.md)
- [Layout Manager](./layout-manager.md)

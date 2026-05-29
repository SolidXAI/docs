---
title: Custom Views
icon: "layout-grid"
description: Clarifies how to choose between metadata-driven custom widgets and bespoke route-level pages.
summary: "Clarifies how to choose between metadata-driven custom UI in `admin-layout` and bespoke route-level UI in `custom-layout`. Includes module-based location, manifest registration, and API usage conventions."
keywords: [custom views, frontend customization, custom widgets, custom pages]
solidx_concerns: [frontend.custom_pages, add_full_custom_ui, create_custom_widget]
---

## Overview

In older discussions, "custom view" is used for two different patterns:

1. Metadata-driven custom UI blocks inside form/list layouts.
2. Fully bespoke route pages with independent layout/navigation.

Use the correct implementation path below.

## Decision Guide

### Use Custom Widget (metadata-driven form-view block)

Choose this when UI is rendered inside an existing form-view layout node with `type: "custom"` and should remain inside the generated Solid form flow.

- Location: `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/`
- Registration: `<module-name>.ui-module.ts` via `extensionComponents`
- Metadata wiring: layout JSON `type: "custom"`, `attrs.widget: "<registered-name>"`

Use this path for:

- form-view custom widgets rendered through `type: "custom"`
- form buttons
- list buttons
- row actions
- field widgets
- kanban card widgets

### Use Custom Page (bespoke routing)

Choose this when you need a dedicated page shell, route group, or custom navigation unrelated to metadata widgets.

- Location: `solid-ui/src/<module-name>/custom-layout/<layout-reference>/...`
- Route wiring: register route trees in `<module-name>.ui-module.ts` under `routes.extraRoutes`
- App wiring: keep `solid-ui/src/AppRoutes.tsx` thin and let it consume `solidUiModuleRuntime.routes`
- Do not place full custom pages under `solid-ui/src/<module-name>/admin-layout/...`

See [Bespoke Frontend UI](./bespoke-frontend-ui.md) for the full route-level pattern.

## API Convention for Both Paths

For frontend API calls, Solid supports both of these patterns:

1. Direct Solid HTTP helpers from `@solidxai/core-ui`
2. Module-owned Redux / RTK Query integration under `solid-ui/src/<module-name>/redux/`

### Option A: Solid HTTP Helpers

Use:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Guidelines:

- Pass endpoint paths like `/resource` (no hardcoded `/api` prefix).
- Prefer context data (`params`, `formik.values`, route params) instead of hardcoded IDs.
- Handle loading, success, and error explicitly.
- For filter-heavy requests, use `qs.stringify(..., { encodeValuesOnly: true })` or Axios `params`.

### Option B: Redux / RTK Query

If the consuming app prefers store-backed integration, place RTK Query APIs under:

```text
solid-ui/src/<module-name>/redux/
```

Then register reducers and middleware in `<module-name>.ui-module.ts`.

Choose this when you want:

- shared API state
- caching and invalidation
- generated hooks
- a more structured app-wide API layer

See [Redux Module Integration](./redux-module-integration.md) for the full pattern.

## Example: Metadata Custom Widget

```tsx
import { solidGet } from "@solidxai/core-ui";
import { useEffect, useState } from "react";
import type { SolidFormWidgetProps } from "@solidxai/core-ui";

export function BookSimilarTitles({ formData }: SolidFormWidgetProps) {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const title = formData?.title;
    if (!title) return;

    const run = async () => {
      setLoading(true);
      try {
        const query = encodeURIComponent(String(title));
        const resp = await solidGet(`/books/similar?title=${query}`);
        setRows(resp?.data?.data?.records || []);
      } finally {
        setLoading(false);
      }
    };

    run();
  }, [formData?.title]);

  if (loading) return <div>Loading...</div>;
  return <div>Found: {rows.length}</div>;
}
```

Registration:

```ts
import { ExtensionComponentTypes, type SolidUiModule } from "@solidxai/core-ui";
import { BookSimilarTitles } from "./admin-layout/book/extension-components/BookSimilarTitles";

const libraryUiModule = {
  name: "library",
  extensionComponents: [
    {
      name: "BookSimilarTitles",
      component: BookSimilarTitles,
      type: ExtensionComponentTypes.formWidget,
    },
  ],
} satisfies SolidUiModule;

export default libraryUiModule;
```

Layout usage:

```json
{
  "type": "custom",
  "attrs": {
    "name": "book-similar-widget",
    "widget": "BookSimilarTitles"
  }
}
```

## See Also

- [Custom Widgets](./custom-widgets.md)
- [Bespoke Frontend UI](./bespoke-frontend-ui.md)
- [Solid HTTP API](./solid-http-api.md)
- [Redux Module Integration](./redux-module-integration.md)

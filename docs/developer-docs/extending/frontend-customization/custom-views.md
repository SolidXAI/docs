---
title: Custom Views (Legacy Term)
description: Clarifies how to choose between metadata-driven custom widgets and bespoke route-level pages.
summary: Legacy "custom views" requests should be implemented either as form/list custom widgets in `src/extensions` or as bespoke pages in `src/pages`. Includes location, registration, and API usage conventions.
keywords: [custom views, frontend customization, custom widgets, custom pages]
sidebar_position: 6
solidx_concerns: [frontend.custom_pages, add_full_custom_ui, create_custom_widget]
---

## Overview

In older discussions, "custom view" is used for two different patterns:

1. Metadata-driven custom UI blocks inside form/list layouts.
2. Fully bespoke route pages with independent layout/navigation.

Use the correct implementation path below.

## Decision Guide

### Use Custom Widget (metadata-driven)

Choose this when UI is rendered inside an existing form/list layout node (`type: custom`) and should remain inside the generated Solid view flow.

- Location: `solid-ui/src/extensions/<module-name>/<model-name>/custom-widgets/`
- Registration: `solid-ui/src/extensions/solid-extensions.ts` via `registerExtensionComponent(...)`
- Metadata wiring: layout JSON `type: "custom"`, `attrs.widget: "<registered-name>"`

### Use Custom Page (bespoke routing)

Choose this when you need a dedicated page shell, route group, or custom navigation unrelated to metadata widgets.

- Location: `solid-ui/src/pages/<layout-reference>/...`
- Route wiring: `solid-ui/src/routes/AppRoutes.tsx` via `getSolidRoutes({ extraRoutes })`
- Do not place full custom pages under `solid-ui/src/extensions/...`

See [Bespoke Frontend UI](./bespoke-frontend-ui.md) for the full route-level pattern.

## API Convention for Both Paths

For frontend API calls, use Solid HTTP helpers from `@solidxai/core-ui`:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Guidelines:

- Pass endpoint paths like `/resource` (no hardcoded `/api` prefix).
- Prefer context data (`params`, `formik.values`, route params) instead of hardcoded IDs.
- Handle loading, success, and error explicitly.
- For filter-heavy requests, use `qs.stringify(..., { encodeValuesOnly: true })` or Axios `params`.

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
import { registerExtensionComponent } from "@solidxai/core-ui";
import { BookSimilarTitles } from "./library/book/custom-widgets/BookSimilarTitles";

registerExtensionComponent("BookSimilarTitles", BookSimilarTitles);
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

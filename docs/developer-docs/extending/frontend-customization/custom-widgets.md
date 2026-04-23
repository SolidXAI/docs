---
sidebar_position: 2
title: Custom Widgets
description: Build and register form-view custom widgets in SolidX.
summary: "Defines where form-view custom widgets should live in the UI module system, how to register them in `<module-name>.ui-module.ts`, how to wire them through `type: \"custom\"` layout nodes, and how to use Solid API helpers safely inside widget logic."
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_widget]
---


## Overview

Custom widgets in SolidX are form-view extension components rendered through layout nodes with:

```json
{
  "type": "custom"
}
```

Use them when you want a targeted custom UI block inside a generated form view.

This page is specifically about form-view `custom` nodes. It is not the reference page for:

- form buttons
- list buttons
- row actions
- field widgets
- kanban card widgets

## Location and Registration

For model-scoped widgets, use:

- `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/`

Register them in the owning module manifest:

- `solid-ui/src/<module-name>/<module-name>.ui-module.ts`

with:

```ts
import { ExtensionComponentTypes, type SolidUiModule } from "@solidxai/core-ui";
import { MyCustomWidget } from "./admin-layout/book/extension-components/MyCustomWidget";

const libraryUiModule = {
  name: "library",
  extensionComponents: [
    {
      name: "MyCustomWidget",
      component: MyCustomWidget,
      type: ExtensionComponentTypes.formWidget,
    },
  ],
} satisfies SolidUiModule;

export default libraryUiModule;
```


## Layout Wiring

Reference your registered widget in form-view layout metadata:

```json
{
  "type": "custom",
  "attrs": {
    "name": "book-custom-1",
    "widget": "MyCustomWidget"
  }
}
```

## Props Contract

Custom widgets receive a `SolidFormWidgetProps`-style payload in form contexts, including:

- `field`
- `formData`
- `viewMetadata`
- `fieldsMetadata`
- `formViewData`

Always derive context from incoming props (for example `formData`, `field`, or metadata) instead of hardcoded values.

## API Calls in Widgets

When widgets need backend calls, Solid supports both of these patterns:

1. Direct Solid HTTP helpers from `@solidxai/core-ui`
2. Module-owned Redux / RTK Query integration under `solid-ui/src/<module-name>/redux/`

### Option A: Solid HTTP Helpers

Use:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Guidelines:

- Use endpoint paths like `/resource` (no hardcoded `/api`).
- Handle loading/error state explicitly in component logic.
- For list/filter requests, use `qs.stringify(..., { encodeValuesOnly: true })` or Axios `params`.
- Use context IDs/values from props instead of constants.

### Option B: Redux / RTK Query

If the app prefers store-backed integration, keep RTK Query APIs in the owning module's `redux/` folder and register the module's reducers and middleware in `<module-name>.ui-module.ts`.

Choose this when you want shared API state, caching, invalidation, and generated hooks.

See [Redux Module Integration](./redux-module-integration.md) for the full pattern.

## Example

```tsx
import { useEffect, useState } from "react";
import { solidGet } from "@solidxai/core-ui";
import type { SolidFormWidgetProps } from "@solidxai/core-ui";

export function TitleStatsWidget({ formData }: SolidFormWidgetProps) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const title = String(formData?.title || "");
    setCount(title.length);
  }, [formData?.title]);

  return <span>Title length: {count}</span>;
}

export async function loadTitleHints(query: string) {
  const resp = await solidGet("/title-hints", { params: { query } });
  return resp?.data?.data?.records || [];
}
```

## See Also

- [Form View Field Widgets](./form-view-field-widgets.md)
- [List View Field Widgets](./list-view-field-widgets.md)
- [Form View Events](./form-view-events.md)
- [Extension UI Guidelines](./extension-ui-guidelines.md)
- [Solid HTTP API](./solid-http-api.md)
- [Redux Module Integration](./redux-module-integration.md)

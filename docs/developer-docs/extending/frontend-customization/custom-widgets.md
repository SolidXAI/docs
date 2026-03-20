---
sidebar_position: 2
title: Custom Widgets
description: Build and register metadata-driven custom widgets in SolidX.
summary: Defines where custom widgets should live, how to register them, how to wire them in layout metadata, and how to use Solid API helpers safely inside widget logic.
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_widget]
---

## Overview

Custom widgets are metadata-driven extension components rendered from layout nodes such as `type: "custom"`.

Use them when you want targeted UI enhancements inside generated form/list views.

## Location and Registration

For model-scoped widgets, use:

- `solid-ui/src/extensions/<module-name>/<model-name>/custom-widgets/`

Register in:

- `solid-ui/src/extensions/solid-extensions.ts`

with:

```ts
import { registerExtensionComponent } from "@solidxai/core-ui";
registerExtensionComponent("MyCustomWidget", MyCustomWidget);
```

## Layout Wiring

Reference your registered widget in layout metadata:

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

Custom form widgets typically receive a `SolidFormWidgetProps`-style payload, including:

- `field`
- `formData`
- `viewMetadata`
- `fieldsMetadata`
- `formViewData`

Always derive context from incoming props (for example `formData` or metadata) instead of hardcoded values.

## API Calls in Widgets

When widgets need backend calls, use Solid HTTP helpers from `@solidxai/core-ui`:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Guidelines:

- Use endpoint paths like `/resource` (no hardcoded `/api`).
- Handle loading/error state explicitly in component logic.
- For list/filter requests, use `qs.stringify(..., { encodeValuesOnly: true })` or Axios `params`.
- Use context IDs/values from props instead of constants.

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

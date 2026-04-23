---
sidebar_position: 8
title: Layout Manager
description: Use SolidViewLayoutManager for safe runtime layout mutation in frontend listeners.
summary: "Documents runtime layout updates using `SolidViewLayoutManager` in form and list event handlers, including the return flag contracts required for UI updates to be applied."
solidx_concerns: [frontend.extensions.form_event_listeners, frontend.extensions.list_event_listeners]
---

## Overview

`SolidViewLayoutManager` should be the default utility for runtime layout mutation in frontend event handlers.

Use it instead of deep-mutating raw layout objects.

## Where It Is Used

Typical locations in the UI module system:

- `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-functions/`

Typical event hooks:

- form listeners such as `onFormLoad`, `onFieldChange`, and `onFieldBlur`
- list listeners such as `onBeforeListDataLoad` and `onListLoad` when layout updates are needed

## Form Example

```ts
import { SolidViewLayoutManager } from "@solidxai/core-ui";

export function handleBookFormEvents(event: any) {
  if (event.type !== "onFormLoad") return {};

  const manager = new SolidViewLayoutManager(event.viewMetadata.layout);
  manager.updateNodeAttributes("advanced-section", { visible: false });

  return {
    layoutChanged: true,
    newLayout: manager.getLayout(),
  };
}
```

## List Example

```ts
import { SolidViewLayoutManager } from "@solidxai/core-ui";

export function handleBookListEvents(event: any) {
  if (event.type !== "onListLoad") return {};

  const manager = new SolidViewLayoutManager(event.listViewLayout);
  manager.updateNodeAttributes("internal-score-column", { visible: false });

  return {
    layoutChanged: true,
    newLayout: manager.getLayout(),
  };
}
```

## Required Return Flags

Without flags, changes are ignored by the runtime.

- layout mutation: return `layoutChanged: true` with `newLayout`
- data mutation: return `dataChanged: true` with full `newFormData` or `newListData`
- filter override for list prefetch: return `filterApplied: true` with `newFilter`

## Safety Guidance

- Ensure node IDs exist before update operations.
- Keep mutations deterministic.
- For frequent events such as `onFieldChange`, avoid heavy synchronous logic.

## See Also

- [Form View Events](./form-view-events.md)
- [List View Events](./list-view-events.md)

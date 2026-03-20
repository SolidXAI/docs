---
sidebar_position: 8
title: Layout Manager
description: Use SolidViewLayoutManager for safe runtime layout mutation in frontend listeners.
summary: Documents runtime layout updates using SolidViewLayoutManager in form/list event handlers, including return flag contracts required for UI updates to be applied.
solidx_concerns: [frontend.extensions.form_event_listeners, frontend.extensions.list_event_listeners]
---

## Overview

`SolidViewLayoutManager` should be the default utility for runtime layout mutation in extension listeners.

Use it instead of deep-mutating raw layout objects.

## Where It Is Used

- Form listeners (`onFormLoad`, `onFieldChange`, `onFieldBlur`)
- List listeners (`onBeforeListDataLoad`, `onListLoad`) when layout updates are needed

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

- Layout mutation: return `layoutChanged: true` with `newLayout`
- Data mutation: return `dataChanged: true` with full `newFormData` or `newListData`
- Filter override (list prefetch): return `filterApplied: true` with `newFilter`

## Safety Guidance

- Ensure node IDs exist before update operations.
- Keep mutations deterministic.
- For frequent events (for example `onFieldChange`), avoid heavy synchronous logic.

## See Also

- [Form View Events](./form-view-events.md)
- [List View Events](./list-view-events.md)

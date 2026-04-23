---
sidebar_position: 5
title: List View API
description: Learn how to access and control SolidX list views programmatically from external components.
summary: "Documents how SolidX exposes list view handles through `listViewRegistry` for external usage. Covers `getListView`, `getRegisteredListViewIds`, list ID format, `SolidListViewHandle` methods, and practical integration patterns."
solidx_concerns: [frontend.extensions.list_buttons, frontend.extensions.row_buttons, frontend.custom_pages, add_list_header_button_with, add_list_row_button_with, create_custom_widget]
---

## Overview

SolidX exposes a programmatic List View API so external components can control an active list page.

Typical callers now include:

- module-owned list buttons under `admin-layout`
- custom widgets under `admin-layout`
- bespoke route UIs under `custom-layout`

This API is exposed through:

- `listViewRegistry`
- `getListView(listId)`
- `getRegisteredListViewIds()`
- `SolidListViewHandle`

## Source of Truth

Implementation references:

- `src/routes/pages/admin/core/ListPage.tsx`
- `src/components/core/list/listViewRegistry.ts`
- `src/components/core/list/SolidListView.tsx`

## How List Views Are Exposed

`ListPage.tsx` creates a list ID and registers the list handle on mount:

```ts
const listId = `page:${moduleName}:${modelName}:${menuItemId}:${menuItemName}:${actionId}:${actionName}`;
registerListView(listId, handle);
```

It unregisters on unmount:

```ts
unregisterListView(listId);
```

Important details:

- `modelName` is camel-cased in `ListPage`
- `menuItemId`, `menuItemName`, `actionId`, and `actionName` are part of the ID
- treat list IDs as fully-qualified keys and use exact matching

## Registry API

```ts
import { getListView, getRegisteredListViewIds } from "@solidxai/core-ui";
```

Available functions:

- `getListView(listId)`
- `getRegisteredListViewIds()`
- `hasListView(listId)`

## `SolidListViewHandle` API

```ts
type SolidListViewHandle = {
  refresh: () => void;
  clearFilters: () => void;
  applyFilter: (filter: {
    custom_filter_predicate?: any;
    search_predicate?: any;
    saved_filter_predicate?: any;
    predefined_search_predicate?: any;
  }) => void;
  setPagination: (nextFirst: number, nextRows: number) => void;
  setSort: (nextMultiSortMeta: { field: string; order: 1 | -1 }[]) => void;
  setShowArchived: (value: boolean) => void;
  getState: () => any;
};
```

## Typical External Usage

Pattern:

1. Read registered IDs.
2. Build the exact target `listId` from module, model, menu, and action context.
3. Resolve the handle via `getListView`.
4. Invoke handle APIs such as `applyFilter` or `refresh`.

Example:

```ts
import { getListView, getRegisteredListViewIds } from "@solidxai/core-ui";

const listIds = getRegisteredListViewIds();
const listId = "page:onboarding:applicationMaster:menu-123:Applications:action-456:open";
const listView = getListView(listId);

if (listView) {
  listView.applyFilter({
    custom_filter_predicate: {
      $and: [{ applicationNumber: { $in: matchingApplicationNumbers } }],
    },
  });
}
```

## Filter Shape Notes

`applyFilter(...)` accepts predicate buckets used by the list search pipeline:

- `custom_filter_predicate`
- `search_predicate`
- `saved_filter_predicate`
- `predefined_search_predicate`

## Troubleshooting

- list handle is `undefined` -> list may not be mounted yet or the ID does not match exactly
- no matching ID found -> inspect `getRegisteredListViewIds()` and verify every segment
- filter call has no effect -> verify predicate structure and target model field names
- wrong target list updated -> use exact `listId` matching only

## Related

- [List View Events](./list-view-events.md)
- [List View Buttons](./list-view-buttons.md)
- [Bespoke Frontend](./bespoke-frontend-ui.md)

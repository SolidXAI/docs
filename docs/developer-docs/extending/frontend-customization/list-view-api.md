---
sidebar_position: 5
title: List View API
description: Learn how to access and control SolidX list views programmatically from external components.
summary: Documents how SolidX exposes list view handles through `listViewRegistry` for external usage. Covers `getListView`, `getRegisteredListViewIds`, list ID format, `SolidListViewHandle` methods (`refresh`, `clearFilters`, `applyFilter`, `setPagination`, `setSort`, `setShowArchived`, `getState`), and practical integration patterns.
solidx_concerns: [frontend.extensions.list_buttons, frontend.extensions.row_buttons, frontend.custom_pages, add_list_header_button_with, add_list_row_button_with, create_custom_widget]
---

## Overview

SolidX exposes a programmatic List View API so external components (for example popup actions, custom buttons, or widgets) can control an active list page.

This API is exposed through:

- `listViewRegistry` (runtime registry of active list views)
- `getListView(listId)` (fetch one list handle)
- `getRegisteredListViewIds()` (inspect available list IDs)
- `SolidListViewHandle` (imperative methods on a list view instance)

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

- `modelName` is camel-cased in `ListPage`.
- `menuItemId`, `menuItemName`, `actionId`, and `actionName` are required parts of the ID.
- Treat list IDs as fully-qualified keys; use exact matching instead of partial matching.

## Registry API

```ts
import { getListView, getRegisteredListViewIds } from "@solidxai/core-ui";
```

Available functions:

- `getListView(listId)` -> returns `SolidListViewHandle | undefined`
- `getRegisteredListViewIds()` -> returns `string[]`
- `hasListView(listId)` -> boolean check (also exported)

## `SolidListViewHandle` API

`SolidListView` exposes these imperative methods:

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
  getState: () => {
    first: number;
    rows: number;
    multiSortMeta: { field: string; order: 1 | -1 }[];
    showArchived: boolean;
    filters: any;
    filterPredicates: any;
    listData: any[];
    totalRecords: number;
    loading: boolean;
  };
};
```

## Typical External Usage

Pattern:

1. Read registered IDs.
2. Build the exact target `listId` from module/model/menu/action context.
3. Resolve handle via `getListView`.
4. Invoke handle API (`applyFilter`, `refresh`, etc.).

Example:

```ts
import { getListView, getRegisteredListViewIds } from "@solidxai/core-ui";

const listIds = getRegisteredListViewIds();
const listId =
  "page:onboarding:applicationMaster:menu-123:Applications:action-456:open";
const listView = getListView(listId);

if (listView) {
  listView.applyFilter({
    custom_filter_predicate: {
      $and: [
        {
          applicationNumber: { $in: matchingApplicationNumbers },
        },
      ],
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

These are merged into list filters internally, then converted into request query.

## Troubleshooting

- List handle is `undefined` -> list may not be mounted yet, or ID does not match the exact module/model/menu/action context.
- No matching ID found -> inspect `getRegisteredListViewIds()` output and verify every segment of the composed ID.
- Filter call has no effect -> verify predicate structure and target model field names.
- Wrong target list updated -> use exact `listId` matching only.

## Related

- [List View Events](./list-view-events.md)
- [List View Buttons](./list-view-buttons.md)

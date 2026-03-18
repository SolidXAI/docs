---
sidebar_position: 4
title: List View Events
description: Learn how to create event listeners for list view events in your frontend application.
summary: Explains creating event listeners for SolidX list view events to extend frontend functionality. Covers supported events (`onBeforeListDataLoad`, `onListLoad`), registering handlers using `registerExtensionFunction`, event payload/response contracts, and updating filters, list data, or layout dynamically.
solidx_concerns: [frontend.extensions.list_event_listeners]
---

## Overview

List view function extensions let you hook into list lifecycle events in SolidX.

Use them to:

- Modify the outgoing list query/filter before API fetch
- Transform list records after they are loaded
- Adjust list layout dynamically at runtime

You author listener functions, register them with `registerExtensionFunction`, and reference them in your list view layout JSON.

## Supported Events

Based on `SolidListView.tsx`, list view supports these lifecycle events:

1. `onBeforeListDataLoad` - runs just before list API call. Best for filter/query shaping.
2. `onListLoad` - runs after list data is loaded. Best for data/layout transformation.

## Event Execution Behavior

Current list lifecycle flow:

1. List state is prepared (pagination, sort, filters, populate, locale, archived toggle).
2. `onBeforeListDataLoad` executes (if configured).
3. If the handler returns `filterApplied: true` with `newFilter`, that filter object is used for the API request.
4. List API request runs.
5. `onListLoad` executes (if configured) with fetched records.
6. If returned, `newListData` and/or `newLayout` are committed to state.

## Project Structure & File Paths

#### List Event Listeners

- Scope: list-view event listeners for a specific `<module, model>` pair.
- Mandatory listener location:
  - `solid-ui/src/extensions/<module-name>/<model-name>/list-event-listeners/`
- Do not place list-event listeners in generic folders when module/model is known.

Default file selection for list event changes:

1. Create or update a TS/TSX listener inside:
   - `solid-ui/src/extensions/<module-name>/<model-name>/list-event-listeners/`
2. Register the listener in:
   - `solid-ui/src/extensions/solid-extensions.ts`
3. Keep registration key aligned with layout metadata event references (`onBeforeListDataLoad`, `onListLoad`).

Example structure:

```bash
solid-ui/src/extensions/
├── solid-extensions.ts
└── library/
    └── book/
        └── list-event-listeners/
            └── bookListViewChangeHandler.ts
```

## Creating a Handler

Example with both events in one handler:

```ts
import type { SolidBeforeListDataLoad, SolidLoadList, SolidListUiEventResponse } from "@solidxai/core-ui";

const handleBookListViewChange = (
  event: SolidBeforeListDataLoad | SolidLoadList
): SolidListUiEventResponse => {
  // 1) Before fetch: enforce active-only records
  if (event.type === "onBeforeListDataLoad") {
    const nextFilter = structuredClone(event.filter || {});
    const existing = Array.isArray(nextFilter.$and) ? nextFilter.$and : [];

    nextFilter.$and = [...existing, { isActive: { $eq: true } }];

    return {
      filterApplied: true,
      newFilter: nextFilter,
    };
  }

  // 2) After fetch: annotate rows for UI usage
  if (event.type === "onListLoad") {
    const enriched = (event.listData || []).map((row: any) => ({
      ...row,
      _uiRisk: row.score >= 10 ? "high" : "normal",
    }));

    return {
      dataChanged: true,
      newListData: enriched,
    };
  }

  return {};
};

export default handleBookListViewChange;
```

## Registering the Handler

Register the listener with an alias in `solid-extensions.ts`:

```ts
import handleBookListViewChange from "./library/book/list-event-listeners/bookListViewChangeHandler";
import { registerExtensionFunction } from "@solidxai/core-ui";

registerExtensionFunction("bookListViewChangeHandler", handleBookListViewChange);
```

## Using Handlers in Layout Metadata

Reference the handler alias in list layout JSON:

```json
{
  "name": "book-list-view",
  "layout": {
    "type": "list",
    "onBeforeListDataLoad": "bookListViewChangeHandler",
    "onListLoad": "bookListViewChangeHandler"
  }
}
```

## Event Payload (Types)

### `onBeforeListDataLoad` payload

```ts
export type SolidBeforeListDataLoad = {
  type: SolidUiEvents;              // "onBeforeListDataLoad"
  fieldsMetadata: FieldsMetadata;
  viewMetadata: SolidView;
  listViewLayout: ListLayoutType;
  filter?: any;                     // current query/filter object
  queryParams?: any;                // menu/action context
  user: any;
  session: Session;
  params?: SolidListViewParams;
};
```

### `onListLoad` payload

```ts
export type SolidLoadList = {
  type: SolidUiEvents;              // "onListLoad"
  listData: any[];
  fieldsMetadata: FieldsMetadata;
  totalRecords: number;
  viewMetadata: SolidView;
  listViewLayout: ListLayoutType;
  queryParams?: any;                // menu/action context
  user: any;
  session: Session;
  params?: SolidListViewParams;
};
```

## Returning Changes

List event handlers return `SolidListUiEventResponse`:

```ts
export type SolidListUiEventResponse = {
  filterApplied?: boolean;
  newFilter?: any;
  dataChanged?: boolean;
  newListData?: any[];
  layoutChanged?: boolean;
  newLayout?: LayoutNode;
};
```

Usage rules:

- For `onBeforeListDataLoad`: return `filterApplied: true` with `newFilter` to override request filter/query.
- For `onListLoad`: return `dataChanged: true` with `newListData` to replace records.
- For layout mutations: return `layoutChanged: true` with `newLayout`.

## Common Patterns

- Pre-filtering by tenant/role/context in `onBeforeListDataLoad`
- Enforcing default sort or locale-aware query options in `onBeforeListDataLoad`
- Adding computed display-only properties in `onListLoad`
- Runtime layout toggles (column visibility/labels) in `onListLoad`

## Troubleshooting

- Handler does not run -> verify metadata key (`onBeforeListDataLoad`/`onListLoad`) and registration alias match exactly.
- Filter changes not reflected -> ensure you return both `filterApplied: true` and `newFilter`.
- Data changes ignored -> ensure `dataChanged: true` and `newListData` are both returned.
- Layout not updating -> ensure `layoutChanged: true` with a valid `newLayout`.

## See Also

- [List View Buttons](./list-view-buttons.md)
- [List View Field Widgets](./list-view-field-widgets.md)
- [Form View Events](./form-view-events.md)

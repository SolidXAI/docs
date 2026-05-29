---
title: List Events
icon: "zap"
description: Learn how to create event listeners for list view events in your frontend application.
summary: "Explains creating function extensions for SolidX list view events. Covers supported events (`onBeforeListDataLoad`, `onListLoad`), module-based file location, manifest registration, and event payload and response contracts."
solidx_concerns: [frontend.extensions.list_event_listeners]
---

## Overview

List view function extensions let you hook into list lifecycle events in SolidX.

Use them to:

- modify the outgoing list query or filter before API fetch
- transform list records after they are loaded
- adjust list layout dynamically at runtime

You author listener functions, register them in the owning UI module manifest, and reference them in your list view layout JSON.

## Supported Events

Based on `SolidListView.tsx`, list view supports these lifecycle events:

1. `onBeforeListDataLoad` - runs just before the list API call. Best for filter and query shaping.
2. `onListLoad` - runs after list data is loaded. Best for data or layout transformation.

## Event Execution Behavior

Current list lifecycle flow:

1. List state is prepared.
2. `onBeforeListDataLoad` executes if configured.
3. If the handler returns `filterApplied: true` with `newFilter`, that filter object is used for the API request.
4. List API request runs.
5. `onListLoad` executes with fetched records.
6. If returned, `newListData` and or `newLayout` are committed to state.

## Project Structure & File Paths

For model-scoped list event functions, use:

- `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-functions/`

Register them in:

- `solid-ui/src/<module-name>/<module-name>.ui-module.ts`

Example structure:

```text
solid-ui/src/
  <module-name>/
    admin-layout/
      <model-name>/
        extension-functions/
          <model>ListViewChangeHandler.ts
    <module-name>.ui-module.ts
```

## Creating a Handler

Example with both events in one handler:

```ts
import type { SolidBeforeListDataLoad, SolidLoadList, SolidListUiEventResponse } from "@solidxai/core-ui";

const handleBookListViewChange = (
  event: SolidBeforeListDataLoad | SolidLoadList
): SolidListUiEventResponse => {
  if (event.type === "onBeforeListDataLoad") {
    const nextFilter = structuredClone(event.filter || {});
    const existing = Array.isArray(nextFilter.$and) ? nextFilter.$and : [];

    nextFilter.$and = [...existing, { isActive: { $eq: true } }];

    return {
      filterApplied: true,
      newFilter: nextFilter,
    };
  }

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

Register the function in the owning UI module manifest:

```ts
import { ExtensionFunctionTypes, type SolidUiModule } from "@solidxai/core-ui";
import handleBookListViewChange from "./admin-layout/book/extension-functions/bookListViewChangeHandler";

const libraryUiModule = {
  name: "library",
  extensionFunctions: [
    {
      name: "bookListViewChangeHandler",
      fn: handleBookListViewChange,
      type: ExtensionFunctionTypes.onBeforeListDataLoad,
    },
    {
      name: "bookListViewChangeHandler",
      fn: handleBookListViewChange,
      type: ExtensionFunctionTypes.onListLoad,
    },
  ],
} satisfies SolidUiModule;

export default libraryUiModule;
```

## Using Handlers in Layout Metadata

Reference the handler name in list layout JSON:

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

### `onBeforeListDataLoad`

```ts
export type SolidBeforeListDataLoad = {
  type: SolidUiEvents;
  fieldsMetadata: FieldsMetadata;
  viewMetadata: SolidView;
  listViewLayout: ListLayoutType;
  filter?: any;
  queryParams?: any;
  user: any;
  session: Session;
  params?: SolidListViewParams;
};
```

### `onListLoad`

```ts
export type SolidLoadList = {
  type: SolidUiEvents;
  listData: any[];
  fieldsMetadata: FieldsMetadata;
  totalRecords: number;
  viewMetadata: SolidView;
  listViewLayout: ListLayoutType;
  queryParams?: any;
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

- For `onBeforeListDataLoad`, return `filterApplied: true` with `newFilter` to override the request filter.
- For `onListLoad`, return `dataChanged: true` with `newListData` to replace records.
- For layout mutations, return `layoutChanged: true` with `newLayout`.

## Common Patterns

- pre-filtering by tenant, role, or context in `onBeforeListDataLoad`
- enforcing default sort or locale-aware query options
- adding computed display-only properties in `onListLoad`
- runtime column visibility or label changes with `SolidViewLayoutManager`

## Troubleshooting

- Handler does not run -> verify metadata key and registered manifest name match exactly.
- Filter changes not reflected -> ensure you return both `filterApplied: true` and `newFilter`.
- Data changes ignored -> ensure `dataChanged: true` and `newListData` are both returned.
- Layout not updating -> ensure `layoutChanged: true` with a valid `newLayout`.

## See Also

- [List View Buttons](./list-view-buttons.md)
- [List View Field Widgets](./list-view-field-widgets.md)
- [Form View Events](./form-view-events.md)
- [Layout Manager](./layout-manager.md)

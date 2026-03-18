---
sidebar_position: 1
title: Form View Events
description: Learn how to create event listeners for form view events in your frontend application.
summary: Explains creating event listeners for SolidX form view events to extend frontend functionality. Covers supported events (`onFormLoad`, `onFieldChange`, `onFieldBlur`), registering handlers using `registerExtensionFunction`, accessing event data, and returning layout/data updates. Includes a dedicated deprecated section for `onFormLayoutLoad` and `onFormDataLoad`.
solidx_concerns: [add_change_handler_function, onlayoutload_handler_function, ondataload_handler_function]
---

## Overview

Form view **function extensions** let you react to lifecycle events in a SolidX form. Use them to:

- Read or mutate **form data** (via Formik)
- Adjust the **layout dynamically** (hide/show/move fields) with `SolidViewLayoutManager`
- Coordinate with **custom widgets** rendered in the form (see [Form View Field Widgets](./form-view-field-widgets.md))

You author **listener functions**, register them with `registerExtensionFunction`, and reference them in your **form view layout JSON**.

## Supported Events (Current)

SolidX currently supports these form view events:

1. **`onFormLoad`** - unified form-load lifecycle event (recommended for all load-time logic).
2. **`onFieldChange`** - fires whenever a field **value changes**.
3. **`onFieldBlur`** - fires when a field **loses focus**.

:::tip
If your handler mutates layout and/or data, return the appropriate flags:
`layoutChanged: true` and/or `dataChanged: true`. Without these flags, changes are ignored.
:::

## Form Load Execution Behavior

Inside `SolidFormView`, form-load handlers run with a working layout/data context and are committed once at the end.

Current execution sequence:

1. `onFormLayoutLoad` (legacy compatibility hook)
2. `onFormDataLoad` (legacy compatibility hook)
3. `onFormLoad` (recommended unified hook)
4. Commit final `workingLayout` and `workingFormData` to React state

This means `onFormLoad` sees the latest working layout/data and is the best place for load-time logic moving forward.

## Project Structure & File Paths

#### Form Event Listeners

- Scope: form-view event listeners for a specific `<module, model>` pair.
- Mandatory listener location:
  - `solid-ui/src/extensions/<module-name>/<model-name>/form-event-listeners/`
- Do not place form-event listeners in generic folders when module/model is known.

Default file selection for form event changes:

1. Create or update a TS/TSX listener inside:
   - `solid-ui/src/extensions/<module-name>/<model-name>/form-event-listeners/`
2. Register the listener in:
   - `solid-ui/src/extensions/solid-extensions.ts`
3. Keep registration key aligned with layout metadata event references (`onFormLoad`, `onFieldChange`, `onFieldBlur`).

Example structure:

```bash
solid-ui/src/extensions/
├── solid-extensions.ts
└── library/
    └── book/
        └── form-event-listeners/
            └── bookFormViewChangeHandler.ts
```

## Creating a Handler

Here is a concise example that:

- Handles `onFormLoad` for load-time setup
- Handles `onFieldChange` for reactive logic
- Uses one function for all form events

```ts
import { SolidViewLayoutManager } from "@solidxai/core-ui";

const handleBookFormViewChange = (event: SolidUiEvent) => {
  const { type, modifiedField, modifiedFieldValue, formData, viewMetadata } = event;
  const layoutManager = new SolidViewLayoutManager(viewMetadata.layout);

  // Preferred load-time hook
  if (type === "onFormLoad") {
    layoutManager.updateNodeAttributes("book-advanced-section", { visible: false });
    return {
      layoutChanged: true,
      newLayout: layoutManager.getLayout(),
    };
  }

  // Field change example
  if (type === "onFieldChange" && modifiedField === "title") {
    layoutManager.updateNodeAttributes("title-caption-node", { visible: true });

    return {
      layoutChanged: true,
      dataChanged: true,
      newFormData: {
        ...formData,
        ctxtTitleAlphabetCount: modifiedFieldValue ? String(modifiedFieldValue).length : 0,
      },
      newLayout: layoutManager.getLayout(),
    };
  }
};

export default handleBookFormViewChange;
```

:::info
If you set `dataChanged: true`, return the full `newFormData` object, not just the modified field.
:::

:::tip
Keep model concerns together. Use a single file (for example `bookFormViewChangeHandler.ts`) for form-view event logic for that model.
:::

## Registering the Handler

Register each exported function with an alias in `solid-extensions.ts`:

```ts
import handleBookFormViewChange from "./library/book/form-event-listeners/bookFormViewChangeHandler";
import { registerExtensionFunction } from "@solidxai/core-ui";

registerExtensionFunction("bookFormViewChangeHandler", handleBookFormViewChange);
```

## Using Handlers in Layout Metadata

Reference your handler alias in the layout JSON:

```json
{
  "name": "book-form-view",
  "layout": {
    "type": "form",

    // Preferred load hook:
    "onFormLoad": "bookFormViewChangeHandler",

    // Field-level hooks:
    "onFieldChange": "bookFormViewChangeHandler",
    "onFieldBlur": "bookFormViewChangeHandler"
  }
}
```

:::note
Your handler can be one function that switches on `event.type`, or multiple functions registered under different aliases.
:::

## Event Payload (Types)

Handlers receive a `SolidUiEvent` payload.

```ts
export type SolidUiEvent = {
  type: SolidUiEvents;            // e.g., "onFormLoad", "onFieldChange"
  modifiedField?: string;
  modifiedFieldValue?: any;
  queryParams?: any;
  formData: Record<string, any>;  // current Formik values
  viewMetadata: SolidView;        // includes the current layout
  fieldsMetadata: FieldsMetadata; // field definitions & constraints
  formViewLayout: LayoutNode;     // current working layout
};
```

## Returning Changes

Your handler may optionally return an object to apply mutations:

```ts
return {
  layoutChanged: boolean,
  dataChanged: boolean,
  newFormData?: Record<string, any>,
  newLayout?: LayoutNode
};
```

- If you touch **layout**, set `layoutChanged: true` and return `newLayout`.
- If you touch **data**, set `dataChanged: true` and return `newFormData`.
- If you touch both, set both flags and return both payloads.

## Deprecated Load Events (Compatibility Only)

:::warning Deprecated
`onFormLayoutLoad` and `onFormDataLoad` are deprecated for new development.
Prefer `onFormLoad` as the single load lifecycle hook.
:::

These legacy hooks are still executed for backward compatibility, but new implementations should migrate to `onFormLoad`.

Legacy metadata pattern:

```json
{
  "layout": {
    "onFormLayoutLoad": "bookFormViewChangeHandler",
    "onFormDataLoad": "bookFormViewChangeHandler"
  }
}
```

Recommended metadata pattern:

```json
{
  "layout": {
    "onFormLoad": "bookFormViewChangeHandler"
  }
}
```

Migration guidance:

1. Move load-time layout logic from `onFormLayoutLoad` into `onFormLoad`.
2. Move load-time data shaping logic from `onFormDataLoad` into `onFormLoad`.
3. Keep `onFieldChange` and `onFieldBlur` unchanged.
4. Remove deprecated hooks from metadata once migration is complete.

## Common Patterns

- **Conditional sections:** During `onFormLoad`, hide/show layout nodes based on defaults, permissions, or query context.
- **Derived fields:** On `onFieldChange`, compute dependent values and return `newFormData`.
- **Async validations:** Use `onFieldBlur` for lightweight checks. For heavy validation, prefer server-side logic.
- **Safety first:** Avoid deep mutation of layout objects directly; use `SolidViewLayoutManager`.

## Troubleshooting

- **My changes are not applied** -> Verify `layoutChanged`/`dataChanged` flags and corresponding payloads are returned.
- **Load-time logic is not running** -> Ensure the layout has `onFormLoad` and the alias matches `registerExtensionFunction`.
- **Node not found** -> Verify the node ID passed to `updateNodeAttributes` exists in the layout tree.
- **Nothing happens on change** -> Confirm `onFieldChange` is mapped and handler checks the correct field name.

## See Also

- [Form View Field Widgets](./form-view-field-widgets.md) - build custom view/edit widgets and reference them via `viewWidget`/`editWidget`.
- [Module Metadata Schema](../../metadata_schema/index.md) - details on form-view layout JSON and node attributes.

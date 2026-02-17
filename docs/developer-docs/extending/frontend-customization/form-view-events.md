---
sidebar_position: 1
title: Form View Events
description: Learn how to create event listeners for form view events in your frontend application.
summary: Explains creating event listeners for SolidX form view events to extend frontend functionality. Covers supported events (onFormLayoutLoad, onFormDataLoad, onFieldChange, onFieldBlur, onCustomWidgetRender), registering handlers using `registerExtensionFunction`, accessing event data (type, modifiedField, modifiedFieldValue, formData, viewMetadata, fieldsMetadata), modifying UI layout dynamically with `SolidViewLayoutManager`, returning changes (layoutChanged, dataChanged, newFormData, newLayout), and examples like character count tracking.
solidx_concerns: [add_change_handler_function, onlayoutload_handler_function, ondataload_handler_function]
---

import { IoIosArrowForward } from "react-icons/io";

<!-- # Form View Events -->

## Overview

Form view **function extensions** let you react to lifecycle events in a SolidX form. Use them to:
- Read or mutate **form data** (via Formik)
- Adjust the **layout dynamically** (hide/show/move fields) with `SolidViewLayoutManager`
- Coordinate with **custom widgets** rendered in the form (see [Form View Field Widgets](./form-view-field-widgets.md))

You author **listener functions**, register them with `registerExtensionFunction`, and reference them in your **form view layout JSON**.



## Supported Events

SolidX currently supports these form view events:

1. **`onFormLayoutLoad`** – fires when the **layout** is loaded. Great for conditional visibility and structure tweaks.
2. **`onFormDataLoad`** – fires when **data** is loaded (edit mode fetch, or defaults for create). Perfect for setting derived values.
3. **`onFieldChange`** – fires whenever a field **value changes**. Ideal for cascading logic and live calculations.
4. **`onFieldBlur`** – fires when a field **loses focus**. Good for validations or light reflows.
5. **`onCustomWidgetRender`** – fires when a **custom widget** is rendered. Useful for last‑mile UI polish.

:::tip
If your handler **mutates layout and/or data**, return the appropriate flags: `layoutChanged: true` and/or `dataChanged: true`. Without these flags, changes are ignored.
:::



## Project Structure & File Paths

Place your handler(s) under your admin extensions folder. A common convention is **one handler file per model**.

```bash
/solid-ui/app/admin/extensions/bookFormViewChangeHandler.ts
/solid-ui/app/admin/extensions/solid-extensions.ts   # registration
```



## Creating a Handler

Here’s a concise example that:
- Listens to **any form event**
- On `onFieldChange` of `title`, shows a hidden node and injects a **character count** into form data

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>bookFormViewChangeHandler.ts</code>
  </summary>

```ts
import { SolidViewLayoutManager } from "@solidxai/core-ui";

const handleBookFormViewChange = (event: SolidUiEvent) => {
  const { type, modifiedField, modifiedFieldValue, formData, viewMetadata } = event;

  // Work with the *current* layout
  const layoutManager = new SolidViewLayoutManager(viewMetadata.layout);

  if (type === "onFieldChange" && modifiedField === "title") {
    const title = modifiedFieldValue;
    // Reveal a UI node (e.g., a caption area) by nodeId configured in your layout
    layoutManager.updateNodeAttributes("page-1-row-1-div-1-div-1-title-custom", { visible: true });

    return {
      layoutChanged: true,                 // you changed layout; tell SolidX
      dataChanged: true,                   // you changed data; tell SolidX
      newFormData: {
        ...formData,
        // Below is the new field we are injecting, which can be accessed in a custom widget
        ctxtTitleAlphabetCount: title ? String(title).length : 0,
      },
      newLayout: layoutManager.getLayout() // hand back the updated layout
    };
  }

  // For events you don't handle, return nothing.
  // You can also return { layoutChanged: false, dataChanged: false } explicitly.
};

export default handleBookFormViewChange;
```
</details>
:::info
If you are setting dataChanged to true, ensure you return the full newFormData object, not just the modified field.
:::
:::tip
**Keep model concerns together.** Use a single file (e.g., `bookFormViewChangeHandler.ts`) for all form‑view event logic for that model. It makes maintenance and onboarding much easier.
:::



## Registering the Handler

Register each exported function with an **alias** in `solid-extensions.ts`:

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>solid-extensions.ts</code>
  </summary>

```ts
import handleBookFormViewChange from "./bookFormViewChangeHandler";
import { registerExtensionFunction } from "@solidxai/core-ui";

registerExtensionFunction("bookFormViewChangeHandler", handleBookFormViewChange);
// Add more registrations as needed…
```
</details>



## Using Handlers in a Layout

Reference your handler **aliases** in the layout JSON for the form view.

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>module-metadata/&lt;module-name&gt;/&lt;module-name&gt;-metadata.json</code>
  </summary>

```json
{
  "name": "book-form-view",
  "layout": {
    "type": "form",

    // Lifecycle hooks:
    "onFormLayoutLoad": "bookFormViewChangeHandler",
    "onFormDataLoad": "bookFormViewChangeHandler",

    // Field-level hooks:
    "onFieldChange": "bookFormViewChangeHandler",
    "onFieldBlur": "bookFormViewChangeHandler",

    // Widget render hook:
    "onCustomWidgetRender": "bookFormViewChangeHandler"

    // ...rest of your layout tree (children, rows, fields, etc.)
  }
}
```
</details>

:::note
Your handler can be **one function** that switches on `event.type`, or **multiple functions** registered under different aliases. Choose whichever keeps the code clearer for your team.
:::



## Event Payload (Types)

Handlers receive a **`SolidUiEvent`** payload.

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>SolidUiEvent</code>
  </summary>

```ts
export type SolidUiEvent = {
  type: SolidUiEvents;                 // e.g., "onFieldChange"
  modifiedField?: string;              // e.g., "title"
  modifiedFieldValue?: any;            // e.g., "The Pragmatic Programmer"
  formData: Record<string, any>;       // current Formik values
  viewMetadata: SolidView;             // includes the current layout
  fieldsMetadata: FieldsMetadata;      // field definitions & constraints
  formViewLayout: LayoutNode;          // shorthand to the current layout node
};
```
</details>



## Returning Changes

Your handler may optionally return an object to **apply mutations**:

```ts
return {
  layoutChanged: boolean,      // did you alter layout?
  dataChanged: boolean,        // did you alter form data?
  // if dataChanged is true, provide newFormData
  // The new form data can now be accessed by both In-built and Custom Widgets
  newFormData?: Record<string, any>,  
  newLayout?: LayoutNode
};
```

- If you touch **layout**, set `layoutChanged: true` and return `newLayout`.
- If you touch **data**, set `dataChanged: true` and return `newFormData`.
- If you touch **both**, set **both** flags and return both payloads.



## Common Patterns

- **Conditional sections:** During `onFormLayoutLoad`, hide or show layout nodes based on defaults or permissions.
- **Derived fields:** On `onFieldChange`, compute totals, taxes, or dependent values from other fields, then return `newFormData`.
- **Async validations:** Use `onFieldBlur` to kick off lightweight checks (e.g., uniqueness). For heavy work, prefer server‑side validation.
- **Safety first:** Avoid deep mutations of `viewMetadata.layout` directly; use `SolidViewLayoutManager`. Always return flags correctly.



## Troubleshooting
- **“My changes aren’t applied”** → Verify you set `layoutChanged`/`dataChanged` appropriately.
- **On load layout changes not applied** → Ensure you have used `onFormLayoutLoad` and not `onFormDataLoad`, if you are trying to change the layout on load.
- **“Node not found”** → Ensure the **node ID** you pass to `updateNodeAttributes` actually exists in your layout tree.
- **“Nothing happens on change”** → Confirm your **alias** in the layout matches the one passed to `registerExtensionFunction`.
- **“Handlers fight each other”** → Centralize model logic in a single file, or partition clearly by event and document the contract.

---

## See Also

- [Form View Field Widgets](./form-view-field-widgets.md) — build custom view/edit widgets and reference them via `viewWidget`/`editWidget`.
- [Module Metadata Schema](../../metadata_schema/index.md) — details on form view layout JSON and node attributes.


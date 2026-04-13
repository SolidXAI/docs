---
sidebar_position: 2
title: Form View Buttons
description: Build model-scoped form action buttons for SolidX form views.
summary: Documents folder conventions, action component props, registration, metadata wiring, and Solid API patterns for form-view button extensions.
solidx_concerns: [frontend.extensions.form_buttons, add_form_button]
---

## Scope

Form View Buttons are form-level action components for a specific `<module, model>` pair.

Mandatory location:

- `solid-ui/src/extensions/<module-name>/<model-name>/form-buttons/`

Do not place model-scoped form button components in generic folders.

## Default Implementation Flow

1. Create/update a React TSX component under:
   - `solid-ui/src/extensions/<module-name>/<model-name>/form-buttons/`
2. Keep export/import style consistent with neighboring extension files.
3. Register in:
   - `solid-ui/src/extensions/solid-extensions.ts`
4. Keep registration key aligned with layout metadata `action` value.

## Component Props Contract

Form button action components receive extension context with shape equivalent to:

```ts
{
  action: any;
  params: {
    moduleName: string;
    modelName: string;
    id?: string | number;
    handlePopupClose?: () => void;
    [key: string]: any;
  };
  formik: any;
  solidFormViewMetaData: any;
}
```

Guidance:

- Use `params.id` (or equivalent context field) for record-specific actions.
- Guard missing IDs for create mode / embedded contexts.

## Registration

```ts
import { registerExtensionComponent } from "@solidxai/core-ui";
import {
    ExtensionComponentTypes,
    ExtensionFunctionTypes,
    type ExtensionComponentType,
    type ExtensionFunctionType,
} from "../types/extension-registry";
import { ApproveApplicationButton } from "./venue/application/form-buttons/ApproveApplicationButton";

registerExtensionComponent("ApproveApplicationButton", ApproveApplicationButton, ExtensionComponentTypes.form_action);
```

## Layout Metadata Wiring

Buttons are triggered from form layout metadata (`formButtons` + `attrs.action`):

```json
{
  "layout": {
    "type": "form",
    "formButtons": [
      {
        "attrs": {
          "label": "Approve",
          "action": "ApproveApplicationButton",
          "openInPopup": true,
          "actionInContextMenu": false
        }
      }
    ]
  }
}
```

## API Call Guidance

When a form button calls backend APIs, use `@solidxai/core-ui` helpers:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Guidelines:

- Use paths like `/resource` instead of `/api/resource`.
- Derive IDs/context from `params` or `formik.values`.
- Handle loading, success, error explicitly.
- Apply follow-up refresh behavior where required.
- Keep popup close behavior safe and deterministic on both success and error paths.

## UI/Styling Guidance (PrimeReact)

For form action components:

- Prefer PrimeReact controls (`Button`, `Message`, `ProgressSpinner`, `Toast`) over raw HTML controls.
- Keep action areas compact (`p-3`/`p-4`, `gap-2`/`gap-3`).
- Use clear call-to-action hierarchy:
  - Secondary/outlined `Cancel`
  - Primary `Confirm` or `Submit`
- Disable confirm action during async execution and surface loading state.

## Popup Lifecycle and `closePopup`

When `openInPopup: true` is used in metadata:

- SolidX opens the popup container; your component should render clean inner content.
- Always wire cancel/close to `closePopup`.
- On success, either auto-close immediately or show success state with a `Close` button.

Pattern:

```ts
import { closePopup } from "@solidxai/core-ui";
import { useDispatch } from "react-redux";

const dispatch = useDispatch();
const onClose = () => dispatch(closePopup());
```

## Example

```tsx
import { useState } from "react";
import { solidPost } from "@solidxai/core-ui";
import { useDispatch } from "react-redux";
import { closePopup } from "@solidxai/core-ui";

export function ApproveApplicationButton({ params }: any) {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);

  const onApprove = async () => {
    if (!params?.id) return;

    setLoading(true);
    try {
      await solidPost(`/application/${params.id}/approve`, {});
      dispatch(closePopup());
    } catch {
      dispatch(closePopup());
    } finally {
      setLoading(false);
    }
  };

  return (
    <button disabled={loading} onClick={onApprove}>
      {loading ? "Approving..." : "Approve"}
    </button>
  );
}
```

## See Also

- [Form View Events](./form-view-events.md)
- [Extension UI Guidelines](./extension-ui-guidelines.md)
- [Solid HTTP API](./solid-http-api.md)

---
title: Form Buttons
icon: "mouse-pointer"
description: Build model-scoped form action buttons for SolidX form views.
summary: "Documents folder conventions, action component props, module-manifest registration, metadata wiring, and Solid API patterns for form-view button extensions."
solidx_concerns: [frontend.extensions.form_buttons, add_form_button]
---

## Scope

Form View Buttons are form-level action components for a specific `<module, model>` pair.

Mandatory location:

- `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/`

Do not place model-scoped form button components in generic folders.

## Default Implementation Flow

1. Create or update a React TSX component under:
   - `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/`
2. Keep export/import style consistent with neighboring files in that model folder.
3. Register the component in the owning UI module manifest:
   - `solid-ui/src/<module-name>/<module-name>.ui-module.ts`
4. Keep the registration name aligned with the form layout metadata `action` value.

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
- Guard missing IDs for create mode or embedded contexts.

## Registration

Register form action components in the owning module manifest:

```ts
import { ExtensionComponentTypes, type SolidUiModule } from "@solidxai/core-ui";
import { ApproveApplicationButton } from "./admin-layout/application/extension-components/ApproveApplicationButton";

const merchantOnboardingUiModule = {
  name: "merchant-onboarding",
  extensionComponents: [
    {
      name: "ApproveApplicationButton",
      component: ApproveApplicationButton,
      type: ExtensionComponentTypes.formAction,
    },
  ],
} satisfies SolidUiModule;

export default merchantOnboardingUiModule;
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

When a form button calls backend APIs, SolidX supports two valid integration styles.

### Option A: Solid HTTP Helpers

Use `@solidxai/core-ui` helpers such as:

- `solidGet`
- `solidPost`
- `solidPut`
- `solidPatch`
- `solidDelete`
- `solidAxios`

Use this when the action is localized and you do not need shared cached API state.

Guidelines:

- Use paths like `/resource` instead of `/api/resource`.
- Derive IDs/context from `params` or `formik.values`.
- Handle loading, success, and error explicitly.
- Apply follow-up refresh behavior where required.
- Keep popup close behavior safe and deterministic on both success and error paths.

### Option B: Redux / RTK Query

If your form action belongs to a larger module-owned API integration strategy, you can also place RTK Query APIs, reducers, and middleware under:

- `solid-ui/src/<module-name>/redux/`

and register them through the same module manifest.

Use this when the button participates in shared cached state, invalidation, or module-level orchestration.

See also: [Redux Module Integration](./redux-module-integration.md) and [Solid HTTP API](./solid-http-api.md)

## UI/Styling Guidance (Shadcn/Solid Primitives)

For form action components:

- Prefer Solid primitives (`SolidButton`, `SolidMessage`, `SolidSpinner`, `SolidToast`) over raw HTML controls.
- Keep action areas compact (`p-3`/`p-4`, `gap-2`/`gap-3`).
- Use clear call-to-action hierarchy:
  - Secondary or outlined `Cancel`
  - Primary `Confirm` or `Submit`
- Disable confirm action during async execution and surface loading state using the `loading` prop.

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
import { closePopup, solidPost, SolidButton } from "@solidxai/core-ui";
import { useDispatch } from "react-redux";

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
    <SolidButton loading={loading} onClick={onApprove} label="Approve" />
  );
}
```

## See Also

- [Form View Events](./form-view-events.md)
- [Extension UI Guidelines](./extension-ui-guidelines.md)
- [Redux Module Integration](./redux-module-integration.md)
- [Solid HTTP API](./solid-http-api.md)

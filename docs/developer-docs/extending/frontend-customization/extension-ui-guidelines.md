---
sidebar_position: 11
title: UI Guidelines
description: UI baseline and popup patterns for SolidX frontend extensions built with Solid Primitives.
summary: "Practical style and interaction defaults for SolidX extension components and function-driven popup UIs. Covers button sizing, popup composition, `closePopup` usage, loading and error UX, and where these conventions apply in the UI module system."
solidx_concerns: [frontend.extensions.form_buttons, frontend.extensions.list_buttons, frontend.extensions.row_buttons, frontend.extensions.custom_widgets, frontend.extensions.popup_ui, frontend.extensions.close_popup]
---

## Purpose

Use these defaults so frontend extensions generated from prompts look clean and consistent with the SolidX UI.

## Solid Primitives Baseline

- Prefer Solid primitives such as `SolidButton`, `SolidDialog`, `SolidMessage`, `SolidSpinner`, and `SolidToast` over raw HTML or legacy controls.
- Reuse existing utility classes already used in SolidX projects.
- Keep spacing consistent: `p-6` for container padding, `gap-4` for logical sections, and `gap-2` for action groups.

## Row Button Visual Rules

Row-level actions should look like compact inline actions, not full-width bars.

Recommended defaults:

- `size="sm"`
- `variant="outline"` or `variant="ghost"`
- content-based width
- single-line labels
- concise text

Example:

```tsx
<SolidButton
  label="Seed Rates"
  icon="si-refresh"
  size="sm"
  variant="outline"
  className="w-auto whitespace-nowrap"
/>
```

## Popup Composition Rules

### If metadata uses `openInPopup: true`

SolidX already opens a popup container for your extension component. Render popup content only, not another full-screen modal wrapper.

### Popup content structure

- header: icon and title
- body: clear confirmation, success, or error message
- footer: right-aligned actions such as `Cancel`, `Confirm`, or `Close`

Recommended wrapper:

```tsx
<div className="flex flex-col gap-6 p-6" style={{ width: "min(560px, 92vw)" }}>
  {/* header */}
  {/* body */}
  {/* footer */}
</div>
```

## `closePopup` Lifecycle Rules

Always support explicit dismissal in extension popups.

- Cancel closes immediately.
- Success flows should auto-close or show a clear `Close` button.
- Error state should usually stay open long enough for the user to read it.

Pattern:

```ts
import { closePopup } from "@solidxai/core-ui";
import { useDispatch } from "react-redux";

const dispatch = useDispatch();
const close = () => dispatch(closePopup());
```

## Async UX Rules

- Disable confirm actions while a request is in flight.
- Show loading state via the `loading` prop on `SolidButton`.
- Use project-standard toast or global error behavior for failures.
- Avoid duplicate submissions.

## Confirmation Template

```tsx
import { useState } from "react";
import { SolidButton, SolidMessage, solidPost, closePopup } from "@solidxai/core-ui";
import { useDispatch } from "react-redux";

export function SeedCurrencyRates({ rowData }: any) {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  const onCancel = () => dispatch(closePopup());

  const onConfirm = async () => {
    if (!rowData?.id || loading) return;

    setLoading(true);
    try {
      await solidPost(`/country-master/${rowData.id}/seed-currency-rates`, {});
      setDone(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4 p-6" style={{ width: "min(560px, 92vw)" }}>
      {!done ? (
        <>
          <SolidMessage severity="warn" text="Confirm Action" />
          <p className="text-sm text-muted-foreground m-0">
            Confirming will trigger currency fluctuation fetch for this country.
          </p>
          <div className="flex justify-end gap-2 pt-2">
            <SolidButton label="Cancel" variant="outline" onClick={onCancel} />
            <SolidButton label={loading ? "Confirming..." : "Confirm"} onClick={onConfirm} loading={loading} />
          </div>
        </>
      ) : (
        <>
          <SolidMessage severity="success" text="Success" />
          <p className="text-sm text-muted-foreground m-0">
            Currency fluctuation fetch was triggered successfully.
          </p>
          <div className="flex justify-end pt-2">
            <SolidButton label="Close" onClick={onCancel} />
          </div>
        </>
      )}
    </div>
  );
}
```

## Where To Apply These Guidelines

Apply these conventions to:

- `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/`
- popup-style action components rendered by metadata
- UI rendered by handlers in `extension-functions/` when they drive popup or dynamic extension behavior

## See Also

- [Form View Buttons](./form-view-buttons.md)
- [List View Buttons](./list-view-buttons.md)
- [Solid HTTP API](./solid-http-api.md)

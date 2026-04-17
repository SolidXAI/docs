---
sidebar_position: 11
title: UI Guidelines
description: UI baseline and popup patterns for SolidX frontend extensions built with Solid Primitives (Radix UI/Shadcn).
summary: Practical style and interaction defaults for SolidX extension components (form buttons, list buttons, row buttons, widgets). Covers button sizing, popup composition, `closePopup` usage, loading/success/error UX, and a reusable confirmation pattern using Solid Primitives.
solidx_concerns: [frontend.extensions.form_buttons, frontend.extensions.list_buttons, frontend.extensions.row_buttons, frontend.extensions.custom_widgets, frontend.extensions.popup_ui, frontend.extensions.close_popup]
---

## Purpose

Use these defaults so extension UI generated from prompts looks clean and consistent with the Shadcn-based SolidX screens.

## Solid Primitives Baseline

- Prefer Solid Primitives (`SolidButton`, `SolidDialog`, `SolidMessage`, `SolidSpinner`, `SolidToast`) over raw HTML or legacy PrimeReact controls.
- Reuse existing utility classes used in SolidX projects (`flex`, `gap-*`, `p-*`, `m-*`, `text-*`, `w-full`).
- Keep spacing consistent: `p-6` for larger container padding, `gap-4` for logical sections, `gap-2` for action groups.

## Row Button Visual Rules

Row-level actions should look like compact inline actions, not full-width bars.

Recommended defaults:

- `size="sm"` or `size="small"`
- `variant="outline"` or `variant="ghost"` for secondary actions
- Keep width content-based (`w-auto`)
- Keep label on one line (`whitespace-nowrap`)
- Use concise labels (1-3 words)

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

SolidX already opens a popup container (via `SolidDialog`) for your extension component. Render only popup content (header/body/footer), not another full-screen modal wrapper.

### Popup content structure

- Header: icon + title (use `SolidDialogHeader`)
- Body: clear confirmation/success/error message (use `SolidDialogBody`)
- Footer: right-aligned actions (`Cancel`, `Confirm` or `Close`) (use `SolidDialogFooter`)

Recommended popup content wrapper:

```tsx
<div className="flex flex-col gap-6 p-6" style={{ width: "min(560px, 92vw)" }}>
  {/* header */}
  {/* body */}
  {/* footer actions */}
</div>
```

## `closePopup` Lifecycle Rules

Always support explicit dismissal in extension popups.

- Cancel button should close popup immediately.
- Success flows should either:
  - auto-close after action, or
  - show success state with a clear `Close` button.
- Error state should keep popup open for user visibility unless product conventions say otherwise.

Pattern:

```ts
import { closePopup } from "@solidxai/core-ui";
import { useDispatch } from "react-redux";

const dispatch = useDispatch();
const close = () => dispatch(closePopup());
```

## Async UX Rules

- Disable confirm action while request is in-flight (handled automatically by `loading` prop on `SolidButton`).
- Show loading feedback (use `loading` prop on `SolidButton` which shows a spinner).
- Use project-standard toast (`SolidToast`) or global error behavior for server failures.
- Avoid duplicate submissions with a loading guard.

## Confirmation Template (Row/Form/List Actions)

```tsx
import { useState } from "react";
import { 
  SolidButton, 
  SolidMessage, 
  solidPost, 
  closePopup 
} from "@solidxai/core-ui";
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
            <SolidButton 
              label={loading ? "Confirming..." : "Confirm"} 
              onClick={onConfirm} 
              loading={loading} 
            />
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

- `form-buttons/` components
- `list-buttons/` components
- `row-buttons/` components
- popup-style action components rendered by extension metadata

## See Also

- [Form View Buttons](./form-view-buttons.md)
- [List View Buttons](./list-view-buttons.md)
- [Solid HTTP API](./solid-http-api.md)

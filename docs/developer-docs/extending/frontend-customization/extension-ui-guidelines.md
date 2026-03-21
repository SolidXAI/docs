---
sidebar_position: 11
title: Extension UI Guidelines
description: UI baseline and popup patterns for SolidX frontend extensions built with PrimeReact.
summary: Practical style and interaction defaults for SolidX extension components (form buttons, list buttons, row buttons, widgets). Covers button sizing, popup composition, `closePopup` usage, loading/success/error UX, and a reusable confirmation pattern.
solidx_concerns: [frontend.extensions.form_buttons, frontend.extensions.list_buttons, frontend.extensions.row_buttons, frontend.extensions.custom_widgets, frontend.extensions.popup_ui, frontend.extensions.close_popup]
---

## Purpose

Use these defaults so extension UI generated from prompts looks clean and consistent with PrimeReact-based SolidX screens.

## PrimeReact Baseline

- Prefer PrimeReact components (`Button`, `Dialog`, `Message`, `ProgressSpinner`, `Toast`) over raw HTML controls.
- Reuse existing utility classes used in SolidX projects (`p-*`, `flex`, `gap-*`, `surface-*`, `border-round`, `text-*`).
- Keep spacing consistent: `p-3`/`p-4` for container padding, `gap-2`/`gap-3` for item spacing.

## Row Button Visual Rules

Row-level actions should look like compact inline actions, not full-width bars.

Recommended defaults:

- `size="small"`
- `className="p-button-sm"`
- Keep width content-based (`width: "auto"`, `minWidth: "unset"`)
- Keep label on one line (`whiteSpace: "nowrap"`)
- Use concise labels (1-3 words)

Example:

```tsx
<Button
  label="Seed Rates"
  icon="pi pi-refresh"
  size="small"
  className="p-button-sm"
  style={{ width: "auto", minWidth: "unset", whiteSpace: "nowrap" }}
/>
```

## Popup Composition Rules

### If metadata uses `openInPopup: true`

SolidX already opens a popup container for your extension component. Render only popup content (header/body/footer), not another full-screen modal wrapper.

### Popup content structure

- Header: icon + title
- Body: clear confirmation/success/error message
- Footer: right-aligned actions (`Cancel`, `Confirm` or `Close`)

Recommended popup content wrapper:

```tsx
<div className="p-4" style={{ width: "min(560px, 92vw)" }}>
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

- Disable confirm action while request is in-flight.
- Show loading feedback (`Confirming...` label or spinner).
- Use project-standard toast/global error behavior for server failures.
- Avoid duplicate submissions with a loading guard.

## Confirmation Template (Row/Form/List Actions)

```tsx
import { useState } from "react";
import { Button } from "primereact/button";
import { Message } from "primereact/message";
import { solidPost, closePopup } from "@solidxai/core-ui";
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
    <div className="p-4 flex flex-column gap-3" style={{ width: "min(560px, 92vw)" }}>
      {!done ? (
        <>
          <Message severity="warn" text="Confirm Action" />
          <p className="m-0">
            Confirming will trigger currency fluctuation fetch for this country.
          </p>
          <div className="flex justify-content-end gap-2 pt-2">
            <Button label="Cancel" severity="secondary" outlined onClick={onCancel} />
            <Button label={loading ? "Confirming..." : "Confirm"} onClick={onConfirm} loading={loading} />
          </div>
        </>
      ) : (
        <>
          <Message severity="success" text="Success" />
          <p className="m-0">Currency fluctuation fetch was triggered successfully.</p>
          <div className="flex justify-content-end pt-2">
            <Button label="Close" onClick={onCancel} />
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

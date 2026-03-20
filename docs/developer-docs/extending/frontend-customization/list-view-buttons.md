---
sidebar_position: 3
title: List View Buttons
description: Build header and row action buttons for SolidX list views.
summary: Documents mandatory file locations, props contracts, registration, metadata wiring, and API conventions for list header and row button extensions.
solidx_concerns: [frontend.extensions.list_buttons, frontend.extensions.row_buttons, add_list_header_button_with, add_list_row_button_with]
---

## Scope

List button customizations are model-scoped and split into two subtypes:

1. Header/list-wide buttons (`list-buttons`)
2. Row-level buttons (`row-buttons`)

## List Header Buttons

Mandatory location:

- `solid-ui/src/extensions/<module-name>/<model-name>/list-buttons/`

Use for list-wide actions (export, bulk action, filtered processing).

### Header Button Props

Action context can include:

- `action`
- `params`
- `selectedRecords`
- `filters`

Guidance:

- For selection-based operations, guard empty `selectedRecords`.
- Prefer `selectedRecords` and `filters` over hardcoded assumptions.

## Row Buttons

Mandatory location:

- `solid-ui/src/extensions/<module-name>/<model-name>/row-buttons/`

Use for record-specific actions triggered from a clicked row.

### Row Button Props

Action context can include:

- `action`
- `params`
- `rowData`

Guidance:

- Use `rowData` as source of truth for record-level actions.
- Guard missing `rowData`/ID and show clear user feedback.

## Registration

Register components in:

- `solid-ui/src/extensions/solid-extensions.ts`

using:

```ts
import { registerExtensionComponent } from "@solidxai/core-ui";
import { GenerateReportButton } from "./venue/payment/list-buttons/GenerateReportButton";
import { RefundPaymentButton } from "./venue/payment/row-buttons/RefundPaymentButton";

registerExtensionComponent("GenerateReportButton", GenerateReportButton);
registerExtensionComponent("RefundPaymentButton", RefundPaymentButton);
```

Keep action names aligned with metadata.

## Metadata Wiring

Header buttons are typically configured in list layout metadata at:

- `layout.attrs.headerButtons[]`

Row buttons are typically configured at:

- `layout.attrs.rowButtons[]`

Example:

```json
{
  "layout": {
    "type": "list",
    "attrs": {
      "headerButtons": [
        {
          "attrs": {
            "label": "Generate Report",
            "action": "GenerateReportButton"
          }
        }
      ],
      "rowButtons": [
        {
          "attrs": {
            "label": "Refund",
            "action": "RefundPaymentButton"
          }
        }
      ]
    }
  }
}
```

## API Guidance

If list/row button actions require backend calls, use:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Rules:

- Use `/resource` paths (no hardcoded `/api`).
- Handle loading/success/error explicitly.
- Apply explicit refresh behavior after mutation as needed.
- Follow project conventions for popup close and global/toast error handling.

## See Also

- [List View Events](./list-view-events.md)
- [Form View Buttons](./form-view-buttons.md)
- [Solid HTTP API](./solid-http-api.md)

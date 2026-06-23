---
title: Workflow Status
icon: "git-branch"
description: Display and update a record's workflow status (e.g. pending, active, inactive) directly from its form view.
keywords: [workflow, status, form view, workflowField, workflowFieldUpdateEnabled]
---

# Workflow Status on a Form

SolidX can render a **workflow status indicator** at the top of any form view. It reads the current value of a designated status field on the record and displays it visually - making it immediately clear what stage the record is in (e.g. *Pending*, *Active*, *Inactive*).

When enabled, users can also **click the indicator to change the workflow status** without editing any other form field.

---

## Prerequisites

Before configuring the form view, the model must have a field that holds the workflow state - typically a **selectionStatic** or **selectionDynamic** field (e.g. `status`). This field should be defined in the model metadata and configured with the valid state values your workflow uses.

---

## Configuration

Add `workflowField` and optionally `workflowFieldUpdateEnabled` to your form view's `layout.attrs`:

```json
{
  "name": "institute-form-view",
  "displayName": "Institute",
  "type": "form",
  "moduleUserKey": "fees-portal",
  "modelUserKey": "institute",
  "layout": {
    "type": "form",
    "attrs": {
      "name": "form-1",
      "label": "Institute",
      "className": "grid",
      "workflowField": "status",
      "workflowFieldUpdateEnabled": true
    },
    "children": [
      // ... sheets, notebooks, pages, rows, columns, fields
    ]
  }
}
```

**File path:**
```bash
/solid-api/module-metadata/<module-name>/<module-name>-metadata.json
```

---

## Attribute Reference

| Attribute | Type | Required | Description |
|---|---|---|---|
| `workflowField` | `selectionStatic \| selectionDynamic` | Yes | The model field name whose value represents the current workflow state. Its value is displayed in the workflow status indicator at the top of the form. |
| `workflowFieldUpdateEnabled` | `boolean` | No (default: `false`) | When `true`, the user can click the workflow status indicator on the form to update the status directly. When `false`, the indicator is read-only. |

---

## Behavior

### Read-only indicator (`workflowFieldUpdateEnabled: false`)

The workflow status is rendered as a visual badge or stepper at the top of the form, reflecting the current value of `workflowField`. The user cannot change it from this UI - updates must go through another mechanism (e.g. a form button or a backend handler).

Use this when workflow transitions are controlled by business logic or require additional validation before the status can change.

### Updatable indicator (`workflowFieldUpdateEnabled: true`)

The workflow status indicator becomes interactive. The user can click on a target state in the indicator to transition the record to that state directly from the form.

Use this when workflow transitions are straightforward and do not require extra validation or side effects.

---

## Example Use Cases

- **Institute onboarding** - display `Pending → Active → Suspended` states on the institute form, allowing admins to activate or suspend an institute in one click.
- **Payment collection** - show `Unpaid → Partially Paid → Fully Paid` on a payment record form as a read-only progress indicator driven by a computed field.
- **Leave requests** - render `Submitted → Approved → Rejected` on an HR form, letting approvers change the status directly.

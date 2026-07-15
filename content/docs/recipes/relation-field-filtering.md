---
title: Filtering Relation Field Options
icon: "filter"
description: Restrict the options shown in a relation field dropdown using relationFieldFixedFilter (field metadata) and whereClause (layout attribute).
keywords: [relation field, filter, whereClause, relationFieldFixedFilter, many-to-one, dropdown, cascading]
---

# Filtering Relation Field Options

When a form contains a relation field (many-to-one, many-to-many), SolidX fetches all records from the related model to populate the dropdown. In many real-world scenarios you only want to show a **subset** of those records - for example, users who belong to a specific department, or only active records.

SolidX provides two complementary mechanisms for this:

| Mechanism | Where it lives | Scope |
|---|---|---|
| `relationFieldFixedFilter` | Field metadata | Applied globally - every form that uses this field |
| `whereClause` | Layout `attrs` on the field node | Applied per-layout - overrides `relationFieldFixedFilter` when present |

---

## Prerequisites

The filter values use the same **SolidX filter operators** (`$eq`, `$in`, `$containsi`, `$and`, etc.) as the SolidX REST API filter syntax. The value must be serialised as a **JSON string**.

---

## `relationFieldFixedFilter` - Global Field-Level Filter

Set this on the field definition in your field metadata JSON. The filter is applied every time this field appears anywhere in the application.

### When to use

Use `relationFieldFixedFilter` when the restriction is a permanent business rule that applies in every context - for example, a `User` relation field that should always only show users belonging to a specific department.

### Configuration

```json
{
  "name": "assignedUser",
  "displayName": "Assigned User",
  "type": "relation",
  "relationType": "manyToOne",
  "relationCoModelSingularName": "users",
  "relationFieldFixedFilter": "{\"department\":{\"id\":{\"$eq\":3}}}"
}
```

**File path:**
```bash
/solid-api/module-metadata/<module-name>/field-metadata/<model-name>/<field-name>.json
```

---

## `whereClause` - Per-Layout Filter

Set this as an `attrs` property on the field node inside a specific form view layout. It takes priority over `relationFieldFixedFilter` when both are present.

### When to use

Use `whereClause` when the restriction depends on the context of a specific view - for example, showing only **active** users on an assignment form, while a different form for the same field may show all users.

### Static configuration

```json
{
  "name": "assignment-form-view",
  "type": "form",
  "layout": {
    "type": "form",
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "assignedUser",
          "whereClause": "{\"status\":{\"$eq\":\"active\"}}"
        }
      }
    ]
  }
}
```

---

## Filtering Based on Another Form Field

A common requirement is to narrow one dropdown based on what the user has selected in another field on the same form - for example, showing only users who belong to the currently selected department. SolidX supports two approaches for this.

### Approach 1: Handlebars interpolation in `whereClause` (no code required)

`whereClause` supports **Handlebars templates**. When SolidX fetches options for the field, it evaluates the template against the current form values before sending the filter to the API. This means the dropdown automatically re-filters whenever the referenced field changes - no handler needed.

```json
{
  "type": "field",
  "attrs": {
    "name": "assignedUser",
    "whereClause": "{\"department\":{\"id\":{\"$eq\":\"{{department.id}}\"}}}"
  }
}
```

**Behaviour when the referenced field has no value:** if `department` has not been selected yet, the filter evaluates to an empty value and is automatically skipped - the full unfiltered list is shown.

**Limitation in edit mode:** when the form loads an existing record, the child field already has a selected value. If the user then changes the parent field, the child dropdown re-filters correctly but the previously selected value **is not cleared automatically**. This can leave the form in an inconsistent state - the child field still shows a value that no longer belongs to the new parent. Use Approach 2 (handler) if the form is used for editing existing records.

Use this approach when:
- The form is used for creating new records (child field starts empty)
- The filter depends on a single field present on the same form
- No clearing or other side effects are needed when the parent field changes

### Approach 2: `formViewChangeHandler` (programmatic, full control)

Use a `formViewChangeHandler` with `layoutManager.updateNodeAttributes` when you need conditional logic, want to combine the filter with other side effects (e.g. clearing the child field), or the filter value requires computation beyond simple interpolation.

```typescript
// solid-ui/src/<module-name>/admin-layout/<model-name>/extension-functions/<model-name>FormChangeHandler.ts
import { SolidUiEvent, SolidViewLayoutManager } from "@solidxai/core-ui";

const assignmentFormChangeHandler = (event: SolidUiEvent) => {
  const { changedFieldId, modifiedFieldValue } = event;
  const layoutManager = new SolidViewLayoutManager(event.viewMetadata.layout);

  if (changedFieldId === "department") {
    const filter = modifiedFieldValue?.id
      ? { department: { id: { $eq: modifiedFieldValue.id } } }
      : null;

    layoutManager.updateNodeAttributes("assignedUser", {
      whereClause: filter ? JSON.stringify(filter) : null,
    });

    // Optionally clear the child field when the parent changes
    return {
      layoutChanged: true,
      dataChanged: true,
      newLayout: layoutManager.getLayout(),
      newFormData: { ...event.formData, assignedUser: null },
    };
  }

  return { layoutChanged: false, dataChanged: false };
};

export default assignmentFormChangeHandler;
```

Register the handler in `solid-ui/src/<module-name>/<module-name>.ui-module.ts`:

```ts
extensionFunctions: [
  {
    name: "assignmentFormChangeHandler",
    fn: assignmentFormChangeHandler,
    type: ExtensionFunctionTypes.onFieldChange,
  },
]
```

Wire it to the form layout's `onFieldChange` key in your view metadata.

Use this approach when:
- The form is used for editing existing records (child field may already have a selected value)
- You need to clear or reset the child field when the parent changes
- The filter requires conditional logic (e.g. different filters for different parent values)
- The filter depends on data not directly available as a form field value

---

## Priority

When both `relationFieldFixedFilter` and `whereClause` are present on the same field:

```
whereClause (layout attrs)  >  relationFieldFixedFilter (field metadata)
```

`whereClause` wins and completely replaces `relationFieldFixedFilter` for that layout - they are not merged.

---

## Worked Example: Institute Users by Department and Status

**Scenario:** An assignment form lets an admin pick a user from a list. Users belong to departments and have an `active` / `inactive` status. The goal is to show only **active users in Department 3**.

Because `whereClause` completely replaces `relationFieldFixedFilter` (it does not AND with it), both conditions must be combined **inside a single filter** wherever they need to apply together.

### Option A - Both conditions in `relationFieldFixedFilter` (global, static)

Use this when the restriction applies to every form that shows this field and the department ID is fixed.

**Field metadata** (`assigned-user.json`):
```json
{
  "name": "assignedUser",
  "displayName": "Assigned User",
  "type": "relation",
  "re": "manyToOne",
  "relationCoModelSingularName": "users",
  "relationFieldFixedFilter": "{\"$and\":[{\"department\":{\"id\":{\"$eq\":3}}},{\"status\":{\"$eq\":\"active\"}}]}"
}
```

Result: every form showing `assignedUser` will only offer **active users in Department 3**.

### Option B - Both conditions in `whereClause` (per-layout)

Use this when only a specific form view needs this restriction, or when the department ID must come from another field on the form.

**Layout** (`assignment-form-view.json`) with a static department ID:
```json
{
  "type": "field",
  "attrs": {
    "name": "assignedUser",
    "whereClause": "{\"$and\":[{\"department\":{\"id\":{\"$eq\":3}}},{\"status\":{\"$eq\":\"active\"}}]}"
  }
}
```

Result: only on this form, the dropdown shows **active users in Department 3**. The `relationFieldFixedFilter` (if any) is ignored entirely because `whereClause` is present.

### Option C - Dynamic department from a form field (Handlebars)

When the form has a `department` picker, use Handlebars interpolation in `whereClause` - no handler required:

```json
{
  "type": "field",
  "attrs": {
    "name": "assignedUser",
    "whereClause": "{\"$and\":[{\"department\":{\"id\":{\"$eq\":\"{{department.id\"}}}}},{\"status\":{\"$eq\":\"active\"}}]}"
  }
}
```

Result: as soon as the admin picks a department, the `assignedUser` dropdown immediately narrows to **active users in that department**. Before any department is selected, all active users are shown.

### Option D - Dynamic department with child field reset (handler)

When you also want to **clear `assignedUser`** whenever the department changes:

```typescript
// formViewChangeHandler
if (changedFieldId === "department") {
  const filter = modifiedFieldValue?.id
    ? { $and: [{ department: { id: { $eq: modifiedFieldValue.id } } }, { status: { $eq: "active" } }] }
    : null;

  layoutManager.updateNodeAttributes("assignedUser", {
    whereClause: filter ? JSON.stringify(filter) : null,
  });

  return {
    layoutChanged: true,
    dataChanged: true,
    newLayout: layoutManager.getLayout(),
    newFormData: { ...event.formData, assignedUser: null },
  };
}
```

Result: when the admin changes department, `assignedUser` is cleared and the dropdown re-filters to active users in the new department.

---

## Attribute Reference

| Attribute | Where | Type | Description |
|---|---|---|---|
| `relationFieldFixedFilter` | Field metadata | `string` (JSON) | Permanent filter applied every time this relation field is rendered. Serialised SolidX filter object. |
| `whereClause` | Layout field node `attrs` | `string` (JSON or Handlebars JSON) | Per-layout filter. Overrides `relationFieldFixedFilter`. Supports `{{fieldId.property}}` Handlebars interpolation. Can be updated at runtime via `layoutManager.updateNodeAttributes`. |

---

## Example Use Cases

- **HR module** - an "Assign Reviewer" field that only shows users with the `reviewer` role.
- **Multi-branch retail** - a "Branch Staff" field on a sales order form that only shows staff belonging to the selected branch (cascading via `formViewChangeHandler`).
- **Support tickets** - an "Escalate To" field that only shows senior agents (filtered by tier) and only active ones (filtered by status).

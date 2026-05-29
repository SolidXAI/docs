---
title: Field Documentation SOP
description: Standard operating procedure for documenting SolidX field types across schema, rendering, and quality check artifacts.
sidebar_position: 2
---

# Field Documentation SOP

This page defines the standard operating procedure for documenting each SolidX field type.

It is the working contract used when expanding field coverage across:

- [Field Metadata](./field-metadata.md)
- [View Metadata](./view-metadata.md)
- frontend quality checklists in `solid-core-ui`
- backend quality checklists in `solid-core-module`

The goal is consistency. Each field type should be documented with the same structure, the same split of responsibility, and the same level of evidence.

## Scope

For each field type, we update the following artifacts together:

1. [field-metadata.md](/Users/harishpatel/Code/javascript/solidxai-docs/docs/developer-docs/metadata_schema/field-metadata.md)
2. [view-metadata.md](/Users/harishpatel/Code/javascript/solidxai-docs/docs/developer-docs/metadata_schema/view-metadata.md)
3. [field-quality-check-fixes.md](/Users/harishpatel/Code/javascript/solid-core-ui/src/components/core/form/field-quality-check-fixes.md)
4. [field-quality-check-fixes.md](/Users/harishpatel/Code/javascript/solid-core-ui/src/components/core/list/field-quality-check-fixes.md)
5. [field-quality-check-fixes.md](/Users/harishpatel/Code/javascript/solid-core-module/src/helpers/field-crud-managers/field-quality-check-fixes.md)

## Documentation Split

The same field type appears in more than one place, but each page has a distinct job.

### Field Metadata

`field-metadata.md` is the schema and runtime contract for a field type.

It answers questions such as:

- What does this field type mean?
- Which attrs belong to the field definition itself?
- How is the field validated?
- How does it persist?
- How does it participate in filtering, querying, relation handling, or other backend behavior?

It does not own widget catalogs or layout behavior.

### View Metadata

`view-metadata.md` is the rendering and layout contract for a field type.

It answers questions such as:

- How does this field render by default in a form?
- How does it render by default in a list?
- Which layout attrs and field-node attrs matter?
- Which alternative widgets are supported?
- Which widget-specific attrs are supported?
- What do real metadata examples look like?

### Quality Checklist Files

The quality checklist files are the improvement backlog that sits next to the implementation.

- `solid-core-ui/src/components/core/form/field-quality-check-fixes.md`
  Covers form-layer concerns
- `solid-core-ui/src/components/core/list/field-quality-check-fixes.md`
  Covers list and tree rendering concerns
- `solid-core-module/src/helpers/field-crud-managers/field-quality-check-fixes.md`
  Covers backend validation, transformation, persistence, and correctness concerns

## Per-Field Workflow

For each field type, follow this sequence:

1. Review the backend field contract in `solid-core-module`
2. Review the form implementation in `solid-core-ui`
3. Review the list and tree implementation in `solid-core-ui`
4. Search for real metadata examples in consuming projects
5. Update `field-metadata.md`
6. Update `view-metadata.md`
7. Update the three quality checklist files

This keeps the docs and the implementation backlog aligned.

## Research Inputs

Every field-type pass should be grounded in the actual implementation.

Only document attributes that are currently supported by the platform. If an attribute exists in an entity or code path but is not supported in practice, do not mention it in the docs, examples, or per-field reference tables until support is real and reviewable.

### Backend sources

Review the relevant backend behavior in:

- `solid-core-module/src/entities/field-metadata.entity.ts`
- `solid-core-module/src/services/crud.service.ts`
- `solid-core-module/src/services/crud-helper.service.ts`
- `solid-core-module/src/helpers/field-crud-managers/`

### Frontend sources

Review the relevant frontend behavior in:

- `solid-core-ui/src/components/core/form/fields/`
- `solid-core-ui/src/components/core/list/columns/`
- `solid-core-ui/src/components/core/list/widgets/`
- `solid-core-ui/src/helpers/registry.ts`

### Consumer examples

Search for real metadata usage across consuming projects under:

- `/Users/harishpatel/Code/javascript`

Prefer examples from application metadata over invented snippets. Use full widget names, aliases, and likely field names when searching.

If no trustworthy example exists, explicitly use:

`Example coming soon..`

## Field Metadata SOP

For each field type section in [field-metadata.md](/Users/harishpatel/Code/javascript/solidxai-docs/docs/developer-docs/metadata_schema/field-metadata.md), use this structure:

1. Short overview
2. Attribute reference table
3. Runtime behavior
4. Representative field metadata example
5. Pointer to view metadata for rendering concerns

### What to include

- semantic meaning of the field
- field-level attrs only
- validation behavior
- persistence behavior
- filtering and query behavior where relevant
- platform flags where relevant
- specialized semantics such as relation, media, selection, or computed behavior

### What not to include

- layout attrs
- widget-specific attrs
- widget catalogs
- list, form, or tree rendering documentation
- unsupported field attrs, even if they exist in the underlying entity shape

## View Metadata SOP

For each field type section in [view-metadata.md](/Users/harishpatel/Code/javascript/solidxai-docs/docs/developer-docs/metadata_schema/view-metadata.md), use this structure under the relevant view families.

### List View and Form View

For each field type under `List View` and `Form View`:

1. Short rendering overview
2. Main tab group:
   - `Default rendering`
   - `Alternative widgets`

### Default rendering tab

The `Default rendering` tab should contain:

- the default widget or widgets
- default behavior
- relevant layout attrs and field-node attrs
- one default example inside the standard collapsed accordion

### Alternative widgets tab

The `Alternative widgets` tab should contain:

- a summary table of supported alternative widgets
- all widget-specific documentation for that field type

Each alternative widget should then have:

1. A small subsection within the `Alternative widgets` tab
2. A nested tab group:
   - `Extra attrs`
   - `Example`

If a widget has no real consumer example yet, the example tab should say:

`Example coming soon..`

### Tree View

`Tree View` should document only tree-specific behavior.

If the tree renderer reuses list widgets, say that clearly and avoid duplicating the full widget catalog.

### Card And Kanban Views

`Card` and `Kanban` should be documented at the card-composition level unless a field type has meaningful field-specific widget behavior there.

## Example Selection SOP

Use the following rules when choosing examples:

1. Prefer real metadata from consuming projects
2. Prefer examples that are clean and representative
3. Prefer examples that demonstrate the actual behavior being documented
4. Avoid examples that blur field-type boundaries or rely on unusual edge cases unless the edge case is the point
5. If a widget is registered but no trustworthy real usage exists, do not invent one without calling that out

## Quality Checklist SOP

For each field type, update all three checklist files.

### Backend checklist

Add items for:

- validation gaps
- attr contract ambiguities
- transformation and normalization concerns
- persistence or query consistency issues
- logical enhancements that preserve the current architecture

### Form checklist

Add items for:

- edit and view widget gaps
- input behavior issues
- accessibility and UX improvements
- attribute support gaps
- meaningful alternative widget opportunities

### List checklist

Add items for:

- list and tree rendering gaps
- truncation, scanability, and discoverability issues
- widget support gaps
- ambiguous rendering behavior
- meaningful alternative widget opportunities

## Tone And Quality Bar

All documentation should read like product documentation rather than internal notes.

Write in a style that is:

- clear
- direct
- implementation-aware
- user-facing
- consistent across field types

Avoid:

- internal shorthand
- notes to ourselves
- excessive service or class name references
- implementation narration when a stable behavioral explanation is enough

## Definition Of Done

A field type is considered complete for a given pass when:

1. `field-metadata.md` is updated
2. `view-metadata.md` is updated
3. the three quality checklist files are updated
4. real examples have been added where available
5. placeholders remain only where evidence is not yet available
6. the docs read cleanly without mixing backend and frontend concerns

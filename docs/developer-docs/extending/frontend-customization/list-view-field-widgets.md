---
sidebar_position: 5
title: List Column Widgets
description: Learn how to create list column widgets for the frontend of your application.
summary: "Guide to customizing list field display in SolidX using built-in or custom widgets. Covers module-based file location, manifest registration, `viewWidget` wiring, `SolidListFieldWidgetProps`, and examples like score widgets with aliases."
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_list_field_widget]
---

## Overview

List view field widgets let you customize how fields are displayed in a list view.

They are configured with the `viewWidget` attribute in list view layout JSON.

You can use either:

- built-in widgets provided by `@solidxai/core-ui`
- custom widgets registered through the owning UI module manifest

For example, to display a user's name with an avatar, you can use the built-in `SolidShortTextAvatarWidget`.

## Configuring a List View Widget

```json
{
  "name": "model-list-view",
  "layout": {
    "type": "list",
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "fullName",
          "label": "Name",
          "viewWidget": "SolidShortTextAvatarWidget",
          "isSearchable": true
        }
      }
    ]
  }
}
```

:::tip
When registering a custom widget, you can provide an alias so the layout references a short stable name instead of the full component name.
:::

## Built-in Widgets

SolidX ships with pre-built list column widgets. Reference them directly in your layout JSON via `viewWidget`.

<div style={{overflowX: 'auto'}}>

| Field Type | Description | Widget Name | Alias |
|---|---|---|---|
| `shortText` | Default plain text column | `DefaultTextListWidget` | — |
| `shortText` | Masked text | `MaskedShortTextListViewWidget` | `maskedShortTextList` |
| `shortText`, `relation` | Text with a colored initials avatar badge | `SolidShortTextAvatarWidget` | — |
| `shortText` | Render value as a thumbnail image | `SolidShortTextFieldImageListWidget` | — |
| `boolean` | Boolean column display | `DefaultBooleanListWidget` | — |
| `date` | Published or Draft status tag | `PublishedStatusListViewWidget` | `publishedStatus` |
| `mediaSingle` | Single media thumbnail | `DefaultMediaSingleListWidget` | — |
| `mediaMultiple` | Multiple media thumbnails | `DefaultMediaMultipleListWidget` | — |
| `relation.many2one` | Many-to-one relation label | `DefaultRelationManyToOneListWidget` | — |
| `relation.many2one` | Many-to-one with colored initials avatar | `SolidManyToOneRelationAvatarListWidget` | — |
| `relation.many2many` | Many-to-many comma-separated labels | `DefaultRelationManyToManyListWidget` | — |
| `relation.many2many` | Many-to-many with colored initials avatars | `SolidManyToManyRelationAvatarListWidget` | — |
| `relation.one2many` | One-to-many relation column | `DefaultRelationOneToManyListWidget` | — |

</div>

## Creating a Custom Widget

### 1. Create the Widget Component

```tsx
import { SolidListFieldWidgetProps } from "@solidxai/core-ui";

export const ScoreWidget = ({ rowData, fieldMetadata }: SolidListFieldWidgetProps) => {
  let labelColor;
  let backgroundColor;

  if (rowData[fieldMetadata.name] >= 1 && rowData[fieldMetadata.name] <= 2) {
    labelColor = "#1DD900";
    backgroundColor = "#E7FDE4";
  } else if (rowData[fieldMetadata.name] >= 3 && rowData[fieldMetadata.name] <= 4) {
    labelColor = "#008C26";
    backgroundColor = "#E9FFEF";
  } else if (rowData[fieldMetadata.name] >= 5 && rowData[fieldMetadata.name] <= 9) {
    labelColor = "#FFA600";
    backgroundColor = "#FFF7E7";
  } else {
    labelColor = "#E63946";
    backgroundColor = "#FDE8E9";
  }

  return (
    <div className="flex items-center justify-start">
      <p style={{ color: labelColor, backgroundColor, padding: "8px", borderRadius: "5px" }}>
        {rowData[fieldMetadata.name]}
      </p>
    </div>
  );
};
```

File location:

```text
solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/ScoreWidget.tsx
```

### 2. Register the Widget

Register the widget in the owning module manifest:

```ts
import { ExtensionComponentTypes, type SolidUiModule } from "@solidxai/core-ui";
import { ScoreWidget } from "./admin-layout/book/extension-components/ScoreWidget";

const libraryUiModule = {
  name: "library",
  extensionComponents: [
    {
      name: "ScoreWidget",
      component: ScoreWidget,
      type: ExtensionComponentTypes.list_field_widget,
      aliases: ["score"],
    },
  ],
} satisfies SolidUiModule;

export default libraryUiModule;
```

### 3. Use in Layout

```json
{
  "type": "field",
  "attrs": {
    "name": "score",
    "label": "Score",
    "viewWidget": "ScoreWidget"
  }
}
```

## How It Works

1. SolidX loads the list view layout.
2. It checks fields with a `viewWidget` attribute.
3. The registered widget component is resolved by name or alias.
4. The widget is rendered for each row with props of type `SolidListFieldWidgetProps`.

```tsx
export type SolidListFieldWidgetProps = {
  rowData: any;
  solidListViewMetaData: any;
  fieldMetadata: FieldMetadata;
  column: any;
};
```

## Parameter Notes

- `rowData`: current row record being rendered
- `solidListViewMetaData`: list metadata and layout context
- `fieldMetadata`: model field definition for the current column
- `column`: resolved column config from the active list layout

## API Integration Inside Widgets

List field widgets can use either supported frontend API style.

### Option A: Solid HTTP Helpers

Use `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, or `solidAxios` for localized API interaction.

### Option B: Redux / RTK Query

If the widget participates in wider shared state, place RTK Query APIs, reducers, and middleware under:

- `solid-ui/src/<module-name>/redux/`

and register them through the same module manifest.

## Related

- [Form View Field Widgets](./form-view-field-widgets.md)
- [Kanban Card Widget](./kanban-card-widget.md)
- [Custom Widgets](./custom-widgets.md)
- [Redux Module Integration](./redux-module-integration.md)

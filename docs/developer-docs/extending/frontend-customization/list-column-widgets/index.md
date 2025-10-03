---
sidebar_position: 2
title: List Column Widgets
description: Learn how to create list column widgets for the frontend of your application.
---

import { IoIosArrowForward } from "react-icons/io";


#  List Column Widgets

##  Overview
List view widgets allow you to **customize the display of fields** in a list view.  
You can render fields using **built-in widgets** or by creating your own **custom widgets**.

 For example, to display a user's name along with their avatar, you can use the built-in widget **`SolidShortTextAvatarWidget`**.

The view widget is configured using the `viewWidget` attribute in the **list view layout JSON**.



##  Configuring a List View Widget

```json
{
  "name": "model-list-view",
  ...
  "layout": {
    "type": "list",
    ...
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

 The widgets can be:
- **Built-in** (provided by `@solidstarters/solid-core-ui`)
- **Custom** (created by you)

In the example above, `SolidShortTextAvatarWidget` is a **built-in widget** that displays the user's name and avatar.



##  Creating a Custom Widget

If you need a custom display (e.g. a **score widget** with colors based on score values), follow these steps:

### 1. Create the Widget Component
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>ScoreWidget</code>
</summary>

```tsx
import { SolidListFieldWidgetProps } from "@solidstarters/solid-core-ui/dist/types/solid-core";

export const ScoreWidget = ({ rowData, solidListViewMetaData, fieldMetadata, column }: SolidListFieldWidgetProps) => {
    let labelColor;
    let backgroundColor;

    if (rowData[fieldMetadata.name] >= 1 && rowData[fieldMetadata.name] <= 2) {
        labelColor = '#1DD900';
        backgroundColor = '#E7FDE4';
    } else if (rowData[fieldMetadata.name] >= 3 && rowData[fieldMetadata.name] <= 4) {
        labelColor = '#008C26';
        backgroundColor = '#E9FFEF';
    } else if (rowData[fieldMetadata.name] >= 5 && rowData[fieldMetadata.name] <= 9) {
        labelColor = '#FFA600';
        backgroundColor = '#FFF7E7';
    } else if (rowData[fieldMetadata.name] >= 10 && rowData[fieldMetadata.name] <= 16) {
        labelColor = '#E63946';
        backgroundColor = '#FDE8E9';
    } else if (rowData[fieldMetadata.name] >= 17 && rowData[fieldMetadata.name] <= 25) {
        labelColor = '#DC0600';
        backgroundColor = '#FFF2F1';
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start' }}>
            <p style={{ color: labelColor, backgroundColor: backgroundColor, padding: '8px', borderRadius: '5px' }}>
                {rowData[fieldMetadata.name]}
            </p>
        </div>
    );
};
```
</details>

 **File Path:**
```
/solid-ui/app/admin/extensions/ScoreWidget.tsx
```



### 2. Register the Widget
Register the widget in `solid-extensions.ts` so the framework recognizes it.

```tsx
registerExtensionComponent("ScoreWidget", ScoreWidget);
```

 **File Path:**
```
/solid-ui/app/admin/extensions/solid-extensions.ts
```



### 3. Use in Layout
Now you can use `ScoreWidget` in your layout JSON:

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



##  How It Works

1. When the **SolidX app** loads the list view, it reads the **layout configuration**.
2. It checks fields that have a `viewWidget` attribute.
3. The corresponding widget is **dynamically imported**.
4. The widget is rendered for each row, with props of type `SolidListFieldWidgetProps`:

```tsx
export type SolidListFieldWidgetProps = {
    rowData: any;
    solidListViewMetaData: any
    fieldMetadata: FieldMetadata;
    column: any;
}

export type FieldMetadata = CommonEntity & {
    id: number;
    name: string;
    displayName: string;
    // For now we have kept it flexible allowing any number of other key / value pairs...
    [key: string]: any;
}
```
5. The widget displays data based on **custom logic** you define.



##  TODO
- Add detailed explanation of each parameter passed to the widget:
  - `rowData`
  - `solidListViewMetaData`
  - `fieldMetadata`
  - `column`
<!-- ```tsx -->

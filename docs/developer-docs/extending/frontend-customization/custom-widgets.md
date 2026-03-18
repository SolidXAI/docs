---
sidebar_position: 2
title: Custom Widgets
description: Learn how to create custom widgets for the frontend of your application.
summary: Guide to creating custom widgets in SolidX using the built-in `CustomHtml` widget for extending UI functionality without field associations. Covers configuring widgets in form layouts with dynamic HTML rendering, using placeholders for field values and custom variables (e.g., `{{ctxtTitleAlphpabetCount}}`), receiving `SolidFormWidgetProps`, and setting custom variables via form event handlers for enhanced UI interactions.
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_widget]
---

import { IoIosArrowForward } from "react-icons/io";


#  Custom Widgets

##  Overview
Custom widgets allow you to **extend the UI functionality** of your frontend application by adding new components to your view layouts.  
These widgets:
- Are **not associated with any fields** in the model.  
- Are used to **enhance the UI** by providing **custom rendering** or **interaction capabilities**.  

 SolidX provides a built-in way to create custom widgets using the **`CustomHtml`** widget.



##  How to Configure the `CustomHtml` Widget

 Example: Display how many characters a user has typed in a text field.

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Code: CustomHtml Widget Configuration
</summary>

```json
{
  "type": "custom",
  "attrs": {
    "name": "page-1-row-1-div-1-div-1-title-custom",
    "widget": "CustomHtml",
    "html": "<span>You have typed {{ctxtTitleAlphpabetCount}}</span>",
    "visible": false
  }
}
```
</details>

###  Explanation
- Uses the `CustomHtml` widget to show a dynamic message.  
- Displays the **number of characters typed** in a text field.  
- Receives props of type `SolidFormWidgetProps`.  
- The variable `{{ctxtTitleAlphpabetCount}}` is replaced dynamically.  

 This placeholder can represent:  
- A **field value** (referenced by field name).  
- A **custom variable**, set in the form data via a **form handler**.  

 Learn more here: [Form View Event Listeners](./form-view-events)



##  How It Works

1. SolidX loads the **form layout** in edit/view mode.  
2. It identifies **custom fields** (`type: custom`).  
3. It dynamically imports the corresponding widget component.  
4. The widget is rendered with the following props:  

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Code: Props Interface
</summary>

```tsx
export type SolidFormWidgetProps = {
    field: any;
    // This comes from Formik...
    formData: Record<string, any>;
    viewMetadata: SolidView;
    fieldsMetadata: FieldsMetadata;
    formViewData: any;
};
```
</details>

5. The widget applies your **custom rendering logic**.  



 With this approach, you can create **reusable UI enhancements** and extend your SolidX frontend with ease.

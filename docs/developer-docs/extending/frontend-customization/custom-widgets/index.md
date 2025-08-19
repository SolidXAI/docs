---
sidebar_position: 2
title: Custom Widgets
description: Learn how to create custom widgets for the frontend of your application.
---

## Overview
Custom widgets allow you to extend the UI functionality of your frontend application by adding new components to your view layouts, that can be reused.
These widgets are not associated with any fields in the model.
Instead, they are used to enhance the user interface by providing custom rendering or interaction capabilities.

SolidX does provide a built-in way to create custom widgets using the `CustomHtml` widget.

## How to configure the CustomHtml widget
For e.g if i need to create a custom widget that displays how many characters a user has typed in a text field, I can create a custom widget and place it below a particular fields in the form layout.

You can configure it as below:

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

Above configuration uses the `CustomHtml` widget to display a message that shows the number of characters typed in a text field.

It receives props of type SolidFormWidgetProps


The `{{ctxtTitleAlphpabetCount}}` is a placeholder that will be replaced with the actual count dynamically. This variable could either be a field value which can accessed using the field name or a custom variable, which can be set in the form data using the custom handler. You can read more about form handlers in this section [Form View Event Listners](../form-view-event-listeners/index.md)

## 🔄 How It Works
1. SolidX loads the **form layout** in edit/view mode.  
2. It identifies custom fields i.e with type custom 
3. It dynamically imports the corresponding widget component.  
4. The widget is rendered with props like:
``` tsx
export type SolidFormWidgetProps = {
    field: any;
    // This comes from Formik...
    formData: Record<string, any>;
    viewMetadata: SolidView;
    fieldsMetadata: FieldsMetadata;
    formViewData: any;
}
```
5. The widget then applies your **custom rendering logic**.  
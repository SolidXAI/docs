---
sidebar_position: 1
title : Form View Events
description: Learn how to create event listeners for form view events in your frontend application.
summary: Explains creating event listeners for SolidX form view events to extend frontend functionality. Covers supported events (onFormLayoutLoad, onFormDataLoad, onFieldChange, onFieldBlur, onCustomWidgetRender), registering handlers using `registerExtensionFunction`, accessing event data (type, modifiedField, modifiedFieldValue, formData, viewMetadata, fieldsMetadata), modifying UI layout dynamically with `SolidViewLayoutManager`, returning changes (layoutChanged, dataChanged, newFormData, newLayout), and examples like character count tracking.
solidx_concerns: [add_change_handler_function, onlayoutload_handler_function, ondataload_handler_function]
---

## Overview
Form view event listeners allow you to extend the functionality of your frontend application by responding to specific SolidX UI events that occur in form views.

These listeners give you the capability to modify the UI layout i.e hide/show certain fields and form data as well i.e set/unset data in the form fields, as well as access the form state or metadata using the built in methods provided by SolidX.

Currently, SolidX supports the following types of form event listeners:

SolidX supports below types of form  event listeners:
1. **onFormLayoutLoad**: - Triggered when the form layout is loaded.
2. **onFormDataLoad**: - Triggered when the form data is loaded.
3. **onFieldChange**: - Triggered when a field value changes.
4. **onFieldBlur**: - Triggered when a field loses focus.
5. **onCustomWidgetRender**: - Triggered when a custom widget is rendered.

These handlers are registered as below in the solid-extensions.ts file in the solid-ui/app folder, using the built-in `registerExtensionFunction` method:

Below is an example of registering a form view event listener which gets triggered when the form layout is loaded. This set a new variable in the form data which tracks the characters typed. This variable can then be accessed in the Custom components for rendering the in the UI accordingly. 

For e.g you may refer [Custom Widget](../custom-widgets/index.md) to see how this variable can be used in the custom widget to show the character count.

Configuring a form view event listener:

1. Create the listener function in your extensions folder e.g `solid-ui/app/admin/extensions/bookFormViewChangeHandler.ts`
``` typescript
const handleBookFormViewChange = (event: SolidUiEvent) => {

    const { type, modifiedField, modifiedFieldValue, formData, viewMetadata, fieldsMetadata } = event;
    const layout = viewMetadata.layout;

    // handle change to title.
    // TODO: here we intend on injecting something in the form context which we will then use to render a message somewhere on the form view.
    if (modifiedField === 'title') {
        // const title = formData['title'];
        const title = modifiedFieldValue;
        const layoutManager = new SolidViewLayoutManager(layout);
        layoutManager.updateNodeAttributes('page-1-row-1-div-1-div-1-title-custom', { visible: true });
        return {
            layoutChanged: true,
            dataChanged: true,
            newFormData: {
                ctxtTitleAlphpabetCount: title ? title.length : 0
            },
            newLayout: layoutManager.getLayout()
        }
    }

}
export default handleBookFormViewChange;
```

```typescript
registerExtensionFunction("bookFormViewChangeHandler", handleBookFormViewChange);
```
 
The handler gets the below props:
``` typescript
export type SolidUiEvent = {
    type: SolidUiEvents;
    modifiedField?: string;
    modifiedFieldValue?: any;
    // This comes from Formik...
    formData: Record<string, any>;
    viewMetadata: SolidView;
    fieldsMetadata: FieldsMetadata;
    formViewLayout: LayoutNode;
}
```

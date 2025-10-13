---
sidebar_position: 4
title: Form View Field Widgets
description: Learn how to create form view field widgets for the frontend of your application.
summary: Details creating custom form view field widgets in SolidX for customizing field display in view and edit modes. Covers using built-in widgets (e.g., `integerSlider`) or creating custom ones, implementing components with `SolidFormFieldWidgetProps` (formik, fieldContext, metadata), registering widgets via `registerExtensionComponent`, configuring `editWidget`/`viewWidget` in form layout JSON, handling field validation, labels, and examples like slider widgets with tooltips and color-coded values.
solidx_concerns: [create_custom_form_field_widget]
---

import { IoIosArrowForward } from "react-icons/io";


<!-- #  Form View Field Widgets -->

##  Overview
Form view widgets allow you to **customize how fields are displayed** in a form view.  
They support both **view mode** and **edit mode**.

You can use either:
- **Built-in widgets** (provided by the framework), or  
- **Custom widgets** (that you create).

 Example: Display an integer field `score` as a **slider** using the built-in `integerSlider` widget.
<details>
    <summary className="card-title card-headear-wrapper">
        <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
        <code>Using Built-in Widget</code>
    </summary>
```json
{
  "name": "model-form-view",
  ...
  "layout": {
    "type": "form",
    ...
    "children": [
      {
        "type": "field",
        "attrs": {
          "name": "score",
          "label": "Score",
          "editWidget": "integerSlider"
        }
      }
    ]
  }
}
```
</details>
:::tip
In the above example, the `editWidget` attribute specifies the widget to use in **edit mode**. While registering a widget, you can provide an **alias** (like `integerSlider`) to reference it easily in the layout instead of the full component name e.g. `SolidIntegerSliderStyleFormEditWidget`.
:::



##  Creating a Custom Widget

### 1. Create the Widget Component
Here’s an example of an **integer slider widget**. This widget allows users to select an integer value using a slider.
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>SolidIntegerSliderStyleFormEditWidget</code>
</summary>

```tsx
import { SolidFormFieldWidgetProps } from "@solidstarters/solid-core-ui/dist/types/solid-core";

export const SolidIntegerSliderStyleFormEditWidget = ({ formik, fieldContext }: SolidFormFieldWidgetProps) => {
    const fieldMetadata = fieldContext.fieldMetadata;
    const fieldLayoutInfo = fieldContext.field;
    const fieldLabel = fieldLayoutInfo.attrs.label ?? fieldMetadata.displayName;
    const showFieldLabel = fieldLayoutInfo?.attrs?.showLabel;
    const min = fieldMetadata.min || 0;
    const max = fieldMetadata.max || 5;
    const fieldName = fieldLayoutInfo.attrs.name;
    const currentValue = Number(formik.values[fieldName] ?? min);

    const isFormFieldValid = (formik: any, fieldName: string) => 
        formik.touched[fieldName] && formik.errors[fieldName];

    return (
        <div className="w-full" style={{ height: '60px' }}>
            {showFieldLabel !== false && (
                <div className="font-medium mb-2">
                    {fieldLabel}
                    {fieldMetadata.required && <span className="text-red-500"> *</span>}
                </div>
            )}
            <div className="relative h-12">
                <Range
                    step={1}
                    min={min}
                    max={max}
                    values={[currentValue]}
                    onChange={(values) => {
                        formik.setFieldValue(fieldName, values[0]);
                    }}
                    renderTrack={({ props, children }) => {
                        const percent = ((currentValue - min) / (max - min)) * 100;
                        return (
                            <div {...props} style={{
                                ...props.style,
                                height: "10px",
                                width: "100%",
                                borderRadius: "8px",
                                backgroundColor: "var(--primary-light-color)",
                                position: "relative"
                            }}>
                                <div style={{
                                    position: "absolute",
                                    height: "100%",
                                    width: `${percent}%`,
                                    backgroundColor: "var(--primary-color)",
                                    borderRadius: "5px",
                                    top: 0,
                                    left: 0
                                }} />
                                {children}
                            </div>
                        )
                    }}
                    renderThumb={({ props }) => (
                        <div {...props} key={props.key} style={{
                            ...props.style,
                            height: "18px",
                            width: "18px",
                            border: "4px solid var(--surface-0)",
                            borderRadius: '50%',
                            backgroundColor: "var(--primary-color)"
                        }} />
                    )}
                />
                <div className="flex align-item-center justify-content-between mt-2">
                    {Array.from({ length: max - min + 1 }, (_, i) => {
                        const num = i + min;
                        return (
                            <span key={num} className="text-sm">
                                {num === 0 ? '' : num}
                            </span>
                        );
                    })}
                </div>
                {isFormFieldValid(formik, fieldLayoutInfo.attrs.name) && (
                    <div className="absolute mt-2">
                        <Message severity="error" text={formik?.errors[fieldLayoutInfo.attrs.name]?.toString()} />
                    </div>
                )}
            </div>
        </div>
    );
}

```
</details>

 **File Path:** 
 
 As per project structure, place the widget component in the `extensions` folder:

```bash
/solid-ui/app/admin/extensions/SolidIntegerSliderStyleFormEditWidget.tsx
```



### 2. Register the Widget
Widgets must be **registered** in `solid-extensions.ts`:
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   <code>Registering the Widget</code>
   </summary>
```tsx
registerExtensionComponent(
  "SolidIntegerSliderStyleFormEditWidget", // component name
  SolidIntegerSliderStyleFormEditWidget, // component reference
  ["integerSlider"]   // alias name
);
```
</details>

 **File Path:**
```
/solid-ui/app/admin/extensions/solid-extensions.ts
```


### 3. Use in Layout 
Now you can configure the widget within the form view layout configuration in the module metadata schema JSON file:
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   <code>Using Custom Widget in Layout</code>
   </summary>
```json
{
  "name": "institute-form-view",
  ... // other attributes
  "layout": {
    "type": "form",
    ... // other attributes
    "children": [
      {
      "type": "field",
      "attrs": {
          "name": "score",
          "label": "Score",
          "editWidget": "integerSlider"
        }
      }
    ]
  }
}
```
</details>

File Path:
``` /solid-api/module-metadata/<module-name>/<module-name>-metadata.json ```


##  How It Works

1. SolidX loads the **form layout** in edit mode.  
2. It identifies fields with an `editWidget`.  
3. It dynamically imports the corresponding widget component.  
4. The widget is rendered with props of type `SolidFormFieldWidgetProps`:
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   <code>SolidFormFieldWidgetProps</code>
   </summary>
``` tsx
export type SolidFormFieldWidgetProps = {
    formik: any; // Formik instance for form state management
    fieldContext?: SolidFieldProps; 
}

export type SolidFieldProps = {
    solidFormViewMetaData: any; // Metadata of the form view
    fieldMetadata: any, // Metadata of the specific field
    field: any, // Layout info of the field
    data: any, // Current data of the form
    modelName?: any, // Name of the model
    readOnly?: any, // Is the field read-only
    viewMode?: any // Is the form in view mode
    onChange?: any, // Callback for change events
    onBlur?: any, // Callback for blur events
    // Used in embedded views i.e for relation fields
    parentData?: any, // Data of the parent entity
}
```
</details>
5. The widget then applies your **custom rendering logic**.  
6. Default widgets are also rendered using the same mechanism.



##  View Widgets (Read-Only Mode)

Similarly, you can create **view widgets** for **read-only mode** using `viewWidget` instead of `editWidget`.

### Example: Boolean View Widget
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   <code>CustomBooleanFormViewWidget</code>
</summary>


```tsx
export const CustomBooleanFormViewWidget = ({ formik, fieldContext }: SolidFormFieldWidgetProps) => {
    const fieldMetadata = fieldContext.fieldMetadata;
    const fieldLayoutInfo = fieldContext.field;
    const fieldLabel = fieldLayoutInfo.attrs.label ?? fieldMetadata.displayName;

    return (
        <div className="mt-2 flex-column gap-2">
            <p className="m-0 form-field-label font-medium">{fieldLabel}</p>
            <p className="m-0">
                {formik.values[fieldLayoutInfo.attrs.name] === true ||
                 formik.values[fieldLayoutInfo.attrs.name] === "true"
                 ? "Yes" : "No"}
            </p>
        </div>
    );
}
```
</details>

This allows you to render a **boolean field as "Yes/No"** in view mode.



 With this approach, you can **seamlessly extend** SolidX form views using custom widgets for both **edit** and **view** modes.

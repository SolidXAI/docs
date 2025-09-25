---
sidebar_position: 2
title: Form View Field Widgets
description: Learn how to create form view field widgets for the frontend of your application.
---

import { IoIosArrowForward } from "react-icons/io";


#  Form View Field Widgets

##  Overview
Form view widgets allow you to **customize how fields are displayed** in a form view.  
They support both **view mode** and **edit mode**.

You can use either:
- **Built-in widgets** (provided by the framework), or  
- **Custom widgets** (that you create).

 Example: Display an integer field `score` as a **slider** using the built-in `integerSlider` widget.

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



##  Creating a Custom Widget

### 1. Create the Widget Component
Here’s an example of an **integer slider widget**:
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
```bash
/solid-ui/app/admin/extensions/SolidIntegerSliderStyleFormEditWidget.tsx
```



### 2. Register the Widget
Widgets must be **registered** in `solid-extensions.ts`:

```tsx
registerExtensionComponent(
  "SolidIntegerSliderStyleFormEditWidget",
  SolidIntegerSliderStyleFormEditWidget,
  ["integerSlider"]   // alias name
);
```

 **File Path:**
```
/solid-ui/app/admin/extensions/solid-extensions.ts
```

 **Note:** The alias `integerSlider` allows you to use this widget in layout configuration easily.



### 3. Use in Layout
Now you can configure the widget in the form view layout:

```json
{
  "type": "field",
  "attrs": {
    "name": "score",
    "label": "Score",
    "editWidget": "integerSlider"
  }
}
```



##  How It Works

1. SolidX loads the **form layout** in edit mode.  
2. It identifies fields with an `editWidget`.  
3. It dynamically imports the corresponding widget component.  
4. The widget is rendered with props of type `SolidFormFieldWidgetProps`:
``` tsx
export type SolidFormFieldWidgetProps = {
    formik: any;
    fieldContext?: SolidFieldProps;
}

export type SolidFieldProps = {
    solidFormViewMetaData: any;
    fieldMetadata: any,
    field: any,
    data: any,
    modelName?: any,
    readOnly?: any,
    viewMode?: any
    onChange?: any,
    onBlur?: any,
    parentData?: any,
}
```
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

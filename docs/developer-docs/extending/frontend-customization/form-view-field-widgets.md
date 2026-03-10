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
<details open>
    <summary className="card-title ">
        <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
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



## Built-in Widgets

SolidX ships with a set of pre-built widgets for every field type. You can reference these directly in the layout JSON without writing or registering any code.

### Edit Widgets (`editWidget`)

Used in **edit mode** via the `editWidget` attribute on a form field.

| Widget Name | Alias | Field Type | Description |
|---|---|---|---|
| `DefaultShortTextFormEditWidget` | — | `shortText` | Default single-line text input |
| `MaskedShortTextFormEditWidget` | `maskedShortTextEdit` | `shortText` | Password-style masked input |
| `SolidIconEditWidget` | — | `shortText` | Google Material Symbols icon picker dialog |
| `DefaultLongTextFormEditWidget` | — | `longText` | Default multi-line textarea |
| `DynamicJsonEditorFormEditWidget` | `jsonEditor` | `longText` | JSON editor with syntax highlighting |
| `CodeEditorFormEditWidget` | `codeEditor` | `longText` | Code editor with syntax highlighting |
| `DefaultIntegerFormEditWidget` | — | `integer` | Default number input for integers |
| `SolidIntegerSliderStyleFormEditWidget` | `integerSlider` | `integer` | Range slider for integer values |
| `DefaultDecimalFormEditWidget` | — | `decimal` | Decimal number input |
| `DefaultEmailFormEditWidget` | — | `email` | Email input with format validation |
| `DefaultPasswordFormEditWidget` | — | `password` | Password input (edit mode) |
| `DefaultPasswordFormCreateWidget` | — | `password` | Password + confirm-password input (create mode) |
| `DefaultTimeFormEditWidget` | — | `time` | Time picker |
| `DefaultDateFormEditWidget` | — | `date` | Date picker (calendar) |
| `DefaultDateTimeFormEditWidget` | — | `datetime` | Combined date and time picker |
| `DefaultBooleanFormEditWidget` | `booleanSelectbox` | `boolean` | Dropdown select (Yes / No) |
| `SolidBooleanCheckboxStyleFormEditWidget` | `booleanCheckbox` | `boolean` | Checkbox style |
| `SolidBooleanSwitchStyleFormEditWidget` | — | `boolean` | Toggle switch style |
| `DefaultJsonFormEditWidget` | — | `json` | JSON field editor |
| `DefaultRichTextFormEditWidget` | — | `richText` | WYSIWYG rich text editor |
| `DefaultSelectionStaticAutocompleteFormEditWidget` | — | `selectionStatic` | Autocomplete dropdown for static options |
| `SolidSelectionStaticRadioFormEditWidget` | — | `selectionStatic` | Radio button group |
| `SolidSelectionStaticSelectButtonFormEditWidget` | — | `selectionStatic` | Segmented select buttons |
| `DefaultSelectionDynamicFormEditWidget` | — | `selectionDynamic` | Autocomplete for API-driven dynamic options |
| `DefaultMediaSingleFormEditWidget` | — | `mediaSingle` | Single file / image upload |
| `DefaultMediaMultipleFormEditWidget` | — | `mediaMultiple` | Multiple files / images upload |
| `DefaultRelationManyToOneFormEditWidget` | — | `relation.many2one` | Autocomplete relation selector |
| `PseudoRelationManyToOneFormWidget` | — | `relation.many2one` | Short-text field wired to a many-to-one value |
| `DefaultRelationManyToManyAutoCompleteFormEditWidget` | — | `relation.many2many` | Many-to-many autocomplete chips |
| `DefaultRelationManyToManyCheckBoxFormEditWidget` | — | `relation.many2many` | Checkbox list for many-to-many selection |
| `RolePermissionsManyToManyFieldWidget` | `inputSwitch` | `relation.many2many` | Toggle-switch grid for role permissions |
| `DefaultRelationOneToManyFormEditWidget` | — | `relation.one2many` | Embedded editable table for one-to-many |
| `PseudoRelationOneToManyFormWidget` | — | `relation.one2many` | Pseudo one-to-many form widget |

### View Widgets (`viewWidget`)

Used in **view (read-only) mode** via the `viewWidget` attribute on a form field.

| Widget Name | Alias | Field Type | Description |
|---|---|---|---|
| `DefaultShortTextFormViewWidget` | — | `shortText`, `longText`, `email` | Default plain text display |
| `MaskedShortTextFormViewWidget` | `maskedShortTextForm` | `shortText` | Masked text display |
| `SolidShortTextFieldAvatarWidget` | — | `shortText` | Text with a colored initials avatar |
| `SolidIconViewWidget` | — | `shortText` | Renders a stored icon name as a Material Symbols icon |
| `DefaultIntegerFormViewWidget` | — | `integer` | Plain integer display |
| `DefaultDecimalFormViewWidget` | — | `decimal` | Plain decimal display |
| `DefaultTimeFormViewWidget` | — | `time` | Formatted time display |
| `DefaultDateFormViewWidget` | — | `date` | Formatted date display |
| `DefaultDateTimeFormViewWidget` | — | `datetime` | Formatted date and time display |
| `DefaultBooleanFormViewWidget` | — | `boolean` | Boolean display |
| `DefaultJsonFormViewWidget` | — | `json` | JSON read-only display |
| `DynamicJsonEditorFormViewWidget` | `jsonViewer` | `longText` | Read-only JSON viewer with syntax highlighting |
| `DefaultPasswordFormViewWidget` | — | `password` | Masked password display |
| `DefaultRichTextFormViewWidget` | — | `richText` | Rendered rich text (HTML) |
| `DefaultSelectionStaticFormViewWidget` | — | `selectionStatic` | Static selection label display |
| `DefaultSelectionDynamicFormViewWidget` | — | `selectionDynamic` | Dynamic selection label display |
| `DefaultMediaSingleFormViewWidget` | — | `mediaSingle` | Single media preview |
| `DefaultMediaMultipleFormViewWidget` | — | `mediaMultiple` | Multiple media thumbnails |
| `DefaultRelationManyToOneFormViewWidget` | — | `relation.many2one` | Many-to-one relation label |
| `SolidRelationFieldAvatarFormWidget` | — | `relation` | Relation value(s) rendered as avatar chips |
| `DefaultRelationOneToManyFormViewWidget` | — | `relation.one2many` | Read-only embedded table for one-to-many |



##  Creating a Custom Widget

### 1. Create the Widget Component
Here’s an example of an **integer slider widget**. This widget allows users to select an integer value using a slider.
<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    <code>SolidIntegerSliderStyleFormEditWidget</code>
</summary>

```tsx
import { SolidFormFieldWidgetProps } from "@solidxai/core-ui";

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
<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
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
<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
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
<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
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
<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
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

## Related

- [List View Field Widgets](./list-view-field-widgets) — built-in and custom widgets for list column display
- [Kanban Field Widgets](./kanban-field-widgets) — widgets for kanban card fields
- [Custom Widgets](./custom-widgets) — general guide to registering extension components

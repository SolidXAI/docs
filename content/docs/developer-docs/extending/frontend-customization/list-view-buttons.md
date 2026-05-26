---
title: List View Buttons
description: Learn how to customize list view buttons in your frontend application.
summary: Explains how to add and customize list view buttons in SolidX. Covers creating header buttons for list-wide actions and row buttons for record-specific actions, including configuration examples and prop details.
solidx_concerns: [add_list_header_button_with, add_list_row_button_with]
---

## Overview

List View Buttons enable you to add **custom actions** in list views.  
They can be used to trigger navigation, open dialogs, or perform API-based operations.

These buttons can appear at two levels:

1. **Header Buttons** — actions for the entire list (e.g., “Generate Report”).  
2. **Row Buttons** — actions for specific records (e.g., “Refund Payment”).  

---

## Adding Custom List Buttons

To add custom buttons in a list view, follow these steps:

1. **Create the button component.**  
2. **Register the component.**  
3. **Configure the layout JSON.**  

> The process is similar to [Form View Buttons](./form-view-buttons.md).  
> You can reuse the same registration and component creation logic; only the props differ slightly.

---

## Configure in Layout JSON

Below are examples of how to configure both header and row buttons in the module metadata JSON file.

### Header Button Example
<details>
<summary>
  
  `Generate Report Header Button`
</summary>

```json
{
  "name": "paymentCollectionItem-list-view",
  "displayName": "Created Payments",
  "type": "list",
  "layout": {
    "type": "list",
    "attrs": {
      "headerButtons": [
        {
          "attrs": {
            "label": "Generate Report",
            "action": "GenerateReport",
            "actionInContextMenu": false,
            "openInPopup": true,
            "icon": "pi pi-chart-bar",
            "className": "p-button-success p-button p-component",
            "closable": true
          }
        }
      ]
    }
  }
}
```
</details>

---

### Row Button Example
<details>
<summary>
  
  `Refund Payment Row Button`
</summary>

```json
{
  "name": "institute-list-view",
  "displayName": "Institutes",
  "type": "list",
  "layout": {
    "type": "list",
    "attrs": {
      "rowButtons": [
        {
          "attrs": {
            "label": "Refund Payment",
            "action": "RefundPayment",
            "actionInContextMenu": true,
            "openInPopup": true,
            "icon": "pi pi-undo",
            "className": "p-button-info p-button p-component",
            "closable": true
          }
        }
      ]
    }
  }
}
```
</details>

**File Path**
```bash
/solid-api/module-metadata/<module-name>/<module-name>-metadata.json
```

---

## Props Reference

Each list button component receives a consistent set of props from the SolidX list engine.  
Header buttons receive the **selected records** and **filters**, while row buttons receive the **row data**.

<details>
<summary>
  
  `Action Component Props`
</summary>

```ts
{
  action, // action component name e.g., "GenerateReport" or "RefundPayment"
  params: {
    moduleName: string;       // e.g. "fees-portal"
    modelName: string;        // e.g. "institute"
    id: string;               // record ID in edit mode
    embeded: boolean;         // true if the form is embedded
    handlePopupClose?: any;   // function to close popup
    customCreateHandler?: any;
    inlineCreateAutoSave?: boolean;
    customLayout?: any; 
    parentData?: any; 
    redirectToPath?: string;
    onEmbeddedFormSave?: () => void;
  },
  solidFormViewMetaData: solidFormViewMetaData.data, // form metadata
  selectedRecords: selectedRecords, // Header button only: selected list records
  filters, // Header button only: active filters applied on list
  rowData // Row button only: data of the specific row where button was clicked
}
```
</details>

> **Info**
> **Note:**  
> - **Header Buttons** → Linked Components receives `selectedRecords` and `filters`.  
> - **Row Buttons** → Linked Components receive `rowData` for the clicked record.  

---

## How It Works

1. SolidX renders the **list view** and identifies buttons in the layout.  
2. When a button is clicked, it resolves the registered component by its `action` name.  
3. The component receives contextual props (`rowData`, `selectedRecords`, etc.).  
4. The button component executes custom logic (API call, navigation, etc.).  
5. If `"openInPopup": true`, the component runs inside a modal and can close itself via `closePopup()`.

---

## Example Use Cases

### Header Buttons
- 🧾 **Generate Report** — Generate and download a summary report for all selected transactions.  

### Row Buttons
- 💸 **Refund Payment** — Initiate a refund process for that record.  
- ✉️ **Send Receipt** — Email a payment receipt for that transaction.

---

With this approach, you can **extend your list views** with interactive, contextual buttons that perform powerful actions across the list or on specific rows.

---
title: Form View Buttons
description: Learn how to customize form view buttons in your frontend application.
summary: Explains customizing SolidX form view buttons to enhance user interaction. Covers adding custom buttons, modifying existing buttons, and handling button actions using `registerExtensionComponent`. Includes a working example `PreviewPortal` button that redirects to an external hosted page.
solidx_concerns: [add_form_button]
---

## Overview

Form View Buttons let you add **custom actions** to form views.  
You can use them to trigger navigation, open dialogs, or perform API-based operations.

These buttons can be rendered **inline** or inside a **context menu**, and can either open a **popup dialog** or redirect the user elsewhere.

## Example: PreviewPortal Button

Below is a complete example of a **custom form view button** that redirects to an external hosted page (for example, a portal for an institute).  
It reads the `id` from form data or row context, calls an API to get the hosted prefix, and opens the page in a new browser tab.

<details>
<summary>
  
  `PreviewPortal.tsx`
</summary>

```tsx
import React, { useEffect, useRef, useState } from 'react';
import { Toast } from 'primereact/toast';
import axios from 'axios';
import { getSession } from 'next-auth/react';
import { useDispatch } from 'react-redux';
import { closePopup } from '@solidstarters/solid-core-ui/dist/redux/features/popupSlice';
import { Dialog } from 'primereact/dialog';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;

/**
 * This component is triggered when the user clicks a custom button in a form view.
 * It fetches the hosted page prefix for an entity and redirects the user to that hosted page.
 */
const PreviewPortal = (action: any) => { // View Props Reference section for shape
  const id = action?.params?.id;
  const dispatch = useDispatch();
  const toast = useRef<Toast>(null);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const fetchAndRedirect = async () => {
      try {
        const session: any = await getSession();
        const token = session?.user?.accessToken || '';

        // Fetch hosted page prefix for the record
        const response = await axios.get(`${API_URL}/api/institute/${id}`, {
          headers: {
            Authorization: \`Bearer \${token}\`,
          },
        });

        const hostedPagePrefix = response.data?.data?.hostedPagePrefix;
        if (!hostedPagePrefix) throw new Error('hostedPagePrefix not found');

        // Open the hosted page in a new tab and close the popup
        window.open(\`https://\${hostedPagePrefix}.com\`, '_blank');
        dispatch(closePopup());
      } catch (error) {
        console.error('Redirect failed:', error);
        toast.current?.show({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to redirect',
          life: 3000,
        });
        dispatch(closePopup());
      }
    };

    fetchAndRedirect();
  }, [id, dispatch]);

  return (
    <>
      
      <Dialog
        header=""
        visible={visible}
        style={{ width: '25vw' }}
        modal
        onHide={() => dispatch(closePopup())}
        dismissableMask={false}
      >
        <div>
          <i style={{ fontSize: '2rem' }}></i>
          Redirecting...
        </div>
      </Dialog>
    </>
  );
};

export default PreviewPortal;
```
</details>

**File Path**
```bash
/solid-ui/app/admin/extensions/PreviewPortal.tsx
```

## Register the Component

You must register your button component so that SolidX can resolve and invoke it when the form button is clicked.

<details>
<summary>
  
  `solid-extensions.ts`
</summary>

```tsx
import { registerExtensionComponent } from '@solidstarters/solid-core-ui';
import PreviewPortal from '@/app/admin/extensions/PreviewPortal';  

registerExtensionComponent('PreviewPortal', PreviewPortal);
```
</details>

**File Path**
```bash
/solid-ui/app/admin/extensions/solid-extensions.ts
```

## Configure in Layout JSON

Now, you can use this button inside your form layout metadata JSON configuration.

<details>
<summary>
  
  `Using in Layout JSON`
</summary>

```json
{
  "name": "institute-form-view",
  "layout": {
    "type": "form",
    "formButtons": [
      {
        "attrs": {
          "label": "Preview Portal",
          "icon": "pi pi-external-link",
          "action": "PreviewPortal",
          "actionInContextMenu": true,
          "openInPopup": true,
          "customComponentIsSystem": false,
          "closable": true
        }
      }
    ]
  }
}
```
</details>

**File Path**
```bash
/solid-api/module-metadata/<module-name>/<module-name>-metadata.json
```

## Props Reference

### Action Component Props

Each form button component receives a consistent set of props from the SolidX form engine.
<details>
<summary>
  
  `Action Component Props`
</summary>
```ts
{
  action, // action component name i.e PreviewPortal
  params : {
    moduleName: string;       // e.g. "fees-portal"
    modelName: string;        // e.g. "institute"
    id: string;               // record ID in edit mode
    embeded: boolean;         // true if the form is embedded
    handlePopupClose?: any;   // function to close popup
    customCreateHandler?: any; // custom create handler function
    inlineCreateAutoSave?: boolean; // true if inline create auto save is enabled
    customLayout?: any; // custom layout JSON if any
    parentData?: any; // parent data if any (for embedded forms)
    redirectToPath?: string; // path to redirect after save
    onEmbeddedFormSave?: () => void; // callback after embedded form save
  }
  formik, // contains formik props like values, setFieldValue, handleSubmit, etc.
  solidFormViewMetaData: solidFormViewMetaData.data // contains the form view metadata
}
```
</details>

## How It Works

1. SolidX renders the **form view** and identifies buttons in the layout.  
2. When a button is clicked, it looks up the registered component i.e action (e.g., `PreviewPortal`).  
3. SolidX passes relevant **context props** to that component.  
4. The component executes its logic — calling APIs, opening pages, etc.  
5. If the button was configured with `"openInPopup": true`, the component runs inside a modal dialog and can close itself via `closePopup()`.

This pattern lets you **add interactive buttons** in your form views that can trigger **custom logic**, such as navigating to hosted portals or previewing related content dynamically.

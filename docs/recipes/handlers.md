---
sidebar_position: 5
---

# SolidX Handlers

SolidX Handlers let you add custom logic and behavior to forms, lists, or pages in the SolidX UI. They’re ideal for things like validations, dynamic field updates, or workflow automation. Handlers work through the SolidX extension system, so you can customize without touching core code.

### Creating a SolidX Handler

We can create solidX handlers by following steps.

- Go to the extensions Folder in the SolidX UI Codebase
- Create a Handler File

Example code (paymentCollectionChangeHandler.ts)

```
import { getSession } from "next-auth/react";
import axios from "axios";
const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;
const paymentCollectionHandler = async (event: any) => {
  const { modifiedField, modifiedFieldValue, viewMetadata, formData } = event;
  const session: any = await fetchUser();
  const token = session?.user?.accessToken || "";
  const instituteData = await fetchInstituteData(
    session?.user?.user?.id,
    token
  );
  const newFormData: any = {
    institute: {
      solidManyToOneLabel: instituteData?.data?.institute?.instituteName,
      solidManyToOneValue: instituteData?.data?.institute?.id,
    },
  };
  return {
    layoutChanged: false,
    dataChanged: true,
    newFormData: newFormData,
  };
};

const fetchUser = async () => {
  let session: any = await getSession();
  return session;
};
const fetchInstituteData = async (id: number, token: any) => {
  try {
    const response = await axios.get(
      `${API_URL}/api/institute-user/${id}?populate=institute`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error: any) {
    console.error(
      "Error fetching institute user data:",
      error.response?.data || error.message
    );
    return null;
  }
};
export default paymentCollectionHandler;

```
- After creating handler we have to register this handler in solid-extension.ts file.

```
import {registerExtensionFunction } from "@solidstarters/solid-core-ui";
import ImageGrid12Column from "./admin/extensions/ImageGrid12Column";
import paymentCollectionHandler from "./admin/extensions/paymentCollectionChangeHandler";

// Registering a custom function
registerExtensionFunction('paymentCollectionHandler', paymentCollectionHandler);

```
- Once Handler is register we have to define it in the metadata json file.

```
{
  "name": "paymentCollection-form-view",
  "type": "form",
  "modelUserKey": "paymentCollection",
  "layout": {
    "type": "form",
    "attrs": {
      "label": "Payment Collection",
      "formButtons": [
        {
          "attrs": {
            "label": "Template",
            "action": "GenerateTemplateFormat",
            "openInPopup": true
          }
        }
      ]
    },
    "onFieldChange": "paymentCollectionHandler",
    "children": [
      {
        "type": "field",
        "attrs": { "name": "name" }
      },
      {
        "type": "field",
        "attrs": { "name": "description" }
      }
    ]
  }
}

```



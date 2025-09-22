---
title: View Metadata
description: Metadata schema for defining views in SolidX applications.
sidebar_position: 4
---

import { IoIosArrowForward } from "react-icons/io";
import { InfoBox } from '@site/src/common/InfoBox';




## Overview
Views define UI presentation of models and automatically generate:
    - List Views: Tabular display with search, filter, pagination
    - Form Views: Input forms for create/edit operations
    - Kanban Views: Card-based display with drag-and-drop

For a conceptual overview / guide/ recipes of how views can be used in SolidX, refer to the [View Metadata Guide](../../recipes/view-configurations-guide.md).

---

### Example: Fee Portal List/Form Views
<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    View Schema
  </summary>
  
``` json
    { // List View for Institute Model
      "name": "institute-list-view", 
      "displayName": "Institute",
      "type": "list",
      "context": "{}",
      "moduleUserKey": "fees-portal",
      "modelUserKey": "institute",
      "layout": {
        "type": "list",
        "attrs": {
          "pagination": true,
          "pageSizeOptions": [
            10,
            25,
            50
          ],
          "enableGlobalSearch": true,
          "create": true,
          "edit": true,
          "delete": true,
          "rowButtons": [
            {
              "attrs": {
                "className": "",
                "label": "Enable",
                "action": "ActivatePortal",
                "icon": "pi",
                "actionInContextMenu": false,
                "customComponentIsSystem": true,
                "openInPopup": true,
                "closable": true
              }
            },
            {
              "attrs": {
                "className": "",
                "label": "Disable",
                "action": "DeActivatePortal",
                "icon": "pi",
                "actionInContextMenu": false,
                "openInPopup": true,
                "customComponentIsSystem": true,
                "closable": true
              }
            },
            {
              "attrs": {
                "className": "",
                "label": "Preview",
                "action": "PreviewPortal",
                "icon": "pi",
                "actionInContextMenu": true,
                "openInPopup": true,
                "customComponentIsSystem": true,
                "closable": true
              }
            }
          ],
          "configureViewActions": {
            "import": {
              "roles": [
                "Admin",
                "Mswipe Admin"
              ]
            },
            "showArchived": {
              "roles": [
                "Admin",
                "Mswipe Admin"
              ]
            },
            "export": {
              "roles": [
                "Admin",
                "Mswipe Admin",
                "Institute Admin"
              ]
            },
            "customizeLayout": {
              "roles": [
                "Admin",
                "Mswipe Admin"
              ]
            },
            "saveCustomFilter": {
              "roles": [
                "Admin",
                "Mswipe Admin"
              ]
            }
          }
        },
        "children": [
          {
            "type": "field",
            "attrs": {
              "name": "id",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "instituteName",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "logo",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "description",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "paymentGatewayMerchantId",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "paymentGatewayAccessKey",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "paymentGatewayAccessSecret",
              "viewWidget": "MaskedShortTextListViewWidget",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "instituteAddress",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "supportEmail",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "supportMobile",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "faqs",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "privacyPolicy",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "tnC",
              "sortable": true,
              "filterable": true,
              "isSearchable": true
            }
          }
        ]
      }
    },
    { // Form View for Institute Model
      "name": "institute-form-view",
      "displayName": "Institute",
      "type": "form",
      "context": "{}",
      "moduleUserKey": "fees-portal",
      "modelUserKey": "institute",
      "layout": {
        "type": "form",
        "attrs": {
          "name": "form-1",
          "label": "Institute",
          "className": "grid",
          "formButtons": [
            {
              "attrs": {
                "className": "",
                "label": "Preview",
                "action": "PreviewPortal",
                "icon": "pi",
                "actionInContextMenu": true,
                "openInPopup": true,
                "customComponentIsSystem": true,
                "closable": true
              }
            }
          ]
        },
        "onFormLayoutLoad": "instituteEditHandler",
        "children": [
          {
            "type": "sheet",
            "attrs": {
              "name": "sheet-1"
            },
            "children": [
              {
                "type": "notebook",
                "attrs": {
                  "name": "notebook-1"
                },
                "children": [
                  {
                    "type": "page",
                    "attrs": {
                      "name": "page-1",
                      "label": "Institutes"
                    },
                    "children": [
                      {
                        "type": "row",
                        "attrs": {
                          "name": "sheet-1"
                        },
                        "children": [
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Institutes Basic",
                              "className": "col-6"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "instituteName"
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "description"
                                }
                              }
                            ]
                          },
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Institutes Contact",
                              "className": "col-6"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "instituteAddress",
                                  "disabled": false
                                }
                              }
                            ]
                          },
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Institutes Logo",
                              "className": "col-12"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "logo",
                                  "disabled": false,
                                  "showLabel": false
                                }
                              }
                            ]
                          },
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Institutes Brochure",
                              "className": "col-12"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "instituteBrochure",
                                  "disabled": false,
                                  "showLabel": false
                                }
                              }
                            ]
                          },
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Institute Intro Video",
                              "className": "col-12"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "instituteIntroVideo",
                                  "disabled": false,
                                  "showLabel": false
                                }
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "page",
                    "attrs": {
                      "name": "page-2",
                      "label": "Payment Gateway Details"
                    },
                    "children": [
                      {
                        "type": "row",
                        "attrs": {
                          "name": "sheet-1"
                        },
                        "children": [
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Payment Gateway Details",
                              "className": "col-6"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "paymentGatewayMerchantId"
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "paymentGatewayAccessKey"
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "paymentGatewayAccessSecret",
                                  "viewWidget": "MaskedShortTextFormViewWidget",
                                  "editWidget": "MaskedShortTextFormEditWidget"
                                }
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "page",
                    "attrs": {
                      "name": "page-4",
                      "label": "Support"
                    },
                    "children": [
                      {
                        "type": "row",
                        "attrs": {
                          "name": "sheet-1"
                        },
                        "children": [
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Basic",
                              "className": "col-6"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "emailDomain",
                                  "disabled": false
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "supportEmail"
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "supportMobile",
                                  "disabled": false
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "gst",
                                  "disabled": false
                                }
                              }
                            ]
                          },
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Standard Informational",
                              "className": "col-12"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "privacyPolicy",
                                  "disabled": false
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "faqs"
                                }
                              },
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "tnC",
                                  "disabled": false
                                }
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "page",
                    "attrs": {
                      "name": "page-5",
                      "label": "Fee Types"
                    },
                    "children": [
                      {
                        "type": "row",
                        "attrs": {
                          "name": "sheet-1"
                        },
                        "children": [
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Fee Types",
                              "className": "col-12"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "feeTypes",
                                  "inlineCreate": "true",
                                  "showFieldLabel": false,
                                  "showLabel": false
                                }
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "page",
                    "attrs": {
                      "name": "page-6",
                      "label": "Institute Users"
                    },
                    "children": [
                      {
                        "type": "row",
                        "attrs": {
                          "name": "sheet-1"
                        },
                        "children": [
                          {
                            "type": "column",
                            "attrs": {
                              "name": "group-1",
                              "label": "Institute Users",
                              "className": "col-12"
                            },
                            "children": [
                              {
                                "type": "field",
                                "attrs": {
                                  "name": "instituteUsers",
                                  "inlineCreate": "false",
                                  "showFieldLabel": false,
                                  "showLabel": false
                                }
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
  ```  
</details>

### Example: Kanban View
You can refer to the [Kanban View Example](../../recipes/view-configurations-guide#4-kanban-view-configuration) for a detailed example of Kanban view metadata.

## View Metadata Attributes

### `name` *(string, required, unique)*
Name of the view (used for referencing).  
**Default:** N/A

---

### `displayName` *(string, required)*
Display name of the view (shown in the UI).  
**Default:** N/A

---

### `type` *(string, required)*
Type of view. Supported types:
- `list`: List view for displaying multiple records in a tabular format.
- `form`: Form view for creating/editing a single record.
- `kanban`: Kanban view for visualizing records as cards in columns.
**Default:** N/A

---

### `context` *(JSON, optional)*
JSON object defining context-specific parameters for the view.  
**Default:** N/A

---

### `layout` *(JSON, required)*

Defines the **layout and structure** of the view.  
Controls how fields, widgets, buttons, and other UI elements are organized.

**Default:** N/A

#### 📖 Further Reference

For detailed attribute-level documentation of the `layout` schema per view type, see:

-  **List View:** [List View Layout Attributes](../../recipes/view-configurations-guide#list-view-attributes)  
-  **Form View:** [Form View Layout Attributes](../../recipes/view-configurations-guide#form-view-attributes)  
-  **Kanban View:** [Kanban View Layout Attributes](../../recipes/view-configurations-guide#kanban-view-attributes)




<InfoBox>
  Each view type has its own expected `layout` schema. Use the links above to understand required keys, optional properties, and usage examples.

</InfoBox>


---
### `moduleUserKey` *(string, optional)*
User key of the module this view belongs to.  
**Default:** N/A

---

### `modelUserKey` *(string, optional)*
User key of the model this view is associated with.  
**Default:** N/A    

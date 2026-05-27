---
title: Views and Layouts
---

### Customizing Views: The Institute Form Example

SolidX allows you to fully customize the layout of your forms and lists using a flexible JSON-based view definition. This means you can arrange fields, create tabs, and define complex structures directly within your module metadata, without writing any frontend code.

The `institute-form-view` is defined within the `fees-portal-metadata.json` file. This view uses a tabbed layout to organize the numerous fields of the `Institute` model into logical groups, making the form more user-friendly.

**Understanding the Layout Structure:**

The `layout` object within a view definition uses a hierarchical structure:

-   `type: "form"`: Indicates this is a form layout.

-   `children`: An array that defines the main containers of the form.

    -   `type: "sheet"`: A top-level container.

    -   `type: "notebook"`: Represents a tabbed interface. Its `children` are `page`s.

    -   `type: "page"`: Defines an individual tab. The `attrs.label` property sets the tab title.

    -   `type: "row"`: Arranges elements horizontally.

    -   `type: "column"`: Arranges elements vertically within a row, often defining column widths (`attrs.className: "col-6"` for half-width).

    -   `type: "field"`: Represents a single field from your model. Its `attrs.name` refers to the model's field name.

**Institute Form View Layout Snippet:**

Below is the layout JSON for the `institute-form-view`. This example demonstrates how fields are organized into tabs like "Institutes", "Payment Gateway Details", "Support", "Fee Types", and "Institute Users". You can just paste this layout directly in metadata JSON under layout object of `institute-form-view`.
<details>
<summary>&emsp; View JSON</summary>

```json
{
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
            "className": "p-button-text",
            "label": "Preview",
            "action": "PreviewPortal",
            "icon": "pi pi-image",
            "actionInContextMenu": true,
            "openInPopup": true,
            "customComponentIsSystem": true,
            "closable": true
          }
        },
        {
          "attrs": {
            "icon": "pi pi-caret-right",
            "name": "InstituteActivateById",
            "className": "p-button-text",
            "label": "Activate Institute",
            "action": "InstituteActivateById",
            "customComponentIsSystem": true,
            "actionInContextMenu": true,
            "openInPopup": true,
            "visible": false
          }
        },
        {
          "attrs": {
            "icon": "pi pi-circle-off",
            "name": "InstituteDeactivateById",
            "className": "p-button-text",
            "label": "Deactivate Institute",
            "action": "InstituteDeactivateById",
            "customComponentIsSystem": true,
            "actionInContextMenu": true,
            "openInPopup": true,
            "visible": false
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
                          },
                          {
                            "type": "field",
                            "attrs": {
                              "name": "hostedPagePrefix"
                            }
                          },
                          {
                            "type": "field",
                            "attrs": {
                              "name": "status",
                              "visible": false,
                              "disabled": true
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
                              "viewWidget": "maskedShortTextForm",
                              "editWidget": "maskedShortTextEdit"
                            }
                          },
                          {
                            "type": "field",
                            "attrs": {
                              "name": "custUserId"
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
}
```
</details>


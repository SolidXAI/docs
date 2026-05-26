---
title: 3. Admin Layout
---

# 3. Admin Layout

When a new model is added to a SolidX module the system automatically generates the following metadata for the admin ui. 

1. A menu is created 
2. Action is created 
3. List view 
4. Form view 

By default the list view & form view will contain all the fields which were added in the model at the time of creation. 

The layout simply arranges all the fields in a left to right (for list view) or top to bottom (for form view) manner. 

To make modifications to the generated layout files we can manually edit the json and save it, this will update the layout. Layout custommisations are also possible at multiple levels, we will take a look at a few of them in the customisations section. 

For now we will arrange the list view & form view of the generate models to make them a little more relevant to the business problem at hand.

## Institute 

### List View 

```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "instituteName",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "logo",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "description",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "hostedPagePrefix",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentGatewayMerchantId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentGatewayAccessKey",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentGatewayAccessSecret",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "pointOfContactName",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "pointOfContactMobile",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "instituteAddress",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "instituteContactNumber",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "instituteContactEmail",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "pointOfContactEmail",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Institute",
    "className": "grid"
  },
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
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteAddress",
                            "disabled": true
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
                            "name": "instituteContactNumber",
                            "disabled": true
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteContactEmail",
                            "disabled": true
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "hostedPagePrefix",
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
                            "disabled": true
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
                            "name": "paymentGatewayAccessSecret"
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
                "name": "page-3",
                "label": "Contacts"
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
                        "label": "Contacts",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "pointOfContactName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "pointOfContactMobile"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "pointOfContactEmail"
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
```

## Institute User 

### List View 
```json
{
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
      "delete": true
   },
   "children": [
      {
         "type": "field",
         "attrs": {
            "name": "firstName",
            "isSearchable": true
         }
      },
      {
         "type": "field",
         "attrs": {
            "name": "lastName",
            "isSearchable": true
         }
      },
      {
         "type": "field",
         "attrs": {
            "name": "emailAddress",
            "isSearchable": true
         }
      },
      {
         "type": "field",
         "attrs": {
            "name": "mobileNumber",
            "isSearchable": true
         }
      },
      {
         "type": "field",
         "attrs": {
            "name": "userType",
            "isSearchable": true
         }
      },
      {
         "type": "field",
         "attrs": {
            "name": "institute",
            "isSearchable": true
         }
      }
   ]
}
```
### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Institute",
    "className": "grid"
  },
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
                        },
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
                        "label": "Institutes Contact",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteContactNumber",
                            "disabled": false
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteContactEmail",
                            "disabled": false
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "hostedPagePrefix",
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
                            "name": "paymentGatewayAccessSecret"
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
                "name": "page-3",
                "label": "Contacts"
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
                        "label": "Contacts",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "pointOfContactName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "pointOfContactMobile"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "pointOfContactEmail"
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
            }
          ]
        }
      ]
    }
  ]
}
```

## Institute Fee Type

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "feeType",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "View Metadata",
    "className": "grid"
  },
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
                "label": "General Info"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-1-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-1",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "name"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "displayName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "type"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "module"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "model"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-2",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "context"
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
                "label": "Layout"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-2-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-2-row-1-col-1",
                        "label": "",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "layout",
                            "height": "80vh"
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
```
## Institute Reminder 

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "scheduleName",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "isActive",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "frequency",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "startTime",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "endTime",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "startDate",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "endDate",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "dayOfMonth",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "lastRunAt",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "nextRunAt",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "dayOfWeek",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "job",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "View Metadata",
    "className": "grid"
  },
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
                "label": "General Info"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-1-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-1",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "name"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "displayName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "type"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "module"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "model"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-2",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "context"
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
                "label": "Layout"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-2-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-2-row-1-col-1",
                        "label": "",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "layout",
                            "height": "80vh"
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
```
## Student 

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "studentName",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "studentEmailAddress",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "studentMobileNumber",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "parentName",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "parentMobileNumber",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "parentEmailAddress",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "studentId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "View Metadata",
    "className": "grid"
  },
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
                "label": "General Info"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-1-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-1",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "name"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "displayName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "type"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "module"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "model"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-2",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "context"
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
                "label": "Layout"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-2-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-2-row-1-col-1",
                        "label": "",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "layout",
                            "height": "80vh"
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
```
## Payment Collection 

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "name",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "description",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentFile",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "View Metadata",
    "className": "grid"
  },
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
                "label": "General Info"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-1-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-1",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "name"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "displayName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "type"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "module"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "model"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-2",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "context"
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
                "label": "Layout"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-2-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-2-row-1-col-1",
                        "label": "",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "layout",
                            "height": "80vh"
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
```
## Payment Collection Item 

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "student",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollection",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "feeType",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "dueDate",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "amountToBePaid",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "partPaymentAllowed",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "status",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "amountPaid",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "amountPending",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "isOverdue",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "overdueByDays",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Payment Collection Item",
    "className": "grid"
  },
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
                "label": "Payment Collection Item"
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
                            "name": "student"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "paymentCollection"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "institute"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "feeType"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "isOverdue"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "partPaymentAllowed"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Configuration",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "dueDate"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "amountToBePaid"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "status"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "amountPaid"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "amountPending"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "overdueByDays"
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
                "label": "Payment Collection Item Details"
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
                        "label": "Payment Collection Item Details",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "paymentCollectionItemDetails",
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
```
## Payment Collection Item Detail 

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "student",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItem",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentDate",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "amountPaid",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "isRefunded",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "payment",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "View Metadata",
    "className": "grid"
  },
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
                "label": "General Info"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-1-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-1",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "name"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "displayName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "type"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "module"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "model"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-1-row-1-col-2",
                        "label": "",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "context"
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
                "label": "Layout"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "page-2-row-1",
                    "label": "",
                    "className": ""
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "page-2-row-1-col-1",
                        "label": "",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "layout",
                            "height": "80vh"
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
```

## Payment

### List View 
```json
{
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
    "delete": true
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "id",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "institute",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "student",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "mSwipeIpgOrderId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "mSwipeIpgPaymentId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "mSwipeIpgTransId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "mSwipeIpgInvoiceId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "mSwipeEncodedIpgId",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "mSwipeIpgStatus",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "amount",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "isRefunded",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentStatus",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
 ```json
 {
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Payment",
    "className": "grid"
  },
  "children": [
    {
      "type": "sheet",
      "attrs": {
        "name": "sheet-1"
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
                    "name": "institute"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "student"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "amount"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "paymentStatus"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "isRefunded"
                  }
                }
              ]
            },
            {
              "type": "column",
              "attrs": {
                "name": "group-1",
                "label": "IPG Configuration",
                "className": "col-6"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "mSwipeIpgOrderId"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "mSwipeIpgPaymentId"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "mSwipeIpgTransId"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "mSwipeIpgInvoiceId"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "mSwipeEncodedIpgId"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "mSwipeIpgStatus"
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
 ```

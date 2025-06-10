---
sidebar_position: 3
---

# 3. Admin Layout

When a new model is added to a SolidX module the system automatically generates the following metadata for the admin ui. 

1. A menu is created 
2. Action is created 
3. List view 
4. Form view 

Buy default the list view & form view will contain all the fields which were added in the model at the time of creation. 

The layout simply arranges all the fields in a left to right (for list view) or top to bottom (for form view) manner. 

To make modifications to the generated layout files we can manually edit the json and save it, this will update the layout. Layout custommisations are also possible at multiple levels, we will take a look at a few of them in the customisations section. 

For now we will arrange the list view & form view of the generate models to make them a little more relevant to the business problem at hand.


## Institute 

### List View 

```
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
    }
  ]
}
```

### Form View

## Institute User 

### List View 

### Form View

## Institute Fee Type

### List View 
```
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

## Institute Reminder 

### List View 
```
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

## Student 

### List View 
```
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
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItems",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItemDetails",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "payments",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItems",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItems",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItemDetails",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View

## Payment Collection 

### List View 
```
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
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItems",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItems",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItems",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View

## Payment Collection Item 

### List View 
```
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
        "name": "paymentCollectionRequest",
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
        "name": "paymentCollectionItemDetails",
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
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItemDetails",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItemDetails",
        "sortable": true,
        "filterable": true
      }
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItemDetails",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View

## Payment Collection Item Detail 

### List View 
```
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
        "name": "paymentCollectionItem",
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
        "name": "payment",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View

## Payment

### List View 
```
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
    },
    {
      "type": "field",
      "attrs": {
        "name": "paymentCollectionItemDetails",
        "sortable": true,
        "filterable": true
      }
    }
  ]
}
```

### Form View
 
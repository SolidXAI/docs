# Customizing UI (Colors, Formatting, Filters)
**2. Status Badge Colors**

```json
"statusColors": {
  "Pending": "warning",
  "Partially Paid": "info",
  "Fully Paid": "success",
  "Cancelled": "danger"
}
```

**3. Conditional Formatting**

```json
"conditionalFormatting": [
  {
    "field": "amountPending",
    "condition": "{{value > 0}}",
    "className": "text-danger font-bold"
  },
  {
    "field": "isOverdue",
    "condition": "{{value === true}}",
    "rowClassName": "bg-red-50"
  }
]
```

**Benefits:**
- Visual indicators for overdue items (red highlight)
- Clear status identification with colored badges
- Easy identification of partially paid items
- Quick scanning of pending amounts

**4. Advanced Filters**

```json
"quickFilters": [
  {
    "label": "Pending Payments",
    "filters": [
      { "field": "status", "operator": "in", "value": ["Pending", "Partially Paid"] }
    ]
  },
  {
    "label": "Overdue",
    "filters": [
      { "field": "isOverdue", "operator": "eq", "value": true }
    ]
  },
  {
    "label": "Payment Gateway",
    "filters": [
      { "field": "mode", "operator": "eq", "value": "PG" }
    ]
  }
]
```

**Benefits:**
- Quick access to common views
- One-click filtering for urgent items
- Reduces time to find specific records
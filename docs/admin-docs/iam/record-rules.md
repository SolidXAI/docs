---
sidebar_position: 4
title: Record Rules
---

import { IoIosArrowForward } from "react-icons/io";


# Record Rules

Record Rules in SOLID provide fine-grained access control at the data level, allowing you to define who can access specific records based on various conditions.

## Overview

Record Rules enable:
- Row-level security
- Dynamic access control
- User-specific data visibility
- Role-based data access

## Rule Types

### User-Based Rules

Rules based on the current user:

```json
{
  "name": "own_records",
  "resource": "projects",
  "condition": {
    "field": "created_by",
    "operator": "equals",
    "value": "${currentUser.id}"
  }
}
```

### Role-Based Rules

Rules based on user roles:

```json
{
  "name": "department_records",
  "resource": "employees",
  "condition": {
    "field": "department",
    "operator": "equals",
    "value": "${currentUser.department}",
    "roles": ["department_manager"]
  }
}
```

### Complex Rules

Combining multiple conditions:

```json
{
  "name": "regional_sales",
  "resource": "sales_orders",
  "condition": {
    "operator": "and",
    "conditions": [
      {
        "field": "region",
        "operator": "equals",
        "value": "${currentUser.region}"
      },
      {
        "field": "status",
        "operator": "in",
        "value": ["active", "pending"]
      }
    ]
  }
}
```

## Rule Configuration

### Available Operators

| Operator | Description | Example |
|----------|-------------|---------|
| equals | Exact match | `field = value` |
| not_equals | Negative match | `field != value` |
| in | In array | `field IN (values)` |
| not_in | Not in array | `field NOT IN (values)` |
| greater_than | Greater than | `field > value` |
| less_than | Less than | `field < value` |
| contains | String contains | `field LIKE %value%` |
| starts_with | String starts with | `field LIKE value%` |

### Dynamic Values

Available context variables:

- `${currentUser}` - Current user object
- `${currentRole}` - Current user's role
- `${timestamp}` - Current timestamp
- `${custom}` - Custom context variables

## Implementation

### Creating a Rule

```json
{
  "name": "active_projects",
  "description": "Access to active projects in user's department",
  "resource": "projects",
  "condition": {
    "operator": "and",
    "conditions": [
      {
        "field": "status",
        "operator": "equals",
        "value": "active"
      },
      {
        "field": "department",
        "operator": "equals",
        "value": "${currentUser.department}"
      }
    ]
  },
  "actions": ["read", "update"],
  "priority": 1
}
```

### Rule Priority

Rules are evaluated in priority order:
1. Higher priority rules override lower priority
2. More specific rules take precedence
3. Deny rules override allow rules



## Common Scenarios

### Team-Based Access

```json
{
  "name": "team_access",
  "resource": "tasks",
  "condition": {
    "operator": "or",
    "conditions": [
      {
        "field": "assigned_team",
        "operator": "equals",
        "value": "${currentUser.team}"
      },
      {
        "field": "created_by",
        "operator": "equals",
        "value": "${currentUser.id}"
      }
    ]
  }
}
```

### Hierarchical Access

```json
{
  "name": "hierarchical_access",
  "resource": "employees",
  "condition": {
    "field": "department_path",
    "operator": "starts_with",
    "value": "${currentUser.department_path}"
  }
}
```

### Time-Based Access

```json
{
  "name": "time_restricted_access",
  "resource": "documents",
  "condition": {
    "operator": "and",
    "conditions": [
      {
        "field": "valid_from",
        "operator": "less_than",
        "value": "${timestamp}"
      },
      {
        "field": "valid_to",
        "operator": "greater_than",
        "value": "${timestamp}"
      }
    ]
  }
}
```




## Best Practices

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Rule Design
  </summary>
  <ul className="card-desc">
    <li>Keep rules simple and focused</li>
    <li>Use meaningful names</li>
    <li>Document rule purpose</li>
    <li>Consider performance impact</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Security
  </summary>
  <ul className="card-desc">
    <li>Test rule combinations</li>
    <li>Validate rule logic</li>
    <li>Monitor rule effectiveness</li>
    <li>Regular security audits</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Maintenance
  </summary>
  <ul className="card-desc">
    <li>Regular rule review</li>
    <li>Update documentation</li>
    <li>Clean up unused rules</li>
    <li>Monitor performance</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Testing
  </summary>
  <ul className="card-desc">
    <li>Test edge cases</li>
    <li>Verify rule combinations</li>
    <li>Check rule priorities</li>
    <li>Validate performance</li>
  </ul>
</details>

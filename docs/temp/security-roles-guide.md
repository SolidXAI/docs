# SolidX Security & Roles Guide

This guide provides comprehensive documentation for security roles and access control configurations in SolidX platform metadata, with real examples from the fees-portal module.

## 1. SECURITY OVERVIEW

SolidX provides comprehensive security through:
- **Role-based access control (RBAC)**: Users are assigned roles that determine their permissions
- **Security rules**: JSON-based policies that filter data access
- **Field-level security**: Control over which fields users can view/edit
- **Action-level security**: Control over which actions users can perform

## 2. ROLES CONFIGURATION

Roles define user permissions and access levels within the system.

### Basic Role Structure
```json
{
  "name": "Admin",                           // Role name/identifier
  "displayName": "Administrator",            // User-friendly role name
  "description": "Full system access",       // Role description
  "permissions": {                          // Permission configuration
    "models": {                             // Model-level permissions
      "create": ["institute", "user"],       // Can create these models
      "read": ["*"],                        // Can read all models
      "update": ["*"],                      // Can update all models
      "delete": ["*"]                       // Can delete all models
    },
    "actions": ["*"],                       // Can perform all actions
    "fields": {                            // Field-level permissions
      "hidden": [],                         // Fields to hide
      "readonly": []                        // Fields that are read-only
    }
  },
  "isSystem": false,                        // System-defined role
  "isDefault": false                        // Default role for new users
}
```

### Real Examples from Fees Portal

#### Institute Admin Role
```json
{
  "name": "Institute Admin",
  "displayName": "Institute Administrator",
  "description": "Administrator for a specific institute with limited access",
  "permissions": {
    "models": {
      "create": ["student", "feeType", "paymentCollection"],
      "read": ["institute", "student", "feeType", "paymentCollection", "payment"],
      "update": ["student", "feeType", "paymentCollection"],
      "delete": ["student", "feeType"]
    },
    "actions": [
      "institute-list-view",
      "student-list-view",
      "feeType-list-view",
      "paymentCollection-list-view",
      "create-student",
      "update-student"
    ],
    "fields": {
      "hidden": ["paymentGatewaySecret"],
      "readonly": ["instituteName", "paymentGatewayMerchantId"]
    }
  },
  "isSystem": false,
  "isDefault": false
}
```

#### Mswipe Admin Role
```json
{
  "name": "Mswipe Admin",
  "displayName": "Mswipe Administrator",
  "description": "Super administrator with full system access",
  "permissions": {
    "models": {
      "create": ["*"],
      "read": ["*"],
      "update": ["*"],
      "delete": ["*"]
    },
    "actions": ["*"],
    "fields": {
      "hidden": [],
      "readonly": []
    }
  },
  "isSystem": true,
  "isDefault": false
}
```

#### Student Role
```json
{
  "name": "Student",
  "displayName": "Student",
  "description": "Student user with limited access to their own data",
  "permissions": {
    "models": {
      "create": [],
      "read": ["student", "feeType", "payment"],
      "update": ["student"],
      "delete": []
    },
    "actions": [
      "view-profile",
      "view-fees",
      "view-payment-history"
    ],
    "fields": {
      "hidden": ["paymentGatewaySecret", "adminNotes"],
      "readonly": ["studentId", "enrollmentDate"]
    }
  },
  "isSystem": false,
  "isDefault": true
}
```

## 3. SECURITY RULES CONFIGURATION

Security rules define data access policies using JSON-based filter expressions.

### Basic Security Rule Structure
```json
{
  "name": "rule-name",                       // Rule identifier (kebab-case)
  "description": "Rule description",         // Human-readable description
  "roleUserKey": "RoleName",                // Role this rule applies to
  "modelMetadataUserKey": "modelName",      // Model this rule applies to
  "securityRuleConfig": {                   // Rule configuration
    "filters": {                           // Data filters
      "fieldName": {                       // Field to filter on
        "$operator": "value"               // Filter condition
      }
    },
    "permissions": {                       // Additional permissions
      "create": true,                      // Can create records
      "update": true,                      // Can update records
      "delete": false                      // Cannot delete records
    }
  }
}
```

### MongoDB-Style Filter Operators

SolidX security rules use MongoDB-style query operators:

```json
{
  "filters": {
    "status": { "$eq": "active" },           // Equal to
    "age": { "$gt": 18 },                   // Greater than
    "age": { "$gte": 18 },                  // Greater than or equal
    "age": { "$lt": 65 },                   // Less than
    "age": { "$lte": 65 },                  // Less than or equal
    "status": { "$ne": "inactive" },        // Not equal
    "status": { "$in": ["active", "pending"] },  // In array
    "status": { "$nin": ["inactive", "suspended"] },  // Not in array
    "tags": { "$exists": true },            // Field exists
    "name": { "$regex": "^John" },          // Regular expression
    "createdAt": { "$between": ["2023-01-01", "2023-12-31"] }  // Between values
  }
}
```

### Real Examples from Fees Portal

#### Institute Data Access Rule
```json
{
  "name": "institute",
  "description": "Show institute associated with the user",
  "roleUserKey": "Institute Admin",
  "modelMetadataUserKey": "institute",
  "securityRuleConfig": {
    "filters": {
      "instituteUsers": {
        "id": {
          "$eq": "$activeUserId"
        }
      }
    }
  }
}
```

This rule ensures Institute Admins can only see institutes they are associated with.

#### Institute User Access Rule
```json
{
  "name": "institute-user",
  "description": "Show institute user associated with the institute",
  "roleUserKey": "Institute Admin",
  "modelMetadataUserKey": "instituteUser",
  "securityRuleConfig": {
    "filters": {
      "institute": {
        "instituteUsers": {
          "id": {
            "$eq": "$activeUserId"
          }
        }
      }
    }
  }
}
```

This rule creates a chain: Institute Admin → Institute → Institute Users.

#### Fee Type Access Rule
```json
{
  "name": "feeType",
  "description": "Show feeType associated with the institute user",
  "roleUserKey": "Institute Admin",
  "modelMetadataUserKey": "feeType",
  "securityRuleConfig": {
    "filters": {
      "institute": {
        "instituteUsers": {
          "id": {
            "$eq": "$activeUserId"
          }
        }
      }
    }
  }
}
```

#### Payment Collection Access Rule
```json
{
  "name": "payment-collection",
  "description": "Show payment collection associated with the institute",
  "roleUserKey": "Institute Admin",
  "modelMetadataUserKey": "paymentCollection",
  "securityRuleConfig": {
    "filters": {
      "institute": {
        "instituteUsers": {
          "id": {
            "$eq": "$activeUserId"
          }
        }
      }
    }
  }
}
```

## 4. VARIABLE SUBSTITUTION

Security rules support dynamic variables:

```json
{
  "filters": {
    "createdBy": { "$eq": "$activeUserId" },      // Current user's ID
    "organizationId": { "$eq": "$userOrgId" },   // User's organization
    "department": { "$eq": "$userDepartment" },  // User's department
    "createdAt": { "$gte": "$currentDate" }      // Current date
  }
}
```

### Built-in Variables
- `$activeUserId`: Current authenticated user's ID
- `$userOrgId`: User's organization ID
- `$userDepartment`: User's department
- `$currentDate`: Current date
- `$currentDateTime`: Current date and time

## 5. COMPLEX SECURITY SCENARIOS

### Multi-Level Access Control
```json
{
  "name": "department-manager-access",
  "description": "Department managers can access their department and sub-departments",
  "roleUserKey": "Department Manager",
  "modelMetadataUserKey": "employee",
  "securityRuleConfig": {
    "filters": {
      "$or": [
        {
          "departmentId": { "$eq": "$userDepartmentId" }
        },
        {
          "department": {
            "parentDepartmentId": { "$eq": "$userDepartmentId" }
          }
        }
      ]
    }
  }
}
```

### Time-Based Access
```json
{
  "name": "business-hours-access",
  "description": "Access restricted to business hours",
  "roleUserKey": "Employee",
  "modelMetadataUserKey": "document",
  "securityRuleConfig": {
    "filters": {
      "$or": [
        {
          "createdBy": { "$eq": "$activeUserId" }
        },
        {
          "isPublic": { "$eq": true }
        }
      ]
    },
    "timeRestrictions": {
      "allowedHours": ["09:00", "17:00"],
      "allowedDays": ["monday", "tuesday", "wednesday", "thursday", "friday"]
    }
  }
}
```

### Field-Level Security
```json
{
  "name": "salary-field-security",
  "description": "Salary field access control",
  "roleUserKey": "Employee",
  "modelMetadataUserKey": "employee",
  "securityRuleConfig": {
    "fieldPermissions": {
      "salary": {
        "read": ["Manager", "HR"],
        "write": ["HR"],
        "hide": ["Employee"]
      },
      "ssn": {
        "read": ["HR"],
        "write": ["HR"],
        "hide": ["Manager", "Employee"]
      }
    }
  }
}
```

## 6. ROLE HIERARCHIES

### Hierarchical Role Structure
```json
{
  "roles": [
    {
      "name": "SuperAdmin",
      "parentRole": null,
      "permissions": { "models": { "create": ["*"], "read": ["*"], "update": ["*"], "delete": ["*"] } }
    },
    {
      "name": "Admin",
      "parentRole": "SuperAdmin",
      "permissions": { "models": { "delete": ["exclude:critical_data"] } }
    },
    {
      "name": "Manager",
      "parentRole": "Admin",
      "permissions": { "models": { "delete": ["exclude:*"] } }
    }
  ]
}
```

## 7. DYNAMIC ROLE ASSIGNMENT

### Attribute-Based Access Control
```json
{
  "name": "location-based-access",
  "description": "Access based on user location",
  "roleUserKey": "FieldWorker",
  "modelMetadataUserKey": "workOrder",
  "securityRuleConfig": {
    "filters": {
      "location": {
        "$eq": "$userLocation"
      }
    },
    "dynamicAssignment": {
      "attribute": "location",
      "valueSource": "userProfile"
    }
  }
}
```

## 8. AUDIT AND COMPLIANCE

### Audit Trail Configuration
```json
{
  "auditConfig": {
    "enabled": true,
    "trackFields": ["salary", "personalData"],
    "trackActions": ["create", "update", "delete"],
    "retentionPeriod": "7_years",
    "complianceFrameworks": ["GDPR", "HIPAA"]
  }
}
```

## 9. SECURITY BEST PRACTICES

### Principle of Least Privilege
```json
{
  "name": "minimal-access-rule",
  "description": "Users can only access their own data",
  "roleUserKey": "User",
  "securityRuleConfig": {
    "filters": {
      "createdBy": { "$eq": "$activeUserId" },
      "isPublic": { "$ne": true }
    },
    "permissions": {
      "create": true,
      "read": true,
      "update": { "ownRecords": true },
      "delete": { "ownRecords": true }
    }
  }
}
```

### Defense in Depth
```json
{
  "securityLayers": [
    {
      "layer": "network",
      "rules": ["ip_whitelist", "vpn_required"]
    },
    {
      "layer": "application",
      "rules": ["role_based_access", "field_level_security"]
    },
    {
      "layer": "data",
      "rules": ["encryption_at_rest", "data_masking"]
    }
  ]
}
```

## 10. COMPLETE SECURITY EXAMPLE

Here's a complete security configuration example from the fees-portal:

```json
{
  "roles": [
    {
      "name": "Institute Admin",
      "displayName": "Institute Administrator",
      "permissions": {
        "models": {
          "create": ["student", "feeType", "paymentCollection"],
          "read": ["institute", "student", "feeType", "paymentCollection", "payment"],
          "update": ["student", "feeType", "paymentCollection"],
          "delete": ["student", "feeType"]
        },
        "actions": [
          "institute-list-view",
          "student-list-view",
          "feeType-list-view",
          "paymentCollection-list-view"
        ]
      }
    },
    {
      "name": "Mswipe Admin",
      "displayName": "Mswipe Administrator",
      "permissions": {
        "models": {
          "create": ["*"],
          "read": ["*"],
          "update": ["*"],
          "delete": ["*"]
        },
        "actions": ["*"]
      }
    }
  ],
  "securityRules": [
    {
      "name": "institute",
      "description": "Show institute associated with the user",
      "roleUserKey": "Institute Admin",
      "modelMetadataUserKey": "institute",
      "securityRuleConfig": {
        "filters": {
          "instituteUsers": {
            "id": { "$eq": "$activeUserId" }
          }
        }
      }
    },
    {
      "name": "student",
      "description": "Show student list associated with the institute",
      "roleUserKey": "Institute Admin",
      "modelMetadataUserKey": "student",
      "securityRuleConfig": {
        "filters": {
          "institute": {
            "instituteUsers": {
              "id": { "$eq": "$activeUserId" }
            }
          }
        }
      }
    }
  ]
}
```

This comprehensive guide covers all aspects of security and roles in SolidX, from basic role-based access control to complex multi-level security rules, with real examples from your fees-portal module.

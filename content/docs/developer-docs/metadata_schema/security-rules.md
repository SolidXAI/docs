---
title: Security Rules
description: Metadata schema for defining security rules in SolidX applications.
summary: This document explains security rules metadata in SolidX, which controls data access at the model level to ensure only authorized users can view sensitive information. Each rule includes a name, description, associated role, target model, and security rule configuration with filter conditions. The filter configuration supports complex query structures using operators like $eq with dynamic values such as $activeUserId for user-specific data filtering. Examples demonstrate restricting fee type visibility to institute users through relational filtering across associated models. The document links to detailed guides on creating and managing security rules in the backend customization section.
json_pointer: "/securityRules"
jsonpath: "$.securityRules"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#security-rules-metadata-attributes"
solidx_concerns: [add/update_security_record_rule]
---

# Security Rules
> **Where it lives**  
> **JSON Pointer:** `/securityRules`  
> **JSONPath:** `$.securityRules`  
> **Parent:** Root of the metadata file

## Overview
Security rules are crucial for controlling access to data in SolidX. By defining these rules, you can restrict visibility at the model level and ensure that only authorized users can access sensitive information.

For a guide on how to create and manage security rules in SolidX, refer to the [Creating Security Rules](../extending/backend-customization/security-rules).

## Example: Security Rules Metadata
<summary> Security Rules Schema </summary>

``` json
{
  ..., // Other metadata sections
  "securityRules": [
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
  ]
}
```

## Security Rules Metadata Attributes

### `name` *(string, required, unique)*
Name of the security rule.
This should be unique across all security rules.

### `description` *(string, required)*
A brief description of what the security rule does. This helps in understanding the purpose of the rule.

### `roleUserKey` *(string, required)*
The user key of the role to which this security rule applies. This helps in associating the rule with a specific user role.

### `modelMetadataUserKey` *(string, required)*
The user key of the model (entity) to which this security rule applies. This helps in associating the rule with a specific data model.

### `securityRuleConfig` *(JSON, required)*
A JSON object defining the actual security rule configuration. This typically includes filters that determine which records are accessible based on the active user's context.
Contains a json object with a `filters` key that defines the filtering logic. The filters object is consistent with the filter structure used in queries, allowing for complex conditions and relationships.

####  Further Reference
 -  Understanding Filters: See [Filters Documentation](../rest-apis/retrieve) for details on constructing filter objects.

<div>
  Tip
Verify if the security rules are working as expected by making API calls with the filters defined in the security rules.

<span> For example: </span>

```http
/GET api/v1/feeType
?filters[institute][instituteUsers][id][$eq]
=$activeUserId
```

</div>

---
title: Security Rules
description: Metadata schema for defining security rules in SolidX applications.
sidebar_position: 13
---

## Overview
Security rules are crucial for controlling access to data in SolidX. By defining these rules, you can restrict visibility at the model level and ensure that only authorized users can access sensitive information.

For a guide on how to create and manage security rules in SolidX, refer to the [Creating Security Rules](../../developer-docs/extending/backend-customization/security-rules/index.md).

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

#### 📖 Further Reference
 - 📋 Understanding Filters: See [Filters Documentation](../../developer-docs/rest-apis/retrieve/index.md) for details on constructing filter objects.

:::tip
Verify if the security rules are working as expected by making API calls with the filters defined in the security rules.

For example: 
```http
/GET api/v1/feeType
?filters[institute][instituteUsers][id][$eq]
=$activeUserId
```
:::

:::info
You can also use interactive query builder to convert filter objects to query strings. See [Interactive Query Builder](https://docs.strapi.io/cms/api/rest/interactive-query-builder)
:::




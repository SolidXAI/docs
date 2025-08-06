---
sidebar_position: 2
title: Security Rules
description: Learn how to customize security rules in SolidX.
keywords: [backend, security, customization]
---
## Overview
In this section, we will explore how to customize security rules in SolidX.
Security rules are essential for controlling access to data and ensuring that users can only interact with the data they are authorized to see. By defining security rules, you can enforce data visibility at a model level, and ensure that data is only accessible to authorized roles. 

## Add a New Security Rule
1. Add a new security rule to the securityRules array in the module metadata JSON file, for the corresponding module.
2. Define the rule's name, description, roleUserKey, modelMetadataUserKey. Every security rule must have a unique name and needs to be associated with a specific role and model metadata.
3. Define the security rule's configuration in the securityRuleConfig object. This object contains the filters that will be applied whenever the model data is retrieved from the api's for user logged in with a particular role.
``` json
{
  ...,  
  "securityRules": [
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
  ]
}

## How it Works
1. Security rules are implemented as part of the retrieve logic in the file called `SolidBaseRepository` provided by `@solidstarters/solid-core`.
2. Any repository that extends `SolidBaseRepository` will automatically apply the security rules defined in the module metadata JSON file, when the repository query builder is used to retrieve data. (TODO: Need to support the find method as well)
3. Since all the generated model repositories extend `SolidBaseRepository`, the security rules will be applied whenever these repositories are used to retrieve data.
4. When a user makes a request to the find endpoint of a model controller, the CRUD service will end up calling the repository's find method, which will apply the security rules defined in the module metadata JSON file.
5. Security rules are loaded at application startup from the database and stored in the Solid Registry. This requires that the server be restarted after adding or modifying security rules.

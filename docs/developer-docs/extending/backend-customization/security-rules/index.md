---
sidebar_position: 2
title: Security Rules
description: Learn how to customize security rules in SolidX.
keywords: [backend, security, customization]
---

import { IoIosArrowForward, IoIosLock, IoIosInformationCircle, IoIosWarning } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';



#  Security Rules in SolidX

Security rules are crucial for **controlling access to data** in SolidX. By defining these rules, you can restrict visibility at the model level and ensure that only authorized users can access sensitive information.

---

  <h2 className=" card-headear-wrapper">
    <IoIosLock size={26} style={{ marginRight: "10px" }} />

## Adding a New Security Rule
</h2>



Follow these steps to configure a custom security rule:

1.  Add a rule inside the `securityRules` array in the module metadata JSON file.
2.  Define the following properties:
   - `name`: Unique identifier for the rule
   - `description`: What the rule does
   - `roleUserKey`: The role for which the rule applies (e.g., "Institute Admin")
   - `modelMetadataUserKey`: The model this rule applies to (e.g., "institute")
3.  Define the logic inside `securityRuleConfig.filters`. These filters are applied when data is retrieved for the logged-in user, depending upon the user's role and the model data they are accessing.

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Example: Rule for <code>Institute Admin</code>
</summary>

```json
{
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
```

</details>
4. The `$activeUserId` variable is automatically replaced with the ID of the currently logged-in user when the rule is applied.

---


  <h2 className=" card-headear-wrapper">
    <IoIosInformationCircle size={26} style={{ marginRight: "10px" }} />

##  How It Works
</h2>


1.  Security rules are evaluated within the `SolidBaseRepository` class (from `@solidstarters/solid-core`).
2.  Any repository that extends `SolidBaseRepository` will automatically enforce security rules during data retrieval via query builders.
3.  All generated model repositories in SolidX inherit this behavior — security filters are applied transparently.
4.  When users call a model controller’s `find` endpoint, the logic goes through the CRUD service → repository → `find` or query builder → applying security rules.
5.  Security rules are loaded from the database **at server startup** and stored in the Solid Registry.
   -  After updating or adding rules, **restart the server** for the changes to take effect.



<NoteBoxs>
  Support for applying rules in the basic <span className="color-green"> find() </span> method is still a TODO.
</NoteBoxs>

  <h2 className=" card-headear-wrapper">
    <IoIosWarning size={26} style={{ marginRight: "10px" }} />

## Troubleshooting
</h2>
If you encounter issues with security rules:
-  Ensure the server is restarted after making changes to the security rules.
- Ensure that the `roleUserKey` and `modelMetadataUserKey` are correctly defined and match the roles and models in your application.
- Ensure that the permissions related to the security rules are not assigned to the "Public" role, since public endpoints skip security checks. 
- Check the logic in `securityRuleConfig.filters` to ensure it correctly references the user ID and model data.
- Enable debug sql logging, by adding the  DEFAULT_DATABASE_LOGGING=true environment variable, to see the SQL queries being generated and applied. This can help identify if the security rules are being applied correctly if the sql queries are being generated and applied correctly.
---
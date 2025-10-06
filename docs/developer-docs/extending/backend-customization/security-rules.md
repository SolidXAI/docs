---
sidebar_position: 11
title: Security Rules
description: Learn how to customize security rules in SolidX.
keywords: [backend, security, customization]
solidx_concerns: [add/update_security_record_rule]
---

import { IoIosArrowForward, IoIosLock, IoIosInformationCircle, IoIosWarning } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';

# Security Rules in SolidX

Security rules control **who can see which records**. You attach rules **per role** and **per model** so different roles get different visibility.

<NoteBoxs>
By default, **no security rules are enforced** — all authenticated users can access all data for all models. Add rules in your module metadata to restrict access.
</NoteBoxs>



## When you’d use them

- A **Super Admin** can view all clients.
- A **Client Admin** should only see the **single Client** they belong to.
- A **Custom User** should only see **their own** user record.

If a user has **multiple roles**, SolidX applies the **most permissive** matching rule.

> **Scope:** Security rules apply only to **authenticated** requests. **Public** endpoints skip security checks.



## Define a rule

Add entries to the `securityRules` array in your module’s metadata JSON.

**Required fields**

| Field                     | Type     | Purpose                                                     |
|--------------------------|----------|-------------------------------------------------------------|
| `name`                   | string   | Unique name for the rule                                    |
| `description`            | string   | What the rule does                                          |
| `roleUserKey`            | string   | The role this rule targets (e.g., `"Institute Admin"`)      |
| `modelMetadataUserKey`   | string   | The model this rule applies to (e.g., `"institute"`)        |
| `securityRuleConfig.filters` | object | **Record-level filter** applied to queries for this role    |

**Special variables**

- `$activeUserId` — replaced at runtime with the **logged-in user’s ID**.

<h2 className=" card-headear-wrapper">
  <IoIosLock size={26} style={{ marginRight: "10px" }} />

  Adding a New Security Rule
</h2>


1) In your module metadata, add a rule to `securityRules`.  
2) Fill in the required fields above.  
3) Put your access logic under `securityRuleConfig.filters`.

<details>
  <summary className="card-title card-header-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Example: <code>Institute Admin</code> sees only their institute
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
            "id": { "$eq": "$activeUserId" }
          }
        }
      }
    }
  ]
}
```

</details>



<h2 className=" card-headear-wrapper">
  <IoIosInformationCircle size={26} style={{ marginRight: "10px" }} />

  How It Works
</h2>

1. Rules are evaluated inside **`SolidBaseRepository`** (`@solidstarters/solid-core`).  
2. Any repository **extending** `SolidBaseRepository` automatically enforces rules during query building.  
3. All generated model repositories inherit this behavior.  
4. Controller `find` → CRUD service → repository → query builder → **security filters applied**.  
5. Rules are loaded from the database **at server startup** and cached in the **Solid Registry**.  
   - After adding/changing rules, **restart the server**.


<h2 className=" card-headear-wrapper">
  <IoIosWarning size={26} style={{ marginRight: "10px" }} />

  Common Pitfalls & Troubleshooting
</h2>



- **Restart required:** Rules are read on startup. Restart the server after changes.  
- **Exact keys:** Check `roleUserKey` and `modelMetadataUserKey` spellings and that they exist.  
- **Public endpoints bypass rules:** Do **not** grant sensitive controller permissions to the **Public** role.  
  - Example: If `"InstituteController.findMany"` is granted to `"Public"`, `GET /api/institute` becomes unauthenticated and **no security rules** apply.  
- **Filters correctness:** Validate your `securityRuleConfig.filters` structure and paths (e.g., relation names, field names).  
- **SQL visibility:** Turn on SQL debug to see applied filters:

  ```bash
  DEFAULT_DATABASE_LOGGING=true
  ```



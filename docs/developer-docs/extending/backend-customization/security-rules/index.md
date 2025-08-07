---
sidebar_position: 2
title: Security Rules
description: Learn how to customize security rules in SolidX.
keywords: [backend, security, customization]
---

# 🔐 Security Rules in SolidX

Security rules are crucial for **controlling access to data** in SolidX. By defining these rules, you can restrict visibility at the model level and ensure that only authorized users can access sensitive information.

---

## ➕ Adding a New Security Rule

Follow these steps to configure a custom security rule:

1. ✍️ Add a rule inside the `securityRules` array in the module metadata JSON file.
2. 🔐 Define the following properties:
   - `name`: Unique identifier for the rule
   - `description`: What the rule does
   - `roleUserKey`: The role for which the rule applies (e.g., "Institute Admin")
   - `modelMetadataUserKey`: The model this rule applies to (e.g., "institute")
3. ⚙️ Define the logic inside `securityRuleConfig.filters`. These filters are applied when data is retrieved for the logged-in user, depending upon the user's role and the model data they are accessing.

<details>
<summary>📄 Example: Rule for <code>Institute Admin</code></summary>

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

## ⚙️ How It Works

1. ✅ Security rules are evaluated within the `SolidBaseRepository` class (from `@solidstarters/solid-core`).
2. ✅ Any repository that extends `SolidBaseRepository` will automatically enforce security rules during data retrieval via query builders.
3. ✅ All generated model repositories in SolidX inherit this behavior — security filters are applied transparently.
4. 🧠 When users call a model controller’s `find` endpoint, the logic goes through the CRUD service → repository → `find` or query builder → applying security rules.
5. ♻️ Security rules are loaded from the database **at server startup** and stored in the Solid Registry.
   - ℹ️ After updating or adding rules, **restart the server** for the changes to take effect.

:::info Note
Support for applying rules in the basic `find()` method is still a TODO.
:::

---
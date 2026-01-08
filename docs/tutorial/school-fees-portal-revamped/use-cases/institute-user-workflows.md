---
sidebar_position: 2
---

# Institute Admin

This section covers the primary workflows for an institute's administrative user, from creation to logging in and managing users to initiating payments and handling cancellations.

:::info Pre-requisite
This guide assumes you have the necessary data models configured, including a one-to-many relationship between `Institute` and `InstituteUser`, where `InstituteUser` is a child of the main `User` table.
:::

## 1. Add Institute Users

Once an institute is created, the Super Admin or an Institute Admin can add other users to manage the institute's operations. These users are assigned roles that grant them specific permissions, such as initiating payments, managing student records, or viewing transaction reports.

There are two ways to add institute users:
1.  **With Password**: The admin sets an initial password for the user, which they can use to log in immediately.

![Institute User Login Screens](/img/tutorial/school-fees-portal/6-usecase/ins-5.png)

2.  **Without Password**:

![Institute User Login Screens](/img/tutorial/school-fees-portal/6-usecase/ins-user.png)



## 2. Institute User Login and Access Control

An `InstituteUser` is a user who belongs to a specific institute. Their access must be strictly limited to their own institute's data. When an institute user logs in, they should only see the students, fee structures, and payment records associated with their institute.

<div style={{ display: "flex", gap: "2%"}}>
  <img src="/img/tutorial/school-fees-portal/6-usecase/login1.png" alt="Institute User Login Screen 1" style={{ width: "48%" }} />
  <img src="/img/tutorial/school-fees-portal/6-usecase/login2.png" alt="Institute User Login Screen 2" style={{ width: "48%" }} />
</div>

###

_After a successful login, the user is redirected to the institute's dashboard._

![Institute Dashboard](/img/tutorial/school-fees-portal/6-usecase/ins-6.png)

### The Magic of Security Record Rules

**SolidX** achieves this data isolation not by writing complex queries in every service, but by using ***Security Record Rules***. These are powerful, metadata-driven rules that automatically filter data for a user based on their role and relationships.

**Example Rule:**

-   **Goal:** An Institute Admin should only see records from their own institute.
-   **Rule Logic:** "For a user with the 'Institute Admin' role, when they query for any model that has a relation with `institute`, only return the records where the `institute` field matches the `institute` field of the logged-in user's own `InstituteUser` record."

#### Explaining the Security Rule Snippet

```json
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
```

-   `"roleUserKey": "Institute Admin"`: This rule applies only to users with the "Institute Admin" role.
-   `"modelMetadataUserKey": "institute"`: This rule will apply to any data model that has a field named "institute".
-   `"securityRuleConfig"`: This defines the filter logic.
-   `"filters": { "instituteUsers": { "id": { "$eq": "$activeUserId" } } }`: This is the core of the rule. It filters the `instituteUsers` table to find the record matching the currently logged-in user (`$activeUserId`). SolidX then uses this to identify the user's institute and applies it as a filter to all queries on models with an `institute` field.

To configure security rule, Go to **Solid Core > IAM > Security Rules** section of the admin panel. After that, every query, API call, and list view is automatically and securely filtered.

![Security Record Rule Configuration](/img/tutorial/school-fees-portal/6-usecase/ins-7.png)

Next, we will explore how an institute user can initiate single or bulk payments (via Excel), cancel payments, and configure scheduled auto-reminders (daily, weekly, monthly, etc.).
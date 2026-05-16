---
sidebar_position: 11
title: Security Rules
description: Learn how to customize security rules in SolidX, including rules backed by custom providers.
summary: Explains SolidX record-level security rules for controlling data visibility per role and model. Covers both static metadata filters and dynamic securityRuleConfigProvider-based rules, how rule evaluation works inside SolidBaseRepository, how multiple rules combine, and how to implement and register a custom provider in a consuming project.
keywords: [backend, security, customization]
solidx_concerns: [add/update_security_record_rule]
---

import { IoIosLock, IoIosInformationCircle, IoIosWarning } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';

# Security Rules in SolidX

Security rules control **who can see which records**. You attach rules **per role** and **per model** so different roles get different visibility.

<NoteBoxs>
By default, **no security rules are enforced**. If a model has no matching security rules for the active user's roles, SolidX does not add record-level restrictions for that model.
</NoteBoxs>

## When you'd use them

- A **Super Admin** can view all clients.
- A **Client Admin** should only see the **single Client** they belong to.
- A **Venue User** should only see records tied to their assigned venues.
- A **workflow role** should only see records in certain statuses and only when those records are assigned to them.

Security rules are especially useful when access logic depends on the active user, their role, or related records such as associations, territories, venues, or reporting structures.

## Two ways to define a rule

SolidX supports two patterns:

1. **Static metadata filters**
   Use `securityRuleConfig.filters` directly in metadata when the rule can be expressed as a normal SolidX filter object.
2. **Dynamic provider-backed filters**
   Use `securityRuleConfigProvider` when the filter must be computed at runtime, for example by loading related records for the active user first.

The provider-backed pattern is the right choice when access logic depends on data you cannot express cleanly in a static JSON snippet.

## Static metadata rule

Add entries to the `securityRules` array in your module metadata JSON.

**Important fields**

| Field | Type | Purpose |
| --- | --- | --- |
| `name` | string | Unique name for the rule |
| `description` | string | Human-readable explanation |
| `roleUserKey` | string | The target role, for example `"Institute Admin"` |
| `modelMetadataUserKey` | string | The target model, for example `"institute"` |
| `securityRuleConfig.filters` | object | Static record-level filter |
| `securityRuleConfigProvider` | string | Optional provider class name for dynamic rule evaluation |

**Special variable**

- `$activeUserId` is replaced at runtime with the logged-in user's ID.

**Preferred naming convention**

- Prefer naming security rules as `model:<model-name>-role:<role-name>`.
- Example: `model:lead-role:Surveyor`

<details open>
  <summary className="card-title ">
    Example: <code>Institute Admin</code> sees only their institute
  </summary>

```json
{
  "securityRules": [
    {
      "name": "model:institute-role:Institute Admin",
      "description": "Show institute associated with the active user",
      "roleUserKey": "Institute Admin",
      "modelMetadataUserKey": "institute",
      "securityRuleConfig": {
        "filters": {
          "instituteUsers": {
            "id": { "$eq": "$activeUserId" }
          }
        }
      },
      "securityRuleConfigProvider": ""
    }
  ]
}
```

</details>

This is enough when a direct filter is available and only simple active-user substitution is needed.

<h2 className="card-headear-wrapper">
  <IoIosLock size={26} style={{ marginRight: "10px" }} />
  Dynamic Security Rules With Custom Providers
</h2>

Use a custom provider when the final filter must be built dynamically at runtime.

Common examples:

- load the active user's associations first, then build an `$in` filter
- apply different filters for different roles inside one shared provider
- add model-specific logic inside the provider based on `securityRule.modelMetadata`
- return a deny-all fallback when required context cannot be resolved

In the core implementation, SolidX checks `securityRuleConfigProvider` first. If it is present, SolidX resolves that provider from the registry and calls its `securityRuleConfig(activeUser, securityRule)` method. If no provider is configured, SolidX falls back to parsing `securityRuleConfig` from metadata.

## Implement a custom security rule provider

Create a provider class in your backend module and decorate it with `@SecurityRuleConfigProvider()`.

The provider must:

- be decorated with `@Injectable()`
- implement `ISecurityRuleConfigProvider`
- return a `SecurityRuleConfig`

Example pattern:

```ts
import { Injectable } from "@nestjs/common";
import {
  ActiveUserData,
  ISecurityRuleConfigProvider,
  SecurityRule,
  SecurityRuleConfig,
  SecurityRuleConfigProvider,
} from "@solidxai/core";
import { VenueUserService } from "../venue-user.service";

@SecurityRuleConfigProvider()
@Injectable()
export class VenueAwareSecurityRuleConfigProvider
  implements ISecurityRuleConfigProvider
{
  constructor(private readonly venueUserService: VenueUserService) {}

  async securityRuleConfig(
    activeUser: ActiveUserData,
    securityRule: SecurityRule
  ): Promise<SecurityRuleConfig> {
    const venueUser = await this.venueUserService.findOne(activeUser.sub, {
      populate: ["venues", "venues.venueMaster"],
    });

    const venueIds =
      venueUser?.venues?.map((association) => association.venueMaster.id) ?? [];

    if (venueIds.length === 0) {
      return {
        filters: {
          id: { $eq: -1 },
        },
      };
    }

    if (securityRule.modelMetadata.singularName === "lead") {
      return {
        filters: {
          $and: [
            {
              venue: {
                id: { $in: venueIds },
              },
            },
            {
              surveyor: {
                id: { $eq: activeUser.sub },
              },
            },
          ],
        },
      };
    }

    return {
      filters: {
        id: { $eq: -1 },
      },
    };
  }
}
```

### What the provider receives

- `activeUser`
  The authenticated user's runtime context.
- `securityRule`
  The resolved security rule entity, including the linked role and model metadata.

This means the same provider can branch on:

- `securityRule.role.name`
- `securityRule.modelMetadata.singularName`
- any related application data you load yourself

## Register the provider in your module

Add the provider to the Nest module's `providers` list so SolidX can resolve it from the application container.

```ts
import { VenueAwareSecurityRuleConfigProvider } from "./services/security-rules/venue-aware-security-rule-config-provider";

@Module({
  providers: [
    VenueAwareSecurityRuleConfigProvider,
  ],
})
export class VenueModule {}
```

If the provider is not registered, SolidX will fail when it tries to resolve `securityRuleConfigProvider`.

## Wire the provider from metadata

In metadata, point the rule at the provider by class name.

```json
{
  "securityRules": [
    {
      "name": "model:lead-role:Surveyor",
      "description": "Show me leads where Surveyor is me and the lead belongs to my venue.",
      "roleUserKey": "Surveyor",
      "modelMetadataUserKey": "lead",
      "securityRuleConfig": {},
      "securityRuleConfigProvider": "VenueAwareSecurityRuleConfigProvider"
    }
  ]
}
```

This pattern is used in consuming projects where many role-and-model combinations reuse one dynamic provider, and the provider decides the exact filter to return for each rule.

## How rule evaluation works

<h2 className="card-headear-wrapper">
  <IoIosInformationCircle size={26} style={{ marginRight: "10px" }} />
  How It Works
</h2>

At query time:

1. `SolidBaseRepository` asks the security rule repository for rules matching the current model and the active user's roles.
2. For each matching rule:
   - if `securityRuleConfigProvider` is set, SolidX calls the provider
   - otherwise SolidX parses `securityRuleConfig` and resolves `$activeUserId`
3. Each evaluated rule contributes one filter group.
4. SolidX combines those rule groups with **OR** at the top level.
5. Within an individual rule's `filters`, your normal filter logic still applies, including `$and`, `$or`, relation traversal, `$in`, and so on.

This is why users with multiple applicable roles effectively get the **most permissive** access across those matching rules.

### Mental model for combining rules

- **Across rules**: OR
- **Inside one rule**: whatever your `filters` object says

So if a user has:

- one rule that allows records from `venue A`
- another rule that allows records assigned to them personally

the final query can return records matching **either** rule.

## Real-world pattern from a consuming project

One common production pattern is:

- metadata creates one security rule per role and per model
- most of those rules point to the same `securityRuleConfigProvider`
- the provider loads user associations first
- the provider returns model-specific filters such as:
  - leads in the user's venues
  - call logs whose related lead is in the user's venues
  - tighter status filters for roles like Telecaller

This keeps metadata declarative while moving the dynamic logic into normal TypeScript service code.

## When to choose static vs provider-backed rules

- Use **static metadata filters** when a plain filter object is enough.
- Use a **provider** when you need to query supporting data before deciding the final filter.
- Use a **shared provider** when many rules across several models follow the same access pattern.

As a rule of thumb: if you are tempted to encode business logic into awkward metadata or duplicate many near-identical rules, move that logic into a provider.

<h2 className="card-headear-wrapper">
  <IoIosWarning size={26} style={{ marginRight: "10px" }} />
  Common Pitfalls & Troubleshooting
</h2>

- **Restart required:** Rules are loaded into the registry at startup. Restart the server after changing metadata or adding a new provider.
- **Provider name must match:** `securityRuleConfigProvider` must match the registered provider name that SolidX resolves from the registry.
- **Provider must be registered in the module:** Decorating the class is not enough if Nest never instantiates it.
- **Return a valid `SecurityRuleConfig`:** The provider should always return an object shaped like `{ filters: ... }`.
- **Use a safe fallback:** If the active user has no associations, prefer a deny-all fallback such as `id = -1` rather than returning a broad filter accidentally.
- **Remember OR semantics across matching rules:** Multiple matching role rules widen visibility.
- **Public endpoints bypass rules:** Do not rely on security rules for unauthenticated routes.
- **Static and dynamic rules are not merged for one rule entry:** when `securityRuleConfigProvider` is present, SolidX evaluates the provider path for that rule.
- **Provider errors fail the request:** If your provider throws, the query fails. Keep the logic defensive.
- **Validate relation paths carefully:** Your returned filters still have to match real model fields and relations.

### Debugging tips

- Turn on SQL logging to inspect the generated query behavior:

```bash
DEFAULT_DATABASE_LOGGING=true
```

- Add temporary logging inside the provider to confirm:
  - which rule was resolved
  - which role and model were passed in
  - what final filter object was returned

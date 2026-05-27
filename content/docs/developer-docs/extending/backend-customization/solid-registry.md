---
title: Solid Registry
description: Learn how to extend and use the Solid Registry in your SolidX application.
summary: Explains the Solid Registry as SolidX's central discovery and configuration hub, acting as a cache and metadata manager. Provides fast component lookups, application-wide consistency for rules/modules/providers, and extensibility via decorator-based auto-discovery. Covers the registry pattern (Decorator → Interface → Implementation → Registry → Consumer), registered components including error code providers, selection providers, computed field providers, scheduled jobs, email/SMS/WhatsApp providers, and security rules.
keywords: [backend, solid registry, customization, metadata]
---

The **Solid Registry** is the central **discovery and configuration hub** of your SolidX application.  
It acts both as a **cache** and a **metadata manager**, providing:

- **Fast lookups**: Components can be resolved without repeated database queries.
- **Consistency**: Application-wide rules, modules, and providers are available in one place.
- **Extensibility**: Drop in a new provider, decorate it, and the registry auto-discovers it.

At application startup, the registry loads all relevant components and makes them available for runtime resolution.  
If you update registered metadata, you **must restart the application** to reload the registry.

## Registered Components

The following components are tracked by the Solid Registry:

Seeders

**Purpose:** Populate your database with initial or default data (e.g., system roles, default fee types).  
**How it works:** The registry maintains a catalog of all available seeders. Developers can easily list, execute, or selectively run seeders.  
**See also:** [Seeders Guide](../../database-seeding)

Scheduled Jobs

**Purpose:** Define recurring tasks such as reminders, report generation, and cleanup jobs.  
**How it works:** Registered jobs are tied into the scheduling engine. The registry ensures all jobs are loaded, discoverable, and can be managed or paused centrally.  
**See also:** [Jobs & Scheduling](./scheduled-jobs)

Selection Providers

**Purpose:** Provide dynamic values for selection fields in the UI (e.g., dropdowns, filters).  
**How it works:** A `@SelectionProvider` class can be created, registered, and then consumed by form components. The registry ensures all providers are globally available without additional wiring.  
**See also:** [Field Metadata](../../metadata_schema/field-metadata)

Computed Fields

**Purpose:** Derive field values dynamically based on logic (e.g., total amount, status based on conditions).  
**How it works:** Each computed field provider is registered with metadata, making them discoverable by the runtime when evaluating entity fields.  
**See also:** [Computed Fields](/docs/recipes/computed-fields)

Solid Database Modules

**Purpose:** Define your application’s database schema, models, and relations.  
**How it works:** Modules (like Fees, School, Library) are registered in the Solid Registry, ensuring schema consistency and discoverability across the application.  
**See also:** [Modules Overview](/docs/admin-docs/module-builder/module-management)

Controllers

**Purpose:** Handle incoming HTTP requests and expose routes.  
**How it works:** The registry tracks all controllers, enabling automated route mapping and simplifying metadata introspection for APIs.  
**See also:** [Controllers](./extending-controllers)

Security Rules

**Purpose:** Restrict access to entities and fields based on roles and policies.  
**How it works:** The registry stores all declared rules. Every query automatically applies these rules by resolving them from the registry.  
**See also:** [Security Rules](./security-rules)

Locales

**Purpose:** Manage localization, translations, and regional formats.  
**How it works:** Each locale configuration is registered at startup. Applications can dynamically switch or apply formats based on user preference.  
**See also:** [Localization](/docs/developer-docs/extending/backend-customization/solid-registry)

Dashboard Variable Selection Providers

**Purpose:** Provide dynamic lists of variables for dashboards (e.g., filters like branch, department, or timeframe).  
**How it works:** Developers can implement new providers that populate variables at runtime. The registry ensures these providers are available to all dashboards.  
**See also:** [Dashboards](./dashboard-providers)

Dashboard Question Data Providers

**Purpose:** Supply data sources for dashboard questions (charts, KPIs, summaries).  
**How it works:** Providers can query APIs, databases, or aggregates. The registry makes them available for dynamic dashboard rendering.  
**See also:** [Dashboard Questions](/docs/developer-docs/extending/backend-customization/solid-registry)

## When Is the Registry Populated?

All components are registered **at application startup**.  

- This ensures they are immediately discoverable.  
- If you modify any registered metadata, restart the application.  
- Hot-reload of providers is not supported (yet).  

> **Note**
> If you are running the application in a dev mode i.e using `npm run solidx:dev`, the application will automatically restart when it detects file changes, so you don't need to manually restart it for registry changes to take effect.


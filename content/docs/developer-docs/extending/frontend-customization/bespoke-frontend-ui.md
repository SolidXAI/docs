---
title: Bespoke Frontend
icon: "paintbrush"
description: Build fully custom React applications inside Solid using module-owned custom layouts, manifest-based route registration, and Solid HTTP helpers.
summary: "Comprehensive guide for creating bespoke frontend experiences in SolidX using Vite + React. Covers folder conventions under `custom-layout`, creating layout wrappers with isolated CSS, registering routes in `<module>.ui-module.ts`, aggregating them through the UI module runtime, and building pages with Solid HTTP helpers (`solidGet`, `solidPost`, etc.)."
solidx_concerns: [frontend.custom_pages, add_full_custom_ui]
---

## Overview

Solid supports building completely bespoke user interfaces in React, outside metadata-driven form/list rendering.

This pattern is intended for app-like experiences (for example merchant apps, kiosk flows, domain-specific workflows) where you want full control over:

- Layout
- Navigation
- Components
- Styling
- API orchestration

## Required Pattern

For bespoke UIs, follow this operating model:

1. Create a dedicated layout component and wrapper with its own CSS.
2. Keep bespoke route-level UI under `src/<module-name>/custom-layout/<layout-reference>/...`.
3. Register bespoke routes in the owning module manifest (`<module-name>.ui-module.ts`).
4. Build pages as pure React and use Solid HTTP helpers for backend calls.

## Where Files Should Live

Bespoke UI should live inside the owning module under `custom-layout/`, not inside `admin-layout/` extension folders.

Recommended structure:

```bash
solid-ui/src/
├── <module-name>/
│   ├── custom-layout/
│   │   └── <layout-reference>/
│   │       ├── <LayoutReference>Layout.tsx
│   │       ├── <LayoutReference>LayoutWrapper.tsx
│   │       ├── <LayoutReference>.css
│   │       ├── common/
│   │       ├── home/
│   │       ├── feature-a/
│   │       └── feature-b/
│   ├── redux/
│   └── <module-name>.ui-module.ts
└── AppRoutes.tsx
```

Example from production-style implementation:

- `src/tranaction/custom-layout/merchant-app/MerchantAppLayout.tsx`
- `src/tranaction/custom-layout/merchant-app/MerchantAppLayoutWrapper.tsx`
- `src/tranaction/custom-layout/merchant-app/MerchantApp.css`
- `src/tranaction/tranaction.ui-module.ts` with `/merchant-app/...` routes
- `src/AppRoutes.tsx` consuming aggregated module routes

## Step 1: Create a Dedicated Layout

Create a layout component that controls your bespoke shell (nav, header, drawer, responsive behavior, etc.) and imports its own CSS.

```tsx
import "./MerchantApp.css";

export const MerchantAppLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="merchant-app-layout">
      <main className="merchant-app-main">{children}</main>
    </div>
  );
};
```

## Step 2: Create a Layout Wrapper with `Outlet`

The wrapper connects your layout shell to nested route pages:

```tsx
import { Outlet } from "react-router-dom";
import { MerchantAppLayout } from "./MerchantAppLayout";

export function MerchantAppLayoutWrapper() {
  return (
    <MerchantAppLayout>
      <Outlet />
    </MerchantAppLayout>
  );
}
```

## Step 3: Register Bespoke Routes in `<module>.ui-module.ts`

Declare your bespoke route tree in the owning UI module manifest using `routes.extraRoutes`.

```ts
import { createElement } from "react";
import { AuthGuard, type SolidUiModule } from "@solidxai/core-ui";
import { MerchantAppLayoutWrapper } from "./custom-layout/merchant-app/MerchantAppLayoutWrapper";
import { HomePage } from "./custom-layout/merchant-app/home-page/HomePage";
import { ReportPage } from "./custom-layout/merchant-app/report/ReportPage";

const tranactionUiModule = {
  name: "tranaction",
  routes: {
    extraRoutes: [
      {
        element: createElement(AuthGuard),
        children: [
          {
            element: createElement(MerchantAppLayoutWrapper),
            children: [
              { path: "/merchant-app/home", element: createElement(HomePage) },
              { path: "/merchant-app/report", element: createElement(ReportPage) },
            ],
          },
        ],
      },
    ],
  },
} satisfies SolidUiModule;

export default tranactionUiModule;
```

Then let the app aggregate all module manifests through `solid-ui-modules.ts`, and let `AppRoutes.tsx` remain thin:

```tsx
import { useRoutes } from "react-router-dom";
import { getSolidRoutes } from "@solidxai/core-ui";
import { solidUiModuleRuntime } from "./solid-ui-modules";

export function AppRoutes() {
  const routes = getSolidRoutes(solidUiModuleRuntime.routes);
  return useRoutes(routes);
}
```

Use a stable base route namespace such as:

- `/merchant-app/...`
- `/field-force/...`
- `/partner-portal/...`

The folder name under `custom-layout/` should still be a logical layout reference (for example `merchant-app`, `public-site`, `partner-portal`), but the mounted route path does not have to match that folder name.

You can mount a custom layout anywhere you want, including:

- `/merchant-app/...`
- `/partner/...`
- `/dashboard/...`
- `/`

Mounting a custom layout at `/` makes it the effective homepage shell of the consuming Solid project. This is especially useful when using Solid as a full-stack framework for CMS-driven websites, public-facing sites, landing experiences, or other projects where the bespoke frontend should become the default application surface.

## Step 4: Build Pages as Pure React

Inside bespoke pages you can use any React patterns and libraries:

- Shadcn, MUI, Chakra, Primereact, Tailwind, plain CSS, CSS Modules, etc.
- React hooks/state machines/context
- Any reusable local component architecture

No metadata schema is required for these pages.

## Step 5: Choose an API Integration Style

Solid supports both of these patterns for bespoke frontend work:

1. Solid HTTP helpers for direct promise-based API calls
2. Redux / RTK Query integration through module-owned reducers and middleware

This is a developer choice. Both are valid and supported.

### Option A: Use Solid HTTP Helpers

Use `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete` for direct data access.

```tsx
import { useEffect, useState } from "react";
import { solidGet, solidPost } from "@solidxai/core-ui";

export function HomePage() {
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const resp = await solidGet("/merchant-dashboard");
        setItems(resp?.data?.data?.records || []);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const createItem = async () => {
    await solidPost("/merchant-dashboard", { name: "New item" });
  };

  return <div>{loading ? "Loading..." : `Items: ${items.length}`}</div>;
}
```

Use this style when you want lightweight, local API orchestration without central store concerns.

### Option B: Use Module-Owned Redux / RTK Query

If you prefer store-backed API integration, place RTK Query APIs under the owning module's `redux/` folder and register them in `<module-name>.ui-module.ts`.

Example:

```ts
import type { SolidUiModule } from "@solidxai/core-ui";
import { reportApi } from "./redux/reportApi";
import { transactionApi } from "./redux/getTransactionApi";

const tranactionUiModule = {
  name: "tranaction",
  reducers: {
    [reportApi.reducerPath]: reportApi.reducer,
    [transactionApi.reducerPath]: transactionApi.reducer,
  },
  middlewares: [
    reportApi.middleware,
    transactionApi.middleware,
  ],
} satisfies SolidUiModule;
```

The runtime aggregates these registrations and passes them to `StoreProvider` through `solidUiModuleRuntime`.

Use this style when you want:

- shared API state across multiple screens
- caching and invalidation
- generated query/mutation hooks
- a more structured app-wide API layer

For a full walkthrough, see [Redux Module Integration](./redux-module-integration.md). For direct API helpers, see [Solid HTTP API](./solid-http-api.md).

## Styling Guidance

Each bespoke layout should own its styling boundary.

Recommended:

- Keep one root CSS file per bespoke app shell (for example `MerchantApp.css`)
- Use app-specific class prefixes (for example `merchant-app-*`)
- Keep feature-level CSS close to feature page folders (`home.css`, `report.css`, etc.)
- Keep layout assets and related feature files together under the module's `custom-layout/` tree

This prevents accidental style collisions with the default Solid admin UI.

## Routing and Navigation Notes

- Use nested routes under one wrapper when pages share the same bespoke shell.
- Use separate wrappers if you need multiple bespoke shells.
- Keep route paths explicit and versionable (`/merchant-app/v2/...`) when evolving UX.

## Integration Boundaries

Use bespoke pages when you need full UI freedom.

Use metadata-driven customization in `admin-layout/` when you want to extend existing generated Solid views.

You can combine both approaches in one application.

## Common Mistakes

- Placing full bespoke route UIs in `admin-layout/` instead of `custom-layout/`
- Skipping a layout wrapper and duplicating shell UI across each page
- Mixing bespoke CSS with generic global selectors
- Hardcoding backend URLs instead of using `solid-http` helpers

## Checklist

1. Create `Layout.tsx` + `LayoutWrapper.tsx` + dedicated CSS under `src/<module-name>/custom-layout/<layout-reference>/`.
2. Register nested routes in `<module-name>.ui-module.ts` under `routes.extraRoutes`.
3. Ensure `solid-ui/src/solid-ui-modules.ts` aggregates module manifests.
4. Keep `AppRoutes.tsx` beside `App.tsx` and use `getSolidRoutes(solidUiModuleRuntime.routes)`.
5. Ensure routes are grouped under a clear base path (`/<layout-reference>/...`).
6. Build pages as React components.
7. Choose either direct Solid HTTP helpers or module-owned Redux / RTK Query integration.

## See Also

- [Solid HTTP API](./solid-http-api.md)
- [Redux Module Integration](./redux-module-integration.md)
- [Custom Views](./custom-views.md)

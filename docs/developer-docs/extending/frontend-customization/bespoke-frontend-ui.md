---
sidebar_position: 10
title: Bespoke Frontend
description: Build fully custom React applications inside Solid using dedicated page layouts, route injection, and Solid HTTP helpers.
summary: Comprehensive guide for creating 100% bespoke frontend experiences in SolidX using Vite + React. Covers folder conventions under `pages`, creating layout wrappers with isolated CSS, wiring routes via `AppRoutes.tsx` and `getSolidRoutes`, and building pages with `solid-http` helpers (`solidGet`, `solidPost`, etc.).
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
2. Keep bespoke pages under `src/pages/<layout-reference>/...`.
3. Inject routes through `AppRoutes.tsx` using `getSolidRoutes({ extraRoutes })`.
4. Build pages as pure React and use Solid HTTP helpers for backend calls.

## Where Files Should Live

Bespoke UI pages should live in `pages` (not extension widget folders).

Recommended structure:

```bash
solid-ui/src/
├── pages/
│   └── <layout-reference>/
│       ├── <LayoutReference>Layout.tsx
│       ├── <LayoutReference>LayoutWrapper.tsx
│       ├── <LayoutReference>.css
│       ├── common/
│       ├── home/
│       ├── feature-a/
│       └── feature-b/
└── routes/
    └── AppRoutes.tsx
```

Example from production-style implementation:

- `src/pages/merchant-app/MerchantAppLayout.tsx`
- `src/pages/merchant-app/MerchantAppLayoutWrapper.tsx`
- `src/pages/merchant-app/MerchantApp.css`
- `src/routes/AppRoutes.tsx` with `/merchant-app/...` routes

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

## Step 3: Add Bespoke Routes in `AppRoutes.tsx`

Inject your route tree using `extraRoutes` in `getSolidRoutes`.

```tsx
import { useRoutes } from "react-router-dom";
import { getSolidRoutes } from "@solidxai/core-ui";
import { MerchantAppLayoutWrapper } from "../pages/merchant-app/MerchantAppLayoutWrapper";
import { HomePage } from "../pages/merchant-app/home/HomePage";
import { ReportPage } from "../pages/merchant-app/report/ReportPage";

export function AppRoutes() {
  const routes = getSolidRoutes({
    extraRoutes: [
      {
        element: <MerchantAppLayoutWrapper />,
        children: [
          { path: "/merchant-app/home", element: <HomePage /> },
          { path: "/merchant-app/report", element: <ReportPage /> },
        ],
      },
    ],
  });

  return useRoutes(routes);
}
```

Use a stable base route namespace such as:

- `/merchant-app/...`
- `/field-force/...`
- `/partner-portal/...`

## Step 4: Build Pages as Pure React

Inside bespoke pages you can use any React patterns and libraries:

- PrimeReact, MUI, Chakra, Tailwind, plain CSS, CSS Modules, etc.
- React hooks/state machines/context
- Any reusable local component architecture

No metadata schema is required for these pages.

## Step 5: Use Solid HTTP Helpers for API Calls

Use `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete` for data access.

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

For full HTTP helper guidance, see [Solid HTTP API](./solid-http-api.md).

## Styling Guidance

Each bespoke layout should own its styling boundary.

Recommended:

- Keep one root CSS file per bespoke app shell (for example `MerchantApp.css`)
- Use app-specific class prefixes (for example `merchant-app-*`)
- Keep feature-level CSS close to feature page folders (`home.css`, `report.css`, etc.)

This prevents accidental style collisions with the default Solid admin UI.

## Routing and Navigation Notes

- Use nested routes under one wrapper when pages share the same bespoke shell.
- Use separate wrappers if you need multiple bespoke shells.
- Keep route paths explicit and versionable (`/merchant-app/v2/...`) when evolving UX.

## Integration Boundaries

Use bespoke pages when you need full UI freedom.

Use metadata-driven customization (form/list widgets, events, buttons) when you want to extend existing generated Solid views.

You can combine both approaches in one application.

## Common Mistakes

- Placing full bespoke pages in `src/extensions/...` instead of `src/pages/...`
- Skipping a layout wrapper and duplicating shell UI across each page
- Mixing bespoke CSS with generic global selectors
- Hardcoding backend URLs instead of using `solid-http` helpers

## Checklist

1. Create `Layout.tsx` + `LayoutWrapper.tsx` + dedicated CSS under `src/pages/<layout-reference>/`.
2. Add nested routes in `AppRoutes.tsx` with `getSolidRoutes({ extraRoutes })`.
3. Ensure routes are grouped under a clear base path (`/<layout-reference>/...`).
4. Build pages as React components.
5. Call APIs via `solidGet`/`solidPost`/etc.

## See Also

- [Solid HTTP API](./solid-http-api.md)
- [Custom Views](./custom-views.md)

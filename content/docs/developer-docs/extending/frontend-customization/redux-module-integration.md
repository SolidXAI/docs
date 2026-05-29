---
title: Redux Integration
icon: "layers"
description: Register module-owned Redux reducers and middleware in SolidX frontend modules.
summary: "Documents how to organize RTK Query APIs, reducers, and middleware under `solid-ui/src/<module-name>/redux/`, register them in `<module-name>.ui-module.ts`, and let the UI module runtime aggregate them into `StoreProvider`. Covers the NBF-style pattern for module-owned API integration and when to choose Redux over direct Solid HTTP helpers."
solidx_concerns: [frontend.custom_pages, add_full_custom_ui, frontend.redux_module_integration]
---

## Overview

SolidX supports two valid frontend API integration styles:

1. Direct promise-based API calls with Solid HTTP helpers such as `solidGet` and `solidPost`
2. Redux-based integration using RTK Query APIs, reducers, and middleware registered per UI module

Both are supported. The choice depends on how you want to structure the consuming app.

Use Redux module integration when you want:

- shared cached API state
- generated query/mutation hooks
- reducer and middleware composition per module
- a consistent app-wide RTK Query pattern

Use direct Solid HTTP helpers when you want:

- lightweight one-off API calls
- bespoke flows without centralized store concerns
- minimal setup for route-local or component-local logic

## Folder Convention

Put module-owned Redux code under:

```text
solid-ui/src/<module-name>/redux/
```

Example from NBF:

```text
solid-ui/src/merchant-onboarding/redux/
  applicationApi.tsx
  applicationBankApi.tsx
  applicationLocationApi.tsx
  applicationTerminalApi.tsx

solid-ui/src/tranaction/redux/
  authApi.tsx
  dynamicQrCodeApi.tsx
  getTransactionApi.tsx
  payByLinkApi.tsx
  reportApi.tsx
  requestToPayApi.tsx
  staticQrApi.tsx
```

## Module Manifest Registration

Register reducers and middleware in the owning UI module manifest.

Example:

```ts
import type { SolidUiModule } from "@solidxai/core-ui";
import { applicationApi } from "./redux/applicationApi";
import { applicationLocationApi } from "./redux/applicationLocationApi";

const merchantOnboardingUiModule = {
  name: "merchant-onboarding",
  reducers: {
    [applicationApi.reducerPath]: applicationApi.reducer,
    [applicationLocationApi.reducerPath]: applicationLocationApi.reducer,
  },
  middlewares: [
    applicationApi.middleware,
    applicationLocationApi.middleware,
  ],
} satisfies SolidUiModule;

export default merchantOnboardingUiModule;
```

This keeps API ownership inside the module rather than in `App.tsx`.

## App Wiring

The app should not manually import every module API.

Instead, aggregate modules in `solid-ui-modules.ts`:

```ts
import {
  createSolidUiModuleRuntime,
  getSolidUiModules,
  registerSolidUiModuleExtensions,
  type SolidUiModule,
} from "@solidxai/core-ui";

const moduleImports = import.meta.glob<SolidUiModule>("./*/*.ui-module.ts", {
  eager: true,
  import: "default",
});

export const solidUiModules = getSolidUiModules(moduleImports);

registerSolidUiModuleExtensions(solidUiModules);

export const solidUiModuleRuntime = createSolidUiModuleRuntime(solidUiModules);
```

Then wire the store once in `App.tsx`:

```tsx
import { StoreProvider } from "@solidxai/core-ui";
import { solidUiModuleRuntime } from "./solid-ui-modules";

<StoreProvider
  reducers={solidUiModuleRuntime.reducers}
  middlewares={solidUiModuleRuntime.middlewares}
>
  {children}
</StoreProvider>
```

If no module contributes custom reducers or middleware, the runtime still returns valid empty values:

```ts
reducers: {}
middlewares: []
```

So the app can keep the same `StoreProvider` invocation regardless of whether modules currently register store extensions.

## Example RTK Query API

```ts
import { createApi } from "@reduxjs/toolkit/query/react";
import { baseQueryWithAuth } from "@solidxai/core-ui";

export const applicationApi = createApi({
  reducerPath: "applicationApi",
  baseQuery: baseQueryWithAuth,
  tagTypes: ["Application"],
  endpoints: (builder) => ({
    createApplication: builder.mutation({
      query: (body) => ({
        url: "/application",
        method: "POST",
        body,
      }),
    }),
  }),
});

export const {
  useCreateApplicationMutation,
} = applicationApi;
```

## Choosing Between Solid HTTP and Redux

### Choose Solid HTTP helpers when:

- the flow is local to one page or one component
- you do not need shared cached state
- you want a minimal promise-based implementation
- the API orchestration is custom or multi-step

### Choose Redux / RTK Query when:

- multiple screens or components need the same API state
- you want generated hooks and caching
- you want tag-based invalidation and refetch behavior
- the project already uses module-owned RTK Query APIs as a standard

Both approaches are valid in the same application.

For example:

- a bespoke CMS homepage in `custom-layout/` may use `solidGet` directly
- a merchant workflow in `tranaction/redux/` may use RTK Query hooks for shared app state

## Best Practices

- Keep Redux code owned by the module that owns the backend model or workflow
- Register reducers and middleware only in that module's `.ui-module.ts`
- Avoid duplicating reducer paths across modules
- Keep `App.tsx` module-agnostic
- Prefer stable module ownership over a central `src/redux/` dumping ground

## Troubleshooting

- `Duplicate Solid UI reducer path registered`:
  two modules are registering the same API reducer path
- Missing hooks or store behavior:
  verify the module manifest includes both `reducers` and `middlewares`
- State is not available:
  verify `StoreProvider` is using `solidUiModuleRuntime.reducers` and `solidUiModuleRuntime.middlewares`

## See Also

- [Bespoke Frontend UI](./bespoke-frontend-ui.md)
- [Solid HTTP API](./solid-http-api.md)
- [Solid Entity API](./solid-entity-api.md)

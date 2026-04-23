---
sidebar_position: 7
title: Solid Entity API
description: Learn how to use the Solid Entity API to interact with entities in your application.
summary: "Guide to using the Solid Entity API for managing entities in SolidX applications. Covers generated RTK Query CRUD APIs, common query and mutation flows, caching and invalidation behavior, and where these APIs fit in the UI module system."
solidx_concerns: [frontend.custom_pages, add_full_custom_ui]
---

## Overview

`createSolidEntityApi` provides a consistent RTK Query surface for common CRUD operations across entities in SolidX applications.

Use it when you want:

- generated query and mutation hooks
- RTK Query caching and invalidation
- a reusable module-owned API layer under `solid-ui/src/<module-name>/redux/`

This pattern fits especially well with the new UI module system, where each module can own its own reducers, middleware, and API clients.

## Recommended Location in Module-Based UIs

Place entity APIs under:

- `solid-ui/src/<module-name>/redux/`

Then register the generated reducer and middleware through:

- `solid-ui/src/<module-name>/<module-name>.ui-module.ts`

See also: [Redux Module Integration](./redux-module-integration.md)

## Factory Overview

```ts
export const createSolidEntityApi = (entityName: string) => {
  const kebabEntityName = kebabCase(entityName);

  return createApi({
    reducerPath: `genericSolid${entityName}Api`,
    baseQuery: baseQueryWithAuth,
    tagTypes: [entityName],
    endpoints: (builder) => ({
      getSolidEntities: builder.query({}),
      getSolidEntityById: builder.query({}),
      createSolidEntity: builder.mutation({}),
      updateSolidEntity: builder.mutation({}),
      patchUpdateSolidEntity: builder.mutation({}),
      deleteSolidEntity: builder.mutation({}),
      deleteMultipleSolidEntities: builder.mutation({}),
      recoverSolidEntity: builder.mutation({}),
      recoverSolidEntityById: builder.query({}),
    }),
  });
};
```

## Endpoints and Semantics

### `getSolidEntities`

- method: GET
- use for list fetches, pagination, filtering, sorting, and grouping
- cache key is based on the query argument, typically the serialized query string

### `getSolidEntityById`

- method: GET
- use for entity detail fetches by ID

### Mutations

Mutations invalidate the relevant RTK Query tags so detail and list queries refresh automatically.

- `createSolidEntity`
- `updateSolidEntity`
- `patchUpdateSolidEntity`
- `deleteSolidEntity`
- `deleteMultipleSolidEntities`
- `recoverSolidEntity`
- `recoverSolidEntityById`

## Building Query Strings

Recommended serialization:

```ts
import qs from "qs";

const queryData = {
  limit: 10,
  offset: 0,
  filters: { status: { $eq: "active" } },
};

const queryString = qs.stringify(queryData, { encodeValuesOnly: true });
```

## Hook Usage Examples

### Find many

```tsx
const qsValue = useMemo(() => qs.stringify(filtersObj, { encodeValuesOnly: true }), [filtersObj]);
const { data, isLoading, isFetching, refetch } = useGetSolidEntitiesQuery(qsValue);
```

### Conditional fetch

```tsx
const { data } = useGetSolidEntitiesQuery(qsValue, { skip: !qsValue });
```

### Lazy fetch

```tsx
const [trigger, { data, isFetching }] = useLazyGetSolidEntitiesQuery();
```

### Mutations

```tsx
const [createEntity] = useCreateSolidEntityMutation();
await createEntity(payload);
```

## When To Use It

Use Solid Entity API when:

- your use case matches standard entity list and detail patterns
- you want caching and invalidation automatically handled by RTK Query
- the module benefits from shared API state

Prefer direct HTTP helpers when the workflow is custom, multi-step, or not entity-shaped. See [Solid HTTP API](./solid-http-api.md).

## Best Practices

- keep serialization stable so cache keys remain predictable
- use `LIST` invalidation for collection refreshes
- invalidate both record and list tags on update or delete
- keep generated APIs close to the owning module

## Related

- [Redux Module Integration](./redux-module-integration.md)
- [Solid HTTP API](./solid-http-api.md)
- [Bespoke Frontend](./bespoke-frontend-ui.md)

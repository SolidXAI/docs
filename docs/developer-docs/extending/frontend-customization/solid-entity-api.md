---
sidebar_position: 7
title: Solid Entity API
description: Learn how to use the Solid Entity API to interact with entities in your application.
summary: Guide to using the Solid Entity API for managing entities in SolidX applications. Covers importing and using the `SolidEntityApi` class, performing CRUD operations (create, read, update, delete), querying entities with filters, and handling relationships between entities. Includes code examples for common operations and best practices for effective entity management.
solidx_concerns: [frontend.custom_pages, add_full_custom_ui]
---

## Overview

This generic Solid Entity API factory (`createSolidEntityApi`) provides a single, consistent surface for common CRUD operations across "entities" in SolidX applications.  
Goals:

- Keep API layer DRY by generating endpoints for common patterns (find many, find one, create, update, delete, recover, patch).
- Standardize caching and invalidation using RTK Query `providesTags` / `invalidatesTags`.
- Allow flexible server-side filtering via query-string filters while keeping a simple client-side hook surface.
- Make it easy to plug into frontends (React + RTK Query) with clear patterns for eager vs lazy fetching, conditional fetch, and refetch control.

## Factory overview (reference)

```ts
export const createSolidEntityApi = (entityName: string) => {
  const kebabEntityName = kebabCase(entityName);

  return createApi({
    reducerPath: `genericSolid${entityName}Api`,
    baseQuery: baseQueryWithAuth,
    tagTypes: [entityName],
    endpoints: (builder) => ({
      getSolidEntities: builder.query({...}),
      getSolidEntityById: builder.query({...}),
      createSolidEntity: builder.mutation({...}),
      updateSolidEntity: builder.mutation({...}),
      patchUpdateSolidEntity: builder.mutation({...}),
      deleteSolidEntity: builder.mutation({...}),
      deleteMultipleSolidEntities: builder.mutation({...}),
      recoverSolidEntity: builder.mutation({...}),
      recoverSolidEntityById: builder.query({...}),
    }),
  });
};
```

> The actual implementation used in the project defines `providesTags` for read endpoints and `invalidatesTags` for mutations to ensure automatic refetches of affected queries.

## Endpoints and semantics

### `getSolidEntities` — find many
- **Method:** GET  
- **Path:** `/${kebabEntityName}?${qs}`  
- **Returns:** `{ records: any[], meta: object, groupMeta?: any, groupRecords?: any[] }`  
- **Provides tags:** `[{ type: entityName, id: record.id }, { type: entityName, id: 'LIST' }]` for each record and a LIST tag.

**Use-cases:**
- Listing, table/grid data.
- Paginated requests using `offset` and `limit`.
- Complex server-side filtering using `filters[...]` query string structure.
- Sorting, selecting fields, populating relations, grouping.

**Important:** caching is keyed by the query string argument — identical `qs` (string) → same cache entry.

### `getSolidEntityById` — find one
- **Method:** GET  
- **Path:** `/${kebabEntityName}/${id}?${qs}`  
- **Provides tags:** `{ type: entityName, id }`

**Use-cases:**
- Detail view for a single resource.
- Fetch by id with optional `qs` to control fields/populates.

### Create / Update / Patch / Delete / Recover
Mutations are implemented with appropriate HTTP methods and `invalidatesTags` so that after a successful mutation, relevant cached queries are invalidated and refetched automatically.

- `createSolidEntity` — `POST /${kebabEntityName}` → `invalidatesTags: [{ type: entityName, id: 'LIST' }]`
- `updateSolidEntity` — `PUT /${kebabEntityName}/${id}` → invalidates the record id and `LIST`
- `patchUpdateSolidEntity` — `PATCH /${kebabEntityName}/${id}` → invalidates the record id and `LIST`
- `deleteSolidEntity` — `DELETE /${kebabEntityName}/${id}` → invalidates the record id and `LIST`
- `deleteMultipleSolidEntities` — `DELETE /${kebabEntityName}/bulk/` → invalidates `LIST`
- `recoverSolidEntity` — `POST /${kebabEntityName}/bulk-recover/` → invalidates `LIST`
- `recoverSolidEntityById` — `GET /${kebabEntityName}/recover/${id}` → provides tag for id

## How caching and invalidation work (quick primer)
- RTK Query caches each **query by its argument** (here typically the `qs` string or `{ id, qs }`).
- `providesTags` tells RTK Query **what tags** the data corresponds to.
- `invalidatesTags` in mutations tells RTK Query to mark those tags stale and **auto-refetch** related queries.
- By default, when a cached query has **no active subscribers**, RTK Query keeps it for `keepUnusedDataFor` seconds (default: 60). You can override this globally or per-endpoint.
- If a component remounts **before** the `keepUnusedDataFor` timer expires, RTK Query **reuses cached data instantly** (no network request) unless `refetchOnMountOrArgChange` is configured.

### Building the query string

**Recommended serialization:**
```ts
import qs from 'qs';

const queryData = {
  limit: 10,
  offset: 0,
  filters: { status: { $eq: 'active' } },
};

const queryString = qs.stringify(queryData, { encodeValuesOnly: true });
// pass queryString to the hook: useGetSolidEntitiesQuery(queryString);
```

> Using `encodeValuesOnly: true` keeps keys readable (`filters[name][$eq]=John`) while properly encoding values. 

#### Further References
- For comprehensive filtering syntax, see the [Retrieve API Filters documentation](../../rest-apis/retrieve/index.md).

## Hook usage examples (React + RTK Query)

Assume `const api = createSolidEntityApi('Person')` and hooks are exported like:
```ts
const {
  useGetSolidEntitiesQuery,
  useLazyGetSolidEntitiesQuery,
  useGetSolidEntityByIdQuery,
  useLazyGetSolidEntityByIdQuery,
  useCreateSolidEntityMutation,
  useUpdateSolidEntityMutation,
  // ...
} = api;
```

### 1) Find many — automatic fetch (eager)
```tsx
function PersonList({ filtersObj }) {
  const qs = useMemo(() => qs.stringify(filtersObj, { encodeValuesOnly: true }), [filtersObj]);
  const { data, isLoading, isFetching, refetch } = useGetSolidEntitiesQuery(qs);

  // data.records, data.meta
  return <List ... />;
}
```

### 2) Find many — conditional (skip when filters not ready)
```tsx
const { data } = useGetSolidEntitiesQuery(qs, { skip: !qs });
```

### 3) Find many — lazy (on-demand fetch, e.g., on search button)
```tsx
const [trigger, { data, isFetching }] = useLazyGetSolidEntitiesQuery();
<button onClick={() => trigger(qs)}>Search</button>
```

### 4) Find one — eager
```tsx
const { data } = useGetSolidEntityByIdQuery({ id, qs });
```

### 5) Find one — lazy
```tsx
const [trigger, { data }] = useLazyGetSolidEntityByIdQuery();
<button onClick={() => trigger({ id, qs })}>Load</button>
```

### 6) Create / Update / Delete
```tsx
const [createEntity] = useCreateSolidEntityMutation();
await createEntity(payload); // invalidates LIST -> causes getSolidEntities to refetch

const [updateEntity] = useUpdateSolidEntityMutation();
await updateEntity({ id, data }); // invalidates id and LIST

const [deleteEntity] = useDeleteSolidEntityMutation();
await deleteEntity(id); // invalidates id and LIST
```



## When to use `useGet` vs `useLazyGet`

**`useGetXQuery` (eager)** — Use when:
- You want the data to be fetched automatically when the component mounts.
- The query args (e.g., `qs` or `id`) are available synchronously on mount.
- You want built-in re-fetch strategies (on focus, reconnect, arg change).

**`useLazyGetXQuery` (manual)** — Use when:
- You need to fetch **on demand** (e.g., user presses "Search", or a form submits).
- You don’t have query args at mount time and don’t want to use `skip`.
- You want full programmatic control over when the request happens.

**Important: never conditionally call hooks.** Use `skip` option or lazy hooks to control whether the fetch runs.

**Examples:**
- If you only fetch after user input and want simple UX: `useLazyGetSolidEntitiesQuery()` + `trigger(qs)`.
- If you want to mount and auto fetch when `id` becomes available, prefer:
  ```ts
  useGetSolidEntityByIdQuery({ id, qs }, { skip: !id });
  ```



## Intricacies & best practices

- **Stable serialization is crucial:** Because RTK Query keys are based on the hook arguments, different string ordering produces different cache entries. Use `qs.stringify` with deterministic options.
- **Prefer the `LIST` tag for collection invalidation:** Your factory tags the list with `id: 'LIST'` so writes that change the list can invalidate and refetch the collection view.
- **Invalidate both id + LIST on update/delete:** This removes stale record pages and refreshes lists that may be affected.
- **`keepUnusedDataFor` behavior:** If components unmount and remount within `keepUnusedDataFor` window, cached data is reused. Change the value if you need shorter/longer retention.
- **Refetch behavior on mount:** `refetchOnMountOrArgChange: 'always' | true | false` controls whether cached data is revalidated on remount. Default is `false` (no refetch).
- **Paged requests:** Ensure pagination params (`offset`, `limit`) are part of the `qs` argument so different pages are cached separately.
- **Soft-deleted data:** Use `showSoftDeleted` option to include soft-deleted records when needed.



## Examples: Typical flows

### Create -> Auto refresh list
1. User opens list page => `useGetSolidEntitiesQuery(qs)` runs and shows cached or fetched data.
2. User creates a new entity using `createSolidEntity` mutation.
3. `invalidatesTags: [{ type: 'Person', id: 'LIST' }]` triggers a refetch of `getSolidEntities`.

### Update detail -> Auto refresh detail & list
1. User opens detail page => `useGetSolidEntityByIdQuery({ id, qs })`.
2. User edits and `updateSolidEntity({ id, data })`.
3. `invalidatesTags` includes both the `{ id }` and `{ id: 'LIST' }` tags so both detail and collection views are refreshed.



## Troubleshooting

- **Cache misses unexpectedly**: Check your `qs` serialization. Non-deterministic ordering or extra whitespace changes the key.
- **Queries not refetching after mutation**: Verify `invalidatesTags` returns the correct tag shape and your `tagTypes` includes the entity type.
- **Hook errors about conditional calls**: Ensure hooks are called unconditionally; use `skip` or lazy hooks instead.
- **Data seems stale**: Consider `refetchOnFocus`, `refetchOnReconnect`, or lower `keepUnusedDataFor`.



## Summary (cheat sheet)
- Use `useGet...Query(arg)` for automatic fetch; use `useLazy...Query()` + `trigger(arg)` for manual fetch.
- Build deterministic `qs` strings for caching.

### Appendix: Quick copy-paste examples

**List hook (eager):**
```tsx
const qs = qs.stringify({ offset: 0, limit: 10 }, { encode: false, arrayFormat: 'brackets' });
const { data } = useGetSolidEntitiesQuery(qs);
```

**Get by id (eager):**
```tsx
const { data } = useGetSolidEntityByIdQuery({ id: 12, qs: qs.stringify({ fields: ['id','name'] }) });
```

**Triggering lazy search:**
```tsx
const [trigger] = useLazyGetSolidEntitiesQuery();
<button onClick={() => trigger(qs)}>Search</button>
```

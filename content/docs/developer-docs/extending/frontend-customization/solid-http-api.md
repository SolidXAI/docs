---
title: Solid HTTP API
icon: "globe"
description: Learn how to use the Solid HTTP API helpers to interact with backend APIs in your application.
summary: "Guide to using the `solidAxios` HTTP helpers in SolidX applications. Covers importing and using `solidGet`, `solidPost`, `solidPut`, `solidPatch`, and `solidDelete`, building filter query strings, handling loading and errors, and where these helpers fit in the UI module system."
solidx_concerns: [frontend.custom_pages, add_full_custom_ui]
---

## Overview

The Solid HTTP API helpers provide a lightweight way to call backend APIs from custom frontend code.

Use them when you want:

- direct promise-based API calls
- full control over when requests run
- custom workflows that do not fit a generated entity API pattern

These helpers are commonly used from:

- extension components in `admin-layout`
- handler logic in `extension-functions`
- bespoke route UIs in `custom-layout`

## Helper Overview

```ts
import { solidAxios, solidGet, solidPost, solidPut, solidPatch, solidDelete } from "@solidxai/core-ui";
```

`solidAxios` is a preconfigured Axios instance that:

- uses the configured backend base URL
- attaches the access token from session when available
- emits global error events on network errors or server failures
- normalizes accidental `/api` prefixes in request paths

Convenience exports:

- `solidGet`
- `solidPost`
- `solidPut`
- `solidPatch`
- `solidDelete`

## Methods and Semantics

### `solidGet`

Use for reads such as list fetches, detail fetches, or lookup requests.

### `solidPost`

Use for creates, custom actions, or trigger endpoints.

### `solidPut` and `solidPatch`

Use for full or partial updates.

### `solidDelete`

Use for deletes or delete-like custom endpoints.

## Building Query Strings and Filters

You can either build a query string manually:

```ts
import qs from "qs";

const query = qs.stringify(
  {
    offset: 0,
    limit: 10,
    filters: { status: { $eq: "active" } },
  },
  { encodeValuesOnly: true }
);

const resp = await solidGet(`/application-master?${query}`);
```

or pass `params` through Axios config:

```ts
const resp = await solidGet("/employee", {
  params: {
    filters: { Is_Account_Person: { $eq: true } },
    limit: 500,
  },
});
```

## Usage Patterns

### Fetch on mount

```tsx
const [loading, setLoading] = useState(false);
const [records, setRecords] = useState<any[]>([]);

useEffect(() => {
  let alive = true;

  const run = async () => {
    setLoading(true);
    try {
      const resp = await solidGet("/payment-otp-payment-reason-vtb");
      if (alive) setRecords(resp?.data?.data?.records || []);
    } finally {
      if (alive) setLoading(false);
    }
  };

  run();
  return () => {
    alive = false;
  };
}, []);
```

### On-demand fetch

```tsx
const onSearch = async (qsValue: string) => {
  const resp = await solidGet(`/application-master?${qsValue}`);
  setData(resp.data?.data);
};
```

### Mutation flow

```tsx
const onSave = async () => {
  try {
    const resp = await solidPost("/application-master/change-status", payload);
    showToast("success", "Success", resp.data?.message || "Saved");
  } catch (error: any) {
    showToast("error", "Error", error?.response?.data?.message || "Save failed");
  }
};
```

## Solid Entity API vs Solid HTTP API

Use **Solid Entity API** when:

- you want generated CRUD hooks with RTK Query caching and auto-refetch
- your use case matches standard entity list or detail patterns
- you want module-owned reducers and middleware under `redux/`

Use **Solid HTTP API** when:

- you need custom multi-step workflows or action endpoints
- you want direct promise-based control in component logic
- you are building one-off integration logic in widgets, buttons, dialogs, or bespoke route UIs

Both patterns are supported in the same app. This is a structural choice, not a framework limitation.

## Best Practices

- handle loading and errors explicitly
- use `qs.stringify(..., { encodeValuesOnly: true })` for filter-heavy endpoints
- prefer context-derived IDs over hardcoded values
- remember there is no automatic cache invalidation; manually refresh where needed

## Related

- [Solid Entity API](./solid-entity-api.md)
- [Redux Module Integration](./redux-module-integration.md)
- [Bespoke Frontend](./bespoke-frontend-ui.md)

---
sidebar_position: 9
title: Solid HTTP API
description: Learn how to use the Solid HTTP API helpers to interact with backend APIs in your application.
summary: Guide to using the `solidAxios` HTTP helpers in SolidX applications. Covers importing and using `solidGet`, `solidPost`, `solidPut`, `solidPatch`, and `solidDelete`, building filter query strings, handling loading and errors, and implementing multi-step API flows in custom frontend components.
solidx_concerns: [add_full_custom_ui,onlayoutload_handler_function,ondataload_handler_function,add_form_button,add_list_header_button_with,add_list_row_button_with,create_custom_form_field_widget,create_custom_list_field_widget]
---

## Overview

The Solid HTTP API helpers (`solidAxios`, `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`) provide a lightweight way to call backend APIs from custom frontend code.

Goals:

- Keep API calls simple for custom widgets, form buttons, dialogs, and other UI extensions.
- Reuse one preconfigured Axios client for auth token handling and base URL configuration.
- Support custom request flows that do not fit a generated entity API pattern.
- Give full control over when and how requests run (manual fetch, chained requests, custom payload shaping).

## Helper overview (reference)

```ts
import { solidAxios, solidGet, solidPost, solidPut, solidPatch, solidDelete } from "@solidxai/core-ui";
```

`solidAxios` is a preconfigured Axios instance that:

- Uses `NEXT_PUBLIC_BACKEND_API_URL + "/api"` as `baseURL`.
- Injects `Authorization: Bearer <accessToken>` from `getSession()` on each request (when available).
- Emits a global error event (`AppEvents.GlobalError`) on network errors or 5xx responses.
- Normalizes URLs that accidentally start with `/api` so you can consistently call endpoints like `/application-master`.

Convenience exports:

- `solidGet = solidAxios.get`
- `solidPost = solidAxios.post`
- `solidPut = solidAxios.put`
- `solidPatch = solidAxios.patch`
- `solidDelete = solidAxios.delete`

## Methods and semantics

### `solidGet` — read data
- **Method:** GET
- **Typical use:** list fetches, by-id fetches, dropdown options, metadata lookups
- **Examples:**
  - `solidGet("/application-master/98")`
  - `solidGet("/employee", { params: { filters: { Is_Account_Person: { $eq: true } }, limit: 500 } })`

### `solidPost` — create / trigger custom actions
- **Method:** POST
- **Typical use:** create records, submit action payloads, custom backend workflows
- **Example:** `solidPost("/application-master/change-status", payload)`

### `solidPut` / `solidPatch` — update data
- **Method:** PUT / PATCH
- **Typical use:** full update (`PUT`) or partial update (`PATCH`)
- **Examples:**
  - `solidPut("/application-master/98", data)`
  - `solidPatch("/application-master/98", { paymentStatus: "Cleared" })`

### `solidDelete` — delete data
- **Method:** DELETE
- **Typical use:** remove records or call delete endpoints
- **Example:** `solidDelete("/application-master/98")`

## Building query strings and filters

You can pass filters in either of these ways:

1. Build a query string manually (useful when endpoint expects `filters[...]` format):

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

2. Pass `params` through Axios config:

```ts
const resp = await solidGet("/employee", {
  params: {
    filters: { Is_Account_Person: { $eq: true } },
    limit: 500,
  },
});
```

#### Further References
- For comprehensive filtering syntax, see the [Retrieve API Filters documentation](../../rest-apis/retrieve/index.md).

## Usage patterns (React)

Unlike RTK Query hooks, Solid HTTP helpers are promise-based and manual. You control loading state, errors, and when requests run.

### 1) Fetch on mount with local loading state

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

### 2) On-demand fetch (button/search triggered)

```tsx
const [data, setData] = useState<any>(null);
const [loading, setLoading] = useState(false);

const onSearch = async (qs: string) => {
  setLoading(true);
  try {
    const resp = await solidGet(`/application-master?${qs}`);
    setData(resp.data?.data);
  } finally {
    setLoading(false);
  }
};
```

### 3) Mutation flow with success/error handling

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

## Example: Chained API flow (custom field widget)

A common pattern is to call multiple endpoints in sequence, then map the final response into dropdown options:

1. Fetch parent record (example: application).
2. Fetch related entity info (example: business entity details).
3. Build payload using values from prior responses.
4. Call a custom options endpoint and set dropdown options.

This is a good fit for `solidGet` + `solidPost` because the flow is custom and context-dependent.

## Solid Entity API vs Solid HTTP API

Use **Solid Entity API** when:

- You want generated CRUD hooks with RTK Query caching and auto-refetch behavior.
- Your use case matches standard entity list/detail/mutation patterns.

Use **Solid HTTP API** when:

- You need custom multi-step workflows, action endpoints, or non-standard payloads.
- You want direct promise-based control in custom React logic.
- You are building one-off integration logic in widgets/buttons/dialogs.

You can use both together in the same app.

## Intricacies & best practices

- **Always handle loading and errors explicitly:** these helpers do not manage UI state for you.
- **Use `qs.stringify(..., { encodeValuesOnly: true })` for filter-heavy endpoints.**
- **Avoid hardcoded IDs where possible:** prefer `formik.values`, route params, or context data.
- **Reuse helper functions for chained flows:** split API calls into small composable functions.
- **Use Axios config when needed:** headers, params, timeout, and cancel behavior can be passed as the third argument (or second for GET/DELETE).
- **Remember there is no automatic cache invalidation:** if data changed, manually refetch the relevant data.

## Troubleshooting

- **401/403 issues:** verify session exists and token is valid; `solidAxios` only attaches token when session contains `accessToken`.
- **Unexpected 404 with `/api/...` paths:** pass paths like `/resource`; helper already uses `/api` base URL.
- **No automatic UI refresh after save/delete:** call your own `refreshData()` or re-fetch function.
- **Global error banner appears on server/network failures:** this comes from the built-in response interceptor (`AppEvents.GlobalError`).

## Summary (cheat sheet)

- Import from `@solidxai/core-ui`: `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`.
- Use for custom, manual API workflows in frontend extensions.
- Manage loading/error/refetch in component state.
- Use `qs` or Axios `params` for filterable list endpoints.

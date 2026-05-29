---
title: API Testing
icon: "code"
description: Metadata-driven API testing support in SolidX, including steps, auth flow, assertions, and typical patterns.
---

# API Testing

SolidX supports automated API testing through the shared testing engine and the API adapter.

API scenarios are a strong fit when you want:

- fast feedback,
- direct backend verification,
- stable automation that does not depend on browser rendering,
- and easy chaining of response-driven workflows.

## How API Testing Works

At runtime:

1. the runner loads `api` or `mixed` scenarios from metadata
2. API steps are registered into the step registry
3. the API adapter executes HTTP requests
4. responses are stored into the runtime context
5. follow-up assertions or dependent steps use those results

This makes API testing a first-class part of the same metadata-driven system used for UI testing.

## Core API Operations

### `api.request`

This is the main HTTP execution primitive.

Use it for:

- `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- JSON requests
- query parameter requests
- plain text bodies
- multipart/form-data uploads

Typical `with` fields:

- `method`
- `url`
- `headers`
- `json`
- `bodyText`
- `query`
- `formData`

The step returns:

- `status`
- `headers`
- `bodyText`
- `bodyJson` when the response is JSON
- `body` as a convenience alias

It also updates the last API response in the runtime context, which is useful for follow-up assertions.

### Authentication

The standard pattern for authenticated scenarios is to POST to `/api/iam/authenticate` using `api.request`, save the full response as `loginSuccess`, and let all dependent scenarios read the token from there.

```json
{
  "given": {
    "op": "api.request",
    "with": {
      "method": "POST",
      "url": "${env:TEST_API_BASE_URL}/api/iam/authenticate",
      "json": {
        "email": "libTestEditor@test.local",
        "username": "",
        "password": "Test@1234"
      }
    },
    "saveAs": "loginSuccess"
  }
}
```

Dependent scenarios start with `util.require` to guard the resource, then read the token via `${res:loginSuccess.bodyJson.data.accessToken}`.

## Assertions Commonly Used With API Steps

### `assert.httpStatus`

Checks the HTTP status of the last API response, or a supplied response.

This is one of the most common API assertions.

### `assert.equals`

Use when you want strict equality between actual and expected values.

### `assert.contains`

Use when you expect one string value to contain another.

### `assert.matches`

Use when you want regex-based matching.

### `assert.jsonPath`

Use when you want to extract and assert a nested JSON value from a response payload.

This is especially useful for asserting response content without needing a custom test spec.

## Typical API Testing Pattern

A common API scenario pattern looks like this:

1. authenticate and save a bearer token
2. create or fetch a resource
3. assert the status
4. save an id or response body
5. make a follow-up request using the saved values
6. assert business behaviour

The `venue` module follows this pattern directly:

- `api-authenticate-success` creates a reusable login response
- later scenarios begin with `util.require` to assert that bootstrap resource exists
- authenticated requests read the token via `${res:loginSuccess.bodyJson.data.accessToken}`
- request bodies are often sourced from `testing.data`

## Example Flow

The bootstrap scenario authenticates and saves `loginSuccess`. All dependent scenarios use `util.require` to guard it, then read the token from the saved response.

**Bootstrap:**

```json
{
  "id": "api-authenticate-success",
  "type": "api",
  "tags": ["smoke"],
  "steps": [
    {
      "given": {
        "op": "api.request",
        "with": {
          "method": "POST",
          "url": "${env:TEST_API_BASE_URL}/api/iam/authenticate",
          "json": {
            "email": "libTestEditor@test.local",
            "username": "",
            "password": "Test@1234"
          }
        },
        "saveAs": "loginSuccess"
      }
    },
    { "then": { "op": "assert.httpStatus", "with": { "is": 200 } } },
    { "and": { "op": "assert.contains", "with": { "actual": "${res:loginSuccess.bodyText}", "expected": "accessToken" } } }
  ]
}
```

**Dependent scenario:**

```json
{
  "id": "api-create-example",
  "type": "api",
  "steps": [
    {
      "given": {
        "op": "util.require",
        "with": { "resource": "loginSuccess" }
      }
    },
    {
      "when": {
        "op": "api.request",
        "with": {
          "method": "POST",
          "url": "${env:TEST_API_BASE_URL}/api/example",
          "headers": {
            "Authorization": "Bearer ${res:loginSuccess.bodyJson.data.accessToken}"
          },
          "json": { "name": "Example" }
        },
        "saveAs": "example.create"
      }
    },
    {
      "then": {
        "op": "assert.httpStatus",
        "with": { "is": 201 }
      }
    }
  ]
}
```

## Multipart and File Upload Testing

`api.request` also supports multipart form submission.

This is useful for:

- media upload testing,
- APIs that mix files and text fields,
- metadata-driven creation flows that expect file attachments.

SolidX supports file values such as:

- `file:/absolute/path`
- `url:https://...`

This makes API automation practical even for file-heavy workflows.

The `venue` module demonstrates two strong real-world patterns here:

- create a lead with `formData: "${data:lead[\"LeadWithFile\"]._rec}"`
- create a hierarchy import transaction with `formData: "${data:hierarchyImportTransaction[\"HierarchyImportSample\"]._rec}"`

This is a good pattern because file-heavy payloads stay in `testing.data`, while scenarios remain short and focused.

## Query Filter Testing

The `venue` module also shows that SolidX API tests are a good fit for verifying query semantics on list endpoints.

Patterns covered there include:

- equality filters with `$eq`
- case-insensitive prefix filters with `$startsWithi`
- nested relation filters
- `$or` combinations
- `$and` combinations

A representative pattern looks like this:

```json
{
  "when": {
    "op": "api.request",
    "with": {
      "method": "GET",
      "url": "${env:TEST_API_BASE_URL}/api/state-master",
      "headers": {
        "Authorization": "Bearer ${res:loginSuccess.bodyJson.data.accessToken}"
      },
      "query": {
        "filters": {
          "name": {
            "$eq": "${data:stateMaster[\"Maharashtra\"].name}"
          }
        }
      }
    }
  }
}
```

## Good API Testing Practices

Recommended practices:

- prefer API tests for backend-heavy business logic
- keep auth setup reusable through `saveAs`
- assert both status and response payload shape
- use `assert.jsonPath` when validating nested response data
- keep scenarios independent when possible
- use test data fixtures instead of embedding large payloads in every scenario
- create one reusable authentication bootstrap scenario per module when most API scenarios need auth
- use `util.require` when a scenario intentionally depends on a previously saved auth or setup resource
- use metadata fixtures for expected values in query assertions so payloads and expectations stay aligned

## When To Prefer API Tests

Prefer API testing when:

- you are validating service behaviour, not browser behaviour
- you want fast smoke or regression coverage
- the UI is not important to the specific risk you are testing
- data setup and response assertions are the main concern

Next: [UI Testing](./ui-testing.md)

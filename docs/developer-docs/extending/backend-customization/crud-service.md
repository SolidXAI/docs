---
sidebar_position: 3
title: CRUD Service
description: Learn how to create and customize CRUD services in your application.
summary: Guide to creating and customizing CRUD services in SolidX applications for managing data layer operations, including methods for create, read, update, and delete functionality with business logic integration.
keywords: [backend, services, CRUD, customization]
solidx_concerns: [using_crud_service_method, add_custom_service_method, add_controller_endpoint]
---

# CRUD Service — Usage & Extension Guide

The **CRUD Service** is the backbone of data management in **SolidX**. It standardizes Create, Read, Update, and Delete operations for any model and adds niceties like permission checks, field-level validation/transformations, media handling, and soft-delete recovery.

This document explains how to **extend** the `CRUDService<T>` for your models and how **clients** (controllers, other services) can call each **public API**. Every section first **explains what the example demonstrates**, followed by a **collapsible code block** you can copy‑paste.

> The generated service classes for SolidX models already extend the CRUD service. You can also extend it manually for your own modules.

---

## What You Get Out‑of‑the‑Box

- **Public API** (available on any subclass):  
  - `create(createDto, files?, context?)` — create a record  
  - `update(id, updateDto, files?, isPartial?, context?)` — update/patch a record  
  - `delete(id, context?)` — delete (soft/hard based on model)  
  - `find(filterDto, context?)` — list with filters, pagination, grouping  
  - `findOne(id, query, context?)` — fetch 1 by id, with relations/media  
  - `insertMany(createDtos, filesArray?, context?)` — bulk insert  
  - `deleteMany(ids, context?)` — bulk delete  
  - `recover(id, context?)` — unarchive a soft-deleted row  
  - `recoverMany(ids, context?)` — bulk unarchive

- **Metadata‑driven** field managers (validation + transformation per field type)  
- **Media** storage/retrieval for `mediaSingle` / `mediaMultiple` fields  
- **Computed fields** & **relations** handled consistently  
- **Soft delete** & **recovery** flows supported  
- **Permission checks** via `CrudHelperService`

---

## Extending the CRUD Service

**What this shows:** How to define a model‑specific service (e.g., `PersonService`) that **inherits** all CRUD methods and optionally adds custom methods like `findByEmail`. You typically inject this service into a controller to expose REST endpoints.

<details open>
<summary>Show example</summary>

```ts
import { Injectable } from "@nestjs/common";
import { CRUDService } from "@solidxai/core";
import { Person } from "../entities/person.entity";

@Injectable()
export class PersonService extends CRUDService<Person> {

  constructor(
    readonly modelMetadataService: ModelMetadataService,
    readonly moduleMetadataService: ModuleMetadataService,
    readonly configService: ConfigService,
    readonly fileService: FileService,
    readonly discoveryService: DiscoveryService,
    readonly crudHelperService: CrudHelperService,
    @InjectEntityManager()
    readonly entityManager: EntityManager,
    readonly repo: PersonRepository,
    readonly moduleRef: ModuleRef,
  ) {
    super(
      modelMetadataService,
      moduleMetadataService,
      configService,
      fileService,
      discoveryService,
      crudHelperService,
      entityManager,
      repo,
      "person",
      "myModule",
      moduleRef
    );
  }

  // Add your custom application logic here (optional)
  async findByEmail(email: string) {
    return this.repo.findOne({ where: { email } });
  }
}
```
</details>

> Any subclass automatically inherits all CRUD methods and can call `this.repo`, `this.entityManager`, etc.

---

## DTOs You’ll Use When Reading

**What this shows:** The shape of pagination & filtering DTOs your **clients** pass to `find`/`findOne`. You can extend or narrow these DTOs in your own app, but the base service already understands them via `CrudHelperService`.

### `PaginationQueryDto`

<details open>
<summary>Show example</summary>

```ts
limit?: number = 10;
offset?: number = 0;
filters?: Record<string, any>;
```
</details>

### `BasicFilterDto` (extends `PaginationQueryDto`)

<details open>
<summary>Show example</summary>

```ts
fields?: string[];
sort?: string[];
groupBy?: string[];
populate?: string[];
populateMedia?: string[];
showSoftDeleted?: "inclusive" | "exclusive";
populateGroup?: boolean;
groupFilter?: BasicFilterDto;
locale?: string;
status?: string; // publish | draft (when draft/publish workflow is enabled)
```
</details>

---

## Permissions & Context

**Note:** The optional `context` parameter accepts an **ActiveUser** object. It is generally auto‑populated by controllers from the request context to perform permission checks for the logged‑in user before CRUD operations. If you call service methods manually, `context` is optional.

<details open>
<summary>ActiveUser shape</summary>

```ts
export interface ActiveUserData {
  /**
   * The "subject" of the token. The value of this property is the user ID
   * that granted this token.
   */
  sub: number;

  /**
   * The subject's (user) username.
   */
  username: string;

  /**
   * The subject's (user) email.
   */
  email: string;

  /**
   * The subject's (user) roles.
   * These are part of the JWT token, we simply decode them.
   */
  roles: string[];

  /**
   * The subject's (user) permissions.
   * These are not part of the JWT token, we query them from the database each time the access-token guard is run. 
   * So basically each time an authenticated request is initiated, we end up loading all the users permissions.
   */
  permissions: string[];
}
```
</details>

---

## CrudService API (with Examples )

Below are **explained** examples for each method. Read the **explanation** first, then expand the **closeable** snippet.

### 1) `create(createDto, files?, context?)`

**What this shows:** How to create an entity, including optional media uploads (`files`). Field managers validate & transform values (e.g., hashing passwords, enforcing regex/length).

<details open>
<summary>Show code</summary>

```ts
// In your controller or another service
await personService.create(
  {
    name: "Jane Doe",
    email: "jane@example.com",
    // For relations: use IDs or shapes accepted by field managers
    // For media: will be taken from `files` below
  },
  [
    // Express.Multer.File[] — optional
    // { fieldname: "fileLocation", ... }, // example media field (mediaSingle)
  ]
  // context is optional when calling manually
);
```
</details>

---

### 2) `update(id, updateDto, files?, isPartial?, context?)`

**What this shows:** How to update an entity by ID. Set `isPartial = true` for PATCH‑style updates; leave it `false` (default) for PUT‑style behavior. Media updates can be supplied via `files` when your model has media fields.

<details open>
<summary>Show code</summary>

```ts
await personService.update(
  12,
  {
    name: "Jane D.",
    // Partial fields are OK when isPartial = true
  },
  [],         // files (optional)
  true        // isPartial (PATCH-like)
  // context optional
);
```
</details>

---

### 3) `delete(id, context?)`

**What this shows:** How to delete a record. If your model has soft delete enabled, the row is archived instead of hard‑removed.

<details open>
<summary>Show code</summary>

```ts
await personService.delete(12 /*, context? */);
```
</details>

---

### 4) `find(filterDto, context?)`

**What this shows:** How to list entities with pagination, selective fields, relation population, media population, sorting, grouping, and optional filter expressions. The return value includes a `meta` block with paging info.

> For the full list of filter operators and examples, see the [Filtering Data](/recipes/filtering) recipe.

<details open>
<summary>Show code</summary>

```ts
const result = await personService.find(
  {
    limit: 10,
    offset: 0,
    // Select only a few columns
    fields: ["id", "name", "email"],
    // Populate TypeORM relations (e.g., "department", "roles.permissions")
    populate: ["department", "roles.permissions"],
    // Include media-derived URLs under `_media`
    populateMedia: ["fileLocation", "attachments"],
    // Sort (ASC by default; use "-" prefix for DESC, depending on your CrudHelperService’s convention)
    sort: ["name"],
    // Optional grouping — returns meta per group and groupRecords if populateGroup=true
    groupBy: [],
    populateGroup: false,
    // Optional filters payload interpreted by your CrudHelperService
    filters: {
      email: { $ilike: "%@example.com" },
      status: { $eq: "active" }
    },
    // Include soft-deleted rows too
    showSoftDeleted: "inclusive"
  }
);

console.log(result.meta);     // { totalRecords, currentPage, totalPages, ... }
console.log(result.records);  // Entity[] with optional `_media` key added
```
</details>

---

### 5) `findOne(id, query, context?)`

**What this shows:** How to fetch one entity by ID with relations populated and media URLs resolved into the non-persistent `_media` key.

> The `query` parameter accepts the same filter syntax as `find()`. See the [Filtering Data](/recipes/filtering) recipe for all available operators.

<details open>
<summary>Show code</summary>

```ts
const entity = await personService.findOne(
  12,
  {
    // Load relations
    populate: ["department", "manager"],
    // Only select a few columns (applies to the root entity)
    fields: ["id", "name", "email"],
    // Also resolve media full URLs into `_media`
    populateMedia: ["fileLocation", "certifications.scan"]
  }
);

// Access media (example: mediaSingle field "fileLocation")
import type { MediaWithFullUrl } from "@solidxai/core";
const first = (entity as any)["_media"]["fileLocation"][0] as MediaWithFullUrl;
console.log(first._full_url); // absolute URL to the file
```
</details>

---

### 6) `insertMany(createDtos, filesArray?, context?)`

**What this shows:** How to bulk insert records. The base implementation ignores `filesArray` (kept as `[]`) — add your own override if you need per-row media support.

<details open>
<summary>Show code</summary>

```ts
const saved = await personService.insertMany(
  [
    { name: "Alice", email: "alice@example.com" },
    { name: "Bob",   email: "bob@example.com" }
  ],
  // Files per row are currently not supported in the base implementation (kept as [])
  []
);

console.log(saved.length); // 2
```
</details>

---

### 7) `deleteMany(ids, context?)`

**What this shows:** How to bulk delete by IDs. Honors soft delete if enabled.

<details open>
<summary>Show code</summary>

```ts
await personService.deleteMany([101, 102, 103]);
```
</details>

---

### 8) `recover(id, context?)`

**What this shows:** How to restore a single soft‑deleted record by ID. If a conflicting unique constraint exists, the service throws a conflict error so you can resolve it first.

<details open>
<summary>Show code</summary>

```ts
const res = await personService.recover(101);
console.log(res.message); // "Record recovered" (per SUCCESS_MESSAGES)
```
</details>

---

### 9) `recoverMany(ids, context?)`

**What this shows:** How to restore multiple soft‑deleted records at once. The response includes the list of recovered IDs.

<details open>
<summary>Show code</summary>

```ts
const res = await personService.recoverMany([101, 102, 103]);
console.log(res.recoveredIds); // [101, 102, 103]
```
</details>

---

## Media Population Cheat‑Sheet

**What this shows:** How to request media URLs for single and nested media fields; the service attaches a runtime `_media` object per entity (and nested entities) without persisting it to the DB.

The media types look like:

<details open>
<summary>Media types</summary>

```ts
export type MediaWithFullUrl = Media & {
  _full_url: string;
};

export class Media extends CommonEntity {
  @Index()
  @Column({ type: "integer" })
  entityId: number;

  @Column({ type: "varchar", nullable: true })
  relativeUri: string;

  @Column({ type: "integer", nullable: true })
  fileSize: number;

  @Column({ type: "varchar", nullable: true })
  mimeType: string;

  @Column({ type: "varchar", nullable: true })
  originalFileName: string;

  @Index()
  @ManyToOne(() => ModelMetadata, { onDelete: "SET NULL", nullable: false })
  @JoinColumn()
  modelMetadata: ModelMetadata;

  @Index()
  @ManyToOne(() => MediaStorageProviderMetadata, { onDelete: "SET NULL", nullable: false })
  @JoinColumn()
  mediaStorageProviderMetadata: MediaStorageProviderMetadata;

  @Index()
  @ManyToOne(() => FieldMetadata, { onDelete: "SET NULL", nullable: false })
  @JoinColumn()
  fieldMetadata: FieldMetadata;
}
```
</details>

<details open>
<summary>Show example</summary>

```ts
const person = await personService.findOne(1, {
  populate: ["documents"],
  populateMedia: ["fileLocation", "documents.scan"]
});

// Access the full URL for a mediaSingle field called "fileLocation"
import type { MediaWithFullUrl } from "@solidxai/core";
const media = (person as any)["_media"]["fileLocation"][0] as MediaWithFullUrl;
console.log(media._full_url);
```
</details>

---

## Filters & Grouping Tips

**What this shows:** How `filters`, `groupBy`, and `showSoftDeleted` affect results. Your `CrudHelperService` defines the exact grammar for `filters` and grouping, so adjust the payload to match your implementation.

<!-- Also see the REST API filter guide: **[REST Filters](../rest-api/filters.md)**. -->

<details open>
<summary>Filters group by example</summary>

```ts
// Request
const response = await personService.find({
  limit: 20,
  offset: 0,
  groupBy: ["department.id"],
  populateGroup: true,
  filters: {
    status: { $eq: "active" }
  },
  showSoftDeleted: "exclusive"
});

// Example shape of the response for groupBy:
console.log(response);
/*
{
  meta: {
    totalRecords: totalGroups
  },
  groupMeta,
  groupRecords
}
*/
```
</details>

---

## Best Practices

- Prefer `find({ fields: [...] })` to limit selected columns on heavy entities.
- Use `isPartial = true` for PATCH-like updates; otherwise the service assumes a PUT-like update.
- When adding media fields to models, configure a `MediaStorageProvider` in metadata.
- Keep custom logic (side effects, complex computed values) in  **Computation Providers** preferably or **TypeORM Subscribers** if necessary.

---

## Summary

By extending `CRUDService<T>` you reuse a **tested, consistent**, and **metadata‑driven** CRUD foundation across your modules.  
Focus on your **domain-specific** logic while the CRUD layer handles validation, relations, media, soft delete, and permissions.

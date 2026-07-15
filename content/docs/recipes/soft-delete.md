---
title: Soft Delete
icon: "trash-2"
description: Archive records instead of permanently deleting them, with built-in recovery.
---

# Soft Delete

Soft delete archives a record rather than removing it from the database. The row stays in place with a `deleted_at` timestamp; all normal queries filter it out automatically. Records can be recovered at any time.

---

## Enabling Soft Delete

Set `enableSoftDelete: true` in the model's metadata JSON:

```json
{
  "modelName": "book",
  "enableSoftDelete": true
}
```

No service or controller changes needed - the CRUD layer picks this up automatically.

---

## Database Impact

`CommonEntity` (the base all SolidX entities extend) already declares two columns for this:

| Column | TypeORM decorator | Active | Deleted |
|--------|-------------------|--------|---------|
| `deleted_at` | `@DeleteDateColumn` | `NULL` | timestamp |
| `deleted_tracker` | `@Column` | `"not-deleted"` | `"deleted"` |

TypeORM appends `WHERE deleted_at IS NULL` to all queries by default, so archived records are invisible without extra effort.

`deleted_tracker` solves a uniqueness problem: SQL unique constraints don't know about TypeORM's soft-delete filter. Without it, soft-deleting a book and then creating a new one with the same ISBN would hit a constraint violation. By including `deleted_tracker` in composite unique indexes, the DB sees `("isbn-123", "deleted")` and `("isbn-123", "not-deleted")` as distinct rows.

---

## Code Generation: Composite Unique Indexes

When `solidctl` generates an entity for a soft-delete-enabled model, any field marked unique gets a composite `@Index` with `deletedTracker` instead of a plain `@Unique`. Example from `Book`:

```typescript
@Entity('lm_book')
@Index(['isbn', 'deletedTracker'], { unique: true })
@Index(['bookUserKey', 'deletedTracker'], { unique: true })
export class Book extends CommonEntity {
  // ...
}
```

If you add a unique field to a soft-delete-enabled model manually, follow this same pattern - don't use `@Unique` or a single-column unique `@Index`.

---

## Runtime Behaviour

**Delete** - calls TypeORM's `softRemove()`, setting `deleted_at` and flipping `deleted_tracker` to `"deleted"`.

REST: `DELETE /api/{model}/{id}` · `DELETE /api/{model}/bulk`  
Service: `bookService.delete(id)` · `bookService.deleteMany([id1, id2])`

**Querying archived records** - use `showSoftDeleted` on `find()`:

```typescript
// active only (default)
await bookService.find({});

// active + archived
await bookService.find({ showSoftDeleted: 'inclusive' });

// archived only - e.g. for a trash view
await bookService.find({ showSoftDeleted: 'exclusive' });
```

The same parameter works on the REST API: `GET /api/book?showSoftDeleted=inclusive`.

**Recover** - clears `deleted_at` and resets `deleted_tracker` to `"not-deleted"`. If a new active record already holds the same unique value as the one being recovered, the service throws a conflict error - resolve the conflict first.

```typescript
await bookService.recover(id);
await bookService.recoverMany([id1, id2, id3]);
```

REST: `POST /api/{model}/recover/{id}` · `POST /api/{model}/recover/bulk` (body: array of IDs)

See [Delete endpoint](/docs/developer-docs/rest-apis/delete) and [Recover endpoint](/docs/developer-docs/rest-apis/recover) for full request/response examples.

---

## UI

When `enableSoftDelete: true`, the list view gains a **"Show Archived Records"** checkbox in the settings (cog) menu. Toggling it sends `showSoftDeleted: "inclusive"` with the list query - archived rows appear greyed out alongside active ones. Each archived row shows a **Recover** icon instead of the usual context menu; selecting multiple archived rows surfaces a bulk **Recover** button in the toolbar.

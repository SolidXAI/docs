---
title: Important Configuration Notes
description: Essential configuration guidelines for creating models in SolidX
---

## Important Configuration Notes

### Relation Types

- **One-to-Many**: Parent has multiple children (Institute → Fee Types)
- **Many-to-One**: Child belongs to parent (Fee Type → Institute)
- Always set both sides when `relationCreateInverse` is true

### Cascade Options

- **cascade**: Delete children when parent is deleted
- Use for tightly coupled data (Institute and its Fee Types)

### Audit Tracking

- Enable on fields that need change history
- Typically enabled for business-critical fields
- Not needed for computed or temporary fields

### User Key Fields

- Mark fields that uniquely identify records
- Used in URLs and references
- Should be human-readable and unique

### Index Fields

- Enable for fields used in searches and filters
- Improves query performance
- Typically applied to status fields and foreign keys

### Media Storage

- `default-filesystem`: Stored on local server disk
- `default-aws-s3`: Cloud Storage (Amazon S3)
- Set appropriate size limits based on content type

### Child Models

- Inherit from a parent model (Institute User extends User)
- Share parent's primary key
- Get base fields automatically from parent

### Default Values

- Set sensible defaults for status fields ("Pending")
- Set numeric defaults to 0 for amount fields
- Set boolean defaults to false for flags

## Validation After Creation

After creating each model, verify:

1. All required fields are marked correctly
2. Unique constraints are set where needed
3. Relations are bidirectional (if `relationCreateInverse` is true)
4. Default values are appropriate
5. Audit tracking is enabled on business-critical fields
6. Media storage providers are configured
7. Computed field triggers are set correctly (if applicable)

> **Info**
> For more detailed guidance on creating Modules, Models, and Fields in SolidX, refer to the [Module Builder](../../admin-docs/module-builder/index.md) documentation.


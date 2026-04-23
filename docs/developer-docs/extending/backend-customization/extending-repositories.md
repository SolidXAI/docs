---
sidebar_position: 4
title: Custom Repositories
description: Learn how to extend functionality in repositories in your application.
summary: Details extending repositories inheriting from `SolidBaseRepository<T>` with metadata-aware TypeORM behavior and security rule enforcement via `SecurityRuleRepository`. Covers creating custom query methods using overridden `find`/`findOne` (security-scoped), using QueryBuilder for complex joins, centralizing business-specific queries, composable data access patterns, and examples like `findActiveByInstitute()`. Emphasizes separation between data access and business logic for maintainability and testability.
keywords: [backend, repositories, customization]
solidx_concerns: [backend.repository_changes, extending_repository]
---

# Extending Repositories

## Overview

[Generated repositories](../code-generation#repository) inherit from `SolidBaseRepository<T>`, which already:
- wraps TypeORM with metadata-aware behavior,
- enforces query-level access control via `SecurityRuleRepository`,
- provides contextual access with `RequestContextService`, and
- **overrides the default TypeORM `find` methods** (`find`, `findOne`, `findAndCount`, etc.) so they remain security-aware.

**Why extend?**  
To keep *business-specific queries* out of services/controllers and in a single, testable, composable layer.

Extending repositories lets you:
- write expressive methods using simple `find*` calls (since they are already overridden to respect security rules),
- centralize complex joins or custom query builder logic when needed,
- reuse the same queries across multiple services, and
- maintain a clean separation between *data access* and *business logic*.

---

## Step-by-step: add a custom method

### 1) Add a method using `find`

Most cases can be expressed with `find`/`findOne` since they’re already security-scoped.

<details open>
  <summary><strong>Repository: add custom find-based method</strong></summary>

```ts
import { Injectable } from '@nestjs/common';
import { RequestContextService, SecurityRuleRepository, SolidBaseRepository } from '@solidxai/core';
import { DataSource } from 'typeorm';
import { FeeType } from '../entities/fee-type.entity';

@Injectable()
export class FeeTypeRepository extends SolidBaseRepository<FeeType> {
  constructor(
    readonly dataSource: DataSource,
    readonly requestContextService: RequestContextService,
    readonly securityRuleRepository: SecurityRuleRepository,
  ) {
    super(FeeType, dataSource, requestContextService, securityRuleRepository);
  }

  /**
   * Example: find all active fee types for a given institute.
   * Uses overridden `find` so security rules apply automatically.
   */
  async findActiveByInstitute(instituteId: number): Promise<FeeType[]> {
    return this.find({
      where: {
        institute: { id: instituteId },
        isActive: true,
      },
      order: { displayOrder: 'ASC' },
    });
  }

  /**
   * Example: find one by code.
   */
  async findByCode(code: string): Promise<FeeType | null> {
    return this.findOne({ where: { code } });
  }
}
```
</details>

---

### 2) Add a method using Query Builder

For more complex cases (aggregations, raw joins, advanced conditions), fall back to `createQueryBuilder()`.

<details open>
  <summary><strong>Repository: add query builder method</strong></summary>

```ts
async totalsByCategory(instituteId: number) {
  const qb = this.createQueryBuilder('ft')
    .innerJoin('ft.institute', 'inst', 'inst.id = :instituteId', { instituteId })
    .leftJoin('ft.feeItems', 'fi')
    .select('ft.category', 'category')
    .addSelect('COUNT(fi.id)', 'items')
    .addSelect('COALESCE(SUM(fi.amount), 0)', 'total')
    .groupBy('ft.category')
    .orderBy('ft.category', 'ASC');

  return qb.getRawMany<{ category: string; items: string; total: string }>();
}
```
</details>

---

### 3) Consume your custom repository methods

<details open>
  <summary><strong>Service: use find-based and query builder methods</strong></summary>

```ts
import { Injectable } from '@nestjs/common';
import { FeeTypeRepository } from './repositories/fee-type.repository';

@Injectable()
export class FeesService {
  constructor(private readonly feeTypeRepo: FeeTypeRepository) {}

  listActive(instituteId: number) {
    return this.feeTypeRepo.findActiveByInstitute(instituteId);
  }

  getTotals(instituteId: number) {
    return this.feeTypeRepo.totalsByCategory(instituteId);
  }
}
```
</details>

---

## Best practices

- **Prefer `find` / `findOne` / `findAndCount`** when possible. They are overridden in `SolidBaseRepository` to remain security-aware and easier to read.
- **Use `createQueryBuilder()`** only for advanced scenarios (aggregations, raw SQL, unions).
- **Keep authorization checks in services/guards**. Repositories should stay focused on data access.
- **Return typed results** (entities for reads, raw objects for aggregates).
- **Unit-test repository methods** to validate filtering, ordering, and joins.

---

## Quick reference

<details open>
  <summary><strong>Example: security-aware find</strong></summary>

```ts
await feeTypeRepo.find({
  where: { isActive: true },
  order: { displayOrder: 'ASC' },
  relations: ['institute'],
});
```
</details>

<details open>
  <summary><strong>Example: fallback to query builder</strong></summary>

```ts
await feeTypeRepo.totalsByCategory(1);
```
</details>

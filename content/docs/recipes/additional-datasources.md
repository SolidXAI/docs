---
title: Additional Datasources
icon: "database"
description: How to configure and use multiple TypeORM datasources in a SolidX application.
---

# Additional Datasources

SolidX applications sometimes need to connect to more than one database — for example, a legacy system running on a different DB engine, an external analytics store, or a read replica. This recipe walks through the complete pattern for adding a second (or Nth) datasource alongside the default one.

---

## How the Default Datasource Works

Every SolidX app ships with a `DefaultDBModule` in `app-default-database.module.ts`. It wraps `TypeOrmModule.forRootAsync()` (no `name` → TypeORM treats it as `'default'`) and hooks into SolidX's module discovery to load entities automatically.

```typescript
@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      // No name → this is the 'default' connection
      useFactory: (logger: Logger) => {
        const dynamicModules = getDynamicModuleNames();
        const entities = [
          ...coreEntities,
          ...dynamicModules.map(module =>
            join(__dirname, `./${module}/entities/*.entity.{ts,js}`)
          ),
        ];
        return {
          type: 'postgres',
          host: process.env.DEFAULT_DATABASE_HOST,
          port: +process.env.DEFAULT_DATABASE_PORT,
          username: process.env.DEFAULT_DATABASE_USER,
          password: process.env.DEFAULT_DATABASE_PASSWORD,
          database: process.env.DEFAULT_DATABASE_NAME,
          entities,
          synchronize: parseBooleanEnv('DEFAULT_DATABASE_SYNCHRONIZE'),
          logging: parseBooleanEnv('DEFAULT_DATABASE_LOGGING'),
          logger: parseBooleanEnv('DEFAULT_DATABASE_LOGGING')
            ? new WinstonTypeORMLogger(logger)
            : undefined,
          namingStrategy: new SnakeNamingStrategy(),
          maxQueryExecutionTime: 500,
          ssl: process.env.DEFAULT_DATABASE_SSL === 'true'
            ? { rejectUnauthorized: process.env.DEFAULT_DATABASE_SSL_REJECT_UNAUTHORIZED !== 'false' }
            : false,
          extra: {
            max: Number(process.env.DEFAULT_DATABASE_POOL_MAX ?? 60),
            connectionTimeoutMillis: Number(process.env.DEFAULT_DATABASE_CONNECTION_TIMEOUT_MS ?? 60000),
            idleTimeoutMillis: Number(process.env.DEFAULT_DATABASE_IDLE_TIMEOUT_MS ?? 30000),
            statement_timeout: Number(process.env.DEFAULT_DATABASE_STATEMENT_TIMEOUT_MS ?? 60000),
            idle_in_transaction_session_timeout: Number(process.env.DEFAULT_DATABASE_IDLE_IN_TX_TIMEOUT_MS ?? 60000),
          },
          retryAttempts: Number(process.env.DEFAULT_DATABASE_RETRY_ATTEMPTS ?? 0),
          retryDelay: Number(process.env.DEFAULT_DATABASE_RETRY_DELAY_MS ?? 0),
        };
      },
      inject: [WINSTON_MODULE_PROVIDER],
    }),
  ],
})
@SolidDatabaseModule()
export class DefaultDBModule implements ISolidDatabaseModule {
  type(): DatasourceType { return DatasourceType.postgres; }
  name(): string { return 'default'; }
}
```

Additional datasources follow the exact same structure — the only differences are the `name` field, the env var prefix, and the entities list.

---

## Adding an Additional Datasource

For each new datasource you need two files:

| File | Purpose |
|------|---------|
| `app-{name}-database.module.ts` | NestJS module — registers the connection with the DI container |
| `typeorm-{name}-datasource.ts` | Standalone `DataSource` — used by the TypeORM CLI for migrations |

The examples below use `secondary` as the datasource name. Replace it with whatever makes sense for your project.

---

### Step 1 — The NestJS Module (`app-secondary-database.module.ts`)

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import {
  DatasourceType,
  ISolidDatabaseModule,
  parseBooleanEnv,
  SolidDatabaseModule,
  WinstonTypeORMLogger,
} from '@solidxai/core';
import { WINSTON_MODULE_PROVIDER } from 'nest-winston';
import { SnakeNamingStrategy } from 'typeorm-naming-strategies';
import { Logger } from 'winston';

@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      name: 'secondary',           // <-- must be unique across all datasources
      useFactory: (logger: Logger) => {
        const logging = parseBooleanEnv('SECONDARY_DATABASE_LOGGING');
        return {
          type: 'postgres',        // change to 'mssql', 'mysql', etc. as needed
          host: process.env.SECONDARY_DATABASE_HOST,
          port: +(process.env.SECONDARY_DATABASE_PORT || 5432),
          username: process.env.SECONDARY_DATABASE_USER,
          password: process.env.SECONDARY_DATABASE_PASSWORD,
          database: process.env.SECONDARY_DATABASE_NAME,

          // Leave entities empty here — register them per feature module instead (see Step 3)
          entities: [],

          synchronize: parseBooleanEnv('SECONDARY_DATABASE_SYNCHRONIZE'),
          logging,
          logger: logging ? new WinstonTypeORMLogger(logger) : undefined,
          namingStrategy: new SnakeNamingStrategy(),

          extra: {
            max: Number(process.env.SECONDARY_DATABASE_POOL_MAX ?? 20),
            connectionTimeoutMillis: 30000,
            idleTimeoutMillis: 30000,
            statement_timeout: 15000,
            idle_in_transaction_session_timeout: 60000,
          },
          retryAttempts: Number(process.env.SECONDARY_DATABASE_RETRY_ATTEMPTS ?? 0),
          retryDelay: Number(process.env.SECONDARY_DATABASE_RETRY_DELAY_MS ?? 0),
        };
      },
      inject: [WINSTON_MODULE_PROVIDER],
    }),
  ],
})
@SolidDatabaseModule()
export class SecondaryDBModule implements ISolidDatabaseModule {
  type(): DatasourceType { return DatasourceType.postgres; }
  name(): string { return 'secondary'; }
}
```

Key points:
- The `name` in `TypeOrmModule.forRootAsync()` **must match** the string you use everywhere else (`forFeature`, `@InjectDataSource`, migrations).
- `entities: []` is intentional — see Step 3 for the recommended scoping pattern.
- `@SolidDatabaseModule()` + `implements ISolidDatabaseModule` is required so SolidX's internals can discover and manage the connection.

---

### Step 2 — Import `SecondaryDBModule` in the Feature Module (Scoping)

You do **not** need to register the datasource in `AppModule`. Instead, import `SecondaryDBModule` directly into the feature module that owns that datasource, and declare the entity repositories there with `TypeOrmModule.forFeature`. This keeps the connection and its repositories co-located with the code that uses them.

```typescript
// src/orders/orders.module.ts
@Module({
  imports: [
    SecondaryDBModule,                                          // registers the connection
    TypeOrmModule.forFeature([Order, OrderLine], 'secondary'),  // scopes repos to this module
  ],
  providers: [OrdersService, OrderRepository],
  exports: [OrdersService],
})
export class OrdersModule {}
```

Any module that imports `OrdersModule` via `exports` gets access to `OrdersService` — but the repositories themselves stay private to `OrdersModule`. Other modules that also need to query the secondary datasource should import `SecondaryDBModule` and declare their own `TypeOrmModule.forFeature` call.

If multiple unrelated modules need the same datasource, you can still import `SecondaryDBModule` in `AppModule` to ensure the connection is initialised early — but it is not a requirement.

Any entity registered via `forFeature` also needs to be listed in the `entities` array of `SecondaryDBModule` (so TypeORM knows about the schema). Since we left `entities: []` there, you have two options:

**Option A — Explicit list in the datasource module** (recommended for small, stable entity sets):
```typescript
// in app-secondary-database.module.ts, inside useFactory:
entities: [Order, OrderLine, /* ... */],
```

**Option B — Glob path** (useful when many entities are spread across modules):
```typescript
entities: [
  join(__dirname, './orders/entities/*.entity.{ts,js}'),
  join(__dirname, './inventory/entities/*.entity.{ts,js}'),
],
```

Either way, an entity must be registered in the datasource **and** in `forFeature` to be usable.

---

### Step 3 — Inject the Datasource in Repositories

Use `@InjectDataSource('secondary')` to get the raw `DataSource` — the standard approach when extending `SolidBaseRepository`:

```typescript
// src/orders/repositories/order.repository.ts
@Injectable()
export class OrderRepository extends SolidBaseRepository<Order> {
  constructor(
    @InjectDataSource('secondary')
    readonly dataSource: DataSource,
    readonly requestContextService: RequestContextService,
    readonly securityRuleRepository: SecurityRuleRepository,
  ) {
    super(Order, dataSource, requestContextService, securityRuleRepository);
  }
}
```

If you only need a standard TypeORM `Repository<T>` (not a `SolidBaseRepository`), inject it with:

```typescript
@InjectRepository(Order, 'secondary')
private readonly orderRepo: Repository<Order>
```

---

### Step 4 — The Standalone DataSource (`typeorm-secondary-datasource.ts`)

The TypeORM CLI (`migration:run`, `migration:generate`, etc.) needs a plain `DataSource` instance — it cannot use the NestJS DI container. Create this file alongside the NestJS module:

```typescript
import 'reflect-metadata';
import { DataSource } from 'typeorm';
import { parseBooleanEnv } from '@solidxai/core';
import { join } from 'path';
import { SnakeNamingStrategy } from 'typeorm-naming-strategies';
import { config as dotenvConfig } from 'dotenv';

// Load .env so env vars are available when the CLI runs outside NestJS
dotenvConfig({ path: join(__dirname, '../.env') });

// IMPORTANT: synchronize must be false when using migrations
export const SecondaryDataSource = new DataSource({
  type: 'postgres',
  host: process.env.SECONDARY_DATABASE_HOST,
  port: +(process.env.SECONDARY_DATABASE_PORT || 5432),
  username: process.env.SECONDARY_DATABASE_USER,
  password: process.env.SECONDARY_DATABASE_PASSWORD,
  database: process.env.SECONDARY_DATABASE_NAME,

  entities: [
    join(__dirname, './orders/entities/*.entity.{ts,js}'),
    // add other entity paths here
  ],
  migrations: [
    join(__dirname, './orders/migrations/secondary/*.{ts,js}'),
    // add other migration paths here
  ],

  synchronize: false,
  logging: parseBooleanEnv('SECONDARY_DATABASE_LOGGING'),
  namingStrategy: new SnakeNamingStrategy(),
});
```

Run migrations with:

```bash
# Run all pending migrations
npx typeorm -d src/typeorm-secondary-datasource.ts migration:run

# Generate a new migration (TypeORM diffs entities vs DB schema)
npx typeorm -d src/typeorm-secondary-datasource.ts migration:generate \
  src/orders/migrations/secondary/AddOrderStatusColumn
```

---

## Environment Variables

Follow this naming convention so your datasource is consistently configurable across environments:

| Variable | Default | Description |
|----------|---------|-------------|
| `{PREFIX}_DATABASE_HOST` | — | Database host |
| `{PREFIX}_DATABASE_PORT` | 5432 | Database port |
| `{PREFIX}_DATABASE_USER` | — | Username |
| `{PREFIX}_DATABASE_PASSWORD` | — | Password |
| `{PREFIX}_DATABASE_NAME` | — | Database name |
| `{PREFIX}_DATABASE_LOGGING` | `false` | Enable query logging |
| `{PREFIX}_DATABASE_SYNCHRONIZE` | `false` | Auto-sync schema (disable in prod) |
| `{PREFIX}_DATABASE_POOL_MAX` | `20` | Max connection pool size |
| `{PREFIX}_DATABASE_CONNECTION_TIMEOUT_MS` | `30000` | Connection timeout |
| `{PREFIX}_DATABASE_RETRY_ATTEMPTS` | `0` | Reconnect attempts on startup |
| `{PREFIX}_DATABASE_RETRY_DELAY_MS` | `0` | Delay between reconnect attempts |

Replace `{PREFIX}` with an upper-cased version of your datasource name (e.g. `SECONDARY`).

---

## Summary

| What | Where |
|------|-------|
| Connection config (NestJS) | `app-{name}-database.module.ts` |
| Connection config (CLI/migrations) | `typeorm-{name}-datasource.ts` |
| Entity repository scoping | `TypeOrmModule.forFeature([Entity], '{name}')` in each feature module |
| Repository injection | `@InjectDataSource('{name}')` or `@InjectRepository(Entity, '{name}')` |
| Register connection | Import `{Name}DBModule` in `AppModule` |

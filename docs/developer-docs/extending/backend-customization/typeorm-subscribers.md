---
sidebar_position: 8
title: TypeORM Subscribers
description: Learn how to create and use TypeORM subscribers in your SolidX application.
keywords: [backend, TypeORM subscribers, customization]
---

# TypeORM Subscribers

TypeORM **subscribers** are a powerful feature that allow you to listen to and react to various lifecycle events of your entities.  

They can be used to perform side effects such as logging, auditing, triggering workflows, or maintaining consistency across related entities.  

In SolidX, you can create custom subscribers and register them with TypeORM to extend your application’s behavior.

:::tip
For most use cases, prefer using the SolidX **computed fields** / **computed operations** feature, since it uses background jobs for after* hooks operations and has clearer semantics and improved failure handling.
:::

## Overview

A **subscriber** is a class that implements the `EntitySubscriberInterface` from TypeORM.  
It listens to events such as:  

- `beforeInsert`, `afterInsert`  
- `beforeUpdate`, `afterUpdate`  
- `beforeRemove`, `afterRemove`  
- `afterLoad`  
- Transaction events (`beforeTransactionStart`, `afterTransactionCommit`, etc.)  

**Key Points for Using Subscribers in SolidX:**  
1. Add the subscriber to the **database module providers array**, so it gets registered with TypeORM.  
2. Mark the subscriber with the NestJS `@Injectable()` decorator, just like other providers. This enables dependency injection inside subscribers.  
3. Keep your **business logic in a dedicated service**, and call the service from the subscriber. This ensures separation of concerns and maintainability.  


## Example: Creating a Subscriber
Below is an example of a subscriber that listens to `afterInsert` and `afterUpdate` events on a `User` entity. It logs the events and calls a dedicated audit service to handle the business logic.
<details>
<summary>user-subscriber.ts</summary>
```ts
import { Injectable, Logger } from "@nestjs/common";
import { EventSubscriber, EntitySubscriberInterface, InsertEvent, UpdateEvent } from "typeorm";
import { User } from "../entities/user.entity";
import { UserAuditService } from "../services/user-audit.service";

@Injectable()
@EventSubscriber()
export class UserSubscriber implements EntitySubscriberInterface<User> {
  private readonly logger = new Logger(UserSubscriber.name);

  constructor(private readonly auditService: UserAuditService) {}

  listenTo() {
    return User;
  }

  async afterInsert(event: InsertEvent<User>) {
    if (!event.entity) return; // always check entity presence
    this.logger.debug(`User created: ${event.entity.id}`);
    await this.auditService.logCreation(event.entity);
  }

  async afterUpdate(event: UpdateEvent<User>) {
    if (!event.entity) return;
    this.logger.debug(`User updated: ${event.entity.id}`);
    await this.auditService.logUpdate(event.entity);
  }
}
```
</details>

### Registering the Subscriber
<details>
<summary>myModule.module.ts</summary>
```ts
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  providers: [UserSubscriber, UserAuditService],
})
export class MyModule {}
```
</details>

## Best Practices

✅ **Inject services** into your subscriber (via `@Injectable`) instead of embedding business logic directly.  
✅ **Entity checks** Check if (!event.entity) return; in subscribers, except when you are absolutely sure the entity will always be there (like afterInsert).  
✅ **Avoid global state** inside subscribers, as it can cause inconsistent behavior across requests.  
✅ **Use `queryRunner.data`** to safely share data between hooks in the same transaction.  

## Gotchas

⚠️ Transaction hooks (`beforeTransactionStart`, `afterTransactionCommit`) are **not entity-specific**. You may need to check the entity type before using them.  
⚠️ Be careful with **performance** — heavy logic in subscribers can slow down inserts/updates. Offload work to background jobs if needed.  

:::note
TypeORM transaction hooks are not entity specific.
:::

## References

- [TypeORM Docs: Subscribers](https://typeorm.io/listeners-and-subscribers)  

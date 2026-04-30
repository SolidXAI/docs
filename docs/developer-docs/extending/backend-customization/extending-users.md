---
sidebar_position: 9
title: Custom Users
description: Learn how to extend user functionality in SolidX.
summary: Guide to extending the default User model in SolidX by creating custom user models as children. Covers metadata configuration with isChild true and parentModelUserKey, adding custom fields and relationships, and registering an ExtensionUserCreationProvider to handle password hashing, role assignment, and any project-specific creation logic automatically.
keywords: [backend, users, customization]
solidx_concerns: [extending_user]
---

import { IoIosArrowForward } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';

## Overview

In some cases, you may need to extend the default **User** model in SolidX to accommodate additional attributes or relationships specific to your application. This is achieved by creating a **custom user model** as a child of the base `User` model provided by SolidX.

This guide covers how to:
- Create a custom user model
- Add custom fields and relationships
- Register an `ExtensionUserCreationProvider` to handle user creation automatically

---

## Configuring a Custom User Model

As an example, consider extending the `User` model into an `InstituteUser` model. The `InstituteUser` includes fields such as `userType` and a relation to an `Institute`.

### Steps to Create a Custom User Model
1. Set `isChild: true` in your model metadata.
2. Specify `User` as the `parentModelUserKey`.
3. Add your custom fields and relationships.

<details open>
  <summary className="card-title ">
    Sample Field Metadata for <code>instituteUser</code>
  </summary>

```json
{
  "singularName": "instituteUser",
  "pluralName": "instituteUsers",
  "displayName": "Institute User",
  "tableName": "fees_portal_institute_user",
  "isChild": true,
  "parentModelUserKey": "user",
  "enableAuditTracking": true,
  "enableSoftDelete": true,
  "fields": [
    {
      "name": "userType",
      "displayName": "User Type",
      "type": "selectionStatic",
      "ormType": "varchar",
      "defaultValue": "Institute Admin",
      "selectionStaticValues": [
        "App Admin:App Admin",
        "Institute Admin:Institute Admin"
      ],
      "required": true
    },
    {
      "name": "institute",
      "displayName": "Institute",
      "type": "relation",
      "ormType": "integer",
      "relationType": "many-to-one",
      "relationCoModelSingularName": "institute",
      "relationModelModuleName": "fees-portal",
      "relationCascade": "cascade"
    }
  ]
}
```
</details>

This configuration generates list and form views in SolidX to manage your custom users.

---

## Generated Code for Custom User Models

When `isChild: true` and `User` is the parent model, SolidX generates DTOs and an entity extending the base User model:

<details open>
  <summary className="card-title ">
    DTOs & Entity
  </summary>

```ts
// Create DTO — extends CreateUserDto so all base user fields are available
export class CreateInstituteUserDto extends CreateUserDto { ... }

// Update DTO
export class UpdateInstituteUserDto extends UpdateUserDto { ... }

// Entity
@ChildEntity()
export class InstituteUser extends User { ... }
```
</details>

---

## Registering an Extension User Creation Provider

User creation involves more than a simple insert — password hashing, role assignment, and email notifications all need to run correctly. 

To handle this for your custom user, you need to register an **`ExtensionUserCreationProvider`**. This provider allows you to inject custom logic while creating a custom user

You will need to provide the custom logic to handle the additional fields and relationships of your custom user, while SolidX takes care of the standard user creation flow.

SolidX discovers this provider at startup and uses it automatically for every creation path: the API endpoint, the test data seeder, and any direct repository save. You never need to wire it up manually.

### 1. Create the provider

Implement `IExtensionUserCreationProvider<TEntity, TDto>` and decorate it with `@ExtensionUserCreationProvider()`:

| Type parameter | Constraint | Purpose |
|---|---|---|
| `TEntity` | `extends User` | Your custom user entity (e.g. `InstituteUser`) |
| `TDto` | `extends CreateUserDto` | Your generated create DTO (e.g. `CreateInstituteUserDto`) |

The interface requires three members:

| Member | Purpose |
|---|---|
| `readonly repo` | The repository SolidX uses to save the entity |
| `buildExtensionEntity(dto)` | Builds and returns the extension entity with its custom fields populated. Base user fields (password, roles, etc.) are handled by SolidX — only set extension-specific columns here. |
| `roles(dto)` | Returns the roles to assign to the user, derived from the incoming DTO |

<details open>
  <summary className="card-title ">
    <code>InstituteUserCreationProvider</code>
  </summary>

```ts
import { Injectable, BadRequestException } from '@nestjs/common';
import {
  ExtensionUserCreationProvider,
  IExtensionUserCreationProvider,
} from '@solidxai/core';
import { CreateInstituteUserDto } from '../dtos/create-institute-user.dto';
import { InstituteUser } from '../entities/institute-user.entity';
import { InstituteUserRepository } from '../repositories/institute-user.repository';
import { InstituteRepository } from '../repositories/institute.repository';

@ExtensionUserCreationProvider()
@Injectable()
export class InstituteUserCreationProvider
  implements IExtensionUserCreationProvider<InstituteUser, CreateInstituteUserDto> {

  constructor(
    readonly repo: InstituteUserRepository,
    private readonly instituteRepository: InstituteRepository,
  ) {}

  async buildExtensionEntity(dto: CreateInstituteUserDto): Promise<InstituteUser> {
    if (dto.instituteId) {
      const valid = await this.validateEmailDomain(dto.instituteId, dto.email);
      if (!valid) {
        throw new BadRequestException('Email domain is not valid for this institute');
      }
    }

    const institute = dto.instituteId
      ? await this.instituteRepository.findOne({ where: { id: dto.instituteId } })
      : null;

    return this.repo.merge(this.repo.create(), {
      userType: dto.userType,
      institute,
    });
  }

  roles(dto: CreateInstituteUserDto): string[] {
    if (!dto.userType) {
      throw new BadRequestException('userType is required to determine roles');
    }
    return [dto.userType];
  }

  private async validateEmailDomain(instituteId: number, email: string): Promise<boolean> {
    const institute = await this.instituteRepository.findOne({ where: { id: instituteId } });
    if (!institute) return false;
    if (!institute.emailDomain) return true;
    const emailDomain = email.split('@')[1]?.toLowerCase();
    return emailDomain === institute.emailDomain.toLowerCase();
  }
}
```
</details>

`buildExtensionEntity` is responsible only for the extension-specific columns — do not set `username`, `email`, `password`, or other base user fields here. SolidX merges those in during its standard signup flow (password hashing, `activateUserOnRegistration` setting, role initialisation, and notifications).

### 2. Register the provider in your module

Add `InstituteUserCreationProvider` to your module's `providers` array:

```ts
@Module({
  providers: [
    InstituteUserService,
    InstituteUserRepository,
    InstituteUserCreationProvider, // <-- add this
    InstituteRepository,
    ...
  ],
})
export class FeesPortalModule {}
```

That is all that is required. The generated `InstituteUserService` needs no `create()` override.

---

## Test Data Seeding

Add `userType` (and any other extension fields) to your test user specs in `<module>-metadata.json`. SolidX passes the full spec to `buildExtensionEntity` and `roles`, so any fields present in the JSON are available:

```json
{
  "testing": {
    "users": [
      {
        "username": "testInstAdmin",
        "email": "testInstAdmin@test.local",
        "password": "Test@1234",
        "fullName": "Test Institute Admin",
        "userType": "Institute Admin",
        "instituteUserKey": "Test Institute" 
      }
    ]
  }
}
```

No extra seeding code is needed — SolidX detects the extension fields and routes through the registered provider automatically.

---

## How It Works

1. At startup, SolidX discovers any class decorated with `@ExtensionUserCreationProvider()` and registers it in the `SolidRegistry`.
2. When `AuthenticationService.signUp()` is called (from the API endpoint, the seeder, or anywhere else), it inspects the incoming spec for fields beyond the base `SignUpDto` properties.
3. If extension fields are present, SolidX looks up the registered provider. If no provider is found, an `InternalServerErrorException` is thrown immediately.
4. `buildExtensionEntity(dto)` is called to obtain the correctly-typed extension entity with its custom columns populated.
5. `roles(dto)` is called to determine the roles to assign.
6. SolidX then runs the standard signup flow — password hashing, `activateUserOnRegistration` setting, role initialisation, and notifications — against the prepared entity using the provider's `repo`.
7. If no extension fields are present, `signUp` creates a plain `User` as before, and the provider is never consulted.

<NoteBoxs>
All user records, including custom ones, are stored in the same `ss_user` table.
SolidX uses a discriminator column (`type`) to differentiate between custom user types.
</NoteBoxs>

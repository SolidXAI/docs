---
sidebar_position: 9
title: Extending Users
description: Learn how to extend user functionality in SolidX.
keywords: [backend, users, customization]
---

import { IoIosArrowForward } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';

## Overview

In some cases, you may need to extend the default **User** model in SolidX to accommodate additional attributes or relationships specific to your application. This is achieved by creating a **custom user model** as a child of the base `User` model provided by SolidX.

This guide covers how to:  
- Create a custom user model  
- Add custom fields and relationships  
- Override user creation logic to handle password encryption, validation, and persistence  

---

## Configuring a Custom User Model

As an example, consider extending the `User` model into an `InstituteUser` model. The `InstituteUser` includes fields such as `userType` and a relation to an `Institute`.

### Steps to Create a Custom User Model
1. Set `isChild: true` in your model metadata.  
2. Specify `User` as the `parentModelUserKey`.  
3. Add your custom fields and relationships.  

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
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
        "Mswipe Admin:Mswipe Admin",
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

## Overriding User Creation Logic

User creation involves more than a simple insert (password encryption, password history, email notifications). Therefore, you must override the generated `create` method in your custom user controller.

### Default Generated Code

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Default Implementation
  </summary>

```ts
@ApiBearerAuth("jwt")
@Post()
@UseInterceptors(AnyFilesInterceptor())
async create(@Body() createDto: CreateInstituteUserDto, @UploadedFiles() files: Array<Express.Multer.File>) {
  return this.service.create(createDto, files);
}
```
</details>

### Revised Implementation

Replace the default with logic that validates input, converts DTOs, and calls `signupForExtensionUser`:

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Revised Implementation (InstituteController)
  </summary>

```ts
@ApiBearerAuth("jwt")
@Post()
@UseInterceptors(AnyFilesInterceptor())
async create(@Body() createDto: CreateInstituteUserDto, @UploadedFiles() files: Array<Express.Multer.File>) {
  // Custom validation
  const result = await this.service.validateEmailDomain(createDto.instituteId, createDto.email);
  if (result === false) {
    throw new BadRequestException('Email Domain is not Valid');
  }

  // Convert DTOs
  const signupDto = this.service.toSignUpDto(createDto);
  const extensionUserDto = await this.service.toExtensionUserDto(createDto);

  // Persist user
  return this.authenticationService.signupForExtensionUser(signupDto, extensionUserDto, this.repo);
}
```
</details>

### Supporting Methods in Service

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Methods Implementation (InstituteService)
  </summary>

```ts
async toExtensionUserDto(createDto: CreateInstituteUserDto): Promise<any> {
  let institute = null;
  if (createDto.instituteId) {
    institute = await this.InstituteRepo.findOne({ where: { id: createDto.instituteId } });
  }
  return { ...createDto, institute };
}

toSignUpDto(createDto: CreateInstituteUserDto): SignUpDto {
  return {
    fullName: createDto.fullName,
    username: createDto.username,
    email: createDto.email,
    password: createDto.password,
    mobile: createDto.mobile,
    roles: [createDto.userType], // role name = userType
  };
}

async validateEmailDomain(instituteId: number, email: string) {
  const institute = await this.InstituteRepo.findOne({ where: { id: instituteId } });
  if (!institute) return false;
  if (!institute.emailDomain) return true;

  const emailDomain = email.split('@')[1]?.toLowerCase();
  return emailDomain === institute.emailDomain.toLowerCase();
}
```
</details>

> ⚠️ Use the generated code for other CRUD operations as-is. Only `create()` requires overriding.

---

## Generated Code for Custom User Models

When `isChild: true` and `User` is the parent model, SolidX generates DTOs and Entities extending the base User model:

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    DTOs & Entity
  </summary>

```ts
// Create DTO
export class CreateInstituteUserDto extends CreateUserDto { ... }

// Update DTO
export class UpdateInstituteUserDto extends UpdateUserDto { ... }

// Entity
@ChildEntity()
export class InstituteUser extends User { ... }
```
</details>

---

## How It Works

1. The generated custom model extends `User`, inheriting all base fields and methods.  
2. `AuthenticationService.signupForExtensionUser()` handles:  
   - Persistence of user fields  
   - Password encryption & history  
   - Email notifications  
3. SolidX generates both UI and API endpoints for managing custom users.

<NoteBoxs>
All user records, including custom ones, are stored in the same `ss_user` table.  
SolidX uses a discriminator column (`type`) to differentiate between custom user types.
</NoteBoxs>

---
sidebar_position: 3
title: Extending Users
description: Learn how to extend user functionality in SolidX.
keywords: [backend, users, customization]
---

# 👥 Overview

This section covers how to **extend user functionality in SolidX**, including creating custom user fields and implementing the logic required to persist a custom user model.

---

## 🧩 Configuring a Custom User Model

### To create a custom user model:

- Set `isChild: true` and specify `User` as the parent model in your field metadata.
- Below is an example configuration:

<details>
<summary>📄 Sample Field Metadata for <code>instituteUser</code></summary>

```json
{
  "singularName": "instituteUser",
  "pluralName": "instituteUsers",
  "displayName": "Institute User",
  "description": "This table allows us to store institute user records",
  "dataSource": "default",
  "dataSourceType": "postgres",
  "tableName": "fees_portal_institute_user",
  "isChild": true,
  "parentModelUserKey": "user",
  "enableAuditTracking": true,
  "enableSoftDelete": true,
  "draftPublishWorkflow": false,
  "internationalisation": false,
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


- This will generate form/list views in SolidX to manage the custom users.

⸻

## 🛠 Persisting a Custom User

Since user creation is more than just a simple insert i.e (password encryption, user password history management, etc.)  you must override the generated controller code to allow creating a custom user properly.

🔁 Replace This Code:

<details>
<summary>🔧 Default Generated Code</summary>
```typescript
@ApiBearerAuth("jwt")
@Post()
@UseInterceptors(AnyFilesInterceptor())
async create(@Body() createDto: CreateInstituteUserDto, @UploadedFiles() files: Array<Express.Multer.File>) {
  return this.service.create(createDto, files);
}
```
</details>


✅ With This Logic:

<details>
<summary>✅ Revised Implementation</summary>

```typescript
@ApiBearerAuth("jwt")
@Post()
@UseInterceptors(AnyFilesInterceptor())
async create(@Body() createDto: CreateInstituteUserDto, @UploadedFiles() files: Array<Express.Multer.File>) {
  // Add an custom user validation logic for your custom user model
  const result = await this.service.validateEmailDomain(createDto.instituteId, createDto.email);
  if (result === false) {
    throw new BadRequestException('Email Domain is not Valid');
  }

  // Convert the createDto to a signupDto and extensionUserDto
  const signupDto = this.service.toSignUpDto(createDto);
  const extensionUserDto = await this.service.toExtensionUserDto(createDto);

  // Call signupForExtensionUser to persist user in SolidX
  return this.authenticationService.signupForExtensionUser(signupDto, extensionUserDto, this.repo);
}
```
</details>


	4.	Use generated code as-is for other CRUD operations. Only create() requires overriding.
	5.	You can also show parent user fields in layouts like any other fields. No special config needed.

⸻

## 🧪 Generated Code (for custom user models)

<details>
<summary>📦 DTOs & Entity</summary>

```typescript
// Create DTO
export class CreateInstituteUserDto extends CreateUserDto {
  ...
}

// Update DTO
export class UpdateInstituteUserDto extends UpdateUserDto {
  ...
}

// Entity
@ChildEntity()
export class InstituteUser extends User {}
```
</details>



⸻

## ⚙️ How It Works
	1.	The generated model extends User, inheriting all fields & methods.
	2.	AuthenticationService.signupForExtensionUser() handles:
	  -	User field persistence
	  -	Email notifications
	  -	Password encryption & history tracking
	3.	SolidX generates UI + API endpoints to manage custom users.

:::note
All user records, including custom user ones, are stored in the same User i.e `ss_user` table.
SolidX uses a discriminator column to distinguish custom user types.
:::
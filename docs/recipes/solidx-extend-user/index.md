---
sidebar_position: 5
---

# SolidX User Model

## Extending the SolidX user model  

You can extend the built-in **SolidX User** model to attach additional fields or relationships required by your application. Follow the steps below to do this from the **App Builder**:

### Step 1: Navigate to Model Creation
1. Go to the **SolidX Module**.
2. Click on **App Builder** → **Models**.
3. Create a new model or open an existing one that you want to extend.

### Step 2: Enable as Child of SolidX User
1. In the **Model Creation** screen, fill in all the required fields like **Name**, **Display Name**, etc.
2. Scroll down to the **Configuration** section.
3. Enable the **Is Child** checkbox.
4. A dropdown will appear — select **SolidX User** from the list.

![Default Login Page](/img/tutorial/school-fees-portal/4-customization/extend-solidx-user-model.png)

> ✅ Once selected, your model will now **extend the SolidX User model**, allowing it to inherit its core identity fields while adding your own custom fields.

After extending the SolidX User model, your form view might look like this:

![Default Login Page](/img/tutorial/school-fees-portal/5-recipes/user-model-form-view.png)


### Institute User Form View Layout

```
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Institute User",
    "className": "grid"
  },
  "children": [
    {
      "type": "sheet",
      "attrs": {
        "name": "sheet-1"
      },
      "children": [
        {
          "type": "row",
          "attrs": {
            "name": "sheet-1"
          },
          "children": [
            {
              "type": "column",
              "attrs": {
                "name": "group-1",
                "label": "User Detail",
                "className": "col-6"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "fullName"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "email"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "password"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "username"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "mobile"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "userType"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

In the form above:

🟢 fullName, email, mobile, password → come from the SolidX User model

🔵 userType, institute → come from the Institute User model

### Institute User Entity

Once extended, your InstituteUser entity might look like this:

```
@ChildEntity()
export class InstituteUser extends User {
    @Column({ type: "varchar" })
    userType: string;
    @ManyToOne(() => Institute, { onDelete: "CASCADE", nullable: true })
    @JoinColumn()
    institute: Institute;
}
```

### Institute User Create Dto

Once extended, your InstituteUser create Dto might look like this:

```
export class CreateInstituteUserDto extends CreateUserDto {
    @IsNotEmpty()
    @IsString()
    @ApiProperty()
    userType: string;
    @IsOptional()
    @IsInt()
    @ApiProperty()
    instituteId: number;
    @IsString()
    @IsOptional()
    @ApiProperty()
    instituteUserKey: string;
}
```

### Institute User Update Dto

Once extended, your InstituteUser update Dto might look like this:

```
export class UpdateInstituteUserDto extends UpdateUserDto {
    @IsOptional()
    @IsInt()
    id: number;
    @IsNotEmpty()
    @IsOptional()
    @IsString()
    @ApiProperty()
    userType: string;
    @IsOptional()
    @IsInt()
    @ApiProperty()
    instituteId: number;
    @IsString()
    @IsOptional()
    @ApiProperty()
    instituteUserKey: string;
}
```

### Controller Method (Create Institute User)

In the controller, the create method for institute users you need to change like below to use the SolidX auth logic:

```
create(
  @Body() createDto: CreateInstituteUserDto,
  @UploadedFiles() files: Array<Express.Multer.File>
) {
  const signupDto = this.service.toSignUpDto(createDto);
  return this.authenticationService.signupForExtensionUser(signupDto, createDto, this.repo);
}
```

The signupForExtensionUser method is responsible for:

Registering the user using the base SolidX User logic

Handling both provided and missing passwords:

✅ If password is provided: user is created directly

🔐 If password is not provided: a random password is generated and emailed to the user

This way, you get full authentication and user provisioning using SolidX’s base system with custom fields.



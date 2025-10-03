---
title: Extending Controllers
description: Learn how to extend backend controllers in SolidX.
keywords: [backend, controllers, customization]
sidebar_position: 1
---

import { IoIosArrowForward } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';

# Extending Controllers

In SolidX, **controllers** are responsible for handling incoming requests and returning responses.  
Customizing controllers allows you to **add new endpoints**, modify existing ones, or introduce business-specific logic into your application.

---

## Adding a New Endpoint

To add a new endpoint to an existing controller:

1. Identify the controller you want to extend.  
2. Add a new method inside the controller class to handle the endpoint logic.  
3. Decorate the method with the appropriate HTTP method decorator (`@Get()`, `@Post()`, etc.).  
4. Ensure the endpoint is registered in your API documentation.  
5. Optionally, create a dedicated **DTO** for payload validation and Swagger docs.

You can also create an entirely new controller by adding a new file in the `controllers` directory and defining your custom logic there.

---

### Example: Extending `InstituteController`

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Add New Endpoints to <code>InstituteController</code>
  </summary>

```ts
// Adds an endpoint to activate the institute portal
@ApiBearerAuth("jwt")
@Post("activate-institute-portal")
async activateInstitute(@Body() ids: (number | string)[]) {
  // Delegate logic to the service layer
  return this.service.activateInstitutePortal(ids);
}

// Adds an endpoint that accepts multipart/form-data with files + JSON body
@ApiBearerAuth("jwt")
@Post("custom-logic")
@UseInterceptors(AnyFilesInterceptor())
async performCustomLogicUsingBody(
  @Body() payloadDto: CustomPayloadDto,
  @UploadedFiles() files: Array<Express.Multer.File>,
) {
  return this.service.performCustomLogic(payloadDto, files);
}

// DTO definition with Swagger decorators for request validation & docs
export class CustomPayloadDto {
  @ApiProperty({
    description: "The name of the entity",
    example: "Sample Name",
  })
  name: string;

  @ApiProperty({
    description: "The description of the entity",
    example: "This is a sample description.",
  })
  description: string;
}
```
</details>

The first method (`activateInstitute`) handles `POST /activate-institute-portal` requests, while the second (`performCustomLogicUsingBody`) demonstrates handling **multipart/form-data** (files + JSON).

---

## Permission Auto-Generation

<NoteBoxs>
When you run `solid seed`, SolidX scans controllers and their methods to **auto-generate permissions**.  
For example, the method `activateInstitute` in `InstituteController` will generate a permission named:

```
InstituteController.activateInstitute
```
</NoteBoxs>

---

## Related Recipes (TODO)

- Creating a Custom Controller  
- Creating a Controller Endpoint with Custom Authentication  

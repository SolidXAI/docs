---
title: Extending Controllers
description: Learn how to extend the backend controllers in your application.
keywords: [backend, controllers, customization]
sidebar_position: 3
---
import { IoIosArrowForward } from "react-icons/io";
import { NoteBoxs } from '@site/src/common/NoteBoxs';


#  Extending Controllers

Controllers are responsible for handling requests and returning responses. Customizing them allows you to tailor the behavior of your application to meet specific needs.

---

##  Adding a New Endpoint to a Controller

To add a new endpoint to an existing controller, follow these steps:

1.  Identify the controller you want to extend.
2.  Create a new method in the controller class that handles the logic for the new endpoint.
3.  Define the route for the new endpoint in your routing configuration.
4.  Ensure the new endpoint is documented in your API docs.

You can also create your own custom controller by adding a new file in the `controllers` directory and defining your custom controller there.

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Example: Add a new endpoint to <code>InstituteController</code>
</summary>

```ts
@ApiBearerAuth("jwt")
@Post('activate-institute-portal')
async activateInstitute(@Body() ids: (number | string)[]) {
  const result = await this.service.activateInstitutePortal(ids); // Assuming you have created a service method for this
  return result; 
}
```
</details>


This method will handle POST requests to the /activate-institute-portal endpoint and delegate the logic to the activateInstitutePortal method in the service layer.



<NoteBoxs>
    When you run solid seed, SolidX scans the code for controllers and their methods to auto-create permissions.
    For example, the above method in InstituteController will generate a permission named InstituteController.activateInstitutePortal.
</NoteBoxs>


---

##  Related Recipes (TODO)
	-	 Creating a Custom Controller
	-	 Creating a Controller Endpoint with Custom Authentication

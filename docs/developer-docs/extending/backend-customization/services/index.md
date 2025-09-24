---
sidebar_position: 4
title: Extending Services
description: Learn how to extend the backend services in your application.
keywords: [backend, services, customization]
---

import { IoIosArrowForward } from "react-icons/io";


#  Extending Services

Services are responsible for business logic and data manipulation in your application. Extending services allows you to implement custom logic beyond the default behavior.



##  Adding a New Method to a Service

To add a new method to an existing service, follow these steps:

1.  Identify the service you want to extend.  
2.  Create a new method in the service class that implements your logic.  
3.  Update the corresponding controller if you want to expose this functionality via API.

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   Example: Add <code>activateInstitutePortal</code> to <code>InstituteService</code>
</summary>

```ts
async activateInstitutePortal(ids: (number | string)[]): Promise<any> {
  // Logic to activate the institute portal
  // This could involve updating the database, sending notifications, etc.
}
```
</details>


This method encapsulates the logic required to activate an institute’s portal. You can then call this service method from a controller to make it accessible via an endpoint.



##  Related Recipes
	-	 Creating a Custom Service
	-	 Creating a Service Method with Custom Logic

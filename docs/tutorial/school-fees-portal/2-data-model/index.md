---
sidebar_position: 3
---

# 2. Data Model

In this step we will access the newly bootstrapped SolidX projects admin interface and start designing our data model.

## Login 

To Login to the SolidX admin panel visit the following URL - http://localhost:8081 this is where the SolidX admnin interface is running. You can use the default username & password generated when you ran `solid seed`

![Default Login Page](/img/tutorial/school-fees-portal/2-data-model/default-login.png)

After logging in for the first time, SolidX will prompt you to change the password. 

![Change Password](/img/tutorial/school-fees-portal/2-data-model/first-time-login-change-password.png)

Once you have changed the password you will be able to access the SolidX backend. This defaults to the user list screen. 

## Module

### Create Metadata

The first thing in any new SolidX application is to create a new module. We will start with creating a module to represent our school fee collection portal.

To do this go to Solid Core > App Builder > Module, then click on Add.

This will open up the new module form, you can fill in the details as they are mentioned in the below form. For now we have kept the module icon empty, SolidX will generate the icon in the main menu automatically.

![Create Module](/img/tutorial/school-fees-portal/2-data-model/create-new-module.png)

> A note on the data source, when you created the project using the create-solid-app command, among the other files which were bootstrappted SolidX also created a default data source which is connected to the database whose details we specified during the creation process. SolidX does not restrict you to a single data source and you can configure multiple data sources, more on this in this [Multiple Datasources](../../../recipes/).

Finally we can now go to the list view 

### Generate Code

The above step of creating a new module simply creates an entry in the `ss_module_metadata` table. Using this metadata now SolidX is able to generate the boilerplate required to house a module. To do this simply click on the "Generate Code" action under the context menu that opens up against each row. You will have to select this action against the row representing the newly added module. 

![Generate Module Code](/img/tutorial/school-fees-portal/2-data-model/module-generate-code.png)

This opens a confirmation dialog 

![Generate Module Code Confirmation](/img/tutorial/school-fees-portal/2-data-model/module-generate-code-confirmation.png)

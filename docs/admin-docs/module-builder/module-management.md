---
sidebar_position: 1
---

# Modules

When creating a new module in SolidX, you're defining a core building block of your application. A module is a logical container that groups together related models and functionality under a unified domain or feature area.

## Creating a Module

To create a new module:

1. Navigate to the App Builder, then click on the "Module" menu item.
2. This will show a list of existing modules in the system.
2. Click on "New Module"
3. To create a module, you'll be prompted to provide the following metadata:

### Module Metadata

| Field | Description |
|-------|-------------|
| Display Name | This is the human-readable name of the module that will appear in the admin panel's navigation and UI elements (e.g., "Sales Management") |
| Name | A unique identifier for the module, usually in lowercase and using underscores or dashes. This is used internally by the system and in the API (e.g., "sales") |
| Menu Sequence Number | Determines the order in which the module appears in the sidebar or navigation menu. Lower numbers appear first. |
| Description | A short summary of what the module represents or what functionality it encapsulates. Helps other team members understand its purpose at a glance. |
| Data Source | Select the default data source (from a predefined list) that the module will use to read and write its data. Read More. |
| Icon | Choose an icon to visually represent the module in the UI. This helps in quickly identifying modules in the navigation pane. |

Once you've entered the above details, saving the module will register it in SolidX and allow you to start defining models within it.


### Generate Module

After creating the module Metadata you need to click on the "Generate Module" action button. 

You can find this action button in the list view context menu for each row, and also on the form view header context menu.

TODO: screenshot of the generate module popup to come here.

### Generated Code

After you click on "Generate Module" in the background SolidX does the following. 

1. Makes an entry in the ss_module_metadata table. <br />
   This is a solid core table which contains the details that we just entered. 

2. Create the module folder. <br />
   A folder is created at this location `<project-root>/solid-api/<module-name>`. <br />
   This folder will contain a single file called `<module-name>.module.ts`. <br />
   Keeping in line with our design goal of following industry best practices we have simply generated a standard NestJS module.

3. Register the module. <br />
   Since we are using NestJS modules, SolidX also automatically registers this module in the main app.module.ts file.


## Datasource Configuration


<!-- 
### Data Source Configuration
- Each module can be configured to use a specific data source
- Supports multiple database types (RDBMS and NoSQL)
- Allows for flexible data management across different databases

### Access Control
- Enable/disable modules for different user roles
- Control module visibility in the admin panel
- Manage module-level permissions

### API Integration
- Automatic RESTful API endpoint generation
- Swagger documentation for all endpoints
- Built-in authentication and authorization

### Menu Integration
- Automatic menu structure generation
- Customizable menu ordering
- Role-based menu visibility

## Best Practices

1. **Logical Grouping**
   - Group related functionality together
   - Keep modules focused and single-purpose
   - Consider future scalability

2. **Naming Conventions**
   - Use clear, descriptive names
   - Follow consistent naming patterns
   - Consider internationalization needs

3. **Data Source Planning**
   - Plan database requirements carefully
   - Consider data isolation needs
   - Account for scalability requirements -->

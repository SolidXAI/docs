---
sidebar_position: 1
---

# Modules

When creating a new module in SolidX, you're defining a core building block of your application. A module is a logical container that groups together related models and functionality under a unified domain or feature area.

## Creating a Module

![Module Create Form](/img/admin-docs/module-builder/module-create-form-zoomed.png)

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

When the SolidX project is bootstrapped by default we expect at-least one data source to be configured. 

This is taken care of when a new project is bootstrapped using `npx @solidstarters/create-solid-app`

As part of this bootstrapping a default data source is pre-configured in the file `<project-root>/solid-api/src/app-default-database.module.ts`

```ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import * as SolidCoreModuleExports from '@solidstarters/solid-core';
import { DatasourceType, getDynamicModuleNames, ISolidDatabaseModule, SolidDatabaseModule } from '@solidstarters/solid-core';
import { WINSTON_MODULE_PROVIDER } from 'nest-winston';
import { join } from 'path';
import { getMetadataArgsStorage } from 'typeorm';
import { SnakeNamingStrategy } from 'typeorm-naming-strategies';
import { Logger } from 'winston';
import { WinstonTypeORMLogger } from '@solidstarters/solid-core'; // Assuming you have this custom logger

function getEntitiesFromExports(exports: Record&lt;string, any&gt;) {
    const metadataStorage = getMetadataArgsStorage();
    return Object.values(exports).filter((item) =>
      metadataStorage.tables.some((table) => table.target === item)
    );
}
const coreEntities = getEntitiesFromExports(SolidCoreModuleExports);

@Module({
    imports: [
        TypeOrmModule.forRootAsync({
            useFactory: (logger: Logger) => {
                const dynamicModules = getDynamicModuleNames();

                const entities = [
                    ...coreEntities,
                    ...dynamicModules.map(module =>
                        join(__dirname, `./${module}/entities/*.entity.{ts,js}`)
                    ),
                ];

                return {
                    type: 'postgres',
                    host: process.env.DEFAULT_DATABASE_HOST,
                    port: +process.env.DEFAULT_DATABASE_PORT,
                    username: process.env.DEFAULT_DATABASE_USER,
                    password: process.env.DEFAULT_DATABASE_PASSWORD,
                    database: process.env.DEFAULT_DATABASE_NAME,
                    entities: entities,
                    synchronize: Boolean(process.env.DEFAULT_DATABASE_SYNCHRONIZE),
                    logging: Boolean(process.env.DEFAULT_DATABASE_LOGGING),
                    logger: new WinstonTypeORMLogger(logger),
                    namingStrategy: new SnakeNamingStrategy(),
                }
            },
            inject: [WINSTON_MODULE_PROVIDER]
        }),
    ],
})
@SolidDatabaseModule()
export class DefaultDBModule implements ISolidDatabaseModule {
    type(): DatasourceType {
        return DatasourceType.postgres;
    }

    name(): string {
        return 'default';
    }
}
```


Again in keeping with our design principle of flexibility you can add as many datasources as you like, and have a module use a given datasource as its default datasource. More details on this can be found in the developer docs where we talk about configuring multiple datasources. 


## Related Recipes

Below is a list of recipes that are relevant to module management. 

1. [Additional Datasources](../../recipes/): <br />
   This recipe talks about how you can add additional data sources to your application.


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

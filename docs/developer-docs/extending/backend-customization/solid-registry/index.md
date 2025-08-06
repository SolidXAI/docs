---
sidebar_position: 2
title: Solid Registry
description: Learn how to extend the Solid Registry in your SolidX application.
keywords: [backend, solid registry, customization]
--- 

# Overview
The Solid Registry is a central repository for all the modules, controllers, and other components that make up a SolidX application. It is used to store and manage all the metadata and configuration for the application. It also serves as cache for the application, allowing for quick access to the metadata and configuration, without having to query the database every time.

The Solid Registry registers all the below components:
# Components
- **Seeders**: These are used to seed the database with initial data. The registry keeps track of all the seeders in a SolidX application, allowing for easy access and management.
- **Scheduled Jobs**: These are used to run periodic tasks, such as sending reminders, cleaning up data, or performing regular maintenance tasks. The registry keeps track of all the scheduled jobs in a SolidX application, allowing for easy access and management.
- **Selection Providers**: These are used to provide data for selection fields in the application. The registry keeps track of all the selection providers in a SolidX application, allowing for easy access and management.
- **Computed Fields**: These are used to define fields that are computed based on other fields in the application. The registry keeps track of all the computed fields in a SolidX application, allowing for easy access and management.
- **Solid Database Modules**: These are used to define the database schema for the application. The registry keeps track of all the solid database modules in a SolidX application, allowing for easy access and management.
- **Controllers**: These are used to handle HTTP requests in a SolidX application. The registry keeps track of all the controllers in a SolidX application, allowing for easy access and management.
- **Security Rules**: These are used to define the security rules for the application. The registry keeps track of all the security rules in a SolidX application, allowing for easy access and management.
- **Locales**: These are used to define the localization settings for the application. The registry keeps track of all the locales in a SolidX application, allowing for easy access and management.
- **Computed Field Metadata**: These are used to define the metadata for computed fields in the application. The registry keeps track of all the computed field metadata in a SolidX application, allowing for easy access and management.
- **Dashboard Variable Selection Providers**: These are used to provide data for selection fields in dashboard variables. The registry keeps track of all the dashboard variable selection providers in a SolidX application, allowing for easy access and management.
- **Dashboard Question Data Providers**: These are used to provide data for dashboard questions. The registry keeps track of all the dashboard question data providers in a SolidX application, allowing for easy access and management.

All the above components are registered in the Solid Registry at the time of application startup. So modification to any of the metadata registered in the Solid Registry will require a restart of the application to take effect.
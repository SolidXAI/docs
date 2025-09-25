---
sidebar_position: 2
title: Solid Registry
description: Learn how to extend the Solid Registry in your SolidX application.
keywords: [backend, solid registry, customization]
---

import { FaDatabase,FaCalculator,FaChartBar } from "react-icons/fa";
import { IoMdTimer,IoIosLock } from "react-icons/io";
import { MdTune,MdSettings,MdLanguage,MdViewList ,MdDashboard} from "react-icons/md";
import { FiDatabase} from "react-icons/fi";




# Solid Registry Overview

The **Solid Registry** is a central registry that stores all metadata and configuration for your SolidX application. It serves both as a **cache** and a **metadata manager**, enabling fast access to critical application data without repeatedly querying the database.

At application startup, the registry loads all relevant components, making them available for runtime use.



## Registered Components

Below are the key components tracked by the Solid Registry:

  <h3 className=" card-headear-wrapper">
    <FaDatabase size={16} />

### Seeders
</h3>

Seeders populate your database with initial data. The registry keeps a catalog of all seeders to enable easy discovery and execution.

  <h3 className=" card-headear-wrapper">
    <IoMdTimer size={18} />

### Scheduled Jobs
</h3>


Jobs that run at scheduled intervals (e.g., reminders, cleanups) are registered for monitoring and scheduling control.

  <h3 className=" card-headear-wrapper">
    <MdTune size={18} />

### Selection Providers
</h3>

These supply dynamic values for selection fields (like dropdowns) in the UI, and the registry ensures they're accessible application-wide.

  <h3 className=" card-headear-wrapper">
    <FaCalculator size={18} />

### Computed Fields
</h3>

Computed fields derive values based on logic. The registry stores all metadata for identifying and processing these fields.

  <h3 className=" card-headear-wrapper">
    <FiDatabase size={18} />

### Solid Database Modules
</h3>


Defines your application’s database schema. The registry ensures consistency and availability of all modules.

  <h3 className=" card-headear-wrapper">
    <MdSettings size={18} />

### Controllers
</h3>


Handles incoming HTTP requests. All controllers are registered, simplifying route handling and metadata tracking.


<h3 className=" card-headear-wrapper">
    <IoIosLock size={18} />

### Security Rules
</h3>

Used to restrict data access based on user roles. The registry manages these rules and enforces them on relevant operations.

  <h3 className=" card-headear-wrapper">
    <MdLanguage size={18} />

### Locales
</h3>

Handles localization settings (languages, formats). The registry keeps track of all available locales.

  <h3 className=" card-headear-wrapper">
    <FaChartBar size={20} />

### Computed Field Metadata
</h3>



Metadata definitions for computed fields are separately registered to help with field evaluations.

  <h3 className=" card-headear-wrapper">
    <MdDashboard size={18} />

### Dashboard Variable Selection Providers
</h3>



Provides dynamic data for dashboard variable dropdowns.

  <h3 className=" card-headear-wrapper">
    <MdViewList size={20} />

### Dashboard Question Data Providers
</h3>



Supplies data sources for dashboard questions (charts, summaries, etc).



## When Is the Registry Populated?

All of the above components are registered **at application startup**.

> If you modify any metadata registered in the Solid Registry, you **must restart the application** for those changes to take effect.



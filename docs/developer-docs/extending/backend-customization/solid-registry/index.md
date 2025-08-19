---
sidebar_position: 2
title: Solid Registry
description: Learn how to extend the Solid Registry in your SolidX application.
keywords: [backend, solid registry, customization]
---

# 🧱 Solid Registry Overview

The **Solid Registry** is a central registry that stores all metadata and configuration for your SolidX application. It serves both as a **cache** and a **metadata manager**, enabling fast access to critical application data without repeatedly querying the database.

At application startup, the registry loads all relevant components, making them available for runtime use.

---

## 📦 Registered Components

Below are the key components tracked by the Solid Registry:

### 🌱 Seeders
Seeders populate your database with initial data. The registry keeps a catalog of all seeders to enable easy discovery and execution.

### ⏰ Scheduled Jobs
Jobs that run at scheduled intervals (e.g., reminders, cleanups) are registered for monitoring and scheduling control.

### 🎯 Selection Providers
These supply dynamic values for selection fields (like dropdowns) in the UI, and the registry ensures they're accessible application-wide.

### 🧮 Computed Fields
Computed fields derive values based on logic. The registry stores all metadata for identifying and processing these fields.

### 🗃️ Solid Database Modules
Defines your application’s database schema. The registry ensures consistency and availability of all modules.

### 🚦 Controllers
Handles incoming HTTP requests. All controllers are registered, simplifying route handling and metadata tracking.

### 🔐 Security Rules
Used to restrict data access based on user roles. The registry manages these rules and enforces them on relevant operations.

### 🌍 Locales
Handles localization settings (languages, formats). The registry keeps track of all available locales.

### 🧩 Computed Field Metadata
Metadata definitions for computed fields are separately registered to help with field evaluations.

### 📊 Dashboard Variable Selection Providers
Provides dynamic data for dashboard variable dropdowns.

### 📈 Dashboard Question Data Providers
Supplies data sources for dashboard questions (charts, summaries, etc).

---

## 🔁 When Is the Registry Populated?

All of the above components are registered **at application startup**.

> ⚠️ If you modify any metadata registered in the Solid Registry, you **must restart the application** for those changes to take effect.

---
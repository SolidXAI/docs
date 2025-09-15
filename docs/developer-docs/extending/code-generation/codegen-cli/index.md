---
title: Code Generation CLI
description: This page provides a list of CLI commands that can be used as an alternative to generate backend code in SolidX.
sidebar_position: 2
---

#  Code Generation CLI

This page provides a list of CLI commands that can be used as an alternative to generate backend code in SolidX.

The SolidX code builder—invoked either from the SolidX Admin UI or the CLI—uses Angular Schematics to scaffold code in the backend.

---

##  Add Module

Generates a new module in the SolidX backend.

###  Command

```tsx
solid add-module <options>

Example:
solid add-module -n myNewModule
```

###  Options

- `-n moduleName`, `--moduleName <moduleName>`  
  The name of the module to be generated.

- `-i moduleId`, `--moduleId <moduleId>`  
  The ID of the module to be generated.

- `-d dryRun`, `--dryRun <dryRun>`  
  Whether to run the command in dry-run mode.

---

##  Refresh Model

Creates or updates a model and its related files within an existing module.

###  Command

```tsx
solid refresh-model <options>

Example:
solid refresh-model -n myNewModelSingularName
```

###  Options

- `-n modelName`, `--modelName <modelName>`  
  The name of the model to be generated.

- `-i modelId`, `--modelId <modelId>`  
  The ID of the model to be generated.

- `-d dryRun`, `--dryRun <dryRun>`  
  Whether to run the command in dry-run mode.

 Refer to [Generated code](../index.md) for a breakdown of the files and structure generated.

---

##  Remove Fields

Removes fields from an existing model in the SolidX backend.

###  Command

```bash
solid remove-fields <options>

Example:
solid remove-fields -fids "[myFieldId]" -mid myModelId
```

###  Options

- `-fids fieldIds`, `--fieldIds <fieldIds>`  
  The IDs of the fields to be removed. This needs to be a JSON stringified representation of an array e.g "[1]" or "[2,3]"

- `-mid modelId`, `--modelId <modelId>`  
  The ID of the model from which the fields will be removed.

- `-d dryRun`, `--dryRun <dryRun>`  
  Whether to run the command in dry-run mode.

 Refer to [Generated code](../index.md) for a breakdown of the files and structure after running this command.

---

>  The underlying implementation leverages Angular schematics and schema definitions to validate and process these operations.

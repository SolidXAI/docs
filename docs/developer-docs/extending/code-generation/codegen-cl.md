---
title: Code Generation CLI
description: This page provides a list of CLI commands that can be used as an alternative to generate backend code in SolidX.
sidebar_position: 2
---

import { FaTerminal, FaSlidersH } from "react-icons/fa";

# ⚡ Code Generation CLI

The SolidX code builder—invoked either from the SolidX Admin UI or the CLI—uses Angular Schematics to scaffold backend code.  

While multiple commands exist, **`refresh-model` is the primary and most frequently used command**.  
Other commands such as `add-module` or `remove-fields` are available but are typically required only in special cases.

---

## 🔑 Refresh Model (Most Important)

Creates or updates a model and its related files within an existing module.  
This is the **main command you’ll use** to keep code in sync with metadata.

<h4 className="card-title card-headear-wrapper">
  <FaTerminal size={19} />

### Command
</h4>

```tsx
solid refresh-model <options>

Example:
solid refresh-model -n myNewModelSingularName
```

<h4 className="card-title card-headear-wrapper">
  <FaSlidersH size={18}  />

### Options
</h4>

- `-n modelName`, `--modelName <modelName>`  
  The name of the model to be generated.

- `-i modelId`, `--modelId <modelId>`  
  The ID of the model to be generated.

- `-d dryRun`, `--dryRun <dryRun>`  
  Whether to run the command in dry-run mode.

👉 Refer to [Generated code](../index.md) for a breakdown of the files and structure generated.

---

## 📦 Add Module (Rarely Needed)

Generates a new module in the SolidX backend.  
Mostly useful during **initial setup**, as modules are usually scaffolded automatically when creating metadata.

<h4 className="card-title card-headear-wrapper">
  <FaTerminal size={19} />

### Command
</h4>

```tsx
solid add-module <options>

Example:
solid add-module -n myNewModule
```

<h4 className="card-title card-headear-wrapper">
  <FaSlidersH size={18}  />

### Options
</h4>

- `-n moduleName`, `--moduleName <moduleName>`  
  The name of the module to be generated.

- `-i moduleId`, `--moduleId <moduleId>`  
  The ID of the module to be generated.

- `-d dryRun`, `--dryRun <dryRun>`  
  Whether to run the command in dry-run mode.

---

## 🧹 Remove Fields (Edge Case)

Removes fields from an existing model in the SolidX backend.  
Rarely required — mostly used for cleanup when metadata and generated code need alignment.

<h4 className="card-title card-headear-wrapper">
  <FaTerminal size={19} />

### Command
</h4>

```bash
solid remove-fields <options>

Example:
solid remove-fields -fids "[myFieldId]" -mid myModelId
```

<h4 className="card-title card-headear-wrapper">
  <FaSlidersH size={18}  />

### Options
</h4>

- `-fids fieldIds`, `--fieldIds <fieldIds>`  
  The IDs of the fields to be removed. This needs to be a JSON stringified array e.g "[1]" or "[2,3]".

- `-mid modelId`, `--modelId <modelId>`  
  The ID of the model from which the fields will be removed.

- `-d dryRun`, `--dryRun <dryRun>`  
  Whether to run the command in dry-run mode.

👉 Refer to [Generated code](../index.md) for a breakdown of the files and structure after running this command.

---

> ⚙️ The underlying implementation leverages Angular schematics and schema definitions to validate and process these operations.

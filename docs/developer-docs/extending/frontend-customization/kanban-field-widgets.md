---
sidebar_position: 2
title: Kanban Field Widgets
description: Customize kanban card field rendering in SolidX.
summary: Explains how to apply built-in or custom field widgets for kanban cards, where to place custom widget components, and how to register and wire them in metadata.
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_widget]
---

## Overview

Kanban field widgets control how values are rendered inside kanban cards.

For project-specific widgets, use model-scoped extension files and register them through `solid-extensions.ts`.

## File Location

For model-scoped widgets:

- `solid-ui/src/extensions/<module-name>/<model-name>/custom-widgets/`

## Registration

```ts
import { registerExtensionComponent } from "@solidxai/core-ui";
import { PriorityBadgeKanbanWidget } from "./venue/task/custom-widgets/PriorityBadgeKanbanWidget";

registerExtensionComponent("PriorityBadgeKanbanWidget", PriorityBadgeKanbanWidget);
```

## Metadata Wiring

Use the registered name in kanban layout JSON where widget override is supported by your layout schema.

## API Guidance

If the widget performs API calls, use Solid helpers from `@solidxai/core-ui`:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Use `/resource` paths and handle loading/error explicitly.

## See Also

- [Custom Widgets](./custom-widgets.md)
- [Form View Field Widgets](./form-view-field-widgets.md)
- [List View Field Widgets](./list-view-field-widgets.md)

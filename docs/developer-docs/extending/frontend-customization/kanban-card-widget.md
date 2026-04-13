---
sidebar_position: 2
title: Kanban Card Widgets
description: Customize kanban card rendering in SolidX.
summary: Explains how to apply built-in or custom widget for kanban cards, where to place custom widget components, and how to register and wire them in metadata.
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_widget]
---

## Overview

Kanban card widgets control how values are rendered inside kanban cards.

For project-specific widgets, use model-scoped extension files and register them through `solid-extensions.ts`.

## File Location

For model-scoped widgets:

- `solid-ui/src/extensions/<module-name>/<model-name>/custom-widgets/`

## Registration

```ts
import { registerExtensionComponent } from "@solidxai/core-ui";
import {
    ExtensionComponentTypes,
    ExtensionFunctionTypes,
    type ExtensionComponentType,
    type ExtensionFunctionType,
} from "../types/extension-registry";
import { PriorityBadgeKanbanWidget } from "./venue/task/custom-widgets/PriorityBadgeKanbanWidget";

registerExtensionComponent("PriorityBadgeKanbanWidget", PriorityBadgeKanbanWidget, ExtensionComponentTypes.kanban_card_widget);
```

## Metadata Wiring

Use the registered name in the Kanban layout JSON. The `cardWidget` attribute must be placed inside the `attrs` of the `card` type child within the `kanban` layout.

```json
{
  "name": "task-kanban-view",
  "displayName": "Tasks Kanban",
  "type": "kanban",
  "layout": {
    "type": "kanban",
    "attrs": {
      "groupBy": "stage",
      "draggable": true
    },
    "children": [
      {
        "type": "card",
        "attrs": {
          "name": "Card",
          "cardWidget": "PriorityBadgeKanbanWidget"
        },
        "children": [
          {
            "type": "field",
            "attrs": {
              "name": "name",
              "isSearchable": true
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "priority",
              "isSearchable": true
            }
          }
        ]
      }
    ]
  }
}
```

## API Guidance

If the widget performs API calls, use Solid helpers from `@solidxai/core-ui`:

- `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, `solidAxios`

Use `/resource` paths and handle loading/error explicitly.

## See Also

- [Custom Widgets](./custom-widgets.md)
- [Form View Field Widgets](./form-view-field-widgets.md)
- [List View Field Widgets](./list-view-field-widgets.md)

---
sidebar_position: 2
title: Kanban Card Widgets
description: Customize kanban card rendering in SolidX.
summary: "Explains how to apply built-in or custom widgets for kanban cards, where to place custom widget components, how to register them in a UI module manifest, and how to wire them in metadata."
solidx_concerns: [frontend.extensions.custom_widgets, create_custom_widget]
---

## Overview

Kanban card widgets control how values are rendered inside kanban cards.

For project-specific widgets, place model-scoped files under the owning module and register them through the module manifest.

## File Location

For model-scoped widgets, use:

- `solid-ui/src/<module-name>/admin-layout/<model-name>/extension-components/`

## Registration

```ts
import { ExtensionComponentTypes, type SolidUiModule } from "@solidxai/core-ui";
import { PriorityBadgeKanbanWidget } from "./admin-layout/task/extension-components/PriorityBadgeKanbanWidget";

const taskUiModule = {
  name: "task",
  extensionComponents: [
    {
      name: "PriorityBadgeKanbanWidget",
      component: PriorityBadgeKanbanWidget,
      type: ExtensionComponentTypes.kanban_card_widget,
    },
  ],
} satisfies SolidUiModule;

export default taskUiModule;
```

## Metadata Wiring

Use the registered name in kanban layout JSON. The `cardWidget` attribute belongs inside the `attrs` of the `card` type child within the `kanban` layout.

```json
{
  "name": "task-kanban-view",
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
              "name": "name"
            }
          },
          {
            "type": "field",
            "attrs": {
              "name": "priority"
            }
          }
        ]
      }
    ]
  }
}
```

## API Guidance

Kanban widgets can use either supported frontend API style.

### Option A: Solid HTTP Helpers

Use `solidGet`, `solidPost`, `solidPut`, `solidPatch`, `solidDelete`, or `solidAxios` for localized API interaction.

### Option B: Redux / RTK Query

If the widget participates in a wider module-owned data flow, place RTK Query APIs, reducers, and middleware under:

- `solid-ui/src/<module-name>/redux/`

and register them through the same manifest.

## See Also

- [Custom Widgets](./custom-widgets.md)
- [Form View Field Widgets](./form-view-field-widgets.md)
- [List View Field Widgets](./list-view-field-widgets.md)
- [Redux Module Integration](./redux-module-integration.md)

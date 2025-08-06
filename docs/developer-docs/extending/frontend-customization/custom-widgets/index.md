---
sidebar_position: 2
title: Custom Widgets
description: Learn how to create custom widgets for the frontend of your application.
---

## Overview
Custom widgets allow you to extend the UI functionality of your frontend application by adding new components that can be reused across different views. These widgets can encapsulate specific functionality and associated with a specific field allowing you to render the same field in different ways based on the widget configuration.

There are 2 kinds of custom widgets:
1. **Edit Widgets**: These are used to render fields in a specific way for forms i.e (in create / edit mode)
2. **View Widgets**: These are used to render fields in a specific way for forms i.e (in view mode)

View widget can be used to render fields in forms in view mode, or in list views. 

We can write custom widget to write custom UI functionality which can be used in the form layout json configuration.
The widgets need to registeredas below in the solid-extensions.ts file in the solid-ui/app folder, before using them in the form layout json configuration:
```typescript
registerExtensionComponent("BookSimilarTitles", BookSimilarTitles);
```

## Examples
TODO

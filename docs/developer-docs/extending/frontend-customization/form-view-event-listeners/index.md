---
sidebar_position: 2
title : Form View Event Listeners
description: Learn how to create event listeners for form view events in your frontend application.
---

## Overview
Form view event listeners allow you to extend the functionality of your frontend application by responding to specific events that occur in form views.

SolidX supports below types of form  event listeners:
1. **onFormLayoutLoad**:
2. **onFormDataLoad**:
3. **onFieldChange**:
4. **onFieldBlur**:


We can write custom handler to write custom UI functionality which get triggered on these events. These handlers need to be specified in the form layout json configuration.

The handlers are registered as below in the solid-extenssions.ts file in the solid-ui/app folder:
```typescript
registerExtensionFunction("assessmentFieldChangeHandler", assessmentFieldChangeHandler);
```

## Examples
TODO
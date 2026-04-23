---
title: Reference
description: Reference documentation for built-in providers and components shipped with SolidX.
summary: Reference section for built-in SolidX providers and components. Contains detailed documentation on built-in selection providers, and other pre-built extensibility points that ship with the platform.
sidebar_position: 4
---

# Reference

This section contains reference documentation for the **built-in providers and components** that ship with SolidX. These are ready-to-use building blocks that you can configure via metadata without writing custom code.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    Not every extension point in SolidX requires custom code. Some platform capabilities are already packaged as built-in providers and components that you simply reference from metadata.
  </p>
  <ul>
    <li>Use this section when you want to reuse a built-in capability.</li>
    <li>Use the customization sections when the built-in options are not enough.</li>
    <li>This keeps teams from writing code for cases the platform already solves.</li>
  </ul>
  <p>
    So the intuition is: <strong>start with built-in providers first, then move to custom implementation only when the use case demands it</strong>.
  </p>
</div>

For guides on creating your own providers, see [Backend Customization](../backend-customization).

| Topic | Description |
|---|---|
| [Built-in Selection Providers](./built-in-selection-providers) | `ListOfValuesSelectionProvider` and `PseudoForeignKeySelectionProvider` for populating dynamic dropdowns |

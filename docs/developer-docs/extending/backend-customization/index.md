---
title: Backend
description: This section provides an overview of backend customization capabilities in SolidX.
summary: This document provides an overview of backend customization capabilities in SolidX, covering how developers can extend the NestJS-based backend functionality. Topics include adding custom API endpoints to controllers, modifying and extending existing services with custom business logic, implementing custom providers for specialized functionality, and integrating additional backend features to meet specific application requirements beyond the default CRUD operations.
sidebar_position: 2
---

# Overview
This section provides an overview of backend customization capabilities in SolidX. It covers how to extend the backend functionality, including adding custom endpoints, modifying existing services, adding custom providers, and more.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    SolidX generates a large amount of backend structure for you, but that does not mean the backend is closed for custom work.
    The generated layer gives you a strong default foundation, while backend customization is where you introduce application-specific behavior.
  </p>
  <ul>
    <li>Use metadata when the requirement is declarative and platform-supported.</li>
    <li>Use backend customization when the requirement is business-specific or operationally unique.</li>
    <li>Think of this section as the bridge between generated CRUD and a real production backend.</li>
  </ul>
  <p>
    So the intuition is: <strong>SolidX gives you the baseline backend quickly, and this section shows where to extend it safely</strong>.
  </p>
</div>

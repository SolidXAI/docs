---
sidebar_position: 6
title: REST APIs
description: This section contains details about the SolidX REST APIs serving different functionalities.
summary: This section provides comprehensive documentation of SolidX's auto-generated REST APIs that enable communication between frontend and backend. The APIs cover authentication (password, OTP, OAuth), CRUD operations (create, retrieve, update, delete), record recovery for soft-deleted items, and comprehensive Swagger documentation. Each API endpoint follows RESTful principles with JWT bearer authentication, standardized request/response formats, support for file uploads, filtering, pagination, sorting, and field selection capabilities.
---

# Overview

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    The SolidX REST APIs are the main machine-facing interface of the platform.
  </p>
  <ul>
    <li>The frontend uses them to communicate with the backend.</li>
    <li>Integrations can use them to automate or extend system behaviour.</li>
    <li>Much of the API surface is generated from metadata and backend structure, then extended where needed.</li>
  </ul>
  <p>
    So the intuition is: the REST API layer is the <strong>runtime contract between your metadata-driven backend and the outside world</strong>.
  </p>
</div>

This section provides an overview of the SolidX REST APIs, which are designed to facilitate various functionalities within the SolidX framework. These APIs serve as the backbone for communication between the frontend and backend, enabling seamless data exchange and operations.

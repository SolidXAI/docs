---
sidebar_position: 2
---

# 2. Institute User Workflows

This section covers the primary workflows for an institute's administrative user, from logging in to managing payments.

## User Login and Access Control

### Overview

The "Institute User - Login" use case describes how an administrative user associated with a specific institute gains access to the SolidX admin panel. This process is fundamental for institute staff to manage their fees, students, and other institute-specific data.

### Login Process

1.  **Accessing the Admin Panel:** Institute users will navigate to the SolidX admin panel URL (e.g., `http://localhost:8081/admin`).
2.  **Authentication:** Users enter their username (typically an email address) and password.
3.  **Multi-tenancy:** Upon successful authentication, the SolidX framework identifies the institute(s) the user is associated with. This is crucial for enforcing data isolation and ensuring users only see and manage data relevant to their assigned institute.

### Security Record Rules

Security Record rules are a core feature of SolidX that enable fine-grained access control at the data record level. For "Institute Users," these rules are paramount in a multi-tenant environment to ensure data security and privacy. When an `InstituteUser` logs in, the system applies these rules to automatically filter all data, ensuring they can only access records associated with their institute. This provides robust data isolation and multi-tenancy support without requiring developers to write manual filtering queries.

## Bulk Data Upload via Excel

### Business Reason

Institutes often need to manage a large volume of student and payment data. The "Create Excel For Upload" use case addresses this by providing a mechanism for institute users to bulk upload data using a standardized Excel template. This significantly streamlines the process of populating the system with student records and initiating payment collections.

### Process for Bulk Upload

1.  **Download Template:** The user downloads a pre-defined Excel template from the SolidX admin panel.
2.  **Fill Data:** The user populates the template with student and fee information.
3.  **Upload Excel:** The user uploads the file back into the system, typically within a `PaymentCollection`.

### System Processing

Upon upload, a SolidX subscriber is triggered. This background process reads the Excel file and automatically creates or updates `Student` records and their corresponding `PaymentCollectionItem` records, ensuring data integrity and reducing manual effort.

## Initiate Payment

*(This section is a placeholder and will be detailed later.)*

This workflow will describe how an institute user can initiate a payment request for one or more students, either manually or in bulk. This action will trigger notifications to parents and generate payment links.

## User Dashboard

*(This section is a placeholder and will be detailed later.)*

This section will describe the institute user's dashboard, which will provide an at-a-glance view of key metrics, such as total fees collected, outstanding payments, and recent student activity.

## Cancel Payments

*(This section is a placeholder and will be detailed later.)*

This workflow will explain the process for an institute user to cancel a pending payment, including how the system handles refunds and notifications.

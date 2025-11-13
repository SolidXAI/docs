---
sidebar_position: 1
---

# Revamped: School Fees Portal Tutorial

## Introduction

Building a Fee Collection Platform for Educational Institutions

Managing and collecting student fees efficiently remains a challenge for many educational institutions. Traditional methods often involve manual processes, fragmented systems, and lack transparency for both administrators and parents. This tutorial will walk through the process of building a hosted, multi-tenant fee collection platform tailored for educational institutions using SolidX.

By the end of this tutorial, you will have a functional application that allows institutions to:

-   Onboard themselves and manage their own students and fee structures.
-   Configure a branded landing page for students and parents.
-   Initiate fee collection requests by uploading structured data.
-   Process payments through an integrated payment gateway.
-   Automate reminders and notifications for pending payments.
-   Generate reports and manage financial records, including refunds.

You will learn how to leverage SolidX's low-code capabilities to rapidly model a complex domain, automatically generate APIs and admin interfaces, and customize the application to meet specific business requirements.

## User Roles

We'll support two main user types:

### Super Admin
- Onboards new institutions
- Configures initial landing page and fee types
- Manages admin users for institutions
- Can initiate collections (optional)

### Institution Admin
- Belongs to a specific institution
- Uploads payment collection details
- Tracks payments and generates reports


## Key Use Cases

### 1. Onboarding an Educational Institution

The onboarding process includes:

- Creating a new institution tenant in the platform
- Configuring institutional metadata such as:
  - Name, domain, logo, hosted page prefix
  - Fee types (e.g., Tuition, Bus, Library, Semester 1)
- Adding institution admin users with domain-verified email IDs
- Automatically provisioning branded landing pages (e.g., `school-name.platform.com`)

### 2. Configuring the Landing Page

Each institution will receive a branded landing page where students or parents can:

- Log in using email/mobile OTP
- View due and historical payments
- Start the payment process

> The page design will be standardized, with only the institutions branding (like logo) customized.

### 3. Initiating Payment Collections

Admins can upload payment collection requests via CSV/Excel files.

Each upload:

- Contains fee details for multiple students
- Creates records for students, payment collections, and individual fee items
- Triggers email notifications to students/guardians about dues

> Optionally, WhatsApp or SMS notifications can be integrated in the future.

### 4. Making a Payment

Students/guardians receive emails with payment links. Once authenticated:

- They see a breakdown of fees due by category (e.g., Semester 1, Bus, etc.)
- They can choose partial/full payment amounts
- The platform integrates with a payment gateway to process transactions
- Real-time updates are reflected in the system's records

### 5. Refunds & Chargeback Handling

Institution admins can initiate refunds via the platform.

- Refunds update all related tables and mark items as refunded
- Reporting views automatically adjust based on refund status
- Chargeback logs can be generated using payment and fee-level records

### 6. Notifications

The system supports the following types of notifications:

- **Fee Due Reminders:** Weekly reminders for pending or partially paid fees
- **New Collection Alert:** Sent when new payment collections are uploaded


### 7. Reporting

- **Revenue Tracking:** Exportable Excel files combining payment collection and fee data
- **Receipts:** To be configured based on institution needs
- **Visual Reports:** Future scope for in-system dashboards
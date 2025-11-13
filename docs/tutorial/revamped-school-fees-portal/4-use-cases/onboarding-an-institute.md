---
sidebar_position: 1
---

# 1. Onboarding an Institute

## Business Reason

The "Onboarding an Institute" use case is the foundational step in the school fees portal. It allows a super administrator to register a new educational institution onto the platform. This process is crucial because it captures all the essential details about the institute, including its name, contact information, payment gateway credentials, and branding assets. A well-defined onboarding process ensures that each institute is set up correctly and can operate independently within the multi-tenant environment of the portal.

## Onboarding Process

The onboarding process involves creating the institute, setting up its users, defining fee structures, and configuring technical details. The UI is broken down into logical tabs to make this manageable.

### 1. Institute Details & Branding

This is the primary tab for core information:
*   **Institute Name, Description, Contact Information, GST Number.**
*   **Branding:** Uploading logos, brochures, and intro videos. SolidX's media-provider abstraction allows storing these assets on different backends (e.g., AWS S3 for logos, local file system for videos).
*   **Content:** Terms & Conditions, FAQs, Privacy Policy for student-facing pages.

### 2. Institute Users

This tab is for creating the initial administrative users for the institute. 
*   **Extending the User Model:** The `InstituteUser` model extends the core SolidX `User` model, inheriting fields like name, email, and password, while adding institute-specific fields.
*   **Automated Credentials:** If a user is created without a password, SolidX generates a secure random password and emails the login credentials to the user, using its built-in email abstraction.

### 3. Fee Types

This is where an administrator defines the various fees an institute can collect (e.g., "Tuition Fee", "Hostel Fee").
*   **Uniqueness per Institute:** It's crucial that fee types are unique *per institute*. A composite index on `(instituteId, feeType)` is used to enforce this rule, ensuring no duplicate fee types exist within the same institution.

### 4. Payment Gateway

This tab is for configuring the institute's payment gateway credentials to enable online fee collection.
*   **Credentials:** Merchant ID, Access Key, and Secret.
*   **Payment Link Generation:** The system generates a unique payment link for students.
*   **Handling Callbacks:** After a student completes a payment, the gateway sends a POST callback to the backend, which then updates all related records based on the payment's success or failure.

### 5. Removing the Custom Home Page

By default, a new module in SolidX has a dashboard-like home page. To remove it and revert to a standard list view:
1.  Navigate to **Solid Core > App Builder > Module**.
2.  Select the `fees-portal` module.
3.  Clear the value in the "Home Page View" field and save.

## Advanced Technical Concepts

### Computed Fields

Computed fields dynamically calculate their values based on other data. For example, the `PaymentCollectionItemAmountProvider` automatically calculates the `amountPaid`, `amountPending`, and `status` for a fee item whenever a payment is made, saving the need for real-time calculations.

### Subscribers

Subscribers execute custom logic in response to database events. The `MediaTransactionSubscriber` is a key example. When an Excel file of student fees is uploaded, this subscriber listens for the `afterInsert` event on the `Media` entity, then reads the file, creates or updates student records, and generates the corresponding fee items.

### UI Building Logic & Handlers

The SolidX UI is built dynamically from metadata. Handlers are a powerful extension system to inject custom logic into the UI. They can be used for dynamic form rendering, custom validations, or workflow logic without modifying the core codebase.

### Composite Indexes

Composite indexes span multiple columns to speed up queries and enforce multi-column uniqueness. For instance, a composite index on `(instituteId, studentId)` would ensure that a student ID is unique within a specific institute and would accelerate queries filtering by both fields.

### Scheduled Jobs

SolidX can automate backend tasks using scheduled jobs. These are useful for recurring tasks like sending late fee reminders, syncing data, or running cleanup processes. Jobs can be configured to run at specific intervals and are scoped to modules.


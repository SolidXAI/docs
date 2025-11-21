---
sidebar_position: 1
---

# School Fees Portal Tutorial

## Introduction

Building a Fee Collection Platform for Educational Institute

Managing and collecting student fees efficiently remains a challenge for many educational Institute. Traditional methods often involve manual processes, fragmented systems, and lack transparency for both administrators and students. This tutorial will walk through the process of building a hosted, multi-tenant fee collection platform tailored for educational Institute using SolidX.

By the end of this tutorial, you will have a functional application that allows Institute to:

-   Onboard themselves and manage their own students and fee structures.
-   Create a payment portal for the institue to manage payments for students/guardians.
-   Initiate fee collection requests by uploading structured data.
-   Process payments through an integrated payment gateway.
-   Automate reminders and notifications for pending payments.
-   Generate reports and manage financial records, including refunds.

You will learn how to leverage SolidX's low-code capabilities to rapidly model a complex domain, automatically generate APIs and admin interfaces, and customize the application to meet specific business requirements.

## User Roles

We'll support two main user types:

### Super Admin
- Onboards new institute.
- Configures the fee types for the institute.
- Manages admin users for institute.
- Can initiate payment requests.
- Configure payment portal for the institute to collect/manage payments.

### Institute Admin
- Belongs to a specific institute.
- Uploads payment collection details
- Tracks payments and generates reports

### TODO: Other users e.g. Students, etc...


## Key Use Cases

### 1. Onboarding an Educational Institute

The onboarding process includes:

- Creating a new Institute.
- Adding Institute details:
  - Name
  - Domain
  - Logo
  - Fee types (e.g., Tuition, Bus, Library, Semester 1)
- Adding Institute admin users.
- Creating a hosted website (e.g., `https://my-institute.edu.com`)

### 2. Configuring the website

Each Institute will have a institute payment portal where students or guardians can:

- Log in using email/mobile
- View due and historical payments
- Make due payments.

> The page design will be standardized, with only the Institute branding (like logo) customized.


> TODO: creating a sub-domain on solidxai.com


### 3. Initiating Payment Collections

Admins can initiate payment collection by uploading CSV/Excel files with payment details for a particular institute.

Each upload:

- Contains fee details for multiple students
- Contains fee details for different fee types.

>Each upload creates records for students, payment collections records and triggers email notifications to students/guardians about due payments.

<!-- > Optionally, WhatsApp or SMS notifications can be integrated in the future. -->

### 4. Making a Payment

Students/Guardians will receive emails with institute:

- TODO: details of payment flow...
- They see a breakdown of fees due by category (e.g., Semester 1, Bus, etc.)
- They can choose to make partial/full payments.
- The platform integrates with a payment gateway to process transactions
- Real-time updates are reflected in the system's records

### 5. Notifications

The system supports the following types of notifications via emails:

- **Fee Due Reminders:** Weekly reminders for pending or partially paid fees to institute students.
- **New Payment Request:** Sent when new payment requests are uploaded to institute students.


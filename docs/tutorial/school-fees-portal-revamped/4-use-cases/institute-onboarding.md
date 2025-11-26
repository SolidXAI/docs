---
sidebar_position: 1
---

# Onboarding an Institute

Onboarding an Institute allows platform-level Admins to create and configure new institutes within a multi-tenant fees management ecosystem.
Each onboarded institute functions as an independent tenant, with complete isolation of its data, configurations, workflows, and integrations.


Each institute functions as a fully isolated tenant with its own dedicated:

- Administrative users & roles

- Payment gateway configurations

- Fee types 

- Student master data

- Branding assets (logo, brochure, promotional video, etc.)

- Payout details, and transaction logs

- Email Notification templates


## Why a Multi-Tenant Architecture?

The School Fees Portal is designed to onboard **N number of institutes**, each working independently.  
This architecture provides:

| Benefit | Explanation |
|--------|-------------|
| **Scalability** | Any number of institutes can be added without affecting others. |
| **Data Isolation** | Record rules ensure one institute cannot access another’s data. |
| **Customisation** | Each institute has its own fees, admins, branding, and PG setup. |
| **Operational Independence** | If one institute faces issues, others remain unaffected. |
| **Centralised Governance** | Super Admin retains global visibility and control. |

---

## Onboarding Workflow (Step-by-Step)

The onboarding flow is intentionally modular. An institute can start with basic configuration and progressively enable more features. Below is an explanation of each phase of the institute onboarding workflow.

### 1. Institute Profile

The institute profile is the foundational step where the super admin captures the core details of the institute. This includes the Institute's Name, Address, Contact Information, Hoted Page Prefix and Branding elements like the Logo and Intro video.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/ins-1.png)

> **Tip:** Hosted Page Prefix acts as the unique subdomain allocated to each institute.
It must be unique, and once the institute is activated, it becomes the public-facing URL for all hosted pages.

> Example: `https://<hostedpageprefix>.test.com`

### 2. Payment Gateway Details

This phase involves linking the institute's own payment gateway (PG) credentials to the platform. This ensures that all fees collected from students are routed directly to the institute's bank account. The platform securely stores the API keys, secrets, and other credentials required for the integration.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/ins-2.png)

### 3. Support & Policies Declaration

In this step, the institute defines important communication details and policy documents that will be visible to students and parents inside the student portal. These details help establish trust, compliance, and transparency.

#### The configuration includes:

<!-- - **Email Domain:** can be validated against the institute-user, if provided then only matched domain user  (institute -admin ) can be added.
eg. test.com
admin@test.com
admin1@test.com

and if not then any email will be accepted.

- **Support Contact:** The email address and mobile number for support inquiries.
- **Privacy Policy:** How the institute handles and protects user data.
- **Terms and Conditions (T&C):** The rules and guidelines for using the portal.
- **FAQs:** Frequently asked questions about fees, payments, and other portal-related queries. -->

**Email Domain:**
An optional domain restriction used to validate institute admin user accounts.

If a domain is provided (e.g., test.com), only users with matching email domains can be added as institute admins:

- admin@test.com
- admin1@test.com

:::tip 
If no domain is configured, any email address will be accepted.
:::

**Support Contact:**
Official support email address and mobile number for handling inquiries, issues, and general communication.

**Privacy Policy:**
A declaration explaining how the institute collects, uses, stores, and protects student and parent data.

**Terms and Conditions (T&C):**
Guidelines and rules for using the institute’s portal, payment services, and related features.

**FAQs:**
Commonly asked questions regarding fee payments, receipts, refunds, deadlines, and general portal usage.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/ins-3.png)

### 4. Fee Types & Late Fee Rules

This is a critical step where the institute defines its fee structure. This includes:

- **Fee Types:** Creating different categories of fees, such as "Tuition Fee," "Hostel Fee," "Library Fee," etc.
- **Late Fee Rules:** Configuring penalties for late payments, which can be a fixed amount or a percentage of the outstanding fee.
- **Part Payment:** Allows the admin to enable or disable partial payment support for fee collection.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/ins-4.png)

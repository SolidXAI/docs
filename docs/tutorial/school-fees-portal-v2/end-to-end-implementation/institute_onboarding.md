---
sidebar_position: 4
title: Institute Onboarding
description: Learn how to onboard educational institutes to the Fees Portal.
summary: TODO
keywords: [TODO]
concerns: TODO
---

## Institute Onboarding

Below are the key features related to managing educational institutes within the Fees Portal:
- Complete institute profile management (name, address, contact details)
- Payment gateway configuration per institute
- Custom branding and theming for student portals
- Support personnel information setup
- Multi-tenant architecture supporting multiple institutes i.e (Institute Admins can only see/ manage their own institute data)

### Roles Involved
- Platform Admin
- Institute Admin

You can refer to the [User Roles & Responsibilities](./fees_portal_product_overview#user-roles--responsibilities) in the Product Overview for more details on these roles.

### Data Models Involved

This section describes the data models you need to implement this feature.

#### 1. Institute Model

**What it represents:** Your educational institution (school, college, university) that will collect fees through the portal.

###### Basic Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Institute Name** | Yes | The official name of your institution. Must be unique. | "St. Mary's High School" |
| **Logo** | Yes | Your institution's logo (image file, max 5MB) | Upload .jpg or .png file |
| **Description** | No | Brief description of your institution | "A premier institution established in 1995..." |
| **Institute Address** | No | Complete postal address | "123 Main Street, Mumbai, Maharashtra 400001" |

###### Contact Details

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Support Email** | Yes | Email where parents/students can reach for help | support@stmaryschool.edu |
| **Support Mobile** | Yes | 10-digit contact number for support | 9876543210 |
| **Email Domain** | No | Your institution's email domain (for user validation) | stmaryschool.edu |

###### Payment Gateway Configuration

These credentials will be provided by your payment gateway provider. You'll need them to process payments.

| Field | Required? | Description |
|-------|-----------|-------------|
| **Cust Code** | Yes | Your unique merchant ID from the payment gateway |
| **Access Key** | Yes | API access key for authentication |
| **Access Secret** | Yes | Secret key for secure authentication (keep confidential) |
| **Cust UserID** | Yes | Your customer user identifier |

###### Website & Portal Settings

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Hosted Page Prefix** | Yes | Subdomain for your payment page. Must be unique. | "stmary" creates stmary-edu.antpay.live |
| **Status** | Auto-set | Portal status (starts as "InActive", activate when ready) | InActive → Active |

###### Legal & Content (Optional)

| Field | Required? | Description |
|-------|-----------|-------------|
| **GST Number** | No | Your institution's GST registration number |
| **Terms and Conditions** | No | Legal terms users must accept during payment |
| **FAQs** | No | Frequently asked questions to help users |
| **Privacy Policy** | No | Your data privacy policy |
| **Institute Brochure** | No | Downloadable brochure document (max 5MB) |
| **Institute Intro Video** | No | Introduction video about your institution (max 5MB) |

###### What you can do with this model:
- Each institute can manage multiple fee types (tuition, bus fees, etc.)
- Each institute can have multiple admin users
- When you delete an institute, all its fee types and users are automatically removed

#### 2. Fee Type Model

**What it represents:** Different categories of fees your institution collects (e.g., Tuition Fees, Bus Fees, Hostel Fees, Library Fees, Sports Fees).

###### Basic Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Fee Type** | Yes | Name of this fee category | "Tuition Fees", "Bus Fees", "Lab Fees" |
| **Institute** | Yes | Which institute this fee type belongs to | Select from dropdown |

###### Payment Rules

| Field | Required? | Description | When to Use |
|-------|-----------|-------------|-------------|
| **Part Payment Allowed** | Yes | Can students pay in installments? | • Select **Yes** for expensive fees (like tuition)<br/>• Select **No** for smaller fees that should be paid in full |

###### Late Payment Policy

Configure how you want to handle late payments:

| Field | Required? | Description | Options & Examples |
|-------|-----------|-------------|-------------------|
| **Late Payment Fees Type** | No | How to calculate late fees | • **None**: No penalty<br/>• **Percent**: Percentage of amount (e.g., 5% of ₹10,000 = ₹500)<br/>• **Absolute**: Fixed amount (e.g., ₹100 flat fee) |
| **Late Payment Fees** | No | The fee amount or percentage | • If Percent: Enter 5 (for 5%)<br/>• If Absolute: Enter 100 (for ₹100) |

###### Important Notes:

**Uniqueness Rule:** You cannot create duplicate fee types for the same institute. For example:
- **Valid:** ABC School can have "Tuition Fees"
- **Valid:** XYZ School can also have "Tuition Fees"
- **Invalid:** ABC School cannot have two "Tuition Fees" entries

**Auto-Generated Field:** The system automatically creates a unique identifier by combining the fee type and institute name (e.g., "tuition-fees-abc-school"). You don't need to enter this.

###### Decision Guide:

**When to allow partial payments:**
- **Yes:** Large annual fees (tuition, annual bus fees)
- **Yes:** Fees where families might need flexibility
- **No:** Small one-time fees (exam fees, certificate fees)
- **No:** Fees that must be paid upfront (admission fees)

**Choosing a late fee strategy:**
- **None**: Good for short-term collections where you follow up personally
- **Percent**: Fair for larger amounts (late fee scales with amount owed)
- **Absolute**: Simple and predictable for any amount

#### 3. Institute User Model

**What it represents:** Administrative staff who will manage the fees portal for your institution.

###### Basic Information

These fields are automatically provided by the system's user management:

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Email** | Yes | Login email address (must be unique) | admin@stmaryschool.edu |
| **Password** | Yes | Secure login password | Set during user creation |
| **First Name** | Yes | User's first name | John |
| **Last Name** | Yes | User's last name | Smith |

###### Role & Access

| Field | Required? | Description | Options |
|-------|-----------|-------------|---------|
| **User Type** | Yes | What role should this user have? | • **Institute Admin**<br/>• **Platform Admin** |
:::info
Platform Admin needs to be created only once for the entire system. They can manage all institutes. This can be done using the SolidX IAM user management module.
:::

###### Understanding User Roles:

**Institute Admin** - Choose this for regular staff managing a single institution
- **Can:** Create and manage fee types for their institution
- **Can:** Create payment collection requests
- **Can:** Manage student records
- **Cannot:** Create new institutions
- **Cannot:** Access other institutions' data
- **Cannot:** Change system settings

**Platform Admin** - Choose this for super administrators managing the entire platform
- **Can:** Create and manage all institutions
- **Can:** Access data across all institutions
- **Can:** Activate/deactivate institution portals
- **Can:** Perform system-wide operations

###### Who needs access?

Typical users you'll create:
- Principal or Admin Office staff → **Institute Admin**
- Accounts department staff → **Institute Admin**
- Fee collection desk staff → **Institute Admin**
- Platform super administrator → **Platform Admin**

#### How These Models Connect

Understanding the relationships between your data:

```
Your Institution
  ├── Collects multiple types of fees
  │   └── Example: Tuition, Bus, Hostel, Lab, Sports fees
  │
  └── Has multiple admin users managing it
      └── Example: Principal, Accountant, Desk Staff

Each Fee Type
  └── Belongs to one institution
      └── Your "Tuition Fees" is separate from another school's "Tuition Fees"

Each Institute Admin User
  └── Manages one institution
      └── Cannot access other institutions' data
```

### Building the Data Models

:::info
You can refer to the [Module Builder](../../admin-docs/module-builder/index.md) for additional details on creating data models in SolidX.
:::

### Setup Sequence

Follow this order when implementing this feature:

#### Phase 1: Platform Admin Setup

**Step 1: Login**
- Log in to the SolidX platform using Platform Admin credentials

**Step 2: Create the Institution**
- Enter basic details (name, address, contact info)
- Upload your logo
- Enter payment gateway credentials (from your provider)
- Choose a unique subdomain prefix for your payment page
- Your portal will start in "InActive" status

**Step 3: Create Institute Admin Users**
- Add staff members who will manage the portal
- Set their role as "Institute Admin"
- Link them to the institution created in Step 2
- Note the login credentials for these users

**Step 4: Activate the Institute**
- Access the Institute from the Institute listing page
- Change the status from "InActive" to "Active"
- The institution portal is now ready for configuration

#### Phase 2: Institute Admin Configuration

**Step 5: Login**
- Institute Admin user logs in using the credentials created in Step 3

**Step 6: Add Fee Types**
- Access the Institute from the Institute listing page
- Edit the Institute to add different fee types
- List all fee categories you collect (e.g., Tuition, Bus, Hostel)
- For each fee type, decide:
  - Can students pay in parts?
  - Do you charge late fees? If yes, how much?

Congrats! You've successfully onboarded an institution. Now we can move on to creating payment collections and managing student payments.

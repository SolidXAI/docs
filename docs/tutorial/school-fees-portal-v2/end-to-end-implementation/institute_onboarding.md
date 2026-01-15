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

This section provides step-by-step instructions for creating the Institute, Institute User, and Fee Type models using SolidX. Follow these instructions to implement the data models discussed in the previous section.

#### 1. Creating the Institute Model

Navigate to the model creation interface in SolidX and configure as follows:

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | institute |
| **Plural Name** | institutes |
| **Display Name** | Institute |
| **Description** | The institute name... |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_institute |
| **Enable Audit Tracking** | ✓ Yes |
| **Enable Soft Delete** | ☐ No |
| **Draft Publish Workflow** | ☐ No |
| **Internationalization** | ☐ No |
| **Is Child Model** | ☐ No |

##### Field Definitions

Create the following fields in the order listed:

**Field 1: Institute Name**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteName |
| **Display Name** | Institute Name |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Index** | ✓ Yes |
| **Is User Key** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 2: Logo**

| Attribute | Value |
|-----------|-------|
| **Name** | logo |
| **Display Name** | Logo |
| **Type** | Media (Single) |
| **Media Types** | image |
| **Media Max Size (KB)** | 5120 |
| **Required** | ✓ Yes |
| **Storage Provider** | default-filesystem |

**Field 3: Description**

| Attribute | Value |
|-----------|-------|
| **Name** | description |
| **Display Name** | Description |
| **Type** | Long Text |
| **Required** | ☐ No |

**Field 4: Payment Gateway Merchant ID**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentGatewayMerchantId |
| **Display Name** | Cust Code |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 5: Payment Gateway Access Key**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentGatewayAccessKey |
| **Display Name** | Access Key |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 6: Payment Gateway Access Secret**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentGatewayAccessSecret |
| **Display Name** | Access Secret |
| **Description** | Access Secret Key |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 7: Institute Address**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteAddress |
| **Display Name** | Institute Address |
| **Type** | Long Text |
| **Required** | ☐ No |

**Field 8: Fee Types Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | feeTypes |
| **Display Name** | FeeTypes |
| **Description** | FeeTypes |
| **Type** | Relation |
| **Relation Type** | One-to-Many |
| **Related Model** | feeType |
| **Related Module** | fees-portal |
| **Related Field** | institute |
| **Create Inverse** | ✓ Yes |
| **Cascade** | cascade |
| **Enable Audit Tracking** | ✓ Yes |

**Field 9: Institute Users Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteUsers |
| **Display Name** | InstituteUsers |
| **Description** | InstituteUsers |
| **Type** | Relation |
| **Relation Type** | One-to-Many |
| **Related Model** | instituteUser |
| **Related Module** | fees-portal |
| **Related Field** | institute |
| **Create Inverse** | ✓ Yes |
| **Cascade** | cascade |
| **Enable Audit Tracking** | ✓ Yes |

**Field 10: Institute Brochure**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteBrochure |
| **Display Name** | Institute Brochure |
| **Type** | Media (Single) |
| **Media Types** | file |
| **Media Max Size (KB)** | 5120 |
| **Required** | ☐ No |
| **Storage Provider** | default-filesystem |

**Field 11: Institute Intro Video**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteIntroVideo |
| **Display Name** | Institute Intro Video |
| **Type** | Media (Single) |
| **Media Types** | video |
| **Media Max Size (KB)** | 5120 |
| **Required** | ☐ No |
| **Storage Provider** | default-filesystem |

**Field 12: Support Email**

| Attribute | Value |
|-----------|-------|
| **Name** | supportEmail |
| **Display Name** | Support Email |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 13: Support Mobile**

| Attribute | Value |
|-----------|-------|
| **Name** | supportMobile |
| **Display Name** | Support Mobile |
| **Type** | Short Text |
| **Min Length** | 10 |
| **Max Length** | 10 |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 14: GST**

| Attribute | Value |
|-----------|-------|
| **Name** | gst |
| **Display Name** | GST |
| **Type** | Short Text |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

**Field 15: Terms and Conditions**

| Attribute | Value |
|-----------|-------|
| **Name** | tnC |
| **Display Name** | Terms and Conditions |
| **Type** | Rich Text |
| **Required** | ☐ No |

**Field 16: FAQs**

| Attribute | Value |
|-----------|-------|
| **Name** | faqs |
| **Display Name** | FAQS |
| **Type** | Rich Text |
| **Required** | ☐ No |

**Field 17: Privacy Policy**

| Attribute | Value |
|-----------|-------|
| **Name** | privacyPolicy |
| **Display Name** | Privacy Policy |
| **Type** | Rich Text |
| **Required** | ☐ No |

**Field 18: Email Domain**

| Attribute | Value |
|-----------|-------|
| **Name** | emailDomain |
| **Display Name** | Email Domain |
| **Type** | Short Text |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

**Field 19: Customer User ID**

| Attribute | Value |
|-----------|-------|
| **Name** | custUserId |
| **Display Name** | Cust UserID |
| **Description** | Customer UserID |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ☐ No |

**Field 20: Hosted Page Prefix**

| Attribute | Value |
|-----------|-------|
| **Name** | hostedPagePrefix |
| **Display Name** | Hosted Page Prefix |
| **Description** | Final domain: hostedPagePrefix-baseSuffix.subdomain |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 21: Status**

| Attribute | Value |
|-----------|-------|
| **Name** | status |
| **Display Name** | Status |
| **Description** | Workflow field used to track the workflow status of this Institute. |
| **Type** | Selection (Static) |
| **Default Value** | InActive |
| **Selection Values** | InActive:InActive, Active:Active |
| **Value Type** | string |
| **Index** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |
| **Multi-Select** | ☐ No |

#### 2. Creating the Fee Type Model

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | feeType |
| **Plural Name** | feeTypes |
| **Display Name** | Fee Type |
| **Description** | Model used to capture different fee types that a school, institute might use. |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_fee_type |
| **Enable Audit Tracking** | ✓ Yes |
| **Enable Soft Delete** | ☐ No |
| **Draft Publish Workflow** | ☐ No |
| **Internationalization** | ☐ No |
| **Is Child Model** | ☐ No |

##### Field Definitions

**Field 1: Fee Type**

| Attribute | Value |
|-----------|-------|
| **Name** | feeType |
| **Display Name** | Fee Type |
| **Description** | The actual fee type. Eg. Tuition Fees, Bus Fees |
| **Type** | Short Text |
| **Required** | ✓ Yes |
| **Is User Key** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 2: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Related Field** | feeTypes |
| **Create Inverse** | ✓ Yes |
| **Cascade** | cascade |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 3: Part Payment Allowed**

| Attribute | Value |
|-----------|-------|
| **Name** | partPaymentAllowed |
| **Display Name** | Part Payment Allowed |
| **Type** | Boolean |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 4: Late Payment Fees Type**

| Attribute | Value |
|-----------|-------|
| **Name** | latePaymentFeesType |
| **Display Name** | Late Payment Fees Type |
| **Type** | Selection (Static) |
| **Default Value** | None |
| **Selection Values** | None:None, Percent:Percent, Absolute:Absolute |
| **Value Type** | string |
| **Enable Audit Tracking** | ✓ Yes |
| **Multi-Select** | ☐ No |

**Field 5: Late Payment Fees**

| Attribute | Value |
|-----------|-------|
| **Name** | latePaymentFees |
| **Display Name** | Late Payment Fees |
| **Type** | Decimal |
| **Default Value** | 0 |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

**Field 6: Fee Type User Key (Computed)**

| Attribute | Value |
|-----------|-------|
| **Name** | feeTypeUserKey |
| **Display Name** | Fee Type User Key |
| **Description** | Concatenation of fee type and institute name |
| **Type** | Computed |
| **Computed Value Type** | string |
| **Value Provider** | ConcatEntityComputedFieldProvider |
| **Provider Context** | `{"fields": ["feeType", "institute.instituteName"], "separator": "-", "slugify": true}` |
| **Trigger Operations** | before-insert |
| **Trigger Model** | feeType |
| **Trigger Module** | fees-portal |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Is User Key** | ✓ Yes |

#### 3. Creating the Institute User Model

##### Model Configuration

| Setting | Value |
|---------|-------|
| **Singular Name** | instituteUser |
| **Plural Name** | instituteUsers |
| **Display Name** | Institute User |
| **Description** | This table allows us to store institute user records |
| **Data Source** | default |
| **Data Source Type** | postgres |
| **Table Name** | fees_portal_institute_user |
| **Enable Audit Tracking** | ✓ Yes |
| **Enable Soft Delete** | ☐ No |
| **Draft Publish Workflow** | ☐ No |
| **Internationalization** | ☐ No |
| **Is Child Model** | ✓ Yes |
| **Parent Model** | user |

##### Field Definitions

**Field 1: User Type**

| Attribute | Value |
|-----------|-------|
| **Name** | userType |
| **Display Name** | User Type |
| **Type** | Selection (Static) |
| **Default Value** | Institute Admin |
| **Selection Values** | Mswipe Admin:Mswipe Admin, Institute Admin:Institute Admin |
| **Value Type** | string |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |
| **Multi-Select** | ☐ No |

**Field 2: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | Relation |
| **Relation Type** | Many-to-One |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Create Inverse** | ☐ No |
| **Cascade** | cascade |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

#### Field Type Reference

When creating fields in SolidX, use this mapping guide:

| Field Type in SolidX | When to Use | Key Attributes to Set |
|---------------------|-------------|----------------------|
| **Short Text** | Names, emails, IDs, brief content | `required`, `unique`, `min`, `max`, `isUserKey` |
| **Long Text** | Addresses, descriptions | `required` |
| **Rich Text** | Formatted content (T&C, FAQs) | `required` |
| **Boolean** | Yes/No flags | `required`, `defaultValue` |
| **Decimal** | Money amounts, percentages | `required`, `defaultValue`, `min`, `max` |
| **Selection (Static)** | Fixed dropdown options | `selectionStaticValues`, `defaultValue`, `isMultiSelect` |
| **Media (Single)** | File uploads | `mediaTypes`, `mediaMaxSizeKb`, `mediaStorageProviderUserKey` |
| **Relation** | Links between models | `relationType`, `relationCoModelSingularName`, `relationCoModelFieldName`, `relationCascade` |
| **Computed** | Auto-calculated fields | `computedFieldValueProvider`, `computedFieldValueProviderCtxt`, `computedFieldTriggerConfig` |
| **Datetime** | Date and time values | `required` |

#### Important Configuration Notes

**Relation Types:**
- **One-to-Many**: Parent has multiple children (Institute → Fee Types)
- **Many-to-One**: Child belongs to parent (Fee Type → Institute)
- Always set both sides when `relationCreateInverse` is true

**Cascade Options:**
- **cascade**: Delete children when parent is deleted
- Use for tightly coupled data (Institute and its Fee Types)

**Audit Tracking:**
- Enable on fields that need change history
- Typically enabled for business-critical fields
- Not needed for computed or temporary fields

**User Key Fields:**
- Mark fields that uniquely identify records
- Used in URLs and references
- Should be human-readable and unique

**Index Fields:**
- Enable for fields used in searches and filters
- Improves query performance
- Typically applied to status fields and foreign keys

**Media Storage:**
- `default-filesystem`: Stored on local server disk
- `default-aws-s3`: Cloud Storage (Amazon S3)
- Set appropriate size limits based on content type

**Child Models:**
- Inherit from a parent model (Institute User extends User)
- Share parent's primary key
- Get base fields automatically from parent

#### Validation After Creation

After creating each model, verify:

1. All required fields are marked correctly
2. Unique constraints are set where needed
3. Relations are bidirectional (if `relationCreateInverse` is true)
4. Default values are appropriate
5. Audit tracking is enabled on business-critical fields
6. Media storage providers are configured
7. Computed field triggers are set correctly

:::info
For more detailed guidance on creating Modules, Models, and Fields in SolidX, refer to the [Module Builder](../../admin-docs/module-builder/index.md) documentation.
:::

### Data Setup

Follow this order when implementing this feature:

#### Phase 1: Login As Platform Admin 

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

#### Phase 2: Login As Institute Admin

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

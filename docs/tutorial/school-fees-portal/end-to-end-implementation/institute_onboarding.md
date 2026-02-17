---
sidebar_position: 1
title: Institute Onboarding
description: Learn how to onboard educational institutes to the Fees Portal.
summary: TODO
keywords: [TODO]
concerns: TODO
---

### Overview
Below are the key features related to managing educational institutes within the Fees Portal Platform:
- Complete institute profile management (name, address, contact details)
- Payment gateway configuration per institute
- Custom branding and theming for student portals
- Support personnel information setup
- Multi-tenant architecture supporting multiple institutes i.e (Institute Admins can only see/ manage their own institute data)

### Roles Involved
- Platform Admin
- Institute Admin

You can refer to the [User Roles & Responsibilities](../fees_portal_product_overview/#user-roles--responsibilities) in the Product Overview for more details on these roles.

### Data Models Involved

This section describes the data models you need to implement this feature.

#### 1. Institute Model

**What it represents:** Your educational institution (school, college, university) that will collect fees through the portal.

###### Basic Information

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Institute Name** | Yes | The official name of your institution. Must be unique. | "Delhi Public School" |
| **Logo** | Yes | Your institution's logo (image file, max 5MB) | Upload .jpg or .png file |
| **Description** | No | Brief description of your institution | "Leading CBSE school in New Delhi" |
| **Institute Address** | No | Complete postal address | "Delhi Public School, Mathura Road, New Delhi 110003" |

###### Contact Details

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Support Email** | Yes | Email where parents/students can reach for help | support@dpsschools.edu.in |
| **Support Mobile** | Yes | 10-digit contact number for support | 9876543210 |
| **Email Domain** | No | Your institution's email domain (for user validation) | dpsschools.edu.in |

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
| **Hosted Page Prefix** | Yes | Unique subdomain prefix for the institute's payment portal. No two institutes can share the same prefix. | If set to `delhi`, the portal URL becomes `delhi.<your-configured-domain>` (e.g., `delhi.dpsschools.edu.in`). The base domain is configured via environment variables. |
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

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Email** | Yes | Login email address (must be unique) | admin@dpsschools.edu.in |
| **Password** | Yes | Secure login password | Set during user creation |
| **First Name** | Yes | User's first name | Rajesh |
| **Last Name** | Yes | User's last name | Sharma |

###### Role & Access

| Field | Required? | Description | Options |
|-------|-----------|-------------|---------|
| **User Type** | Yes | What role should this user have? | Institute Admin (readonly and defaulted) <br/> |

###### Understanding User Roles:

**Institute Admin** - Choose this for regular staff managing a single institution
- **Can:** Create and manage fee types for their institution
- **Can:** Create payment collection requests
- **Can:** Manage student records
- **Cannot:** Create new institutions
- **Cannot:** Access other institutions' data
- **Cannot:** Change system settings

###### Who needs access?

Typical users you'll create:
- Principal or Admin Office staff → **Institute Admin**
- Accounts department staff → **Institute Admin**
- Fee collection desk staff → **Institute Admin**

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

:::tip New to the Module Builder?
If you're unfamiliar with how modules, models, and fields work in SolidX, we recommend reviewing the [Module Builder](../../../admin-docs/module-builder/) documentation first. It covers:
- [Module Management](../../../admin-docs/module-builder/module-management) - Creating and configuring modules
- [Model Management](../../../admin-docs/module-builder/model-management) - Creating models and understanding model settings
- [Field Management](../../../admin-docs/module-builder/field-management) - Understanding field types and configuration options
:::

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
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
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
| **Type** | [Media (Single)](../../../admin-docs/module-builder/field-management#single-media) |
| **Media Types** | image |
| **Media Max Size (KB)** | 5120 |
| **Required** | ✓ Yes |
| **Storage Provider** | default-filesystem |

**Field 3: Description**

| Attribute | Value |
|-----------|-------|
| **Name** | description |
| **Display Name** | Description |
| **Type** | [Long Text](../../../admin-docs/module-builder/field-management#long-text) |
| **Required** | ☐ No |

**Field 4: Payment Gateway Merchant ID**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentGatewayMerchantId |
| **Display Name** | Cust Code |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 5: Payment Gateway Access Key**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentGatewayAccessKey |
| **Display Name** | Access Key |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 6: Payment Gateway Access Secret**

| Attribute | Value |
|-----------|-------|
| **Name** | paymentGatewayAccessSecret |
| **Display Name** | Access Secret |
| **Description** | Access Secret Key |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 7: Institute Address**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteAddress |
| **Display Name** | Institute Address |
| **Type** | [Long Text](../../../admin-docs/module-builder/field-management#long-text) |
| **Required** | ☐ No |

**Field 8: Fee Types Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | feeTypes |
| **Display Name** | FeeTypes |
| **Description** | FeeTypes |
| **Type** | [Relation](../../../admin-docs/module-builder/field-management#relation) |
| **Relation Type** | [One-to-Many](../../../admin-docs/module-builder/field-management#3-one-to-many) |
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
| **Type** | [Relation](../../../admin-docs/module-builder/field-management#relation) |
| **Relation Type** | [One-to-Many](../../../admin-docs/module-builder/field-management#3-one-to-many) |
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
| **Type** | [Media (Single)](../../../admin-docs/module-builder/field-management#single-media) |
| **Media Types** | file |
| **Media Max Size (KB)** | 5120 |
| **Required** | ☐ No |
| **Storage Provider** | default-filesystem |

**Field 11: Institute Intro Video**

| Attribute | Value |
|-----------|-------|
| **Name** | instituteIntroVideo |
| **Display Name** | Institute Intro Video |
| **Type** | [Media (Single)](../../../admin-docs/module-builder/field-management#single-media) |
| **Media Types** | video |
| **Media Max Size (KB)** | 5120 |
| **Required** | ☐ No |
| **Storage Provider** | default-filesystem |

**Field 12: Support Email**

| Attribute | Value |
|-----------|-------|
| **Name** | supportEmail |
| **Display Name** | Support Email |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 13: Support Mobile**

| Attribute | Value |
|-----------|-------|
| **Name** | supportMobile |
| **Display Name** | Support Mobile |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Min Length** | 10 |
| **Max Length** | 10 |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 14: GST**

| Attribute | Value |
|-----------|-------|
| **Name** | gst |
| **Display Name** | GST |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

**Field 15: Terms and Conditions**

| Attribute | Value |
|-----------|-------|
| **Name** | tnC |
| **Display Name** | Terms and Conditions |
| **Type** | [Rich Text](../../../admin-docs/module-builder/field-management#rich-text) |
| **Required** | ☐ No |

**Field 16: FAQs**

| Attribute | Value |
|-----------|-------|
| **Name** | faqs |
| **Display Name** | FAQS |
| **Type** | [Rich Text](../../../admin-docs/module-builder/field-management#rich-text) |
| **Required** | ☐ No |

**Field 17: Privacy Policy**

| Attribute | Value |
|-----------|-------|
| **Name** | privacyPolicy |
| **Display Name** | Privacy Policy |
| **Type** | [Rich Text](../../../admin-docs/module-builder/field-management#rich-text) |
| **Required** | ☐ No |

**Field 18: Email Domain**

| Attribute | Value |
|-----------|-------|
| **Name** | emailDomain |
| **Display Name** | Email Domain |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

**Field 19: Customer User ID**

| Attribute | Value |
|-----------|-------|
| **Name** | custUserId |
| **Display Name** | Cust UserID |
| **Description** | Customer UserID |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ☐ No |

**Field 20: Hosted Page Prefix**

| Attribute | Value |
|-----------|-------|
| **Name** | hostedPagePrefix |
| **Display Name** | Hosted Page Prefix |
| **Description** | Final domain: hostedPagePrefix-baseSuffix.subdomain |
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Unique** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 21: Status**

| Attribute | Value |
|-----------|-------|
| **Name** | status |
| **Display Name** | Status |
| **Description** | Workflow field used to track the workflow status of this Institute. |
| **Type** | [Selection (Static)](../../../admin-docs/module-builder/field-management#static-selection) |
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
| **Type** | [Short Text](../../../admin-docs/module-builder/field-management#short-text) |
| **Required** | ✓ Yes |
| **Is User Key** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 2: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | [Relation](../../../admin-docs/module-builder/field-management#relation) |
| **Relation Type** | [Many-to-One](../../../admin-docs/module-builder/field-management#1-many-to-one) |
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
| **Type** | [Boolean](../../../admin-docs/module-builder/field-management#boolean) |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |

**Field 4: Late Payment Fees Type**

| Attribute | Value |
|-----------|-------|
| **Name** | latePaymentFeesType |
| **Display Name** | Late Payment Fees Type |
| **Type** | [Selection (Static)](../../../admin-docs/module-builder/field-management#static-selection) |
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
| **Type** | [Decimal](../../../admin-docs/module-builder/field-management#decimal) |
| **Default Value** | 0 |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

**Field 6: Fee Type User Key (Computed)**

| Attribute | Value |
|-----------|-------|
| **Name** | feeTypeUserKey |
| **Display Name** | Fee Type User Key |
| **Description** | Concatenation of fee type and institute name |
| **Type** | [Computed](../../../admin-docs/module-builder/field-management#computed) |
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

:::info Why is this a child model?
The Institute User extends SolidX's built-in User model, inheriting standard fields like email, password, first name, and last name. The child model adds only the fields specific to this application (user type and institute relation). For a deeper look at how child user models work — including overriding user creation logic and backend customization — see [Extending Users](../../../developer-docs/extending/backend-customization/extending-users).
:::

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
| **Type** | [Selection (Static)](../../../admin-docs/module-builder/field-management#static-selection) |
| **Default Value** | Institute Admin |
| **Selection Values** | Institute Admin:Institute Admin |
| **Value Type** | string |
| **Required** | ✓ Yes |
| **Enable Audit Tracking** | ✓ Yes |
| **Multi-Select** | ☐ No |

**Field 2: Institute Relation**

| Attribute | Value |
|-----------|-------|
| **Name** | institute |
| **Display Name** | Institute |
| **Type** | [Relation](../../../admin-docs/module-builder/field-management#relation) |
| **Relation Type** | [Many-to-One](../../../admin-docs/module-builder/field-management#1-many-to-one) |
| **Related Model** | institute |
| **Related Module** | fees-portal |
| **Create Inverse** | ☐ No |
| **Cascade** | cascade |
| **Required** | ☐ No |
| **Enable Audit Tracking** | ✓ Yes |

:::tip Quick Reference
For a handy summary of field types and configuration options used in this tutorial, see:
- 📚 [Field Type Reference](../common/field-types.md) - Quick-reference table of field types and their key attributes
- ⚙️ [Configuration Notes](../common/configuration-notes.md) - Quick tips on relations, cascading, audit tracking, and more

For comprehensive documentation, refer to the [Module Builder](../../../admin-docs/module-builder/) section.
:::

### Generating APIs and UI Components

Once you've created the data models, you'll need to generate the REST APIs and UI components.

:::tip Reference Documentation
📋 For detailed step-by-step instructions, see [Generating APIs and UI Components](../common/code-generation.md)
:::

### Customizing the UI

After generating the code using SolidX, default list and form views are automatically created for each model. However, these default views often need customization to match your specific business requirements and improve user experience. This section explains how to customize these views using the layout JSON configuration.

To learn how to apply these customizations, see [Applying View Customizations](../common/applying-view-customizations.md).

#### Institute Form View Customization (Expected Outcome)
![Institute Form View](/img/tutorial/school-fees-portal-v2/institute_form_view.png)
*Screenshot showing the customized Institute Form View with tabs and organized fields.*

**1. Tabbed Organization (Notebook with Multiple Pages)**

The Institute model has 21 fields covering diverse information types. Displaying all fields on a single page would be overwhelming and difficult to navigate. We organized fields into 5 logical tabs:

| Tab | Purpose | Fields Included |
|-----|---------|-----------------|
| **Institutes** | Core institution information | Name, logo, description, address, brochure, video, hosted page prefix |
| **Payment Gateway Details** | Sensitive payment configuration | Merchant ID, access key, access secret, customer user ID |
| **Support** | Contact and legal information | Email domain, support email/mobile, GST, privacy policy, FAQs, T&C |
| **Fee Types** | Related fee types management | One-to-many relation showing all fee types |
| **Institute Users** | User management | One-to-many relation showing all institute admins |

**Benefits:**
- Reduces cognitive load by grouping related fields
- Separates sensitive payment information from general details
- Makes forms easier to navigate and fill out

**2. Two-Column Layout for Related Fields**

Within the "Institutes" tab, we use a two-column layout:
- **Left Column (col-6)**: "Institutes Basic" - Core identity fields (name, description)
- **Right Column (col-6)**: "Institutes Contact" - Location and access info (address, hosted page prefix)

**Layout JSON Snippet:**

```json
{
  "type": "row",
  "attrs": {
    "name": "sheet-1"
  },
  "children": [
    {
      "type": "column",
      "attrs": {
        "name": "group-1",
        "label": "Institutes Basic",
        "className": "col-6"
      },
      "children": [
        {
          "type": "field",
          "attrs": {
            "name": "instituteName"
          }
        },
        {
          "type": "field",
          "attrs": {
            "name": "description"
          }
        }
      ]
    },
    {
      "type": "column",
      "attrs": {
        "name": "group-1",
        "label": "Institutes Contact",
        "className": "col-6"
      },
      "children": [
        {
          "type": "field",
          "attrs": {
            "name": "instituteAddress",
            "disabled": false
          }
        },
        {
          "type": "field",
          "attrs": {
            "name": "hostedPagePrefix"
          }
        },
        {
          "type": "field",
          "attrs": {
            "name": "status",
            "visible": false,
            "disabled": true
          }
        }
      ]
    }
  ]
}
```

**Benefits:**
- Utilizes screen real estate efficiently
- Groups semantically related information
- Creates visual balance and structure

**3. Full-Width Layout for Media Fields**

Logo, brochure, and intro video fields use full-width columns (`col-12`) with `showLabel: false`:

```json
{
  "type": "column",
  "attrs": {
    "name": "group-1",
    "label": "Institutes Logo",
    "className": "col-12"
  },
  "children": [
    {
      "type": "field",
      "attrs": {
        "name": "logo",
        "disabled": false,
        "showLabel": false
      }
    }
  ]
}
```

**Benefits:**
- Media fields need more space for preview/upload UI
- Column label serves as the field label, avoiding redundancy
- Creates cleaner, less cluttered appearance

**4. Hidden Status Field**

The `status` field is hidden and disabled in the form:

```json
{
  "type": "field",
  "attrs": {
    "name": "status",
    "visible": false,
    "disabled": true
  }
}
```

**Rationale:**
- Status changes are managed through custom action buttons ("Activate Institute", "Deactivate Institute")
- Prevents users from manually editing workflow state
- Ensures status transitions follow business rules

**5. Masked Input for Sensitive Fields**

Payment gateway access secret uses custom widgets:

```json
{
  "type": "field",
  "attrs": {
    "name": "paymentGatewayAccessSecret",
    "viewWidget": "maskedShortTextForm",
    "editWidget": "maskedShortTextEdit"
  }
}
```

**Benefits:**
- Protects sensitive credentials from shoulder surfing
- Maintains security while allowing necessary access
- Similar to password fields in standard forms

**6. Inline Creation for Fee Types**

Fee Types relation enables inline creation:

```json
{
  "type": "field",
  "attrs": {
    "name": "feeTypes",
    "inlineCreate": "true",
    "showFieldLabel": false,
    "showLabel": false
  }
}
```

**Benefits:**
- Users can create fee types directly from institute form
- Reduces navigation between different views
- Maintains context during data entry
- Speeds up initial setup process

**7. Custom Action Buttons**

Two custom buttons are added to the form:
- **Activate Institute**: Transitions status from InActive to Active
- **Deactivate Institute**: Transitions status from Active to InActive

```json
"formButtons": [
  {
    "attrs": {
      "icon": "pi pi-caret-right",
      "name": "InstituteActivateById",
      "label": "Activate Institute",
      "action": "InstituteActivateById",
      "actionInContextMenu": true,
      "openInPopup": true,
      "visible": false
    }
  }
]
```

**Benefits:**
- Easily manage institute activation state
- Makes actions discoverable in context menu
- Provides audit trail for status changes

#### Complete Institute Form Layout JSON

Below is the complete form layout JSON for the Institute model:

<details open>
<summary>Click to expand the complete JSON layout</summary>
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Institute",
    "className": "grid",
    "formButtons": [
      {
        "attrs": {
          "icon": "pi pi-caret-right",
          "name": "InstituteActivateById",
          "className": "p-button-text",
          "label": "Activate Institute",
          "action": "InstituteActivateById",
          "customComponentIsSystem": true,
          "actionInContextMenu": true,
          "openInPopup": true,
          "visible": false
        }
      },
      {
        "attrs": {
          "icon": "pi pi-circle-off",
          "name": "InstituteDeactivateById",
          "className": "p-button-text",
          "label": "Deactivate Institute",
          "action": "InstituteDeactivateById",
          "customComponentIsSystem": true,
          "actionInContextMenu": true,
          "openInPopup": true,
          "visible": false
        }
      }
    ]
  },
  "onFormLayoutLoad": "instituteEditHandler",
  "children": [
    {
      "type": "sheet",
      "attrs": {
        "name": "sheet-1"
      },
      "children": [
        {
          "type": "notebook",
          "attrs": {
            "name": "notebook-1"
          },
          "children": [
            {
              "type": "page",
              "attrs": {
                "name": "page-1",
                "label": "Institutes"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "sheet-1"
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Institutes Basic",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteName"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "description"
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Institutes Contact",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteAddress",
                            "disabled": false
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "hostedPagePrefix"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "status",
                            "visible": false,
                            "disabled": true
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Institutes Logo",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "logo",
                            "disabled": false,
                            "showLabel": false
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Institutes Brochure",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteBrochure",
                            "disabled": false,
                            "showLabel": false
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Institute Intro Video",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteIntroVideo",
                            "disabled": false,
                            "showLabel": false
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "type": "page",
              "attrs": {
                "name": "page-2",
                "label": "Payment Gateway Details"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "sheet-1"
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Payment Gateway Details",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "paymentGatewayMerchantId"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "paymentGatewayAccessKey"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "paymentGatewayAccessSecret",
                            "viewWidget": "maskedShortTextForm",
                            "editWidget": "maskedShortTextEdit"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "custUserId"
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "type": "page",
              "attrs": {
                "name": "page-4",
                "label": "Support"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "sheet-1"
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Basic",
                        "className": "col-6"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "emailDomain",
                            "disabled": false
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "supportEmail"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "supportMobile",
                            "disabled": false
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "gst",
                            "disabled": false
                          }
                        }
                      ]
                    },
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Standard Informational",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "privacyPolicy",
                            "disabled": false
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "faqs"
                          }
                        },
                        {
                          "type": "field",
                          "attrs": {
                            "name": "tnC",
                            "disabled": false
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "type": "page",
              "attrs": {
                "name": "page-5",
                "label": "Fee Types"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "sheet-1"
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Fee Types",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "feeTypes",
                            "inlineCreate": "true",
                            "showFieldLabel": false,
                            "showLabel": false
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "type": "page",
              "attrs": {
                "name": "page-6",
                "label": "Institute Users"
              },
              "children": [
                {
                  "type": "row",
                  "attrs": {
                    "name": "sheet-1"
                  },
                  "children": [
                    {
                      "type": "column",
                      "attrs": {
                        "name": "group-1",
                        "label": "Institute Users",
                        "className": "col-12"
                      },
                      "children": [
                        {
                          "type": "field",
                          "attrs": {
                            "name": "instituteUsers",
                            "inlineCreate": "false",
                            "showFieldLabel": false,
                            "showLabel": false
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```
</details>

#### Fee Type Form View Customizations

**1. Grouped Fields Layout**

Fee Type form organizes fields into three columns:

| Column | Label | Width | Fields |
|--------|-------|-------|--------|
| Column 1 | "Fee Type" | col-6 (half) | Fee type name, part payment allowed |
| Column 2 | "Late Payment" | col-6 (half) | Late payment type, late payment fees |
| Column 3 | "Institute" | col-6 (half) | Institute relation (hidden) |

**Layout JSON Snippet:**

```json
{
  "type": "row",
  "attrs": {
    "name": "sheet-1"
  },
  "children": [
    {
      "type": "column",
      "attrs": {
        "name": "group-1",
        "label": "Fee Type",
        "className": "col-6"
      },
      "children": [
        {
          "type": "field",
          "attrs": {
            "name": "feeType"
          }
        },
        {
          "type": "field",
          "attrs": {
            "name": "partPaymentAllowed"
          }
        }
      ]
    },
    {
      "type": "column",
      "attrs": {
        "name": "group-1",
        "label": "Late Payment",
        "className": "col-6"
      },
      "children": [
        {
          "type": "field",
          "attrs": {
            "name": "latePaymentFeesType"
          }
        },
        {
          "type": "field",
          "attrs": {
            "name": "latePaymentFees"
          }
        }
      ]
    },
    {
      "type": "column",
      "attrs": {
        "name": "group-1",
        "label": "Institute",
        "className": "col-6",
        "visible": false
      },
      "children": [
        {
          "type": "field",
          "attrs": {
            "name": "institute"
          }
        }
      ]
    }
  ]
}
```

**Benefits:**
- Related payment settings grouped together
- Visual separation between core info and payment rules
- Efficient use of screen space

**2. Hidden Institute Field**

The institute relation is hidden (`visible: false`):

```json
{
  "type": "column",
  "attrs": {
    "name": "group-1",
    "label": "Institute",
    "className": "col-6",
    "visible": false
  }
}
```

**Rationale:**
- Institute is already known from context (user's current institute)
- Automatically set by form handler (`feeTypeEditHandler`)
- Prevents users from accidentally assigning fees to wrong institute
- Simplifies form interface

---

#### Complete Fee Type Form Layout JSON

Below is the complete form layout JSON for the Fee Type model:

<details open>
<summary>Click to expand the complete JSON layout</summary>
```json
{
  "type": "form",
  "attrs": {
    "name": "form-1",
    "label": "Fee Type",
    "className": "grid"
  },
  "onFormLayoutLoad": "feeTypeEditHandler",
  "children": [
    {
      "type": "sheet",
      "attrs": {
        "name": "sheet-1"
      },
      "children": [
        {
          "type": "row",
          "attrs": {
            "name": "sheet-1"
          },
          "children": [
            {
              "type": "column",
              "attrs": {
                "name": "group-1",
                "label": "Fee Type",
                "className": "col-6"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "feeType"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "partPaymentAllowed"
                  }
                }
              ]
            },
            {
              "type": "column",
              "attrs": {
                "name": "group-1",
                "label": "Late Payment",
                "className": "col-6"
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "latePaymentFeesType"
                  }
                },
                {
                  "type": "field",
                  "attrs": {
                    "name": "latePaymentFees"
                  }
                }
              ]
            },
            {
              "type": "column",
              "attrs": {
                "name": "group-1",
                "label": "Institute",
                "className": "col-6",
                "visible": false
              },
              "children": [
                {
                  "type": "field",
                  "attrs": {
                    "name": "institute"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```
</details>

#### List View Customizations

**Role-Based Action Permissions**

List views configure which roles can perform specific actions:

```json
"configureViewActions": {
  "import": { "roles": ["Admin"] },
  "showArchived": { "roles": ["Admin"] },
  "export": { "roles": ["Admin", "Mswipe Admin", "Institute Admin"] },
  "customizeLayout": { "roles": ["Admin", "Mswipe Admin", "Institute Admin"] },
  "saveCustomFilter": { "roles": ["Admin"] }
}
```

**Benefits:**
- Enforces role-based access control at UI level
- Reduces clutter by hiding unavailable actions
- Improves security by limiting sensitive operations
- Provides appropriate capabilities based on user role

#### General Design Principles

The customizations follow these principles:

1. **Progressive Disclosure**: Show essential information first, details in tabs
2. **Contextual Relevance**: Hide fields that are auto-populated or irrelevant
3. **Guided Input**: Group related fields to guide users through data entry
4. **Security by Design**: Mask sensitive data, control access to actions
5. **Efficiency**: Enable inline operations to reduce navigation
6. **Consistency**: Use similar patterns across related forms

These customizations transform the auto-generated UI into a polished, user-friendly interface tailored to the fees portal domain.

:::tip Applying Your Customizations
Now that you have the customized layout JSONs ready, follow the steps in [Applying View Customizations](../common/applying-view-customizations.md) to apply them via the Layout Builder.
:::

### Data Setup

Follow this order to set up your data and test if the portal is ready for use:

#### Phase 1: Login As Super Admin 

**Step 1: Login**
- Log in to the SolidX platform using Super Admin credentials i.e (`sa` credentials, created during the initial application setup).

**Step 2: Create the Institution**
- Enter basic details (name, address, contact info)
- Upload your logo
- Enter payment gateway credentials (from your provider)
- Choose a unique subdomain prefix for your payment page

**Step 3: Create Institute Admin Users**
- Add staff members who will manage the portal
- Set their role as "Institute Admin"
- Link them to the institution created in Step 2
- Note the login credentials for these users

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

---
title: Email Templates
description: Metadata schema for populating email templates in SolidX applications.
sidebar_position: 9
---

## Overview
Email Templates in SOLID allow you to create and manage HTML/Text based email templates with dynamic content and attachments.

### Example: Email Templates Metadata
<summary> Email Templates Schema </summary>
``` json
{
  ..., // Other metadata 
  "emailTemplates": [
    {
      "name": "new-payment-or-payment-reminder",
      "displayName": "Fees Portal: New Payment or Reminder",
      "body": "fees-portal-new-payment-or-payment-reminder.handlebars.html",
      "subject": "Reminder for a payment",
      "description": "This template is used to send the reminder email to parent for due payments.",
      "active": true,
      "type": "text"
    },
    {
      "name": "otp-verification",
      "displayName": "Fees Portal: Otp Verification",
      "body": "fees-portal-otp-verification.handlebars.html",
      "subject": "One time password for login",
      "description": "This template is used to send the otp email to parent for login.",
      "active": true,
      "type": "text"
    }
  ]
}
```

## Email Templates Metadata Attributes

### `name` *(string, required, unique)*
Unique name for the email template. It should be in kebab-case format (e.g., `example-template-name`).

---
### `displayName` *(string, required)*
Display name for the email template.

---
### `body` *(string, required)*
In the metadata json, the filename of the email template is specified. The templates are searched for in the `seeders/seed-data/email-templates/` directory of the module.
The body is then replaced with the content of the email template file. This can include HTML or plain text content. The body can include dynamic placeholders using Handlebars syntax (e.g., `{{placeholderName}}`).

#### 📖 Further Reference
 - 📋 **Email Body Creation:** [Email Templates Guide](../../admin-docs/notifications/email-templates.md)

:::note
Please refer to the [Handlebars Documentation](https://handlebarsjs.com/) for more information on using Handlebars syntax in email templates.
:::

---
### `subject` *(string, required)*
Subject line of the email template. It can include dynamic placeholders.

---
### `description` *(string, optional)*
A brief description of the email template.

---
### `active` *(boolean, optional)*
Indicates whether the email template is active. Defaults to `true`.

---
### `type` *(string, optional)*
Type of the email template (e.g., `text`, `html`). Defaults to `text`.
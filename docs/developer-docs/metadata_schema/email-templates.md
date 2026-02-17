---
title: Email Templates
description: Metadata schema for populating email templates in SolidX applications.
summary: This document explains email template metadata in SolidX, which enables creation and management of HTML/text-based email templates with dynamic content and attachments. Templates use Handlebars syntax for variable insertion and are stored in separate HTML files referenced by the metadata. Key attributes include template name, display name, body file reference, subject line, description, active status, and template type (text/html). Examples demonstrate configuring templates for payment reminders and OTP verification, including sample HTML template files with dynamic variables, styling, and layout structures. The system supports template file organization in the solid-api/src directory.
sidebar_position: 9
json_pointer: "/emailTemplates"
jsonpath: "$.emailTemplates"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#email-templates-metadata-attributes"
solidx_concerns: [create/update_email_template, new_email_provider]
---

import { IoIosArrowForward } from "react-icons/io";
import { MdEmail } from "react-icons/md";
import { InfoBox } from '@site/src/common/InfoBox';


# Email Templates
> **Where it lives**  
> **JSON Pointer:** `/emailTemplates`  
> **JSONPath:** `$.emailTemplates`  
> **Parent:** Root of the metadata file


## Overview
Email Templates in `SolidX` allow you to create and manage HTML/Text based email templates with dynamic content and attachments.

### Example: Email Templates Metadata
Below is an example configuration for two email templates: one for sending payment reminders and another for OTP verification. The body of the email templates is stored in separate HTML files i.e (specified in the `body` attribute)
<details open>

<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
 Email Templates Schema
  </summary>

``` json
{
  ..., // Other metadata
  "emailTemplates": [
  {
    "name": "new-payment-or-payment-reminder",
    "displayName": "Fees Portal: New Payment or Reminder",
    "body": "new-payment-or-payment-reminder.handlebars.html",
    "subject": "Reminder for a payment",
    "description": "Reminder email for pending payments",
    "active": true,
    "type": "text"
  },
  {
    "name": "otp-verification",
    "displayName": "Fees Portal: Otp Verification",
    "body": "otp-verification.handlebars.txt",
    "subject": "One time password for login",
    "description": "Send OTP email to parent for login.",
    "active": true,
    "type": "text"
  }
  ]
}
```
</details>

### Example : Email Template File

Below are examples of email template files that can be referenced in the `body` attribute of the email template metadata.

This example uses Handlebars syntax for dynamic content insertion.

The variables used in this template (like `{{student.studentName}}`, `{{dueDetails.totalAmountDue}}`, etc.) should correspond to the data structure passed when sending the email.

<details open>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   Email Template File 
  </summary>

``` html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Payment Notification</title>
  <style>
    body {margin:0; padding:0; background:#e8e8e8; font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif; color:#333;}
    .email-container {max-width:600px; margin:40px auto; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.1);}
    .header-section {background:#f5f5f0; padding:40px; text-align:center;}
    .logo {width:80px; height:80px; margin-bottom:25px;}
    .greeting {font-size:22px; font-weight:600; color:#2c3e50; margin:0 0 10px;}
    .main-message, .main-message-text {font-size:20px; font-weight:600; color:#2c3e50; margin:0 0 15px; line-height:1.4;}
    .ref-number {font-size:16px; color:#555; margin:0 0 10px;}
    .payment-details-section {background:#fff; padding:30px 40px;}
    .section-title {font-size:18px; font-weight:600; color:#2c3e50; margin:0 0 25px;}
    .payment-card {background:#f8f9fa; border-radius:8px; padding:20px; margin-bottom:25px;}
    .payment-header {display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;}
    .payment-logo {width:40px; height:40px;}
    .payment-date {font-size:14px; color:#666; font-weight:500;}
    .payment-row-table {width:100%; border-collapse:collapse; margin-bottom:8px;}
    .payment-row-table td {padding:8px 0; border-bottom:1px solid #e9ecef; vertical-align:middle;}
    .payment-row-table:last-child td {border-bottom:none;}
    .payment-label {font-size:14px; color:#666; width:40%;}
    .payment-value {font-size:14px; color:#333; font-weight:500; text-align:right; width:60%;}
    .amount-value {font-size:16px; font-weight:600; color:#333;}
    .status-pending {color:#ff9800; font-weight:600;}
    .pay-button {background:#1e88e5; color:#fff; text-decoration:none; padding:12px 40px; border-radius:6px; font-weight:600; font-size:16px; display:inline-block; width:100%; text-align:center; box-sizing:border-box;}
    .pay-button:hover {background:#1976d2;}
    .help-section {padding:0 40px 30px;}
    .help-title {font-size:16px; font-weight:600; color:#2c3e50; margin:0 0 15px;}
    .help-text {font-size:14px; color:#666; line-height:1.6; margin:0;}
    .help-link {color:#1e88e5; text-decoration:none;}
    .help-link:hover {text-decoration:underline;}
    .footer-section {background:#fff; padding:30px 40px; text-align:center; border-top:1px solid #eee;}
    .footer-logo {width:60px; height:60px; margin-bottom:20px;}
    .footer-links {font-size:12px;}
    .footer-links a {color:#1e88e5; text-decoration:none; margin:0 8px;}
    .footer-links a:hover {text-decoration:underline;}
    .payment-request {font-size:16px; color:#555; margin:0 0 15px; line-height:1.5;}
    .highlight-blue {color:#1e88e5; font-weight:600;}
    .support-value-email{color:#1e88e5; font-weight:500;}
    .support-value-mobile{color:lightgreen; font-weight:500;}
    @media (max-width:640px){
      .email-container{margin:20px; max-width:none;}
      .header-section,.payment-details-section,.help-section,.footer-section{padding:30px 20px;}
      .main-message,.main-message-text{font-size:18px;}
      .greeting{font-size:20px;}
      .payment-header{flex-direction:column; align-items:flex-start; gap:10px;}
      .pay-button{padding:14px 20px; font-size:14px;}
      .payment-request,.ref-number{font-size:14px;}
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header-section">
      {{#if companyLogoUrl}}<div class="logo"><img src="{{companyLogoUrl}}" alt="Company Logo"/></div>{{/if}}
      {{#with student}}<h1 class="greeting">Hey {{studentName}}</h1>{{/with}}
      <h2 class="main-message">{{student.institute.instituteName}}</h2>
      <p class="payment-request">{{student.institute.instituteName}} institute is requesting you to pay the due payments of Student ID <span class="highlight-blue">{{student.studentLoginId}}</span></p>
      <p class="ref-number">Ref: <span class="highlight-blue">{{dueDetails.paymentCollections}}</span></p>
    </div>
    <div class="payment-details-section">
      <h3 class="section-title">Payment Details</h3>
      <div class="payment-card">
        <div class="payment-header"><img src="logo.svg" alt="School Logo" class="payment-logo"/><span class="payment-date"></span></div>
        <table class="payment-row-table"><tr><td class="payment-label">Total Amount</td><td class="payment-value amount-value">₹ {{dueDetails.totalAmountDue}}</td></tr></table>
        <table class="payment-row-table"><tr><td class="payment-label">Due Date:</td><td class="payment-value">{{dueDetails.createdAt}}</td></tr></table>
        <table class="payment-row-table"><tr><td class="payment-label">Institution:</td><td class="payment-value">{{student.institute.instituteName}}</td></tr></table>
        <table class="payment-row-table"><tr><td class="payment-label">Fee Type:</td><td class="payment-value">{{dueDetails.feeTypes}}</td></tr></table>
        <table class="payment-row-table"><tr><td class="payment-label">Payment Status:</td><td class="payment-value status-pending">Pending</td></tr></table>
      </div>
      <a href="{{dueDetails.redirectUrl}}" class="pay-button">Pay Now</a>
    </div>
    <div class="help-section">
      <h3 class="help-title">Need Assistance?</h3>
      {{#with student}}
        <p class="help-text">If you have any questions, we're just an <a href="mailto:{{student.institute.supportEmail}}" class="help-link">email</a> or <a href="tel:{{student.institute.supportMobile}}" class="help-link">call</a> away.</p>
      {{/with}}
    </div>
    <div class="footer-section">
      {{#if companyLogoUrl}}<div class="logo"><img src="{{companyLogoUrl}}" alt="Company Logo"/></div>{{/if}}
      <div class="footer-links">
        <span class="support-value-email">Support email: {{student.institute.supportEmail}}</span>
        <span class="support-value-email">Support Mobile: {{student.institute.supportMobile}}</span>
      </div>
      <div class="footer-links">
        <a href="{{dueDetails.redirectUrl}}">FAQ</a> | <a href="{{dueDetails.redirectUrl}}">Privacy Policy</a> | <a href="{{dueDetails.redirectUrl}}">Terms and Conditions</a>
      </div>
    </div>
  </div>
</body>
</html>
```
</details>
<details open>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   Email Template File (Text)
  </summary>

```tsx
Hi {{ fullName }},

Thank you for signing up for {{ solidAppName }}!

To complete your registration, please use the following One-Time Password (OTP) to verify your email address:

{{ otp }}

This code is valid for 10 minutes. Please do not share this code with anyone.

If you did not attempt to sign up, please disregard this email.

Regards,  
The {{ solidAppName }} Team  

```
</details>

### Example : Sending Email Using Template

Below is a code snippet demonstrating how to send an email using the defined email templates via the `MailServiceFactory`. This example shows how to send an OTP verification email to a user.

<details open>
<summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   Email Sending Code Snippet
  </summary>

``` ts
// Example: sending an email via the MailServiceFactory

import { Injectable } from '@nestjs/common';
import { MailFactory } from '@solidxai/core';

@Injectable()
export class MailerExampleService {
  constructor(private readonly mailFactory: MailFactory) {}

  async sendOTPEmail(
    user: {  email: string; fullName?: string; username: string },
    otp: string) {
    const mailService = this.mailFactory.getMailService();

    await mailService.sendEmailUsingTemplate(
      user.email,                      // to
      'otp-verification',      // template key
      {
        solidAppName: process.env.SOLID_APP_NAME,
        fullName: user.fullName ?? user.username,
        otp: otp,
      },
      /* shouldQueue */ true,           // or from config
      /* cc */ null,
      /* bcc */ null,
      /* entityType */ 'user',
      /* entityId */ user.id,
    );
  }
}
```
</details>

<h2 className=" card-headear-wrapper">
    <MdEmail size={22} style={{ marginRight: "10px" }} />

## Email Templates Metadata Attributes
</h2>

### `name` *(string, required, unique)*
Unique name for the email template. It should be in kebab-case format (e.g., `example-template-name`).


### `displayName` *(string, required)*
Display name for the email template.


### `body` *(string, required)*
    - In the metadata json, the filename of the email template is specified. The templates are searched for in the `module-metadata/<module-name>/email-templates/` directory of the module.
    - The body is then replaced with the content of the email template file. This can include HTML or plain text content. The body can include dynamic placeholders using Handlebars syntax (e.g., `{{placeholderName}}`), as shown in the [Email Template file](#example--email-template-file) above.

####  Further Reference
 -  **Email Body Creation:** [Email Templates Guide](../../admin-docs/notifications/email-templates.md)





<InfoBox>
Please refer to the [Handlebars Documentation](https://handlebarsjs.com/) for more information on using Handlebars syntax in email templates.
</InfoBox>


### `subject` *(string, required)*
Subject line of the email template. It can include dynamic placeholders.


### `description` *(string, optional)*
A brief description of the email template.


### `active` *(boolean, optional)*
Indicates whether the email template is active. Defaults to `true`.


### `type` *(string, optional)*
Type of the email template (e.g., `text`, `html`). Defaults to `text`.
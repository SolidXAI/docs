---
# title: Email Templates
description: Metadata schema for populating email templates in SolidX applications.
sidebar_position: 9
json_pointer: "/emailTemplates"
jsonpath: "$.emailTemplates"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#email-templates-metadata-attributes"
---

import { IoIosArrowForward } from "react-icons/io";
import { InfoBox } from '@site/src/common/InfoBox';


# Email Templates
> **Where it lives**  
> **JSON Pointer:** `/emailTemplates`  
> **JSONPath:** `$.emailTemplates`  
> **Parent:** Root of the metadata file


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

### Example : Email Template File
<details>
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
    body {
      margin: 0;
      padding: 0;
      background-color: #e8e8e8;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      color: #333;
    }
    .email-container {
      max-width: 600px;
      margin: 40px auto;
      background-color: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .header-section {
      background-color: #f5f5f0;
      padding: 40px 40px 30px 40px;
      text-align: center;
    }
    .logo {
      width: 80px;
      height: 80px;
      margin-bottom: 25px;
    }
    .greeting {
      font-size: 22px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 10px 0;
    }
    .main-message {
      font-size: 20px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 15px 0;
      line-height: 1.4;
    }
    .main-message-text {
      font-size: 20px;
      font-weight: 600;
      color: #2c3e50;
    }
    .ref-number {
      font-size: 16px;
      color: #555;
      margin: 0 0 10px 0;
    }
    .payment-details-section {
      background-color: #ffffff;
      padding: 30px 40px;
    }
    .section-title {
      font-size: 18px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 25px 0;
    }
    .payment-card {
      background-color: #f8f9fa;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 25px;
    }
    .payment-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    .payment-logo {
      width: 40px;
      height: 40px;
    }
    .payment-date {
      font-size: 14px;
      color: #666;
      font-weight: 500;
    }
    /* Table-based layout for Gmail compatibility */
    .payment-row-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 8px;
    }
    .payment-row-table td {
      padding: 8px 0;
      border-bottom: 1px solid #e9ecef;
      vertical-align: middle;
    }
    .payment-row-table:last-child td {
      border-bottom: none;
    }
    .payment-label {
      font-size: 14px;
      color: #666;
      margin: 0;
      width: 40%;
    }
    .payment-value {
      font-size: 14px;
      color: #333;
      font-weight: 500;
      margin: 0;
      text-align: right;
      width: 60%;
    }
    .amount-value {
      font-size: 16px;
      font-weight: 600;
      color: #333;
    }
    .status-pending {
      color: #ff9800;
      font-weight: 600;
    }
    .pay-button {
      background-color: #1e88e5;
      color: white;
      text-decoration: none;
      padding: 12px 40px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 16px;
      display: inline-block;
      transition: background-color 0.3s ease;
      width: 100%;
      text-align: center;
      box-sizing: border-box;
    }
    .pay-button:hover {
      background-color: #1976d2;
    }
    .help-section {
      padding: 0 40px 30px 40px;
    }
    .help-title {
      font-size: 16px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 15px 0;
    }
    .help-text {
      font-size: 14px;
      color: #666;
      line-height: 1.6;
      margin: 0;
    }
    .help-link {
      color: #1e88e5;
      text-decoration: none;
    }
    .help-link:hover {
      text-decoration: underline;
    }
    .footer-section {
      background-color: #ffffff;
      padding: 30px 40px;
      text-align: center;
      border-top: 1px solid #eee;
    }
    .footer-logo {
      width: 60px;
      height: 60px;
      margin-bottom: 20px;
    }
    .footer-links {
      font-size: 12px;
    }
    .footer-links a {
      color: #1e88e5;
      text-decoration: none;
      margin: 0 8px;
    }
    .footer-links a:hover {
      text-decoration: underline;
    }
    .payment-request {
      font-size: 16px;
      color: #555;
      margin: 0 0 15px 0;
      line-height: 1.5;
    }
    .highlight-blue {
      color: #1e88e5;
      font-weight: 600;
    }
    /* Table-based support info for Gmail compatibility */
    .support-info-table {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
      }
    .support-value-email{
      color: #1e88e5;
      font-weight: 500;
    }
    .support-value-mobile{
      color: lightgreen;
      font-weight: 500;
    }
    .support-value{
     display: flex;
     align-items: center;
    }
    
    @media (max-width: 640px) {
      .email-container {
        margin: 20px;
        max-width: none;
      }
      .header-section, .payment-details-section, .help-section, .footer-section {
        padding: 30px 20px;
      }
      .main-message {
        font-size: 18px;
      }
      .main-message-text{
        font-size: 18px;
      }
      .greeting {
        font-size: 20px;
      }
      .payment-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
      }
      .pay-button {
        padding: 14px 20px;
        font-size: 14px;
      }
      .payment-request {
        font-size: 14px;
      }
      .ref-number {
        font-size: 14px;
      }
      
    }
  </style>
</head>
<body>
  <div class="email-container">
    <!-- Header Section -->
    <div class="header-section">
      {{#if companyLogoUrl}}
      <div class="logo">
          <img src="{{companyLogoUrl}}" alt="Company Logo" />
      </div>
      {{/if}}

      {{#with student}}
        <h1 class="greeting">Hey {{studentName}}</h1>
      {{/with}}
      
      <h2 class="main-message">
        {{student.institute.instituteName}}
      </h2>

      <p class="payment-request">
        {{student.institute.instituteName}} institute is requesting you to pay the due payments of Student ID <span class="highlight-blue">{{student.studentLoginId}}</span>
      </p>

      <p class="ref-number">
        Ref: <span class="highlight-blue">{{dueDetails.paymentCollections}}</span>
      </p>
    </div>

    <!-- Payment Details Section -->
    <div class="payment-details-section">
      <h3 class="section-title">Payment Details</h3>
      
      <div class="payment-card">
        <div class="payment-header">
          <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMTkiIGZpbGw9IiNmZmYiIHN0cm9rZT0iI2RkZCIgc3Ryb2tlLXdpZHRoPSIxIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9InN1biIgeDI9IjEwMCUiIHkyPSIxMDAlIj4KPHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6I2ZmYzEwNyIvPgo8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmZjk4MDAiLz4KPC9saW5lYXJHcmFkaWVudD4KPGxpbmVhckdyYWRpZW50IGlkPSJ3YXRlciIgeDI9IjEwMCUiIHkyPSIxMDAlIj4KPHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6IzFlODhlNSIvPgo8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiMwMjc3YmQiLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8Y2lyY2xlIGN4PSIyOCIgY3k9IjEwIiByPSIzIiBmaWxsPSJ1cmwoI3N1bikiLz4KPHBhdGggZD0iTTYgMjZRMTAgMjQgMTQgMjZUMjIgMjZUMzAgMjZUMzggMjZWMzJINloiIGZpbGw9InVybCgjd2F0ZXIpIi8+CjxyZWN0IHg9IjMzIiB5PSIxNiIgd2lkdGg9IjEiIGhlaWdodD0iMiIgZmlsbD0iIzI4YTc0NSIvPgo8cmVjdCB4PSIzNSIgeT0iMTUiIHdpZHRoPSIxIiBoZWlnaHQ9IjIiIGZpbGw9IiMyOGE3NDUiLz4KPC9zdmc+" alt="School Logo" class="payment-logo" />
          <span class="payment-date"></span>
        </div>
        
        <!-- Using table instead of flex for Gmail compatibility -->
        <table class="payment-row-table">
          <tr>
            <td class="payment-label">Total Amount</td>
            <td class="payment-value amount-value"> ₹ {{dueDetails.totalAmountDue}}</td>
          </tr>
        </table>
        
        <table class="payment-row-table">
          <tr>
            <td class="payment-label">Due Date:</td>
            <td class="payment-value">{{dueDetails.createdAt}}</td>
          </tr>
        </table>
        
        <table class="payment-row-table">
          <tr>
            <td class="payment-label">Institution:</td>
            <td class="payment-value">{{student.institute.instituteName}}</td>
          </tr>
        </table>
        
        <table class="payment-row-table">
          <tr>
            <td class="payment-label">Fee Type:</td>
            <td class="payment-value">{{dueDetails.feeTypes}}</td>
          </tr>
        </table>
        
        <table class="payment-row-table">
          <tr>
            <td class="payment-label">Payment Status:</td>
            <td class="payment-value status-pending">Pending</td>
          </tr>
        </table>
      </div>
      
      <a href="{{dueDetails.redirectUrl}}" class="pay-button">Pay Now</a>
    </div>

    <!-- Help Section -->
    <div class="help-section">
      <h3 class="help-title">Need Assistance?</h3>
      {{#with student}}
        <p class="help-text">
          If you have any questions or need help getting started, we're just an <a href="mailto:{{student.institute.supportEmail}}" class="help-link">email</a> or <a href="tel:{{student.institute.supportMobile}}" class="help-link">call on </a> away.
        </p>
      {{/with}}
    </div>

    <!-- Footer Section -->
    <div class="footer-section">
      
      {{#if companyLogoUrl}}
      <div class="logo">
          <img src="{{companyLogoUrl}}" alt="Company Logo" />
      </div>
      {{/if}}      
      <!-- Using table instead of flex for Gmail compatibility -->
      <!-- <table class="support-info-table">
        <tr>
          <td><span class="support-value">{{student.institute.supportEmail}}</span></td>
          <td><span class="support-value">{{student.institute.supportMobile}}</span></td>
        </tr>
      </table> -->

      <!-- <div class="support-info-table">
        <div class="support-value">
          <span class="support-value-email">{{student.institute.supportEmail}}</span>
        </div>
        <div class="support-value">
          <span class="support-value-mobile">{{student.institute.supportMobile}}</span>
        </div>
      </div> -->

      <div class="footer-links">
        <span class="support-value-email">Support email: {{student.institute.supportEmail}}</span>
        <span class="support-value-email">Support Mobile: {{student.institute.supportMobile}}</span>
      </div>
      
      <div class="footer-links">
        <a href="{{dueDetails.redirectUrl}}">FAQ</a> |
        <a href="{{dueDetails.redirectUrl}}">Privacy Policy</a> |
        <a href="{{dueDetails.redirectUrl}}">Terms and Conditions</a>
      </div>
    </div>
  </div>
</body>
</html>
```
</details>

## Email Templates Metadata Attributes

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
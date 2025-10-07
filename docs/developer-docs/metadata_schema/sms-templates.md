---
title: SMS Templates

description: Metadata schema for populating SMS templates in SolidX applications.
summary: This document describes SMS template metadata in SolidX, which allows creation and management of SMS templates with dynamic content using Handlebars syntax. Templates are stored in separate text files referenced by the metadata and support variables for personalization. Key attributes include template name, display name, body file reference, description, SMS provider template ID, active status, and type (text). The document provides examples of OTP login templates with dynamic variable substitution, file organization guidelines, and links to implementing custom SMS providers for integration with external SMS services like Twilio or AWS SNS.
sidebar_position: 10
json_pointer: "/smsTemplates"
jsonpath: "$.smsTemplates"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#email-templates-metadata-attributes"
solidx_concerns: [create/update_sms_template, new_sms_provider]



---
# SMS Templates
> **Where it lives**  
> **JSON Pointer:** `/smsTemplates`  
> **JSONPath:** `$.smsTemplates`  
> **Parent:** Root of the metadata file


import { IoIosArrowForward } from "react-icons/io";
import { MdTextsms } from "react-icons/md";
import { InfoBox } from '@site/src/common/InfoBox';

## Overview
SMS Templates in SOLID allow you to create and manage SMS templates with dynamic content.

### Example: SMS Templates Metadata
Below is an example of configuring an SMS template which sends an OTP when a user logs in.
<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    SMS Templates Schema
  </summary>

``` json
{
  ..., // Other metadata 
  "smsTemplates": [
    {
      "name": "otp-on-login-custom",
      "displayName": "Custom: Otp On Login",
      "body": "otp-on-login-custom.handlebars.txt",
      "description": "Send sms with OTP when logging in.",
      "smsProviderTemplateId": "<TEMPLATE_ID_FROM_SMS_PROVIDER>",
      "active": true,
      "type": "text"
    },

  ]
}
```
</details>

### Example : SMS Template File
Below is an example of the content of the SMS template file `otp-on-login-custom.handlebars.txt` referenced in the above metadata. This file contains the actual SMS message with dynamic placeholders.
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   SMS Template File 
  </summary>

```text
Hi {{ firstName }}, Login to {{ solidAppName }}, using {{ mobileVerificationTokenOnLogin }} as your verification code.
```
</details>

### Example : Sending SMS Using Template (TODO ticket)
Below is a code snippet demonstrating how to send an SMS using the defined SMS templates via the `SmsServiceFactory`. This example shows how to send an OTP verification SMS to a user.
<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    SMS Sending Code Snippet
  </summary>

``` ts
import { SmsServiceFactory } from 'your-sms-service';

async sendOtpSms(user: { mobile: string; firstName?: string; username: string, mobileVerificationTokenOnLogin: string }, otp: string) {
  const smsService = SmsServiceFactory.getSmsService();

  await smsService.sendSmsUsingTemplate(
      user.mobile,
      'otp-on-login',
      {
          solidAppName: process.env.SOLID_APP_NAME,
          mobileVerificationTokenOnLogin: user.mobileVerificationTokenOnLogin,
          firstName: user.username,
          fullName: user.fullName ? user.fullName : user.username,
      }
  );
```
</details>

<h2 className=" card-headear-wrapper">
    <MdTextsms size={22} style={{ marginRight: "10px" }} />

## SMS Templates Metadata Attributes
</h2>

### `name` *(string, required, unique)*
Unique name for the sms template. It should be in kebab-case format (e.g., `example-template-name`).


### `displayName` *(string, required)*
Display name for the sms template.


### `body` *(string, required)*
    - In the metadata json, the filename of the sms template is specified. The templates are searched for in the `module-metadata/<module-name>/sms-templates/` directory of the module.
    - The body is then replaced with the content of the sms template file. This will include plain text content. The body can include dynamic placeholders using Handlebars syntax (e.g., `{{placeholderName}}`), as shown in the [SMS Template file](#example--sms-template-file) above.

####  Further Reference
 -  **SMS Body Creation:** [SMS Templates Guide](../../admin-docs/notifications/sms-templates.md)


<InfoBox>
  Please refer to the [Handlebars Documentation](https://handlebarsjs.com/) for more information on using Handlebars syntax in email templates.
</InfoBox>

### `smsProviderTemplateId` *(string, optional)*
Unique identifier for the SMS template from the SMS provider (e.g., Twilio, Nexmo). This ID is used to reference the template when sending SMS messages through the provider's API.


### `description` *(string, optional)*
A brief description of the SMS template.


### `active` *(boolean, optional)*
Indicates whether the SMS template is active. Defaults to `true`.


### `type` *(string, optional)*
Type of the SMS template. Currently supports `text` only.
---
# title: SMS Templates

description: Metadata schema for populating SMS templates in SolidX applications.
sidebar_position: 10
json_pointer: "/smsTemplates"
jsonpath: "$.smsTemplates"
parent_component: root
type: array
items_type: "object"
items_attributes_doc: "#email-templates-metadata-attributes"

---
# SMS Templates
> **Where it lives**  
> **JSON Pointer:** `/smsTemplates`  
> **JSONPath:** `$.smsTemplates`  
> **Parent:** Root of the metadata file


import { IoIosArrowForward } from "react-icons/io";
import { InfoBox } from '@site/src/common/InfoBox';

## Overview
SMS Templates in SOLID allow you to create and manage SMS templates with dynamic content and attachments.

### Example: Email Templates Metadata
<summary> Email Templates Schema </summary>

``` json
{
  ..., // Other metadata 
  "smsTemplates": [
    {
      "name": "otp-on-register-custom",
      "displayName": "Custom: Otp On Register",
      "body": "otp-on-register-custom.handlebars.txt",
      "description": "This template is used to generate the account verification sms sent to users to verify their mobile number when they register.",
      "smsProviderTemplateId": "<TEMPLATE_ID_FROM_SMS_PROVIDER>",
      "active": true,
      "type": "text"
    },
    {
      "name": "otp-on-login-custom",
      "displayName": "Custom: Otp On Login",
      "body": "otp-on-login-custom.handlebars.txt",
      "description": "This template is used to send the sms with the OTP when logging in.",
      "smsProviderTemplateId": "<TEMPLATE_ID_FROM_SMS_PROVIDER>",
      "active": true,
      "type": "text"
    },

  ]
}
```

### Example : SMS Template File
<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   SMS Template File 
  </summary>

```text
Hello {{ firstName }}, Log in to {{ solidAppName }}, using {{ mobileVerificationTokenOnLogin }} as your verification code.
```
</details>

## Email Templates Metadata Attributes

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
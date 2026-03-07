---
title: SMS Templates
description: Learn how to create and manage SMS templates in SolidX, including dynamic content
sidebar_position: 2
---

import { IoIosArrowForward } from "react-icons/io";
import { WarningBox } from '@site/src/common/WarningBox';



<WarningBox>
  Work in Progress - This document is currently being updated. Some sections may be incomplete or subject to change.
</WarningBox>
<br/>

# SMS Templates

SMS Templates in SolidX enable you to create and manage text message templates with dynamic content and integrated link shortening capabilities.

## Template Creation

### Basic Structure

```json
{
  "name": "verification_code",
  "description": "SMS template for sending verification codes",
  "content": "Your verification code is {{code}}. Valid for {{validity}} minutes.",
  "variables": {
    "code": {
      "type": "string",
      "required": true,
      "description": "Verification code"
    },
    "validity": {
      "type": "number",
      "required": true,
      "description": "Code validity in minutes"
    }
  }
}
```

## Features

### Dynamic Content
- Variable replacement
- Conditional text
- Character count validation
- Unicode support
- Link shortening

### Link Shortening

```json
{
  "name": "tracking_update",
  "content": "Your order #{{orderNumber}} is {{status}}. Track here: {{shortLink}}",
  "links": [
    {
      "placeholder": "shortLink",
      "url": "https://your-domain.com/tracking/{{trackingNumber}}",
      "options": {
        "expiry": "7d",
        "trackClicks": true
      }
    }
  ]
}
```

### Message Personalization

```json
{
  "name": "appointment_reminder",
  "content": "Hi {{firstName}}, reminder: your appointment is on {{date}} at {{time}}. {{if location}}Location: {{location}}{{endif}}",
  "variables": {
    "firstName": {
      "type": "string",
      "required": true
    },
    "date": {
      "type": "string",
      "required": true
    },
    "time": {
      "type": "string",
      "required": true
    },
    "location": {
      "type": "string",
      "required": false
    }
  }
}
```

## Template Management

### Creating Templates

1. Navigate to SMS Templates
2. Click "New Template"
3. Configure template:
```json
{
  "name": "delivery_notification",
  "description": "Notify customers about delivery updates",
  "content": "Your order #{{orderNumber}} will be delivered {{timeWindow}}. Track: {{trackingLink}}",
  "variables": {
    "orderNumber": {
      "type": "string",
      "required": true
    },
    "timeWindow": {
      "type": "string",
      "required": true
    },
    "trackingLink": {
      "type": "string",
      "required": true,
      "isShortLink": true
    }
  }
}
```

### Testing Templates

```json
{
  "template": "delivery_notification",
  "test": {
    "to": "+1234567890",
    "variables": {
      "orderNumber": "ORD-123",
      "timeWindow": "between 2-4 PM today",
      "trackingLink": "https://tracking.example.com/ORD-123"
    }
  }
}
```

## Provider Integration

### Twilio Configuration

```json
{
  "provider": "twilio",
  "config": {
    "accountSid": "YOUR_ACCOUNT_SID",
    "authToken": "YOUR_AUTH_TOKEN",
    "fromNumber": "+1234567890",
    "messagingServiceSid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  }
}
```

### Custom Provider

```json
{
  "provider": "custom",
  "config": {
    "endpoint": "https://api.provider.com/sms",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer YOUR_API_KEY"
    },
    "bodyTemplate": {
      "to": "{{phoneNumber}}",
      "message": "{{content}}",
      "sender": "{{fromNumber}}"
    }
  }
}
```

## Common Use Cases

### Verification Code
```json
{
  "name": "verification_code",
  "content": "{{code}} is your verification code for {{service}}. Valid for {{validity}} minutes. Do not share this code.",
  "variables": {
    "code": {
      "type": "string",
      "pattern": "^[0-9]{6}$"
    },
    "service": {
      "type": "string"
    },
    "validity": {
      "type": "number",
      "default": 5
    }
  }
}
```

### Order Status
```json
{
  "name": "order_status",
  "content": "Order #{{orderNumber}} status: {{status}}{{if eta}}. Expected delivery: {{eta}}{{endif}}. Track: {{trackingLink}}",
  "variables": {
    "orderNumber": {
      "type": "string"
    },
    "status": {
      "type": "string",
      "enum": ["confirmed", "shipped", "delivered"]
    },
    "eta": {
      "type": "string",
      "required": false
    },
    "trackingLink": {
      "type": "string",
      "isShortLink": true
    }
  }
}
```

### Appointment Reminder
```json
{
  "name": "appointment_reminder",
  "content": "Reminder: Your {{type}} appointment is {{timeframe}}. {{if location}}Location: {{location}}.{{endif}}{{if instructions}} {{instructions}}{{endif}}",
  "variables": {
    "type": {
      "type": "string"
    },
    "timeframe": {
      "type": "string"
    },
    "location": {
      "type": "string",
      "required": false
    },
    "instructions": {
      "type": "string",
      "required": false
    }
  }
}
```




## Best Practices

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Content
  </summary>
  <ul className="card-desc">
    <li>Keep messages concise</li>
    <li>Clear call-to-action</li>
    <li>Avoid abbreviations</li>
    <li>Include opt-out info</li>
    <li>Respect time zones</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Variables
  </summary>
  <ul className="card-desc">
    <li>Validate input length</li>
    <li>Handle special characters</li>
    <li>Set default values</li>
    <li>Document requirements</li>
    <li>Test edge cases</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Links
  </summary>
  <ul className="card-desc">
    <li>Use link shortening</li>
    <li>Track click rates</li>
    <li>Set link expiry</li>
    <li>Monitor usage</li>
    <li>Secure URLs</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Compliance
  </summary>
  <ul className="card-desc">
    <li>Follow regulations</li>
    <li>Honor opt-outs</li>
    <li>Track consent</li>
    <li>Maintain records</li>
    <li>Regular audits</li>
  </ul>
</details>

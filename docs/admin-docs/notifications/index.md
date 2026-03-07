---
sidebar_position: 6
title: Email & SMS Templates
---
import { FaEnvelope, FaServer, FaSms, FaGlobe,FaFileAlt, FaEdit, FaTruck } from "react-icons/fa";
import { IoIosArrowForward } from "react-icons/io";


# Email & SMS Templates

SOLID provides a powerful template management system for sending emails and SMS messages, with support for dynamic content, attachments, and multiple providers.

## Overview

The notification system offers:
- Template-based messaging
- Multiple provider support
- Dynamic content replacement
- Attachment handling
- Delivery tracking

## Components




### [Email Templates](./email-templates.md)

<div className="border-box">
      - HTML/Text templates
      - Dynamic placeholders
      - Stattachments
      - Dynamic attachments (Reports)
      - Provider abstraction (SMTP, Amazon SES)ic at
</div>

### [SMS Templates](./sms-templates.md)

<div className="border-box">
      - Text templates
      - Dynamic placeholders
      - Link shortening
      - Provider abstraction (Twilio, Msg91, Gupshup)
</div>


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaFileAlt size={16} style={{ marginRight: "10px" }} />
      Template Management
    </h4>
    <ul className="card-desc">
      <li>Version control</li>
      <li>Preview functionality</li>
      <li>Test sending</li>
      <li>Template variables</li>
      <li>Template inheritance</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaEdit size={16} style={{ marginRight: "10px" }} />
      Content Features
    </h4>
    <ul className="card-desc">
      <li>Rich text editing</li>
      <li>Variable validation</li>
      <li>Conditional content</li>
      <li>Multi-language support</li>
      <li>Template categories</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaTruck size={16} style={{ marginRight: "10px" }} />
      Delivery Features
    </h4>
    <ul className="card-desc">
      <li>Queue management</li>
      <li>Retry handling</li>
      <li>Delivery tracking</li>
      <li>Bounce handling</li>
      <li>Analytics</li>
    </ul>
  </div>

</div>


## Provider Support

### Email Providers

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaEnvelope size={16} style={{ marginRight: "10px" }} />
      Amazon SES
    </h4>
    <ul className="card-desc">
      <li>High deliverability</li>
      <li>Detailed analytics</li>
      <li>Bounce management</li>
      <li>Reputation monitoring</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaServer size={14} style={{ marginRight: "10px" }} />
      SMTP
    </h4>
    <ul className="card-desc">
      <li>Standard protocol</li>
      <li>Wide compatibility</li>
      <li>Custom server support</li>
      <li>TLS encryption</li>
    </ul>
  </div>

</div>

### SMS Providers

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaSms size={16} style={{ marginRight: "10px" }} />
      Twilio
    </h4>
    <ul className="card-desc">
      <li>Global coverage</li>
      <li>High reliability</li>
      <li>Delivery tracking</li>
      <li>Two-way messaging</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaGlobe size={16} style={{ marginRight: "10px" }} />
      Additional Providers
    </h4>
    <ul className="card-desc">
      <li>Msg91</li>
      <li>Gupshup</li>
      <li>Custom providers</li>
    </ul>
  </div>

</div>




## Provider Abstraction

The provider abstraction allows easy switching between providers:

```json
{
  "email": {
    "default": "ses",
    "providers": {
      "ses": {
        "type": "amazon-ses",
        "config": {
          "accessKeyId": "YOUR_ACCESS_KEY",
          "secretAccessKey": "YOUR_SECRET_KEY",
          "region": "us-west-2"
        }
      },
      "smtp": {
        "type": "smtp",
        "config": {
          "host": "smtp.example.com",
          "port": 587,
          "secure": true,
          "auth": {
            "user": "username",
            "pass": "password"
          }
        }
      }
    }
  },
  "sms": {
    "default": "twilio",
    "providers": {
      "twilio": {
        "type": "twilio",
        "config": {
          "accountSid": "YOUR_ACCOUNT_SID",
          "authToken": "YOUR_AUTH_TOKEN",
          "fromNumber": "+1234567890"
        }
      }
    }
  }
}
```

## Common Operations

### Testing Templates

```json
{
  "template": "welcome_email",
  "to": "test@example.com",
  "variables": {
    "userName": "John Doe",
    "activationLink": "https://example.com/activate"
  },
  "attachments": [
    {
      "filename": "welcome.pdf",
      "content": "base64_encoded_content"
    }
  ]
}
```

### Sending Messages

```javascript
// Send email
await sendEmail({
  template: 'order_confirmation',
  to: 'customer@example.com',
  variables: {
    orderNumber: '12345',
    items: orderItems,
    total: orderTotal
  }
});

// Send SMS
await sendSMS({
  template: 'delivery_notification',
  to: '+1234567890',
  variables: {
    trackingNumber: 'TN123456',
    estimatedDelivery: '2024-01-01'
  }
});
```

### Managing Delivery

```json
{
  "delivery": {
    "retries": {
      "max": 3,
      "delay": 300
    },
    "tracking": {
      "enabled": true,
      "events": ["delivery", "bounce", "complaint"]
    },
    "queue": {
      "priority": "high",
      "ttl": 3600
    }
  }
}
```


## Best Practices

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Template Design
  </summary>
  <ul className="card-desc">
    <li>Use clear layouts</li>
    <li>Test responsiveness</li>
    <li>Include plain text</li>
    <li>Follow email standards</li>
    <li>Optimize for mobile</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Content Management
  </summary>
  <ul className="card-desc">
    <li>Document variables</li>
    <li>Version templates</li>
    <li>Test thoroughly</li>
    <li>Monitor performance</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Delivery
  </summary>
  <ul className="card-desc">
    <li>Configure SPF/DKIM</li>
    <li>Monitor bounces</li>
    <li>Track engagement</li>
    <li>Handle failures</li>
  </ul>
</details>

<details open>
  <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Maintenance
  </summary>
  <ul className="card-desc">
    <li>Regular updates</li>
    <li>Clean old templates</li>
    <li>Update providers</li>
    <li>Review analytics</li>
  </ul>
</details>

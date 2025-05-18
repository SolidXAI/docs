---
sidebar_position: 6
---

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
- HTML/Text templates
- Dynamic placeholders
- Static attachments
- Dynamic attachments (Reports)
- Provider abstraction (SMTP, Amazon SES)

### [SMS Templates](./sms-templates.md)
- Text templates
- Dynamic placeholders
- Link shortening
- Provider abstraction (Twilio, Msg91, Gupshup)

## Features

### Template Management
- Version control
- Preview functionality
- Test sending
- Template variables
- Template inheritance

### Content Features
- Rich text editing
- Variable validation
- Conditional content
- Multi-language support
- Template categories

### Delivery Features
- Queue management
- Retry handling
- Delivery tracking
- Bounce handling
- Analytics

## Provider Support

### Email Providers
1. **Amazon SES**
   - High deliverability
   - Detailed analytics
   - Bounce management
   - Reputation monitoring

2. **SMTP**
   - Standard protocol
   - Wide compatibility
   - Custom server support
   - TLS encryption

### SMS Providers
1. **Twilio**
   - Global coverage
   - High reliability
   - Delivery tracking
   - Two-way messaging

2. **Additional Providers**
   - Msg91
   - Gupshup
   - Custom providers

## Best Practices

1. **Template Design**
   - Use clear layouts
   - Test responsiveness
   - Include plain text
   - Follow email standards
   - Optimize for mobile

2. **Content Management**
   - Document variables
   - Version templates
   - Test thoroughly
   - Monitor performance

3. **Delivery**
   - Configure SPF/DKIM
   - Monitor bounces
   - Track engagement
   - Handle failures

4. **Maintenance**
   - Regular updates
   - Clean old templates
   - Update providers
   - Review analytics

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

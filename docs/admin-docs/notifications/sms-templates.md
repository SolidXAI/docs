---
sidebar_position: 2
---

# SMS Templates

SMS Templates in SOLID enable you to create and manage text message templates with dynamic content and integrated link shortening capabilities.

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

## Best Practices

1. **Content**
   - Keep messages concise
   - Clear call-to-action
   - Avoid abbreviations
   - Include opt-out info
   - Respect time zones

2. **Variables**
   - Validate input length
   - Handle special characters
   - Set default values
   - Document requirements
   - Test edge cases

3. **Links**
   - Use link shortening
   - Track click rates
   - Set link expiry
   - Monitor usage
   - Secure URLs

4. **Compliance**
   - Follow regulations
   - Honor opt-outs
   - Track consent
   - Maintain records
   - Regular audits

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

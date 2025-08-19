---
sidebar_position: 1
---

# Email Templates

Email Templates in SOLID allow you to create and manage HTML/Text based email templates with dynamic content and attachments.

## Template Creation

### Basic Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{subject}}</title>
</head>
<body>
    <h1>Welcome, {{userName}}!</h1>
    <p>Thank you for joining our platform.</p>
    <p>Click <a href="{{activationLink}}">here</a> to activate your account.</p>
</body>
</html>
```

### Template Configuration

```json
{
  "name": "welcome_email",
  "subject": "Welcome to {{companyName}}",
  "description": "Welcome email sent to new users",
  "html": "template.html",
  "text": "template.txt",
  "variables": {
    "userName": {
      "type": "string",
      "required": true,
      "description": "User's full name"
    },
    "activationLink": {
      "type": "string",
      "required": true,
      "description": "Account activation link"
    },
    "companyName": {
      "type": "string",
      "default": "SOLID Platform",
      "description": "Company name"
    }
  }
}
```

## Features

### Dynamic Content
- Variable replacement
- Conditional sections
- Loop structures
- Helper functions


<!-- <div className="feature-grid">

  <div className="feature-card ">
    <h4 className="card-title">1. Content</h4>
    <ul className="card-desc">
      <li>Variable replacement</li>
      <li>Conditional sections</li>
      <li>Loop structures</li>
      <li>Helper functions</li>
    </ul>
  </div>
</div> -->

### Attachments

#### Static Attachments
```json
{
  "attachments": [
    {
      "filename": "terms.pdf",
      "path": "static/documents/terms.pdf",
      "contentType": "application/pdf"
    }
  ]
}
```

#### Dynamic Attachments
```json
{
  "attachments": [
    {
      "filename": "report-{{date}}.pdf",
      "template": "monthly_report",
      "data": {
        "userId": "{{userId}}",
        "month": "{{month}}"
      }
    }
  ]
}
```

### Template Inheritance

Base template:
```html
<!DOCTYPE html>
<html>
<head>
    {% block head %}
    <meta charset="utf-8">
    <style>
        {% block styles %}{% endblock %}
    </style>
    {% endblock %}
</head>
<body>
    <header>{% block header %}{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}{% endblock %}</footer>
</body>
</html>
```

Child template:
```html
{% extends "base.html" %}

{% block content %}
<div class="container">
    <h1>{{title}}</h1>
    <p>{{content}}</p>
</div>
{% endblock %}
```

## Template Management

### Creating Templates

1. Navigate to Email Templates
2. Click "New Template"
3. Configure template:
```json
{
  "name": "order_confirmation",
  "subject": "Order #{{orderNumber}} Confirmation",
  "category": "orders",
  "description": "Sent after successful order placement",
  "variables": {
    "orderNumber": {
      "type": "string",
      "required": true
    },
    "items": {
      "type": "array",
      "required": true
    },
    "total": {
      "type": "number",
      "required": true
    }
  }
}
```

### Testing Templates

```json
{
  "template": "order_confirmation",
  "test": {
    "to": "test@example.com",
    "variables": {
      "orderNumber": "TEST-123",
      "items": [
        {
          "name": "Product 1",
          "quantity": 2,
          "price": 29.99
        }
      ],
      "total": 59.98
    }
  }
}
```

## Best Practices

<!-- 1. **Design**
   - Use responsive layouts
   - Test across email clients
   - Include plain text version
   - Optimize images
   - Follow email standards

2. **Content**
   - Clear subject lines
   - Consistent branding
   - Mobile-friendly design
   - Accessible content
   - Valid links

3. **Variables**
   - Document all variables
   - Provide defaults when possible
   - Validate data types
   - Handle missing values
   - Use clear naming

4. **Testing**
   - Test all variables
   - Check responsiveness
   - Verify attachments
   - Monitor delivery
   - Track engagement -->



<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title ">1 Design</h4>
    <ul className="card-desc">
      <li>1 Use responsive layouts</li>
      <li>Test across email clients</li>
      <li>Include plain text version</li>
      <li>Optimize images</li>
      <li>Follow email standards</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title ">2 Content</h4>
    <ul className="card-desc">
      <li>Clear subject lines</li>
      <li>Consistent branding</li>
      <li>Mobile-friendly design</li>
      <li>Accessible content</li>
      <li>Valid links</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title ">3 Variables</h4>
    <ul className="card-desc">
      <li>Document all variables</li>
      <li>Provide defaults when possible</li>
      <li>Validate data types</li>
      <li>Handle missing values</li>
      <li>Use clear naming</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title ">4 Testing</h4>
    <ul className="card-desc">
      <li>Test all variables</li>
      <li>Check responsiveness</li>
      <li>Verify attachments</li>
      <li>Monitor delivery</li>
      <li>Track engagement</li>
    </ul>
  </div>

</div>



## Common Use Cases

### Welcome Email
```html
<div class="welcome">
    <h1>Welcome to {{companyName}}</h1>
    <p>Dear {{userName}},</p>
    <p>Thank you for joining us! Please verify your email by clicking the button below:</p>
    <a href="{{verificationLink}}" class="button">Verify Email</a>
</div>
```

### Order Confirmation
```html
<div class="order">
    <h1>Order Confirmation</h1>
    <p>Order Number: {{orderNumber}}</p>
    <table>
        {% for item in items %}
        <tr>
            <td>{{item.name}}</td>
            <td>{{item.quantity}}</td>
            <td>{{item.price}}</td>
        </tr>
        {% endfor %}
    </table>
    <p>Total: {{total}}</p>
</div>
```

### Password Reset
```html
<div class="reset">
    <h1>Password Reset Request</h1>
    <p>Click the link below to reset your password:</p>
    <a href="{{resetLink}}" class="button">Reset Password</a>
    <p>This link will expire in {{expiryTime}} minutes.</p>
</div>
```

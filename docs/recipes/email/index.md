---
sidebar_position: 4
---

# Sending Emails Synchronously

To send emails synchronously, you need to configure the following settings in your .env file of the API project:

```
COMMON_EMAIL_SHOULD_QUEUE=false
COMMON_SMTP_EMAIL_SMTP_HOST=
COMMON_SMTP_EMAIL_SMTP_PORT=587
COMMON_SMTP_EMAIL_USERNAME=
COMMON_SMTP_EMAIL_PASSWORD=
COMMON_SMTP_EMAIL_FROM=
```
COMMON_EMAIL_SHOULD_QUEUE=false

This flag is critical — it ensures the email is sent immediately, without entering any job queue or background task.

The other SMTP settings must be filled with your provider's actual credentials:

HOST – SMTP server address (e.g., smtp.gmail.com)

PORT – usually 587 (for TLS)

USERNAME – your email username

PASSWORD – the SMTP password or app password

FROM – sender's display email (e.g., no-reply@example.com)

✅ After completing all the above configuration, you will be able to send emails synchronously without any additional queue setup.




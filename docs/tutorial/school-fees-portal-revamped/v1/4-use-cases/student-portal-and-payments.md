---
sidebar_position: 3
---

# 3. Student Portal & Payments

This section details the student and parent-facing portal, covering everything from logging in to making payments and receiving notifications.

## Student Portal - Parent Login & Dashboard

### Introduction

To provide a seamless experience for parents and students, we will create a custom frontend for the student portal. This portal will serve as the primary interface for viewing fee details, making payments, and tracking payment history.

### Getting Started with the Frontend

A Git repository will be provided with a base application for the student portal frontend. 
*(Instructions and link to the repository will be added here.)*

### Parent Login

Parents will log in to the portal using credentials provided by the institute. The login process will authenticate them and provide access to their child's fee information.

### Dashboard

Upon logging in, parents will be greeted with a dashboard that provides a clear overview of:
*   **Outstanding Fees:** A summary of all pending payments.
*   **Paid Fees:** A history of all successful payments.
*   **Upcoming Due Dates:** A timeline of upcoming payment deadlines.

## Making a Payment

### Payment Gateway Integration (Stripe)

The portal will be integrated with a payment gateway to facilitate online payments. For this tutorial, we will use **Stripe** as our reference payment gateway. This will involve:
1.  **Configuration:** Setting up Stripe API keys in the SolidX backend.
2.  **Payment Initiation:** When a parent clicks "Pay," the system will generate a secure payment link and redirect them to the Stripe payment page.

### Consuming Webhooks

After a payment is processed by Stripe, it will send a **webhook** to our SolidX backend. This webhook is a crucial part of the process:
1.  **Webhook Listener:** We will create an endpoint in our backend to listen for these webhooks.
2.  **Data Processing:** When a webhook is received, we will verify its authenticity and then update the payment status in our database. This will involve updating the `Payment` and `PaymentCollectionItem` records.

## Payment Processing & Notifications

### Process Payment

This use case covers the backend logic for processing the payment once the webhook is received. It includes updating the database, generating receipts, and triggering notifications.

### Late Fee Calculation

The system will automatically calculate late fees for overdue payments. This will be handled by a scheduled job that runs periodically to check for overdue payments and apply the appropriate late fee charges.

### Email Notifications

The system will send out automated email notifications for various events:
*   **Late Fee Reminders:** Sent to parents when a payment is overdue.
*   **Payment Confirmation:** Sent to parents after a successful payment.

This comprehensive payment and notification system ensures that both the institute and the parents are kept informed throughout the fee payment lifecycle.

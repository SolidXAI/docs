---
title: Product Overview
sidebar_position: 2
description: Overview of the School Fees & Payments Platform - a comprehensive solution for educational institutes to digitize fee collection and payment processing.
summary: A centralized platform enabling institutes to manage fee collection through secure admin and student portals with role-based access, online payments, and bulk processing capabilities.
keywords: [school fees, payment platform, institute management, online payments, fee collection, student portal, admin portal]
---

# School Fees & Payments Platform

## Overview

The School Fees & Payments Platform is a centralized, secure, and configurable solution designed to help educational institutes digitize their fee collection and payment workflows. The platform provides dedicated portals for both administrative users and students, enabling efficient fee management, online payments, and complete auditability.

## Platform Overview

This is a **multi-tenant platform** — a single deployment serves multiple educational institutes, all sharing one database. Data segregation is enforced at the platform level, ensuring each institute can only access and manage its own data.

The solution consists of two main portals:

### Admin Portal
A secure management interface for super admins and institute administrators to:
- Onboard and manage institutes
- Configure fee structures and types
- Invite and manage institute administrative users
- Create and manage student records
- Initiate bulk payment collections via Excel upload
- Monitor payments and perform reconciliation

### Student Portal
A user-friendly interface where students and parents can:
- Authenticate securely via email OTP
- View pending fee dues and amounts
- Review complete payment history
- Make online payments through integrated payment gateways
- Receive payment confirmations and receipts

## User Roles & Responsibilities

### Super Admin
- Manages multiple institutes on the platform
- Controls global configuration and settings
- Oversees institute onboarding and activation

### Institute Admin
- Manages their specific institute's data and configuration
- Creates and maintains fee type structures
- Invites and manages institute-level users
- Initiates payment collections
- Monitors and reconciles payments
- Configures payment gateway settings
- Customizes student portal branding

### Student (Public User)
- Accesses the student portal to view personal dues
- Makes online payments for outstanding fees
- Views payment history and downloads receipts
- Limited to viewing and paying their own obligations only

## Core Features

### Institute Management
- Multi-tenant architecture supporting multiple institutes
- Complete institute profile management (name, address, contact details)
- Payment gateway configuration per institute
- Custom branding and theming for student portals
- Support personnel information setup

### Fee Type Configuration
- Flexible fee structure definitions (tuition, library, lab, etc.)
- Support for full and partial payment options
- Late fee penalty configuration
- Fee type maintenance and updates

### Student Management
- Student record creation and maintenance
- Login ID management
- Parent/guardian contact information
- Association with specific institutes

### Payment Collection
- Bulk payment demand creation via Excel upload
- Support for multiple fee types in a single collection
- Individual payment collection items per student per fee type
- Due date tracking and management
- Multiple payment modes support

### Payment Processing
- Secure online payment gateway integration
- Support for partial payments
- Multiple payment collection item details per fee type
- Complete transaction tracking (PG order ID, transaction ID)
- Payment status monitoring
- Single payment can cover multiple fee items

### Audit & Reporting
- Complete audit trail for financial operations
- Transaction traceability
- Payment reconciliation tools
- Historical payment records

## Data Model

The platform is built around these core domain entities:

| Entity | What it represents |
|--------|-------------------|
| **Institute** | Your educational institution (school, college, university) that will collect fees through the portal |
| **Fee Type** | Different categories of fees your institution collects (e.g., Tuition Fees, Bus Fees, Hostel Fees, Library Fees, Sports Fees) |
| **Institute User** | Administrative staff who will manage the fees portal for your institution |
| **Student** | Individual students enrolled at your institution whose parents/guardians will receive payment collection requests |
| **Payment Collection** | A batch of fee collection requests sent to multiple students at once (e.g., "Q1 2024 Fees", "Annual Sports Fees 2024") |
| **Payment Collection Item** | An individual payment request for one student for one fee type within a collection (e.g., "Rahul Sharma needs to pay ₹10,000 for Tuition Fees") |
| **Payment Collection Item Detail** | Tracks each installment or payment attempt recorded against a payment collection item |
| **Payment** | A single payment transaction initiated by a student through the payment gateway |

**Key Relationships:**
- One Institute has many Institute Users, Fee Types, Students, and Payment Collections
- One Payment Collection has many Payment Collection Items — one per student per fee type
- One Payment Collection Item has many Payment Collection Item Details — one per installment or partial payment
- One Payment can settle multiple Payment Collection Item Details in a single transaction

## Security & Access Control

The platform implements comprehensive security measures:

- **Role-Based Access Control (RBAC)** - Access rights defined by user role
- **Data Isolation** - Institute data strictly separated and accessible only to authorized users
- **Audit Trail** - All critical operations logged for compliance
- **Secure Authentication** - Email OTP for students, secure login for admins
- **Payment Security** - Integration with certified payment gateways
- **Access Restrictions:**
  - Institute admins limited to their own institute's data
  - Students can only view and pay their own dues

## Technical Capabilities

### Performance
- Background job processing for bulk operations
- Asynchronous email and notification delivery
- Efficient handling of large data uploads

### Compliance
- Secure payment processing standards
- Complete transaction traceability
- Reporting capabilities for audits

### Integration
- Email service (SMTP) for notifications
- Payment gateway APIs for transaction processing
- Excel file processing for bulk uploads

## What You'll Build with SolidX

This tutorial demonstrates the following SolidX platform capabilities as you build the Fees Portal:

- **Data Model Configuration** — Define entities, fields, and relationships using the SolidX App Builder without writing code
- **Role & Permission Setup** — Configure roles (Super Admin, Institute Admin, Student) and control what each role can see and do
- **List & Form View Customization** — Tailor how records are displayed and edited using layout configuration
- **Workflows & Actions** — Set up business logic such as institute activation and payment status transitions
- **Bulk Upload** — Use Excel-based bulk upload to create payment collection requests for multiple students at once
- **Student Portal** — Configure a public-facing portal where students authenticate via email OTP and make online payments

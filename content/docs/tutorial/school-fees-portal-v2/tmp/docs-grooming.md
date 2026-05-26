---
title: Solid Features
---

# Solid Features 

- Backend
  - Data modeling 
    - Importance of user key 
    - How we do many-to-one & many-to-many relations 
    - Importance of Workflow field 
    - Touch upon how to enable audit trail on a model 
    - Touch upon how to enable soft delete on a model 
    - Pattern around extending user 

  - Pre defined computed field 
    - Alpha Num 
    - The new Sequence based 

  - Custom computed field
    - Eg. PaymentCollectionItemAmountProvider

  - Entity Subscriber 
    - Eg. MediaTransactionSubscriber

  - Custom Controller Endpoint & Service Method 
  - Background Jobs
    - Eg: (To Be Developed)
    - custom controller endpoint > custom service method > background job (use html to pdf conversion) > use mailFactory (SMTP) to send the mail.

  - RBAC 
    - defining roles with permissions 
    - linking menu visibility to roles 
    - linking different view element visibility to roles (buttons etc)
    - security rules

- Admin Frontend - layout customisation 
- Admin Frontend - 

- User Frontend - 

# Tutorial Flow

## Bootstrap

- talk a bit about system requirements
- create database 
- use npx @solidstarters/solidctl create-app
- show how to seed 
- show how to login 

## Introduction 

- Talk about the school portal in a one page requirements document (all use-cases, basic entities, user frontend & admin frontend)

Institute
FeeType
InstituteUser
PaymentCollection
PaymentCollectionItem 
PaymentCollectionItemDetail 
Payment 
Student 

## Use Case: Institute Onboarding (interface=Admin Frontend, role=Admin) (#DemoDone)

- Creation of the institute (role=Admin, layout should be domain specific & clean, externalId)
- Creation of fee types (one-to-many, composite unique key)
- Invite institute admin user (one-to-many, talk about extending the solid user table, welcome email template configuration??, externalId)
  - (Right now welcome email is missing?? need to create the ticket for it)

## Use Case: Institute Admin User Login (interface=Admin Frontend, role=Institute Admin)

- Can modify everthing about their own Institute (security rule)
- Can add fee types 
- Can invite other institue admin users 
- Cannot create new institutes 
- Triggers payment collection 
- Security rules (for institute and institute users)

## Use Case: Initiate Payment Collection (interface=Admin Frontend, role=Institute Admin) 

- upload payment collection excel 
- background job to parse excel and create students if not existing, create payment collection items
- triggers emails to all impacted students

## Use Case: Create User Frontend (interface=User Frontend, role=Public - custom authentication)

- Use next js to bootstrap a project that will be used to represent the user frontend. 
- Start with building the login functionality 
- Custom endpoints required to implement student login 
- Post login custom endpoints required to render the payments list etc.

## Use Case: Making Payment (interface=User Frontend, role=Public - custom authentication)

- Custom endpoints to render payment list
- Custom endpoint to start payment flow 
- Custom endpoint to capture payment webhook 
- Computation provider to do the calculations of total paid, due etc 
- Scheduled job to mark payments overdue and add penalty 

## Refund & Cancellation Handling (interface=Admin Frontend, role=Institute Admin)(No refund - ??? Ignore)

- Custom endpoint to trigger refunds 
- Custom endpoint to cancel payments 

## Use Case: Configure User Frontend (role=Institute Admin)

- upload logo
- upload banner 
- upload faqs & terms & conditions etc

## Use Case: Activate User Frontend 

## Use Case: Deactivate User Frontend 


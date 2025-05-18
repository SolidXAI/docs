# 

[**SOLID Documentation	2**](#solid-documentation)

[Introduction	2](#introduction)

[User Docs	3](#user-docs)

[Welcome	3](#welcome)

[App Builder / Resource Builder	3](#app-builder-/-resource-builder)

[Module Management	4](#module-management)

[Model Management	4](#model-management)

[Field Management	4](#field-management)

[App Builder / Layout editor	4](#app-builder-/-layout-editor)

[List view	4](#list-view)

[Kanban view	4](#kanban-view)

[Form view	4](#form-view)

[Apps	5](#apps)

[API / Swagger Docs	5](#api-/-swagger-docs)

[Admin / Menu structure	5](#admin-/-menu-structure)

[Admin / List view	5](#admin-/-list-view)

[Admin / Kanban view	5](#admin-/-kanban-view)

[Admin / Form view	6](#admin-/-form-view)

[Media Library	6](#media-library)

[Media View	6](#media-view)

[Storage Providers	6](#storage-providers)

[IAM	7](#iam)

[User	7](#user)

[Role	7](#role)

[Permission	7](#permission)

[Record Rules	7](#record-rules)

[Authentication Providers	7](#authentication-providers)

[Email & SMS Templates	8](#email-&-sms-templates)

[Email Templates	9](#email-templates)

[SMS Templates	9](#sms-templates)

[Report Template Module	9](#report-template-module)

[Link Shortener Module	9](#link-shortener-module)

[Other Settings	9](#other-settings)

[Plugin Architecture	9](#plugin-architecture)

[Developer Docs	9](#developer-docs)

[**Other Notes	10**](#other-notes)

# 

# SOLID Documentation {#solid-documentation}

## **Introduction** {#introduction}

We need to create a page introducing SolidX and what it stands for, maybe a writeup of some of the design goals, we need to position it here as an enterprise low code platform.

Reference design for this could be: [https://docs.strapi.io/](https://docs.strapi.io/) 

As in the above page we can have a paragraph on top instead of the carousel, and the bottom 2 blocks one for the user documentation & other for the developer documentation.

1. Open Source  
2. Non vendor lockin, standards based   
   1. (NestJS \- Node, .NET Core \- C\#, Spring Boot \- Java)  
   2. Database agnostic (RDBMS \- mssql, mysql, oracle & pg \+ NoSQL \- MongoDB)  
   3. Schema agnostic  
   4. React on the Admin frontend.  
   5. Existing developers can easily work on it without re-skilling.  
3. SOLID principles, brings standardisation to development workflows using tried & tested SOPs.   
4. Extensibility & Flexibility, never hit a brick wall in terms of what can be done.   
5. Batteries Attached \- comes with a suite of recipes / features pre built.   
   1. IAM   
   2. Notifications \- Email, SMS, Firebase push notifications & WhatsApp.  
   3. Storage abstraction   
   4. Queues abstraction   
   5. Caching abstraction   
   6. Standard data modeling & resource management features   
      1. RESTful CRUD   
      2. Import   
      3. Export   
      4. Audit Trail   
      5. Saved filters   
      6. Much more.. 

## **User Docs** {#user-docs}

### **Welcome** {#welcome}

Here we can talk about the basics of the admin panel, we need to make a landing page in the admin panel that the user can land on immediately after they login similar to what Strapi has. 

Reference: [https://docs.strapi.io/user-docs/intro](https://docs.strapi.io/user-docs/intro) 

We can start with a link to how one can access the admin panel, the default username & password that gets set up. How the user can login and change the password of the admin user.

At the bottom then we can have sections similar to the above page for us the sections will be (only consider top level bullets for now).

1. App Builder   
   1. Resource builder   
   2. View builder   
2. Apps   
3. Media Library  
   1. Media Storage providers  
4. IAM \- Users, roles & permissions.  
5. Email & SMS Templates  
6. Other Settings  
   1. List of values  
   2. Messages & queue log  
   3. Import & export jobs   
   4. Saved views 

### **App Builder / Resource Builder**  {#app-builder-/-resource-builder}

The App Builder is one of the core modules that comes with SolidX. 

Reference: [https://docs.strapi.io/user-docs/content-type-builder](https://docs.strapi.io/user-docs/content-type-builder) 

#### Module Management {#module-management}

Here we talk about how everything is structured around modules. Explain each field on the module builder form.

We need to probably elaborate on the data source and how to use it, and other features.

#### Model Management {#model-management}

Here we capture details about configuring a model / resource. Explain each field on the model form.

We need to probably elaborate on the data source and how to use it, soft delete, audit tracking, internationalisation and any other features.

#### Field Management {#field-management}

Here we capture all the different field types we have in full detail. This is quite elaborate as we document what all is possible while making each field.

### **App Builder / Layout editor** {#app-builder-/-layout-editor}

In this section we first talk about the different views which are possible for a given SOLID resource / model.

#### List view  {#list-view}

Talk about how the list view comes out, the json layout & all the filtering / searching / importing / exporting / saved queries functionality that the list view exposes.

#### Kanban view  {#kanban-view}

Talk about how the list view comes out, the json layout & all the filtering / searching / importing / exporting / saved queries functionality that the list view exposes.

#### Form view  {#form-view}

Here again we need to talk about the json layout, audit trail functionality, chatter, workflow stages etc. 

### **Apps**  {#apps}

Introduce what apps are \- they are basic pieces around achieving modularity, they encapsulate a logical unit of functionality and expose RESTful API endpoints, services & internal user interface from where users can access & modify data of that module. 

#### API / Swagger Docs {#api-/-swagger-docs}

Talk about how swagger docs get auto-generated, we can demonstrate the login API to generate the token, and then use the other APIs which are automatically generated. 

#### Admin / Menu structure  {#admin-/-menu-structure}

Talk about how for each module & resource a menu structure is automatically created. 

#### Admin / List view  {#admin-/-list-view}

Talk about the list view, talk about the list view layout, how one can customize the list view layout. 

Then we can talk about the different features that the list view exposes by default. 

* Search  
* Filter   
* Group (\*)  
* Import   
* Export  
* Pagination  
* Sorting  
* Configure layout  
* Saved queries  
* Custom action buttons (within record & in header)  
* Saved views (list layout linked to user profile)

#### Admin / Kanban view {#admin-/-kanban-view}

Talk about the kanban view, talk about the kanban view layout, how one can customize the kanban view layout.

Then we can talk about the different sections / features that the list view exposes by default. 

* Standard & custom actions (within record & in header)  
* Search  
* Filter  
* Sort  
* Import  
* Export  
* Group (1 level grouping)  
* Pagination  
* Configure layout \- including image(s) as part of the layout.  
* Saved queries

#### Admin / Form view  {#admin-/-form-view}

Talk about the form view, the view layout & how to customize the form view. 

Then we talk about different sections of the form view. 

* Standard & custom actions  
* Chatter / Audit trail   
* Message log   
* Workflow ribbon   
* Breadcrumbs 

In this section we will also have to talk about how each field type which was configured in the app builder section manifests itself in the form view. 

### **Media Library** {#media-library}

In this section we talk about the media library & media storage provider. 

#### Media View  {#media-view}

We need to create a view of all the media that is uploaded in the system, since we have a common table for the media now. 

This view can be similar to the Strapi media view. 

#### Storage Providers  {#storage-providers}

Again we can create a CRUD interface for the storage providers, and document each storage provider in detail. 

Currently we are supporting filesystem & S3. 

### **IAM**  {#iam}

In this section we first introduce our take on IAM, introducing the user, role & permissions entities. 

#### User  {#user}

Talk about the user list view, how you can create & invite new users to the system. 

#### Role  {#role}

Talk about what roles are, here you need to create a new role and link it to permissions. 

#### Permission {#permission}

Permissions are automatically discovered based on all the controllers present in the codebase, each controller action becomes a permission. 

#### Record Rules {#record-rules}

Talk about what record rules are and how they help us achieve data / record level security linked to RBAC.

#### Authentication Providers  {#authentication-providers}

In this section we need to document all the different ways in which a user can signup & login to the system. 

First we can talk about the login workflow in a bit more detail here. 

Let's say that:

* Solid backend is located at: solid.website.com, and  
* Your app frontend is located at: website.com

Then the workflow works like this: 

1. The user goes on your frontend app (https://website.com) and clicks on your button to connect with Google.  
2. The frontend redirects the tab to the backend URL: [https://solid.website.com/api/iam/google/connect](https://solid.website.com/api/iam/google/connect)   
3. The backend redirects the tab to the Google login page where the user logs in.  
4. Once done, Google redirects the tab to the backend URL: [https://solid.website.com/api/iam/google/connect/callback](https://solid.website.com/api/iam/google/connect/callback). When this callback comes, it comes with the user's profile & access token.  
5. Then, the backend redirects the tab to the url of your choice with the param accessCode (example: [http://website.com/connect/google/dummy-redirect?accessCode=eyfvg](http://website.com/connect/google/dummy-redirect?accessCode=eyfvg)).  
6. The frontend ([http://website.com/connect/google/dummy-redirect](http://website.com/connect/google/dummy-redirect)) calls the backend with [https://solid.website.com/api/iam/google/auth?accessCode=eyfvg](https://solid.website.com/api/iam/google/auth?accessCode=eyfvg) that returns the Solid user profile with its jwt. (Under the hood, the backend asks Google for the user's profile and a match is done on Google user's email address and Solid user's email address).  
7. The frontend now possesses the user's JWT, which means the user is connected and the frontend can make authenticated requests to the backend\!

We then need to document each of the supported providers in more detail. 

* Password based authentication  
* OTP based authentication (passwordless)  
* Google  
* Meta  
* LinkedIn  
* X  
* …  
* …  
* Others can follow.

We can then talk about some of the standard functionalities around authentication. 

* Forgot password  
* Reset password   
* GET User profile   
* Token management \- access token, refresh token, token cache etc.

### **Email & SMS Templates**  {#email-&-sms-templates}

Here we talk about our Email & SMS abstraction.

We allow developers to send emails & text messages both template based & otherwise. 

We have abstracted template management into 2 entities viz. email\_templates & sms\_templates. 

#### Email Templates {#email-templates}

Create HTML/Text based email templates with placeholders which can be replaced at runtime. Templates also support attachments (static & dynamic).   
The dynamic attachments are set up in terms of Report Templates. 

#### SMS Templates  {#sms-templates}

Create text based sms templates with placeholders which can be replaced at runtime. We can link into link shortening here later. 

We also talk about the different providers we are supporting including Amazon SES & SMTP for Email. For SMS we can support Twilio, Msg91, Gupshup as a going in proposition. 

Most importantly, we should document the provider abstraction allowing devs to create their own providers and integrate. 

### **Report Template Module** {#report-template-module}

Allows users to configure HTML to PDF report creation with placeholder replacement.

### **Link Shortener Module** {#link-shortener-module}

### **Other Settings**  {#other-settings}

### **Plugin Architecture** {#plugin-architecture}

## Developer Docs {#developer-docs}

# 

# 

# 

# Other Notes {#other-notes}

- **App Builder**  
  Allows one to model any resource in terms of modules, models & fields abstraction.   
  Once modeled & metadata created for the above 3 entities, app builder allows us to generate boilerplate for that resource.   
  Boilerplate supports CRUD and other standard functionality expected of a resource.   
    
  App Builder generated code allows RESTful endpoints to do the below.  
    
1. Create & Update: 

   All field types supported are semantic field types and not necessarily database field types.

2. Delete: 

   Soft delete is also supported. 

3. Retrieve: 

   A retrieve protocol which is 95% similar to what Strapi supports. 

	GraphQL support for queries & mutations needs to be created.

We are using TypeORM as the ORM tool internally, so we are able to support multiple RDBMSs (currently we are testing against PG)

Coded

1. user key related functionality  
2. soft delete   
3. data source agnostic abstraction both in terms of number of data source & type of data sources.   
4. media field & storage \- allows to store media abstraction using providers filesystem & s3 are supported, azure, SFTP etc to be added. Uploading & saving media to respective storage providers can be done asynchronously.  
5. Handling around each field type, especially semantic fields.

   Groomed backlog

1. primary key abstraction  
2. generic import functionality  
3. generic audit functionality  
4. generic export functionality  
5. generic saved queries  
6. Workflow engine  
7. Security rules for record rule based access control

	Not groomed backlog

8. internationalisation   
9. encryption at rest functionality at the field level  
10. Metabase style dashboard builder   
11. Drag and drop UI builder for layout management of solid core admin backend.

- **IAM**   
  Identity & authentication management. This comes with a pre-built abstraction around users, roles & permissions.   
  This module implements RBAC & permission based access control.  
  This module also supports standard workflows around   
    
1. User signup   
2. User login   
3. Forgot password   
4. Reset password 

   Authentication is provided by means of a "Provider" abstraction. Currently we are supporting 

   

1. Password based authentication provider  
2. Passwordless authentication provider (OTP based)  
3. Google  
4. Meta/Facebook (\*)  
5. X/Twitter (\*)  
6. …  
7. …

	All authentication works using JWT tokens only.

	We also support use-cases around refresh tokens, token expiry, etc.

Authorization is implemented by means of our own Roles & Permissions tables. One pattern we are following for permissions is that each **permission** \= one controller handler method.

- **Queues**  
    
- **Media management** 


  

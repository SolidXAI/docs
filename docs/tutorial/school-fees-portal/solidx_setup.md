---
title: Setting Up SolidX
sidebar_position: 1
description: Learn how to set up the SolidX platform for your project, including installation, configuration, and initial setup steps.
summary: TODO
keywords: [TODO]
concerns: TODO
---

## System Requirements

To try out SolidX on your local machine, ensure you have the following prerequisites installed.

### Prerequisites
- **Node.js**: Latest **Active LTS**
- **npm**: Included with Node.js
- **Docker**: Latest stable version

### Supported Systems
- macOS
- Linux

### System Requirements
- **CPU**: 2 cores  
- **Memory**:
  - Minimum: **4 GB RAM**
  - Recommended: **8 GB RAM** (for a smoother experience)
- **Disk**: **5 GB free space**

> SolidX itself is lightweight and does not require significant memory.  
> The requirements above are intended for a smooth local development experience,
> especially when running development tools and containers.

## Database Setup

:::tip[Already have PostgreSQL?]
If you already have a PostgreSQL database installed and running on your system, you can skip this section and proceed directly to [SolidX Scaffolding Script](#solidx-scaffolding-script). Just make sure you have your database connection details (host, port, username, password, and database name) ready for the scaffolding step.
:::

SolidX requires a relational database to store application data / metadata. Currently supported databases include **PostgreSQL** and **MSSQL**. 

We will be using PostgreSQL for this tutorial. 

Below are instructions to set up PostgreSQL locally using Docker, which provides an isolated and easy-to-manage environment for your database.

### Prerequisites
Before proceeding, Docker must be installed and running on your system.
  - **macOS / Windows**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - **Ubuntu / Linux**: Install [Docker Engine](https://docs.docker.com/engine/install/)

After installation, ensure Docker is running and verify it by executing:

```bash
docker --version

# Expected output (version may vary):
# Docker version 27.5.1, build 9f9e405
```

### Installing PostgreSQL
We will be installing **PostgreSQL 17** using the official Docker image.

#### Step 1: Pull PostgreSQL 17 Image
Pull the official PostgreSQL 17 image from Docker Hub.
```bash
docker pull postgres:17
```

#### Step 2: Run the PostgreSQL Container
Run PostgreSQL with a predefined username, password, database name, port binding, and persistent storage using the **postgres:17** image.

```bash
docker run -d \
  --name SolidX_DB \
  -e POSTGRES_USER=solidx_app_user \
  -e POSTGRES_PASSWORD=strongpassword \
  -e POSTGRES_DB=solidx_app_db \
  -p 5432:5432 \
  -v solidx_pgdata:/var/lib/postgresql/data \
  postgres:17
```
:::info
Above step initializes an empty database with the specified credentials and configuration and starts the PostgreSQL server in a Docker container. 

PostgreSQL data will be stored in the Docker volume **solidx_pgdata** which is specified using the `-v` flag. This is useful for the following reasons:
	- Data persists across container restarts
	- Removing the container does not delete the data
	- Removing the volume deletes all stored data
:::

#### Step 3: Verify the Container Is Running
Check the list of running containers.

```bash
docker ps

# Expected output should include a container named "SolidX_DB" with the postgres:17 image
#CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS         PORTS                    NAMES
#3aabaa074778   postgres:17   "docker-entrypoint.s…"   11 seconds ago   Up 9 seconds   0.0.0.0:5432->5432/tcp   SolidX_DB
```

#### Step 4: Connect to PostgreSQL

Use the following details in your application or database client e.g pgAdmin, DBeaver, or any PostgreSQL client.
	-	Host: localhost
	-	Port: 5432
	-	Username: solidx_app_user
	-	Password: strongpassword
	-	Database: solidx_app_db

![Connect to PostgreSQL Using Dbeaver](/img/tutorial/school-fees-portal-v2/db_client_connect.png)  
*Screenshot showing how to connect to the running PostgreSQL server using DBeaver*
#### Step 5: Managing the Container

Stop the PostgreSQL container.

```bash
docker stop SolidX_DB
```

Start the PostgreSQL container again.

```bash
docker start SolidX_DB
```


:::warning
 - Running PostgreSQL using Docker is recommended for local development and testing environments.
 - For production deployments, it is advised to use a managed PostgreSQL service or a carefully maintained database setup with proper backups, monitoring, and high availability.
:::
:::tip
 - If you want to reset the database and start afresh, you can remove the Docker volume storing the data.
```bash
# Stop the container first
docker stop SolidX_DB
# Remove the container
docker rm SolidX_DB
# Then remove the volume
# Warning: This deletes all data in the database!
docker volume rm solidx_pgdata
```
 - Then you can re-run the container using the command in Step 2 to create a fresh database.
:::

## SolidX Scaffolding Script

SolidX applications are **installed and initialized exclusively** using the official scaffolding script.

To create a new SolidX application, run:

```bash
npx @solidxai/solidctl create-app
```

This command launches an interactive setup and generates a fully configured SolidX workspace, ready for development.

### What the Script Does

Running the SolidX scaffolding script results in a **fully working, end-to-end setup**.

Specifically, it:

1. **Bootstraps the backend (APIs)**  
   - Sets up a fully functional backend application  
   - Exposes a complete set of REST APIs  
   - Generates Swagger / OpenAPI documentation for all APIs

2. **Bootstraps the frontend (Admin Panel)**  
   - Sets up a ready-to-use admin panel  
   - Integrates the frontend with backend REST APIs out of the box

3. **Applies correct SolidX project structure and conventions**  
   - Backend and frontend projects follow SolidX-defined project structures and best practices  
   - Configuration, environment files, and scripts are wired correctly

4. **Provides the SolidX CLI utility**  
   - Seeds/syncs database with metadata and model configurations from JSON files (**solid seed**)
   - Generates code from model configurations (**solid refresh-model** - alternative to UI-based generation)

### Prerequisites

Ensure the following are available before running the starter script.

#### Node.js (Required)

- **Required:** Node.js 22 or later  
- **Recommended:** Latest LTS version (via nvm or from https://nodejs.org)

Verify installation:

```bash
node -v
```

> `npx` is bundled with Node.js and is used to run the SolidX starter without global installation.

#### Recommended: Node Version Manager (nvm)

We recommend installing Node.js using **nvm** to easily manage and switch Node versions, avoid system conflicts, and ensure compatibility with SolidX.

Install `nvm` using the official instructions:  
https://github.com/nvm-sh/nvm

Once installed, set up the required Node version:

```bash
nvm install 22
nvm use 22
```

#### npm

`npm` is bundled with Node.js and is used by the starter script.

Verify installation:

```bash
npm -v
```

### Terminal & Internet Access

- Access to a command-line terminal (macOS, Linux, or Windows)
- Active internet connection (required to download and run the starter)

The next section walks through the scaffolding script **step by step**, including each prompt and screenshots for reference.

## Bootstrapping Your Application
To create a new SolidX application, run the following command in your terminal:

```bash
npx @solidxai/solidctl create-app
```
This command launches an interactive setup and generates a fully configured SolidX workspace, ready for development.
Follow the prompts to configure your application:
### Backend Configuration Prompts
1. **Project Name**: Enter a name for your SolidX application.
 - Example: `school-fees-portal`
 - Default: `my-solid-app`
2. **Backend API Port**: Enter the port for the backend API server.
 - Default: `3000`
3. **Database**: Select the database for your application.
 - Options: `PostgreSQL`, `MSSQL`
 - Default: `PostgreSQL`
4. **Database Host**: Enter the database host address.
 - Default: `localhost`
5. **Database Port**: Enter the database port.
 - Default for PostgreSQL: `5432`
6. **Database Name**: Enter the database name.
 - Default: `solidx_app_db`
7. **Database Username**: Enter the database username.
 - Default: `solidx_app_user`
8. **Database Password**: Enter the database password.
 - Default: `strongpassword`
9. **Sync Database Schema**: Choose whether to automatically synchronize the database schema.
 - Options: `Yes`, `No`
 - Default: `Yes`
 :::warning
  This option is not recommended for production environments, since it modifies the database schema automatically. It is advisable to manage database migrations manually in production.
 :::
### Frontend Configuration Prompts
10. **Admin Panel Port**: Enter the port for the admin panel frontend.
   - Default: `3001`

### SolidX Bootstrapping in Action
![Bootstrapping SolidX](/img/tutorial/school-fees-portal-v2/bootstrapping_solidx.png)
*Screenshot showing the bootstrapping process in the terminal*

## Bootstrapping Application Metadata
SolidX requires foundational metadata: system models, roles, users, email/SMS templates, dashboards, and lists of values. 
The `solid seed` command automates this process by populating the database with all these essentials, making the application ready for immediate use.

To seed the database, navigate to the `solid-api` project directory and run `solid seed`:

```bash
cd school-fees-portal/solid-api
solid seed
```

The seed process also creates an `super admin` user, if one does not already exist. The credentials for this user are displayed in the terminal after seeding is complete.

:::info
`solid` is the SolidX CLI utility installed as part of the SolidX scaffolding process.
:::
:::tip
You can run `solid --help` to see all available commands and options.
:::

This command reads predefined JSON files containing the necessary metadata and populates the database accordingly.

### Seeding in Action
![Seeding SolidX Metadata](/img/tutorial/school-fees-portal-v2/seeding_solidx.png)
*Screenshot showing the seeding process in the terminal*

### Log In as Super Admin
Use the credentials displayed after seeding to access the admin panel with full permissions.

![SolidX Admin Panel Login](/img/tutorial/school-fees-portal-v2/admin_panel_login_page.png)
*Screenshot showing the SolidX admin panel login screen*

After logging in, you will be redirected to the default landing page of the admin panel. This page by default is configured to show the listing of all users in the system.

![SolidX Admin Panel Landing Page](/img/tutorial/school-fees-portal-v2/admin_panel_post_login_redirect_page.png)
*Screenshot showing the default landing page after successful login*

---

## Setup Complete - Ready to Build!

Your SolidX environment is now configured and the admin panel is accessible.

You're ready to build a fully functional **school fees portal** application using the SolidX App Builder. No coding required—just visual configuration to create entities, relationships, workflows, and business logic.

Let's start building!


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
SolidX requires a relational database to store application data / metadata. Currently supported databases include PostgreSQL and MSSQL. We will be using PostgreSQL for this tutorial.

### Prerequisites
Before proceeding, Docker must be installed and running on your system.
  - **macOS / Windows**: Install **Docker Desktop**
  - **Ubuntu / Linux**: Install **Docker Engine**

After installation, ensure Docker is running and verify it by executing:

```bash
docker --version
```

### Installing PostgreSQL
This guide explains how to install and run **PostgreSQL 17** locally using Docker.  
This approach avoids installing PostgreSQL directly on your system and provides a clean, reproducible setup.

#### Step 1: Pull PostgreSQL 17 Image
Pull the official PostgreSQL 17 image from Docker Hub.
```bash
docker pull postgres:17
```

#### Step 2: Run the PostgreSQL Container
Run PostgreSQL with a predefined username, password, database name, port binding, and persistent storage.

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
PostgreSQL data is stored in the Docker volume **solidx_pgdata** using the `-v` flag.
	- Data persists across container restarts
	- Removing the container does not delete the data
	- Removing the volume deletes all stored data
:::

#### Step 3: Verify the Container Is Running
Check the list of running containers.

```bash
docker ps
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
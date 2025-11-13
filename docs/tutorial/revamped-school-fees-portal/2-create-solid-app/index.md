---
sidebar_position: 2
---

# 2. Create Solid App

In this step, we'll initialize a new SolidX project using the official starter CLI.

SolidX provides a powerful CLI tool to scaffold a full-stack multi-tenant SaaS application with a backend API and frontend UI, pre-wired for PostgreSQL, authentication, and data modeling.

## Create Solid App
```bash
npx @solidstarters/create-solid-app
```

When you run this command, the CLI will guide you through a series of prompts. Here's an example interaction:

![Create Solid App](/img/tutorial/school-fees-portal/1-bootstrap/school-fees-setup-bootstrap.png)

### Configuration Options

| Prompt | Description |
|--------|-------------|
| **Project Name** | Name of your SolidX project. This will be the folder name where your codebase is generated. |
| **Backend API Port** | The port number on which the backend API will run locally (e.g., `8080`). |
| **Database Client** | The database type you want to use. Currently supports `pg` and `mysql` (PostgreSQL). |
| **Database Username** | Your local database username for connecting to the database. |
| **Database Password** | Password for the above database user. Entered securely in the terminal. |
| **Database Name** | Name of the database to be used for this project. Make sure that you have created this database on your local database server previously. |
| **Database Host** | Hostname of your database server. Typically `localhost` for local development. |
| **Database Port** | Port on which the database is running. PostgreSQL defaults to `5432`. |
| **Sync Models with Database** | Allows auto-syncing database schema with model definitions. Not recommended for production, but useful during development. |
| **Frontend App Port** | The port on which the frontend app will run locally (e.g., `8081`). |

Once you answer these prompts, the CLI performs the following setup steps:

- Sets up boilerplate for the backend
- Installs the Solid CLI binary globally
- Sets up boilerplate for the frontend
- Generates .env files for both backend and frontend:
    - `/school-fees-portal/solid-api/.env`
    - `/school-fees-portal/solid-ui/.env`
- Displays helpful next steps for running your app

## Output

Once the CLI has finished, a new SolidX project is bootstrapped with both a backend and frontend scaffold.

> Please make sure to run the `solid seed` command below, as this is what will seed the local database with all the tables required for SolidX to run properly.
> After you run `solid seed` a default admin user will be configured the password of which will be printed on the terminal. Please make a note of this as this will not appear again.

### Backend 
```bash
cd school-fees-portal/solid-api

# Seed the database with initial metadata
solid seed

# Start backend in development mode
npm run start:dev

# Optionally, run with debug mode
npm run start:debug

# Run in production mode
npm run start
```

The SolidX backend allows you to generate all your REST API endpoints and comes pre-configured with Swagger documentation which you can access at `http://localhost:8080/docs`.

**Swagger Docs:**

The interactive API documentation, powered by Swagger UI, allows you to explore and test the generated REST API endpoints directly from your browser.

![Swagger Docs](/img/tutorial/school-fees-portal/2-data-model/swagger-docs.png)


### Frontend
```bash
cd school-fees-portal/solid-ui

# Start the frontend UI
npm run dev
```

The frontend application will be running at `http://localhost:8081`.

**Default Admin Login Page:**

![Default Admin Login Page](/img/tutorial/school-fees-portal/2-data-model/default-login.png)


### Generated Code

At this point, you will have a folder named after your project (e.g., `school-fees-portal`) in your working directory. You can open this folder in your code editor.

Inside this project folder, you will find two main subdirectories:
1.  `solid-api`: Contains the entire backend NestJS application.
2.  `solid-ui`: Contains the entire frontend Next.js application.

Each of these folders has its own `.env` file, pre-filled with the configuration you provided during the setup process.
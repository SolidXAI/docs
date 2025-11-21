---
sidebar_position: 2
---

# Create Solid App

In this step, we'll initialize a new SolidX project using the official starter CLI. This single command scaffolds a complete full-stack application, giving you a massive head start.

## Create Solid App

Open your terminal and run the following command:

```bash
npx @solidstarters/create-solid-app
```

The CLI will guide you through a series of prompts to configure your project.

![Create Solid App](/img/tutorial/school-fees-portal/1-bootstrap/create-solid-app-cli.png)

### Configuration Options

| Prompt | Description | Example |
|---|---|---|
| **Project Name** | The folder name for your generated codebase. | `school-fees-portal` |
| **Backend API Port** | The local port for the backend API. | `3000` |
| **Database Client** | The database type. | `PostgreSQL` |
| **Database Username** | Your database username. | `your_db_user` |
| **Database Password** | Your database password (entered securely). | `your_db_password` |
| **Database Name** | The name of the database for this project. | `school_fees_portal` |
| **Database Host** | The database server hostname. | `localhost` |
| **Database Port** | The port your database is running on. | `5432` |
| **Sync Models** | Auto-syncs schema with models. Great for dev, but disable for production. | `Yes` |
| **Frontend App Port** | The local port for the frontend UI. | `3001` |

Once you answer these prompts, the CLI scaffolds your entire project, including setting up `.env` files for both the backend and frontend.

## What You Get Out-of-the-Box

This single command generates a feature-rich starting point. Here’s a look at what's included:

-   **Full-Stack Application:** A complete project with a **NestJS backend** (`solid-api`) and a **Next.js frontend** (`solid-ui`).
-   **Authentication & Users:** A pre-built module for user registration, JWT-based login, and password management.
-   **Auto-Generated Admin UI:** A fully functional admin panel to manage your data as soon as you define your models.
-   **Auto-Generated REST API:** Instant RESTful endpoints for all your data models, complete with interactive **Swagger documentation**.
-   **Database Seeding:** A `solid seed` command to initialize your database with necessary system data and a default admin user.
-   **Configured Environments:** Ready-to-use `.env` files for easy management of ports, database credentials, and other settings.
-   **Extensible Architecture:** A clean, modular structure that's easy to extend with your own custom business logic.

## First Steps with Your New App

### 1. Seed the Database

Before you can run the application, you need to seed the database. This creates the necessary tables for the SolidX core systems and sets up your first admin user.

```bash
cd school-fees-portal/solid-api
solid seed
```

:::danger SECURITY WARNING
The `solid seed` command will create a default admin user and print the password **only once** to the terminal. **Save this password immediately** in a secure location. You will need it to log in to the admin panel.
:::

### 2. Run the Backend

The backend server provides the API and serves the admin panel.

```bash
# Still in school-fees-portal/solid-api

# Start in development mode (with hot-reloading)
npm run solidx:dev
```

Once started, you can access the interactive API documentation (Swagger UI) at `http://localhost:3000/docs`.

![Swagger Docs](/img/tutorial/school-fees-portal/2-data-model/swagger-docs.png)

### 3. Run the Frontend

The frontend is the public-facing part of your application.

```bash
# Open a new terminal window
cd school-fees-portal/solid-ui

# Start the frontend UI
npm run dev
```

The default application and admin login page will be running at `http://localhost:3001`.

![Default Admin Login Page](/img/tutorial/school-fees-portal/2-data-model/default-login.png)

## What's Next?

Now that your application is running, the next step is to model your business domain. You will use the powerful **App Builder** inside the admin panel to define the data structures for the school fees portal.


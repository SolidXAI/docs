---
sidebar_position: 10
title: Going Live
description: Guidance on deploying SolidX applications to production environments.
summary: This section provides guidance on deploying SolidX applications to production environments, covering various deployment strategies, configuration steps, and best practices for taking your application from development to live production use.
---

import { HiOutlineServer, HiOutlineCloud, HiOutlineDesktopComputer } from "react-icons/hi";
import { FaDocker } from "react-icons/fa";

# Going Live

This section provides guidance on how to deploy your SolidX applications to production. We cover a range of deployment strategies to suit your needs, from traditional virtual machines to modern container-based workflows.

<div className="row">
  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h3>
          <HiOutlineServer size={22} />
          &nbsp;Virtual Machine
        </h3>
      </div>
      <div className="card__body">
        <p>
          Deploy your application to a traditional virtual machine. This guide covers setting up your environment, configuring a process manager, and using Nginx as a reverse proxy.
        </p>
      </div>
      <div className="card__footer">
        <a href="/docs/developer-docs/going-live/deploying-to-vm" className="button button--primary button--block">
          Deploy to VM
        </a>
      </div>
    </div>
  </div>
  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h3>
          <HiOutlineCloud size={22} />
          &nbsp;Amazon ECS
        </h3>
      </div>
      <div className="card__body">
        <p>
          Use AWS Fargate to deploy your application in a serverless environment. This guide will walk you through containerizing your app, pushing it to ECR, and setting up your ECS cluster.
        </p>
      </div>
      <div className="card__footer">
        <a href="/docs/developer-docs/going-live/deploying-to-ecs" className="button button--primary button--block">
          Deploy to ECS
        </a>
      </div>
    </div>
  </div>
  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h3>
          <FaDocker size={22} />
          &nbsp;Docker
        </h3>
      </div>
      <div className="card__body">
        <p>
          Containerize your application with Docker for a consistent and reproducible deployment. This guide covers multi-stage builds and setting up a production-ready Docker Compose file.
        </p>
      </div>
      <div className="card__footer">
        <a href="/docs/developer-docs/going-live/deploying-to-docker" className="button button--primary button--block">
          Deploy with Docker
        </a>
      </div>
    </div>
  </div>
</div>

---

## Going Live with a Solid App Template

This guide provides instructions on how to deploy a Solid application generated from the `create-solid-app` template.

We will cover two approaches: a manual deployment and an advanced deployment using Docker.

### Manual Deployment

This approach involves building the frontend and backend applications and running them as separate processes.

#### Prerequisites

*   Node.js and npm installed on your server.
*   A database (e.g., PostgreSQL, MongoDB) running and accessible from your server.

#### Steps

1.  **Clone your project:**
    ```bash
    git clone <your-project-repository>
    cd <your-project-directory>
    ```

2.  **Set up the backend:**
    *   Navigate to the `solid-api` directory:
        ```bash
        cd solid-api
        ```
    *   Install dependencies:
        ```bash
        npm install
        ```
    *   Create a `.env` file and configure your database connection and other environment variables. You can use `.env.example` as a reference.
    *   Build the application:
        ```bash
        npm run build
        ```
    *   Run the application:
        ```bash
        npm run start:prod
        ```

3.  **Set up the frontend:**
    *   Navigate to the `solid-ui` directory:
        ```bash
        cd ../solid-ui
        ```
    *   Install dependencies:
        ```bash
        npm install
        ```
    *   Create a `.env` file and configure your API URL and other environment variables.
    *   Build the application:
        ```bash
        npm run build
        ```
    *   Run the application:
        ```bash
        npm run start
        ```

Your Solid application should now be running. You may want to use a process manager like `pm2` to keep the applications running in the background.

### Advanced Deployment (Docker)

This approach uses Docker to containerize the frontend and backend applications.

#### Prerequisites

*   Docker and Docker Compose installed on your server.

#### Steps

1.  **Clone your project:**
    ```bash
    git clone <your-project-repository>
    cd <your-project-directory>
    ```

2.  **Configure your environment:**
    *   Create a `.env` file in the root of your project and configure your database connection, API URL, and other environment variables. The `docker-compose.yml` file is set up to use this file.

3.  **Build and run the containers:**
    ```bash
    docker-compose up -d --build
    ```

This command will build the Docker images for the `solid-api` and `solid-ui` applications and run them in the background.

Your Solid application is now running and accessible on the ports specified in your `docker-compose.yml` file.

---

Explore the guides to find the deployment strategy that best fits your project's needs. Each guide provides a step-by-step walkthrough to get your SolidX application up and running in a production environment.

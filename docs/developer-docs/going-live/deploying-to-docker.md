---
title: Docker
description: This guide provides a comprehensive walkthrough for deploying SolidX applications using Docker for production.
summary: Learn how to containerize your SolidX application with Docker. This guide covers creating multi-stage Dockerfiles for both the backend and frontend, setting up a production-ready Docker Compose file to manage your multi-container application, and provides instructions for building, running, and pushing your container images.
sidebar_position: 3
---

import { HiOutlineCog, HiOutlineServer, HiOutlineCode, HiOutlineDesktopComputer, HiOutlineCloudUpload } from "react-icons/hi";
import { FaDocker } from "react-icons/fa";
import { InfoBox } from '@site/src/common/InfoBox';

# Deploying with Docker

This guide provides a comprehensive walkthrough for deploying your SolidX application using Docker. Containerizing your application is a best practice for creating a consistent and reproducible production environment.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    Docker is the packaging boundary for a SolidX application. Instead of relying on a manually prepared host, you define the runtime once and move that same containerized setup across environments.
  </p>
  <ul>
    <li>Choose Docker when reproducibility matters across local, staging, and production.</li>
    <li>Think of images as portable runtime snapshots.</li>
    <li>Use Compose when you want to run the app stack as coordinated services.</li>
  </ul>
  <p>
    So the intuition is: <strong>Docker reduces environment drift by making the application runtime explicit and portable</strong>.
  </p>
</div>

<InfoBox>
  Before you begin, ensure you have Docker and Docker Compose installed on your system. You can find installation instructions on the official Docker website.
</InfoBox>

## 1. Dockerizing Your Application

The `create-solid-app` template already provides multi-stage Dockerfiles for both the backend (`solid-api/Dockerfile`) and frontend (`solid-ui/Dockerfile`) to create lean and secure production images.

## 2. Using Docker Compose for Production

The `create-solid-app` template includes a `docker-compose.yml` file to define and manage your multi-container application, including a database. You can find this file in the root of your generated project.

<h3 className="card-headear-wrapper">
    <HiOutlineCog size={22} />
    &nbsp;Configure Environment Variables
</h3>

While the `Dockerfile` defines the environment *inside* the container, the `docker-compose.yml` file and the `.env` file are used to configure the services from the *outside*. This is crucial for security and portability, as it allows you to inject environment-specific variables like database credentials and API keys without hardcoding them into the Docker image.

Create a `.env` file in the root of your project to store your database credentials:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

<InfoBox>
  Docker Compose automatically loads the `.env` file from the root directory and injects these variables into the containers at runtime. Remember to add `.env` to your `.gitignore` file to avoid committing sensitive information.
</InfoBox>

## 3. Building and Running the Containers

Now you can build and run your entire application stack with a single command.

<h3 className="card-headear-wrapper">
    <FaDocker size={22} />
    &nbsp;Build and Run
</h3>

```bash
docker-compose up --build -d
```
This command will build the images and start the containers in detached mode.

<h3 className="card-headear-wrapper">
    <HiOutlineServer size={20} />
    &nbsp;View Logs
</h3>

To view the logs from your running containers:
```bash
docker-compose logs -f
```

## 4. Verifying the Deployment

<h3 className="card-headear-wrapper">
    <HiOutlineServer size={20} />
    &nbsp;Backend API
</h3>

The backend API should be accessible at `http://localhost:3000`, and the Swagger documentation at `http://localhost:3000/docs`.

<h3 className="card-headear-wrapper">
    <HiOutlineDesktopComputer size={20} />
    &nbsp;Frontend Application
</h3>

The frontend should be running at `http://localhost:3001`.

## 5. Post-Deployment

<h3 className="card-headear-wrapper">
    <HiOutlineCloudUpload size={22} />
    &nbsp;Pushing Images to a Container Registry
</h3>

To deploy your application to a cloud provider, you'll need to push your images to a container registry like Docker Hub or AWS ECR.

**1. Log in to your container registry:**
```bash
docker login your_registry_url
```

**2. Tag your images:**
```bash
docker-compose build
docker-compose push
```

You can also manually tag and push your images:
```bash
docker tag <local_image_name>:<tag> <registry_url>/<image_name>:<tag>
docker push <registry_url>/<image_name>:<tag>
```

Congratulations! You have successfully deployed your SolidX application with Docker.

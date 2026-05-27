---
title: Docker
description: This guide provides a comprehensive walkthrough for deploying SolidX applications using Docker for production.
summary: Learn how to containerize your SolidX application with Docker. This guide covers creating multi-stage Dockerfiles for both the backend and frontend, setting up a production-ready Docker Compose file to manage your multi-container application, and provides instructions for building, running, and pushing your container images.
---

This guide provides a comprehensive walkthrough for deploying your SolidX application using Docker. Containerizing your application is a best practice for creating a consistent and reproducible production environment.

> Before you begin, ensure you have Docker and Docker Compose installed on your system. You can find installation instructions on the official Docker website.

## 1. Dockerizing Your Application

The `create-solid-app` template already provides multi-stage Dockerfiles for both the backend (`solid-api/Dockerfile`) and frontend (`solid-ui/Dockerfile`) to create lean and secure production images.

## 2. Using Docker Compose for Production

The `create-solid-app` template includes a `docker-compose.yml` file to define and manage your multi-container application, including a database. You can find this file in the root of your generated project.

### Configure Environment Variables

While the `Dockerfile` defines the environment *inside* the container, the `docker-compose.yml` file and the `.env` file are used to configure the services from the *outside*. This is crucial for security and portability, as it allows you to inject environment-specific variables like database credentials and API keys without hardcoding them into the Docker image.

Create a `.env` file in the root of your project to store your database credentials:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

> Docker Compose automatically loads the `.env` file from the root directory and injects these variables into the containers at runtime. Remember to add `.env` to your `.gitignore` file to avoid committing sensitive information.

## 3. Building and Running the Containers

Now you can build and run your entire application stack with a single command.

### Build and Run

```bash
docker-compose up --build -d
```

This command will build the images and start the containers in detached mode.

### View Logs

To view the logs from your running containers:

```bash
docker-compose logs -f
```

## 4. Verifying the Deployment

### Backend API

The backend API should be accessible at `http://localhost:3000`, and the Swagger documentation at `http://localhost:3000/docs`.

### Frontend Application

The frontend should be running at `http://localhost:3001`.

## 5. Post-Deployment

### Pushing Images to a Container Registry

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

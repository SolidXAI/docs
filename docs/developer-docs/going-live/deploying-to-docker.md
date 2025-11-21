---
title: Docker
description: This guide provides a comprehensive walkthrough for deploying SolidX applications using Docker.
summary: Learn how to containerize your SolidX application with Docker. This guide covers creating Dockerfiles for both the backend and frontend, setting up a Docker Compose file to manage your multi-container application, and provides instructions for building and running your containers.
sidebar_position: 3
---

import { HiOutlineCog, HiOutlineServer, HiOutlineCode, HiOutlineDesktopComputer } from "react-icons/hi";
import { FaDocker } from "react-icons/fa";
import { InfoBox } from '@site/src/common/InfoBox';

# Deploying with Docker

This guide provides a comprehensive walkthrough for deploying SolidX applications using Docker. Containerizing your application with Docker provides a consistent and reproducible environment for your application, simplifying both development and deployment.

<InfoBox>
  Before you begin, ensure you have Docker and Docker Compose installed on your system. You can find installation instructions on the official Docker website.
</InfoBox>

## A) Dockerizing the Application

When you create a new SolidX application using `create-solid-app`, Dockerfiles are already included in the `solid-api` and `solid-ui` directories.

If you don't have them, you can copy them from the templates:

<h3 className="card-headear-wrapper">
    <FaDocker size={22} />
    &nbsp;Copy Dockerfiles
</h3>

```bash
cp ../create-solid-app/templates/nest-template/Dockerfile solid-api/
cp ../create-solid-app/templates/next-template/Dockerfile solid-ui/
```

## B) Using Docker Compose

A `docker-compose.yml` file is also included in the root of your project. If you don't have it, you can copy it from the `create-solid-app` templates.

<h3 className="card-headear-wrapper">
    <HiOutlineCode size={22} />
    &nbsp;Copy `docker-compose.yml`
</h3>

```bash
cp ../create-solid-app/templates/docker-compose.yml .
```

The `docker-compose.yml` file should look like this:

```yaml
services:
  api:
    build:
      context: ./solid-api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - PORT=3000

  ui:
    build:
      context: ./solid-ui
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    depends_on:
      - api
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:3000
```

## C) Building and Running the Containers

Now that you have your Dockerfiles and Docker Compose file set up, you can build and run your containers.

<h3 className="card-headear-wrapper">
    <HiOutlineCog size={22} />
    &nbsp;Build and Run
</h3>

Open a terminal in the root of your project and run the following command:

```bash
docker-compose up --build -d
```

This command will build the images for `solid-api` and `solid-ui` if they don't already exist, and then start the containers in detached mode.

## D) Verifying the Deployment

Once the containers are running, you can verify that the deployment was successful.

<h3 className="card-headear-wrapper">
    <HiOutlineServer size={20} />
    &nbsp;Verify Backend
</h3>

You can access the backend API at `http://localhost:3000`. The Swagger documentation should be available at `http://localhost:3000/docs`.

<h3 className="card-headear-wrapper">
    <HiOutlineDesktopComputer size={20} />
    &nbsp;Verify Frontend
</h3>

The frontend application should be accessible at `http://localhost:3001`.

Congratulations! You have successfully deployed your SolidX application with Docker.
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

<InfoBox>
  Before you begin, ensure you have Docker and Docker Compose installed on your system. You can find installation instructions on the official Docker website.
</InfoBox>

## 1. Dockerizing Your Application

We will use multi-stage builds to create lean and secure production images for both the backend and frontend.

<h3 className="card-headear-wrapper">
    <HiOutlineCode size={22} />
    &nbsp;Backend Dockerfile (`solid-api/Dockerfile`)
</h3>

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS build

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /usr/src/app

COPY --from=build /usr/src/app/node_modules ./node_modules
COPY --from=build /usr/src/app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/main"]
```

<h3 className="card-headear-wrapper">
    <HiOutlineCode size={22} />
    &nbsp;Frontend Dockerfile (`solid-ui/Dockerfile`)
</h3>

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS build

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /usr/src/app

COPY --from=build /usr/src/app/node_modules ./node_modules
COPY --from=build /usr/src/app/.next ./.next
COPY --from=build /usr/src/app/public ./public
COPY --from=build /usr/src/app/package.json ./package.json

EXPOSE 3001

CMD ["npm", "start"]
```

## 2. Using Docker Compose for Production

We will create a `docker-compose.yml` file to define and manage our multi-container application, including a database.

<h3 className="card-headear-wrapper">
    <HiOutlineCode size={22} />
    &nbsp;Create `docker-compose.yml`
</h3>

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./solid-api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
      - DB_HOST=db
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=${DB_NAME}
    depends_on:
      - db
    networks:
      - solidx-net

  ui:
    build:
      context: ./solid-ui
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:3000
    depends_on:
      - api
    networks:
      - solidx-net

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - solidx-net

networks:
  solidx-net:
    driver: bridge

volumes:
  postgres_data:
```

<h3 className="card-headear-wrapper">
    <HiOutlineCog size={22} />
    &nbsp;Configure Environment Variables
</h3>

Create a `.env` file in the root of your project to store your database credentials:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

<InfoBox>
  Docker Compose automatically loads the `.env` file from the root directory. Remember to add `.env` to your `.gitignore` file.
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
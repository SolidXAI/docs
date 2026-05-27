---
title: Deploying to ECS
description: A comprehensive guide for deploying SolidX applications to Amazon ECS with Fargate.
summary: This guide will walk you through the process of deploying your SolidX application to Amazon Elastic Container Service (ECS) using Fargate. We will cover containerizing your application, pushing it to ECR, and setting up the necessary ECS resources.
---

This guide will walk you through deploying your SolidX application to Amazon Elastic Container Service (ECS) with Fargate, a serverless compute engine that allows you to run containers without managing the underlying infrastructure.

> Before you begin, make sure you have an AWS account, the AWS CLI installed and configured, and Docker running on your local machine.

## 1. Containerize and Push to ECR

First, we need to containerize our application and push the images to Amazon Elastic Container Registry (ECR).

### Create ECR Repositories

Create ECR repositories for both the backend and frontend:

```bash
aws ecr create-repository --repository-name solidx-api --region <your-region>
aws ecr create-repository --repository-name solidx-ui --region <your-region>
```

### Authenticate Docker to ECR

Authenticate your Docker client to your ECR registry:

```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

### Build, Tag, and Push Images

Build, tag, and push the Docker images for both services.

**Backend (`solidx-api`):**

```bash
cd solid-api
docker build -t <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/solidx-api:latest .
docker push <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/solidx-api:latest
```

**Frontend (`solidx-ui`):**

```bash
cd ../solid-ui
docker build -t <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/solidx-ui:latest .
docker push <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/solidx-ui:latest
```

## 2. Set Up ECS Resources

Now, let's create the necessary ECS resources to run our application.

### Create an ECS Cluster

Create an ECS cluster to host your services:

```bash
aws ecs create-cluster --cluster-name solidx-cluster --region <your-region>
```

### Create Task Definitions

Create task definitions for the backend and frontend. A task definition is a blueprint for your application.

Create a `solidx-api-task-definition.json` file:

```json
{
    "family": "solidx-api-task",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "solidx-api",
            "image": "<your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/solidx-api:latest",
            "portMappings": [
                {
                    "containerPort": 3000,
                    "hostPort": 3000
                }
            ],
            "essential": true
        }
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "256",
    "memory": "512"
}
```

And a `solidx-ui-task-definition.json` file:

```json
{
    "family": "solidx-ui-task",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "solidx-ui",
            "image": "<your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/solidx-ui:latest",
            "portMappings": [
                {
                    "containerPort": 3001,
                    "hostPort": 3001
                }
            ],
            "essential": true
        }
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "256",
    "memory": "512"
}
```

Now, register the task definitions with ECS:

```bash
aws ecs register-task-definition --cli-input-json file://solidx-api-task-definition.json --region <your-region>
aws ecs register-task-definition --cli-input-json file://solidx-ui-task-definition.json --region <your-region>
```

## 3. Create Services and Load Balancer

We will create an Application Load Balancer (ALB) to route traffic to our services.

### Create an ALB and Target Groups

1. Create a security group for your ALB.
2. Create an Application Load Balancer.
3. Create target groups for `solidx-api` and `solidx-ui`.
4. Create listeners for your ALB to forward traffic to the target groups (e.g., port 80 and 443).

### Create ECS Services

Create the services that will run and maintain your tasks.

Create a `solidx-api-service.json` file:

```json
{
    "cluster": "solidx-cluster",
    "serviceName": "solidx-api-service",
    "taskDefinition": "solidx-api-task",
    "desiredCount": 1,
    "launchType": "FARGATE",
    "networkConfiguration": {
        "awsvpcConfiguration": {
            "subnets": ["<your-subnet-id-1>", "<your-subnet-id-2>"],
            "securityGroups": ["<your-security-group-id>"],
            "assignPublicIp": "ENABLED"
        }
    },
    "loadBalancers": [
        {
            "targetGroupArn": "<your-api-target-group-arn>",
            "containerName": "solidx-api",
            "containerPort": 3000
        }
    ]
}
```

And a `solidx-ui-service.json` file:

```json
{
    "cluster": "solidx-cluster",
    "serviceName": "solidx-ui-service",
    "taskDefinition": "solidx-ui-task",
    "desiredCount": 1,
    "launchType": "FARGATE",
    "networkConfiguration": {
        "awsvpcConfiguration": {
            "subnets": ["<your-subnet-id-1>", "<your-subnet-id-2>"],
            "securityGroups": ["<your-security-group-id>"],
            "assignPublicIp": "ENABLED"
        }
    },
    "loadBalancers": [
        {
            "targetGroupArn": "<your-ui-target-group-arn>",
            "containerName": "solidx-ui",
            "containerPort": 3001
        }
    ]
}
```

Now, create the services:

```bash
aws ecs create-service --cli-input-json file://solidx-api-service.json --region <your-region>
aws ecs create-service --cli-input-json file://solidx-ui-service.json --region <your-region>
```

## 4. Verify Your Deployment

Once the services are running, you can access your application through the DNS name of your Application Load Balancer. You can find the DNS name in the EC2 console under "Load Balancers".

Congratulations! You have successfully deployed your SolidX application to Amazon ECS with Fargate.

---
title: ECS
description: A comprehensive guide for deploying SolidX applications to Amazon ECS with Fargate.
summary: This guide will walk you through the process of deploying your SolidX application to Amazon Elastic Container Service (ECS) using Fargate. We will cover containerizing your application, pushing it to ECR, and setting up the necessary ECS resources.
sidebar_position: 2
---

import { HiOutlineCloud, HiOutlineCog, HiOutlineServer, HiOutlineCloudUpload } from "react-icons/hi";
import { FaAws } from "react-icons/fa";
import { InfoBox } from '@site/src/common/InfoBox';

# Deploying to Amazon ECS with Fargate

This guide will walk you through deploying your SolidX application to Amazon Elastic Container Service (ECS) with Fargate, a serverless compute engine that allows you to run containers without managing the underlying infrastructure.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    ECS with Fargate is the managed-container version of the Docker story. You still package the application as containers, but AWS takes over the responsibility of running them on infrastructure you do not manage directly.
  </p>
  <ul>
    <li>Choose this path when you want container-based deployment with less host management.</li>
    <li>Think in terms of images, task definitions, services, networking, and load balancing.</li>
    <li>This model moves the operational focus from servers to cloud resources and deployment topology.</li>
  </ul>
  <p>
    So the intuition is: <strong>ECS/Fargate lets you keep container discipline while outsourcing server management to AWS</strong>.
  </p>
</div>

<InfoBox>
  Before you begin, make sure you have an AWS account, the AWS CLI installed and configured, and Docker running on your local machine.
</InfoBox>

## 1. Containerize and Push to ECR

First, we need to containerize our application and push the images to Amazon Elastic Container Registry (ECR).

<h3 className="card-headear-wrapper">
    <HiOutlineCloudUpload size={22} />
    &nbsp;Create ECR Repositories
</h3>

Create ECR repositories for both the backend and frontend:
```bash
aws ecr create-repository --repository-name solidx-api --region <your-region>
aws ecr create-repository --repository-name solidx-ui --region <your-region>
```

<h3 className="card-headear-wrapper">
    <HiOutlineCog size={22} />
    &nbsp;Authenticate Docker to ECR
</h3>

Authenticate your Docker client to your ECR registry:
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

<h3 className="card-headear-wrapper">
    <HiOutlineCloudUpload size={22} />
    &nbsp;Build, Tag, and Push Images
</h3>

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

<h3 className="card-headear-wrapper">
    <FaAws size={22} />
    &nbsp;Create an ECS Cluster
</h3>

Create an ECS cluster to host your services:
```bash
aws ecs create-cluster --cluster-name solidx-cluster --region <your-region>
```

<h3 className="card-headear-wrapper">
    <HiOutlineCog size={22} />
    &nbsp;Create Task Definitions
</h3>

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

<h3 className="card-headear-wrapper">
    <HiOutlineServer size={20} />
    &nbsp;Create an ALB and Target Groups
</h3>

1.  Create a security group for your ALB.
2.  Create an Application Load Balancer.
3.  Create target groups for `solidx-api` and `solidx-ui`.
4.  Create listeners for your ALB to forward traffic to the target groups (e.g., port 80 and 443).

<h3 className="card-headear-wrapper">
    <HiOutlineCloud size={22} />
    &nbsp;Create ECS Services
</h3>

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

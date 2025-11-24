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

Explore the guides to find the deployment strategy that best fits your project's needs. Each guide provides a step-by-step walkthrough to get your SolidX application up and running in a production environment.

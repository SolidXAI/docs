---
title: Virtual Machine
description: A step-by-step guide to deploying SolidX applications on Ubuntu virtual machines.
summary: This comprehensive guide walks through deploying SolidX applications on Ubuntu virtual machines. It covers cloning the repository, configuring environment variables, verifying backend and frontend operation, deploying with PM2 process manager (including config files and deploy scripts), database seeding with the rebuild script, and setting up Nginx as a reverse proxy with SSL certificates via Certbot. The guide also includes firewall configuration, virtual host setup, log rotation setup, and automatic restart configuration for production-ready deployment.
---

# Deploying to a Virtual Machine

This guide provides a comprehensive walkthrough for deploying your SolidX application to a virtual machine (VM). We will cover everything from setting up your environment to deploying and securing your application.

  Before you begin, ensure you have completed the [Prerequisites](/docs/developer-docs/prerequisites) and have a running VM with root access.

## 1. Initial Setup

This section covers the initial steps to get your SolidX application running on a VM.

&nbsp;Clone Your Repository

First, clone your application's repository to your VM:
```bash
git clone <your_repository_url>
cd <your_project_directory>
```

&nbsp;Configure Environment Variables

Your application will need environment variables for configuration. Create `.env` files for both the backend and frontend.

**Backend (`solid-api/.env`):**
```
# Server Configuration
PORT=3000

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

# JWT Configuration
JWT_SECRET=your_jwt_secret
```

**Frontend (`solid-ui/.env`):**
```
NEXT_PUBLIC_API_URL=http://localhost:3000
```

  It is crucial to keep your `.env` files secure and out of version control. Add `.env` to your `.gitignore` file.

## 2. Running the Application Manually

Before automating the deployment, let's run the backend and frontend manually to ensure everything is set up correctly.

&nbsp;Verify Backend

```bash
cd solid-api
npm install
npm run build
npm run start
```
You should see a confirmation message that the server is running on port 3000.

&nbsp;Verify Frontend

```bash
cd solid-ui
npm install
npm run build
npm run start
```
The frontend application should now be running on port 3001.

> Press `Ctrl + C` to stop the applications. We will use `pm2` to manage them in the next step.

## 3. Deploying with PM2

PM2 is a process manager that will keep your application running and handle restarts.

&nbsp;Install PM2

```bash
npm install -g pm2
```

&nbsp;Create PM2 Configuration Files

Create `pm2.config.js` files for both the backend and frontend.

**Backend (`solid-api/pm2.config.js`):**
```javascript
module.exports = {
  apps: [
    {
      name: "solidx-api",
      script: "npm",
      args: "run start",
      watch: true,
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
```

**Frontend (`solid-ui/pm2.config.js`):**
```javascript
module.exports = {
  apps: [
    {
      name: "solidx-ui",
      script: "npm",
      args: "run start",
      watch: true,
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
```

&nbsp;Start Applications with PM2

```bash
cd solid-api
pm2 start pm2.config.js

cd ../solid-ui
pm2 start pm2.config.js
```

You can check the status of your applications with `pm2 list`.

## 4. Setting Up Nginx as a Reverse Proxy

Nginx will act as a reverse proxy, directing traffic to your backend and frontend applications.

&nbsp;Install and Configure Nginx

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

&nbsp;Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

&nbsp;Create Nginx Virtual Host Files

Create separate configuration files for your API and UI.

**Backend (`/etc/nginx/sites-available/api.your_domain.com`):**
```nginx
server {
  server_name api.your_domain.com;

  location / {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
  }
}
```

**Frontend (`/etc/nginx/sites-available/your_domain.com`):**
```nginx
server {
  server_name your_domain.com;

  location / {
    proxy_pass http://localhost:3001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
  }
}
```

&nbsp;Enable Virtual Hosts

```bash
sudo ln -s /etc/nginx/sites-available/api.your_domain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/your_domain.com /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx
```

## 5. Securing Your Application with SSL

Secure your application by enabling HTTPS with SSL certificates from Let's Encrypt.

&nbsp;Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

&nbsp;Obtain SSL Certificates

```bash
sudo certbot --nginx -d your_domain.com -d api.your_domain.com
```

Certbot will automatically update your Nginx configuration to use the SSL certificates.

## 6. Post-Deployment

Here are some additional steps to ensure your application runs smoothly in production.

&nbsp;Automatic Restart on Reboot

To ensure your applications restart after a server reboot, run:
```bash
pm2 save
pm2 startup
```

&nbsp;Log Management

PM2 can manage your application's logs. To view logs, run:
```bash
pm2 logs solidx-api
pm2 logs solidx-ui
```

For log rotation, you can use `pm2-logrotate`:
```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:compress true
```

&nbsp;Monitoring

You can monitor your application's resource usage with:
```bash
pm2 monit
```

Congratulations! You have successfully deployed and secured your SolidX application on a VM.

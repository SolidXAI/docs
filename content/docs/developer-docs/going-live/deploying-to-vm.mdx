---
title: Virtual Machine
icon: "server"
description: A step-by-step guide to deploying SolidX applications on Ubuntu virtual machines.
summary: This comprehensive guide walks through deploying SolidX applications on Ubuntu virtual machines. It covers cloning the repository, configuring environment variables, verifying backend and frontend operation, deploying with PM2 process manager (including config files and deploy scripts), database seeding with the rebuild script, and setting up Nginx as a reverse proxy with SSL certificates via Certbot. The guide also includes firewall configuration, virtual host setup, log rotation setup, and automatic restart configuration for production-ready deployment.
---


# Deploying to a Virtual Machine

This guide provides a comprehensive walkthrough for deploying your SolidX application to a virtual machine (VM). We will cover everything from setting up your environment to deploying and securing your application.

<Callout type="info" title="Mental Model">

  VM deployment is the most explicit hosting model in this section. You manage the machine, the processes, the reverse proxy, and the operating-system-level concerns yourself.
  - Choose this path when you want maximum control over the host.
    - Expect to manage process lifecycle, networking, SSL, logs, and patching.
    - This is often the easiest model to reason about if your team is comfortable with Linux operations.
  So the intuition is: <strong>a VM gives you the most control, but also the most operational responsibility</strong>.

</Callout>


  Before you begin, ensure you have completed the **[Prerequisites](/docs/developer-docs/prerequisites)** guide on your VM. This includes installing **Node.js**, **Git**, and **PostgreSQL**, and setting up your initial database user.


## 1. Environment Preparation

Once your core dependencies are installed via the Prerequisites guide, you need to prepare the VM for production traffic.

### Install Deployment Tools

#### Nginx
Install Nginx to act as your reverse proxy.

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### PM2
Install PM2 globally to manage your application processes.

```bash
sudo npm install -g pm2
```

## 2. Project Setup

We will deploy the application in the `/opt/gitco` directory.

<h3 className="">
    
    &nbsp;Prepare Directory and Clone Repository
</h3>

Create the deployment directory and set the appropriate permissions (replace `your_user` with your Ubuntu username):

```bash
sudo mkdir -p /opt/gitco
sudo chown -R $USER:$USER /opt/gitco
cd /opt/gitco
git clone <your_repository_url> .
```

<h3 className="">
    
    &nbsp;Configure Environment Variables
</h3>

Your application will need environment variables for configuration. Create `.env` files for both the backend and frontend.

**Backend (`solid-api/.env`):**
```bash
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
```bash
NEXT_PUBLIC_API_URL=http://localhost:3000
```


  It is crucial to keep your `.env` files secure and out of version control. Add `.env` to your `.gitignore` file.


## 3. Running the Application Manually

Before automating the deployment, let's run the backend and frontend manually to ensure everything is set up correctly.

<h3 className="">
    
    &nbsp;Verify Backend
</h3>

```bash
cd /opt/gitco/solid-api
npm install
npm run build
```
The `solid-api` directory will be served using PM2 and Nginx. In this step, we verify that the project builds successfully on the server, ensuring it’s ready for deployment and further automation.

<h3 className="">
    
    &nbsp;Verify Frontend
</h3>

```bash
cd /opt/gitco/solid-ui
npm install
npm run build
```
Verify that the `dist` directory is created successfully. Note that for `solid-ui`, we serve the directory directly via Nginx without using PM2.

## 4. Deploying the Backend with PM2

PM2 will keep your backend application running and handle restarts.

<h3 className="">
    
    &nbsp;Create PM2 Configuration File
</h3>

Create a `pm2.config.js` file for the backend.

**Backend (`/opt/gitco/solid-api/pm2.config.js`):**
```javascript
module.exports = {
  apps: [
    {
      name: "solidx-api",
      script: "npm",
      args: "run start",
      cwd: "/opt/gitco/solid-api",
      watch: false,
      env: {
        ENV: "production",
      },
    },
  ],
};
```

<h3 className="">
    
    &nbsp;Start Backend with PM2
</h3>

```bash
cd /opt/gitco/solid-api
pm2 start pm2.config.js
```

You can check the status of your applications with `pm2 list`.

## 5. Setting Up Nginx

Nginx will act as a reverse proxy for your backend and serve your frontend as static files.

<h3 className="">
    
    &nbsp;Configure Firewall
</h3>

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

<h3 className="">
    
    &nbsp;Create Nginx Virtual Host Files
</h3>

Create separate configuration files for your API and UI.

**Backend (`/etc/nginx/sites-available/api.your_domain.com`):**
```nginx
server {
  listen 80;
  server_name api.your_domain.com;

  location / {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

**Frontend (`/etc/nginx/sites-available/your_domain.com`):**
```nginx
server {
  listen 80;
  server_name your_domain.com;

  # Vite build output
  root /opt/gitco/solid-ui/dist;
  index index.html;

  # ----------------------------
  # Basic security + hardening
  # ----------------------------
  add_header X-Content-Type-Options "nosniff" always;
  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;

  # ----------------------------
  # Compression (blazing fast)
  # ----------------------------
  gzip on;
  gzip_comp_level 5;
  gzip_min_length 1024;
  gzip_vary on;
  gzip_proxied any;
  gzip_types
    text/plain
    text/css
    text/javascript
    application/javascript
    application/json
    application/xml
    application/rss+xml
    application/atom+xml
    image/svg+xml
    font/ttf
    font/otf
    application/vnd.ms-fontobject;

  # ----------------------------
  # Cache strategy
  # ----------------------------

  # 1) Hashed build assets (Vite typically outputs /assets/* with content hashes)
  location ^~ /assets/ {
    try_files $uri =404;
    expires 365d;
    add_header Cache-Control "public, max-age=31536000, immutable" always;
    access_log off;
  }

  # 2) Other static files (fonts/images/icons/etc.)
  location ~* \.(?:js|css|png|jpg|jpeg|gif|webp|svg|ico|woff2?|ttf|eot|map)$ {
    try_files $uri =404;
    expires 30d;
    add_header Cache-Control "public, max-age=2592000" always;
    access_log off;
  }

  # 3) Do NOT cache index.html (so new deployments take effect immediately)
  location = /index.html {
    expires -1;
    add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0" always;
  }

  # SPA fallback
  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

<h3 className="">
    
    &nbsp;Enable Virtual Hosts
</h3>

```bash
sudo ln -s /etc/nginx/sites-available/api.your_domain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/your_domain.com /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl restart nginx
```

## 6. Securing Your Application with SSL

Secure your application by enabling HTTPS with SSL certificates from Let's Encrypt.

<h3 className="">
    
    &nbsp;Install Certbot
</h3>

```bash
sudo apt install certbot python3-certbot-nginx -y
```

<h3 className="">
    
    &nbsp;Obtain SSL Certificates
</h3>

```bash
sudo certbot --nginx -d your_domain.com -d api.your_domain.com
```

Certbot will automatically update your Nginx configuration to use the SSL certificates.

## 7. Post-Deployment

Here are some additional steps to ensure your application runs smoothly in production.

<h3 className="">
    
    &nbsp;Automatic Restart on Reboot
</h3>

To ensure your applications restart after a server reboot, run:
```bash
pm2 save
pm2 startup
```

<h3 className="">
    
    &nbsp;Log Management
</h3>

PM2 can manage your backend application's logs. To view logs, run:
```bash
pm2 logs solidx-api
```

Nginx logs can be viewed at:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

For log rotation, you can use `pm2-logrotate` for PM2 logs:
```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:compress true
```

<h3 className="">
    
    &nbsp;Monitoring
</h3>

You can monitor your application's resource usage with:
```bash
pm2 monit
```

Congratulations! You have successfully deployed and secured your SolidX application on a VM.

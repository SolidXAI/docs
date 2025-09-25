---
title: Deploying SolidX to VM
description: Step-by-step guide to deploy SolidX applications on Ubuntu virtual machines.
sidebar_position: 1
---

import { HiOutlineCog, HiOutlineServer } from "react-icons/hi2"
import { HiOutlineCode,HiOutlineDesktopComputer } from "react-icons/hi";
import { FaLightbulb } from "react-icons/fa";
import { InfoBox } from '@site/src/common/InfoBox';




# Deploying to VM

This section provides guidance on how to deploy your SolidX applications to a virtual machine (VM).


<InfoBox>
 Before continuing, make sure you've completed the [Prerequisites](/docs/developer-docs/prerequisites).
</InfoBox>

## A) Run SolidX Application

This section explains how to run the SolidX app on a virtual machine.


 <h3 className=" card-headear-wrapper">
    <HiOutlineCode size={22}  />

### Clone Repository
  </h3>



```bash
git clone <repo http url>
```


 <h3 className=" card-headear-wrapper">
    <HiOutlineCog size={22}  />

### Update Environment Variables
  </h3>

Create the `.env` files inside `solid-api` and `solid-ui` with your database credentials and other configs.

 <h3 className=" card-headear-wrapper">
    <HiOutlineServer size={20}  />

### Verify Backend is Running
  </h3>


```bash
cd solid-api
npm i
npm run build
npm run start
```


 <h3 className=" card-headear-wrapper">
    <HiOutlineDesktopComputer size={20}  />

### Verify Frontend is Running
  </h3>


```bash
cd solid-ui
npm i
npm run build
npm run start
```

> Press `Ctrl + C` to exit; we will use `pm2` next.

## B)  Deploy with Process Manager

### 1. Install pm2 Globally

```bash
npm install -g pm2
```

### 2. Create pm2 Config File

Inside both `solid-api` and `solid-ui` folders, create `pm2.config.js`:

```js
module.exports = {
  apps: [
    {
      name: "solid_admin_frontend",
      script: "npm",
      args: "run start",
    },
  ],
};
```

### 3. Start apps with pm2

```bash
npm i && npm run build
pm2 start pm2.config.js
pm2 list
```

### 4. Create deploy scripts

```bash
#!/bin/bash
git pull
npm i
npm run build
pm2 stop solid_admin_frontend
pm2 start solid_admin_frontend
tail -100f ~/.pm2/logs/solid_admin_frontend-out.log
```

Make it executable:

```bash
chmod +x deploy.sh
```

### 5. Run the Deploy Scripts

```bash
cd solid-api
./deploy.sh
cd ../solid-ui
./deploy.sh
```

## C) Seed the Backend Database

```bash
cd solid-api
./rebuild.sh
solid seed
```

## D) Setup Nginx & SSL

### 1. Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### 2. Enable Firewall for Nginx

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### 3. Create Virtual Host Files

```bash
cd /etc/nginx/sites-available
touch <api_domain_name>
touch <ui_domain_name>
```

Sample config for `api_domain_name`:

```bash
server {
  server_name <api_domain_name>;
  root /var/www/html;
  index index.html index.htm;

  location / {
    proxy_pass http://127.0.0.1:<api_port>;
    proxy_read_timeout 60;
    proxy_connect_timeout 60;
    proxy_redirect off;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
  }

  listen 80;
}
```

Link and restart:

```bash
ln -s /etc/nginx/sites-available/<api_domain_name> /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/<ui_domain_name> /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo tail -f /var/log/nginx/error.log
```

Verify if the below urls are working over http before proceeding with installing the http certificate:

- api swagger docs - `http://<api_domain_name>/docs`
- admin UI login - `http://<ui_domain_name>`
- curl request - `curl -I http://<ui_domain_name>` (it should return something like a 200 OK response)

### 4. Install SSL with Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d <api_domain_name>
sudo certbot --nginx -d <ui_domain_name>
sudo systemctl restart nginx
```

Visit: `https://<domain_name>` to verify SSL.




<div className="tips-box">
  <h4 className="card-headear-wrapper">
    <FaLightbulb className="feature-icon" />
    Tip
  </h4>
  You can set up a cron job or use the commands below to ensure apps restart after reboot.

</div>


<br/>

```bash
pm2 save && pm2 startup
```


<div className="tips-box">
  <h4 className="card-headear-wrapper">
    <FaLightbulb className="feature-icon" />
    Tip
  </h4>
You can set up log rotation for pm2 logs using the following command. This will setup log rotation to rotate daily with a max size of <span className="color-green"> 10MB with 30 days </span> rotation by default and compress the rotated logs.
</div>


<br/>


```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:compress true
```

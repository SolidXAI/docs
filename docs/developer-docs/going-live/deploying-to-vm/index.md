---
title: Deploying SolidX to VM
description: Step-by-step guide to deploy SolidX applications on Ubuntu virtual machines.
sidebar_position: 1
---

#  Deploying to VM
This section provides guidance on how to deploy your SolidX applications to a virtual machine (VM).

:::info
📌 Before continuing, make sure you've completed the [Prerequisites](/docs/developer-docs/prerequisites).
:::

##  Run SolidX Application
This section explains how to run the SolidX app on a virtual machine.

###  Clone Repository
```bash
git clone <repo http url>
```

###  Update Environment Variables
Create the `.env` files inside `solid-api` and `solid-ui` with your database credentials and other configs.

###  Verify Backend is Running
```bash
cd solid-api
npm i
npm run build
npm run start
```

###  Verify Frontend is Running
```bash
cd solid-ui
npm i
npm run build
npm run start
```
> Press `Ctrl + C` to exit; we will use `pm2` next.

##  Deploy with Process Manager

###  Install pm2 Globally
```bash
npm install -g pm2
```

### Create pm2 Config File
Inside both `solid-api` and `solid-ui` folders, create `pm2.config.js`:
```js
module.exports = {
  apps: [
    {
      name: 'solid_admin_frontend',
      script: 'npm',
      args: 'run start',
    },
  ],
};
```

### ▶ Start apps with pm2
```bash
pm2 start pm2.config.js
pm2 list
```

###  Create deploy scripts
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

###  Run the Deploy Scripts
```bash
cd solid-api
./deploy.sh
cd ../solid-ui
./deploy.sh
```

##  Seed the Backend Database
```bash
cd solid-api
./rebuild.sh
solid seed
```

##  Setup Nginx & SSL

###  Install Nginx
```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

###  Enable Firewall for Nginx
```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

###  Create Virtual Host Files
```bash
cd /etc/nginx/sites-available
touch <api_domain_name>
touch <ui_domain_name>
```
Sample config for `api_domain_name`:
```nginx
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

###  Install SSL with Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d <api_domain_name>
sudo certbot --nginx -d <ui_domain_name>
sudo systemctl restart nginx
```
Visit: `https://<domain_name>` to verify SSL.

---

:::tip
You can set up a cron job or use the commands below to ensure apps restart after reboot.
:::

```bash
pm2 save && pm2 startup
```

:::tip
You can set up log rotation for pm2 logs using the following command. This will setup log rotation to rotate daily with a max size of 10MB with 30 days rotation by default and compress the rotated logs.
```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:compress true
```
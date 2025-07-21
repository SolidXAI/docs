---
title: Deploying SolidX to VM
description: Step-by-step guide to deploy SolidX applications on Ubuntu virtual machines.
sidebar_position: 1
---

# 🚀 Deploying to VM
This section provides guidance on how to deploy your SolidX applications to a virtual machine (VM).

## 🐘 Setup PostgreSQL Database
This guide assumes you are using PostgreSQL as your database.

:::note
If you're using a different database, please refer to its official documentation.
:::

### 📦 Install PostgreSQL on Ubuntu 22/24
Follow [DigitalOcean's guide](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart) for detailed instructions.

### 👤 Create a PostgreSQL User and Database
1. Create a user:
   ```bash
   sudo -u postgres createuser --interactive
   ```
2. Update the password:
   ```sql
   ALTER USER <user> WITH PASSWORD '<password>';
   ```
3. Create and access the database:
   ```bash
   sudo -u postgres createdb <dbname>
   psql -U <user> -h localhost -d <dbname>
   ```

## 🔧 Run SolidX Application
This section explains how to run the SolidX app on a virtual machine.

### 🛠️ Install Git
```bash
sudo apt update
sudo apt install git -y
git config --global user.name "Server Admin"
git config --global user.email "admin@logicloop.io"
```

### 📁 Clone Repository
```bash
git clone <repo http url>
```

### ⚙️ Update Environment Variables
Create the `.env` files inside `solid-api` and `solid-ui` with your database credentials and other configs.

### 🧱 Install Node.js and npm using nvm
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm --version
nvm install 22.13.1
node -v
npm -v
```

### 🔍 Verify Backend is Running
```bash
cd solid-api
npm i
npm run build
npm run start
```

### 🔍 Verify Frontend is Running
```bash
cd solid-ui
npm i
npm run build
npm run start
```
> Press `Ctrl + C` to exit; we will use `pm2` next.

## 🔄 Set Up the Process Manager

### 🧪 Install pm2 Globally
```bash
npm install -g pm2
```

### ⚙️ Create PM2 Config File
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

### ▶️ Start with PM2
```bash
pm2 start pm2.config.js
pm2 list
```

### 📜 Create `deploy.sh` in Each App
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

### 🚀 Run the Deploy Scripts
```bash
cd solid-api
./deploy.sh
cd ../solid-ui
./deploy.sh
```

## 🌱 Seed the Backend Database
```bash
cd solid-api
./rebuild.sh
solid seed
```

## 🌐 Setup Nginx & SSL

### 🌍 Install Nginx
```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

### 🔐 Enable Firewall for Nginx
```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### 🏷️ Create Virtual Host Files
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
Visit: `http://<domain_name>`

### 🔒 Install SSL with Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d <api_domain_name>
sudo certbot --nginx -d <ui_domain_name>
sudo systemctl restart nginx
```
Visit: `https://<domain_name>` to verify SSL.

---

:::tip
You can set up a cron job or use `pm2 save && pm2 startup` to ensure apps restart after reboot.
:::

---
sidebar_position: 1
---

# Pre-requisites

:::info NOTE
This is a revamped guide to pre-requisites. It includes OS-specific instructions and recommends using Docker for a smoother setup.
:::

**Note:** These installation instructions are provided as a **guideline**. Environments differ, so if you run into issues, you can troubleshoot by consulting the relevant official documentation or searching for solutions on the internet.

## 1. Docker and Docker Compose

For the most seamless and consistent development experience, we strongly recommend using Docker to run your PostgreSQL database. This avoids the complexities of manual installation and configuration on different operating systems.

- **Install Docker Engine:** Follow the official instructions for your OS:
  - [**macOS**](https://docs.docker.com/desktop/install/mac-install/)
  - [**Windows**](https://docs.docker.com/desktop/install/windows-install/)
  - [**Ubuntu**](https://docs.docker.com/engine/install/ubuntu/)

- **Validate Installation:**
  ```bash
  docker --version
  docker-compose --version
  ```

## 2. Database Setup (PostgreSQL)

This guide assumes you're using **PostgreSQL**.

### Recommended: Using Docker

1.  **Create a `docker-compose.yml` file** in your project's root directory with the following content. This file will define your PostgreSQL service.

    ```yaml
    version: '3.8'
    services:
      postgres:
        image: postgres:14-alpine
        container_name: school-fees-portal-db
        restart: always
        environment:
          POSTGRES_USER: your_db_user      # Replace with your desired username
          POSTGRES_PASSWORD: your_db_password  # Replace with a strong password
          POSTGRES_DB: school_fees_portal # Replace with your desired database name
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data

    volumes:
      postgres_data:
    ```

2.  **Start the PostgreSQL container:**

    ```bash
    docker-compose up -d
    ```

3.  **Validate Connection:** You can connect to the database using any SQL client or the following command:

    ```bash
    # Replace with the credentials you set in the docker-compose.yml file
    psql -h localhost -U your_db_user -d school_fees_portal -c "SELECT 1;"
    ```
    You will be prompted for your password. If the command returns `?column?` with a `1` underneath, you are successfully connected.

### Alternative: Manual Installation

If you prefer not to use Docker, you can install PostgreSQL manually.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="ubuntu" label="Ubuntu">

  ```bash
  # Update package lists and install PostgreSQL
  sudo apt update
  sudo apt install postgresql postgresql-contrib -y

  # Validate installation
  psql --version
  sudo systemctl status postgresql --no-pager
  ```

  **Create User and Database:**
  1. Create a user: `sudo -u postgres createuser --interactive`
  2. Set password: `sudo -u postgres psql -c "ALTER USER <user> WITH PASSWORD '<password>';"`
  3. Create database: `sudo -u postgres createdb <dbname>`
  4. Validate: `sudo -u postgres psql -c "\du"`

  </TabItem>
  <TabItem value="macos" label="macOS">

  ```bash
  # Install PostgreSQL using Homebrew
  brew install postgresql

  # Start the PostgreSQL service
  brew services start postgresql

  # Validate installation
  psql --version
  brew services list
  ```
  **Create User and Database:**
  1. Create a user: `createuser --interactive`
  2. Create database: `createdb <dbname>`
  3. Access psql: `psql -d <dbname>`
     - Inside psql, set password: `ALTER USER <user> WITH PASSWORD '<password>';`

  </TabItem>
  <TabItem value="windows" label="Windows">

  1.  **Install via Chocolatey (Recommended):**
      ```powershell
      choco install postgresql
      ```
  2.  **Or, download the installer** from the [PostgreSQL official website](https://www.postgresql.org/download/windows/).
  3.  During installation, you will be prompted to set a password for the default `postgres` user and select a port.

  **Create User and Database:**
  - Use the **pgAdmin** tool that comes with the installation to create a new user and database via a graphical interface.

  </TabItem>
</Tabs>

---

## 3. Git Installation

<Tabs>
  <TabItem value="ubuntu" label="Ubuntu">

  ```bash
  sudo apt update
  sudo apt install git -y
  ```

  </TabItem>
  <TabItem value="macos" label="macOS">

  If you have Homebrew, it's as simple as:
  ```bash
  brew install git
  ```
  Alternatively, installing Xcode Command Line Tools will also install Git.

  </TabItem>
  <TabItem value="windows" label="Windows">

  The easiest way is to download and install **[Git for Windows](https://git-scm.com/download/win)**.

  </TabItem>
</Tabs>

**Validate and Configure Git:**
```bash
# Validate installation
git --version

# Configure your user details (essential for commits)
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"

# Check your configuration
git config --list
```

---

## 4. Node.js & npm (via nvm)

We highly recommend using **Node Version Manager (nvm)** to manage multiple Node.js versions.

<Tabs>
  <TabItem value="ubuntu-macos" label="Ubuntu / macOS">

  ```bash
  # Install nvm
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  # You may need to restart your terminal or run the following commands:
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

  # Validate nvm installation
  nvm --version

  # Install the latest LTS version of Node.js (Recommended)
  nvm install --lts

  # Set the installed version as default
  nvm alias default 'lts/*'
  ```

  </TabItem>
  <TabItem value="windows" label="Windows">

  For Windows, **[nvm-windows](https://github.com/coreybutler/nvm-windows)** is the recommended tool. Download and run the installer from the releases page.

  ```powershell
  # Validate nvm installation
  nvm version

  # Install the latest LTS version
  nvm install lts

  # Use the installed version
  nvm use <version_number> # e.g., nvm use 20.11.0
  ```

  </TabItem>
</Tabs>

**Validate Node.js and npm:**
```bash
node -v
npm -v
```

---

## 5. Project-Specific Tools

SolidX uses several command-line tools for code generation and file operations. The best practice is to install these as **local project dependencies** so they don't conflict with other projects.

You will install these in a later step when you create your SolidX project. When you need to run them, you will use `npx`, which executes commands from your local `node_modules` folder.

-   **`@angular-devkit/schematics-cli`**: Used for generating backend controllers and services.
-   **`copyfiles`**: Used for copying static files during the build process.

No installation is required at this stage. The `npx @solidstarters/create-solid-app` command in the next step will set up a project with these dependencies included.

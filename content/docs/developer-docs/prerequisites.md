---
title: Prerequisites
description: Describes the tools needed before installing SolidX.
summary: This document outlines the essential tools and software required before installing SolidX. It covers installation and setup instructions for PostgreSQL database (including user and database creation), Git version control, Node.js and npm via nvm, schematics-cli for Angular schematics-based code generation, and copyfiles utility. Each section provides platform-specific installation commands for Ubuntu/macOS along with validation steps to ensure proper setup. These prerequisites are necessary for development machines to support SolidX's low-code platform functionality.
---

#  Prerequisites

>  **Note:** These installation instructions are provided as a **guideline**. Environments differ, so if you run into issues, you can troubleshoot by consulting the relevant official documentation or searching for solutions on the internet.

##  1. Database Setup

This guide assumes you're using **PostgreSQL** as your database.

If you're using a different database, please refer to its official documentation.

###  Installing PostgreSQL

####  On Ubuntu / macOS

Follow [DigitalOcean's guide](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart) for detailed installation instructions.  
> Alternatively, you can use your package manager of choice or follow the official PostgreSQL docs for your OS.

```bash
# Example for Ubuntu:
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Validate installation:
psql --version
systemctl status postgresql --no-pager
```

####  Create a PostgreSQL User and Database

Create a PostgreSQL User and Database

1. Create a user:

   ```bash
   sudo -u postgres createuser --interactive
   ```

   > Validate: list users  
   ```bash
   sudo -u postgres psql -c "\du"
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

   > Validate: inside psql, run `\dt` to check available tables.

---

## 2. Git Installation

On Ubuntu / macOS

> If you already have Git installed via another method (Xcode, Homebrew, source build), you can skip this step. You can also search “install git on your distro” for alternatives.

```bash
sudo apt update
sudo apt install git -y

# Validate installation:
git --version

# Configure user details:
git config --global user.name "<User Name>"
git config --global user.email "<User Email>"
git config --list   # Validate configuration
```

---

## 3. Node.js & npm Setup (via nvm)

On Ubuntu / macOS

> You may also use your OS package manager (e.g., brew install node) or download binaries from Node.js official site. We recommend nvm for version management.

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Validate installation:
nvm --version

# Install Node.js (example: v22)
nvm install 22

# Validate versions:
node -v
npm -v
```

---

## 4.  Install schematics-cli

This is only required on development machines, not on production servers. SolidX uses Angular schematics for generating backend controllers and services.

> Alternatively, you can install it locally in your project and run via `npx`. Check [Angular schematics docs](https://angular.io/guide/schematics) for details.

```bash
npm install -g @angular-devkit/schematics-cli

# Validate installation:
schematics --version
```

---

##  5.  Install copyfiles

This is only required on development machines, not on production servers. SolidX uses copyfiles to copy static files.

> If you prefer, you can add copyfiles as a project dependency and use it via `npx`. See [copyfiles on npm](https://www.npmjs.com/package/copyfiles) for options.

```bash
npm install -g copyfiles

# Validate installation:
copyfiles --help | head -n 5
```


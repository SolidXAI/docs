---
# title: Prerequisites
description: Describes the tools needed before installing SolidX.
sidebar_position: 1
---

import { NoteBoxs } from '@site/src/common/NoteBoxs';

# Prerequisites

## Database Setup

This guide assumes you're using **PostgreSQL** as your database.

<NoteBoxs>
If you're using a different database, please refer to its official documentation.
</NoteBoxs>

### Installing PostgreSQL

#### On Ubuntu / macOS:

Follow [DigitalOcean's guide](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-22-04-quickstart) for detailed installation instructions.

### Create a PostgreSQL User and Database

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

---

## Git Installation

### On Ubuntu / macOS:

```bash
sudo apt update
sudo apt install git -y
git config --global user.name "<User Name>"
git config --global user.email "<User Email>"
```

---

## Node.js & npm Setup (via nvm)

### On Ubuntu / macOS:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm --version
nvm install 22
node -v
npm -v
```

## Install Schematics CLI

<NoteBoxs>
This is only required on development machines, not on production servers. SolidX uses Angular schematics for generating backend controllers and services.
</NoteBoxs>

<br/>

```bash
npm install -g @angular-devkit/schematics-cli
```

## Install copyfiles CLI

<NoteBoxs>
This is only required on development machines, not on production servers. SolidX uses copyfiles to copy static files.
</NoteBoxs>

<br/>


```bash
npm install -g copyfiles
``` 
<!-- TODO
Get rid of above 2 steps by using the schematics-cli & copyfiles packages in the node_modules folder.
-->

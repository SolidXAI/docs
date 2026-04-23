---
title: Prerequisites
description: Describes the tools needed before installing SolidX and why they matter.
summary: This document explains the development-machine prerequisites for SolidX, starting with the mental model of what each dependency is for before moving into installation steps. It covers the database, version control, Node.js tooling, and a few development utilities used by the SolidX workflow so developers understand not only what to install, but why those tools are part of the platform setup.
sidebar_position: 1
---

import { FaUserPlus,FaTerminal } from "react-icons/fa";
import { NoteBoxs } from '@site/src/common/NoteBoxs';

#  Prerequisites

>  **Note:** These installation instructions are provided as a **guideline**. Environments differ, so if you run into issues, you can troubleshoot by consulting the relevant official documentation or searching for solutions on the internet.

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    Think of the SolidX prerequisites as the minimum layers required to make a metadata-driven application development environment work.
  </p>
  <ul>
    <li><strong>Database:</strong> stores both application data and SolidX metadata.</li>
    <li><strong>Git:</strong> versions your code and metadata changes safely.</li>
    <li><strong>Node.js + npm:</strong> powers <code>solidctl</code>, dependency installation, and local builds.</li>
    <li><strong>Supporting CLI tools:</strong> help with the current development workflow such as code generation and asset copying.</li>
  </ul>
  <p>
    So the intuition is simple: first prepare persistence, then prepare the toolchain, then add the small helper utilities the workflow still depends on.
  </p>
</div>

##  1. Database Setup

### Why this matters

SolidX is a metadata-driven platform. That means the database is not just storing business records, it is also storing the metadata that defines how much of the platform behaves.

So when we say “set up the database,” what we really mean is:

- prepare the persistence layer for your application data,
- prepare the persistence layer for SolidX metadata,
- and make sure your local project has somewhere to seed and run against.

This guide assumes you're using **PostgreSQL** as your database.

<NoteBoxs>
If you're using a different database, please refer to its official documentation.
</NoteBoxs>

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

<h4 className="card-title card-headear-wrapper">
  <FaUserPlus size={20} style={{ marginRight: "12px" }} />
  Create a PostgreSQL User and Database
</h4>

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

### Why this matters

SolidX projects are normal application codebases. Your metadata, backend code, frontend code, and configuration all live in source control.

That means Git is not optional in practice if you want to:

- collaborate with other developers,
- version metadata changes safely,
- review changes,
- and move work across environments cleanly.

<h4 className="card-title card-headear-wrapper">
  <FaTerminal size={20} style={{ marginRight: "12px" }}  />
   On Ubuntu / macOS
</h4>

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

### Why this matters

Node.js is the runtime behind the project tooling for SolidX development.

You need it because:

- `solidctl` runs through the Node.js toolchain,
- project dependencies for `solid-api` and `solid-ui` are installed through npm,
- and local build/dev workflows depend on a working Node environment.

We recommend `nvm` because different projects may move across Node versions over time, and version management tends to keep development machines healthier.

<h4 className="card-title card-headear-wrapper">
  <FaTerminal size={20} style={{ marginRight: "12px" }}  />
 On Ubuntu / macOS
</h4>

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

### Why this matters

This tool exists because parts of the SolidX development workflow still use schematics-based generation.

Conceptually, this belongs to the **code-generation support layer**, not the core runtime of your app. That is why it is only needed on development machines.

<NoteBoxs>
This is only required on development machines, not on production servers. SolidX uses Angular schematics for generating backend controllers and services.
</NoteBoxs>

<br/>

> Alternatively, you can install it locally in your project and run via `npx`. Check [Angular schematics docs](https://angular.io/guide/schematics) for details.



```bash
npm install -g @angular-devkit/schematics-cli

# Validate installation:
schematics --version
```

---

##  5.  Install copyfiles

### Why this matters

This utility supports parts of the asset-copying workflow used during development and build setup.

Like `schematics-cli`, this is not part of the core business runtime of your application. It is a developer convenience and workflow dependency.

<NoteBoxs>
This is only required on development machines, not on production servers. SolidX uses copyfiles to copy static files.
</NoteBoxs>

<br/>

> If you prefer, you can add copyfiles as a project dependency and use it via `npx`. See [copyfiles on npm](https://www.npmjs.com/package/copyfiles) for options.



```bash
npm install -g copyfiles

# Validate installation:
copyfiles --help | head -n 5
```

<!-- TODO
Get rid of above 2 steps by using the schematics-cli & copyfiles packages in the node_modules folder.
-->

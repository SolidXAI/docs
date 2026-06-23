Set up a new SolidX project for me using the embedded database. Follow these steps in order. Do not skip any step. Report status after each step.

First, ask me for the project name I want to use. Default to "my-solid-app" if I don't specify one.

Prerequisite checks:
- Verify Node.js 22+ is installed. If missing, install it via nvm (curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && source ~/.nvm/nvm.sh && nvm install 22). If nvm is also missing and cannot be installed, stop and tell me to install Node.js 22+ manually.
- Install the SolidX CLI globally: npm i -g @solidxai/solidctl. Verify with `solidctl --version`. If this fails, stop and tell me to install it manually.

Project scaffold (this step takes 5-10 minutes; npm installs all dependencies for both backend and frontend):
- Run: solidctl create-app --no-interactive --embedded --name <PROJECT_NAME>
- Inform me that scaffolding is in progress and will take several minutes. Do not treat the long-running npm install as a failure. Wait for it to complete.
- The embedded database (PGlite) requires no Docker, no PostgreSQL, and no credentials. Do not attempt to set up Docker or an external database.

Start the services (a single supervisor runs the backend, the frontend, and the embedded database together):
- cd <PROJECT_NAME>
- Run: solidctl start:dev
- Run it as a background process so you can continue with the verification step.

Final verification:
- Confirm the backend API is reachable at http://localhost:3000
- Confirm the frontend admin panel is reachable at http://localhost:3001
- Report the project directory path, the URLs, and the super admin login (username: sa, password: Admin@3214$)

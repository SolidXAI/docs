---
title: Installation
description: Overview of how to initialize a SolidX project with links to the full step-by-step tutorial.
summary: This document provides a quick overview of installing SolidX using `solidctl create-app`. It explains the installation flow at a high level, then shows the command used to scaffold a new project containing both `solid-api` and `solid-ui`, along with a link to a full guided tutorial.
sidebar_position: 2
---

#  Installing SolidX

Installing `SolidX` is a breeze with our [`solidctl create-app`](https://www.npmjs.com/package/@solidxai/solidctl) workflow.  

<div className="tips-box information-box">
  <h4 className="card-headear-wrapper">
    Mental Model
  </h4>
  <p>
    Installing SolidX is really a <strong>project bootstrap</strong> step, not just a package installation step.
  </p>
  <ul>
    <li><strong><code>create-app</code></strong> scaffolds a new SolidX application workspace.</li>
    <li>That workspace includes both <code>solid-api</code> and <code>solid-ui</code>.</li>
    <li>You then build the project, seed metadata, and start development from there.</li>
  </ul>
  <p>
    So the intuition is: <strong>you are creating a working SolidX project skeleton</strong>, not merely adding a dependency to an existing folder.
  </p>
</div>

##  Quick Overview
- Run the command below to initialize your SolidX project:  

  ```bash
  npx @solidxai/solidctl@latest create-app
  ```

- Answer a few simple prompts to configure your project.
- This scaffolds a new project with both backend and frontend applications.
- After scaffolding, the usual next steps are to build the project and seed metadata.
- Customize SolidX to fit your needs!

##  Step-by-Step Tutorial
For complete step-by-step installation guidance, including environment setup and configuration, follow the dedicated tutorial:
-  [Bootstrap SolidX for School Fees Portal](/docs/tutorial/school-fees-portal/index.md)

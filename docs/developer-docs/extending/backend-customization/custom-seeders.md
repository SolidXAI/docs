---
sidebar_position: 17
title: Custom Seeders
description: Learn how to create and run custom database seeders in SolidX.
summary: Guide to creating custom seeders for populating your database with initial or test data. Covers implementing a service with a `seed()` method, decorating it with `@SolidSeeder`, registering it in a module, and executing it via the CLI `seed` command.
keywords: [backend, seeders, customization, database, seed data]
solidx_concerns: []
---

import { IoIosArrowForward } from "react-icons/io";

# Custom Seeders

## Overview

Seeders in SolidX let you populate your database with initial or test data — things like default roles, lookup values, demo records, or any other data your application needs to function.

SolidX ships with built-in seeders (e.g. for permission metadata), but you can create your own custom seeders for any data specific to your project.

All a seeder needs is a `seed()` method. SolidX will automatically discover it and make it available through the CLI.

## Creating a Custom Seeder

### 1. Create a Seeder Service

Create a new service class that:
- Is decorated with `@Injectable()` and `@SolidSeeder`
- Has a `seed()` method containing your seeding logic

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Example: Country Seeder
</summary>

```ts
import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { SolidSeeder } from '@solidxai/core';
import { Country } from './entities/country.entity';

@Injectable()
@SolidSeeder
export class CountrySeederService {
  private readonly logger = new Logger(CountrySeederService.name);

  constructor(
    @InjectRepository(Country)
    private readonly countryRepo: Repository<Country>,
  ) {}

  async seed(): Promise<void> {
    const countries = [
      { name: 'United States', code: 'US' },
      { name: 'United Kingdom', code: 'GB' },
      { name: 'Canada', code: 'CA' },
    ];

    for (const country of countries) {
      const existing = await this.countryRepo.findOne({
        where: { code: country.code },
      });

      if (existing) {
        this.logger.log(`Country ${country.name} already exists, skipping.`);
      } else {
        this.logger.log(`Creating country: ${country.name}`);
        const entity = this.countryRepo.create(country);
        await this.countryRepo.save(entity);
      }
    }

    this.logger.log('Country seeding complete.');
  }
}
```
</details>

### 2. Register the Service

Add your seeder service to the `providers` array of the appropriate module.

```ts title="app.module.ts"
import { Module } from '@nestjs/common';
import { CountrySeederService } from './seeders/country-seeder.service';

@Module({
  providers: [CountrySeederService],
})
export class AppModule {}
```

That's it — SolidX will automatically discover any provider decorated with `@SolidSeeder` and register it in the `SolidRegistry`.

## Running a Seeder

Seeders are executed via the CLI using the built-in `seed` command.

### Basic Usage

```bash
npx @solidxai/solidctl seed --seeder CountrySeederService
```

The `--seeder` (`-s`) flag specifies the **class name** of the seeder to run.

## How It Works

1. **Discovery** — On application bootstrap, SolidX scans all providers for the `@SolidSeeder` decorator and registers them in the `SolidRegistry`.
2. **Lookup** — When you run the `seed` CLI command, it looks up the seeder by class name from the registry.
3. **Execution** — The seeder's `seed()` method is called.

## Summary

| Step | Description |
|------|-------------|
| 1 | Create a service with a `seed()` method |
| 2 | Decorate it with `@Injectable()` and `@SolidSeeder` |
| 3 | Register it in your module's `providers` array |
| 4 | Run it via `npx @solidxai/solidctl seed --seeder YourSeederService` |

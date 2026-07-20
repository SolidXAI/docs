---
title: Module Metadata Seeder Events
icon: "radio"
description: Listen to module metadata seeder lifecycle events from a consuming SolidX project.
summary: Shows how core emits `module-metadata-seeder.started` and `module-metadata-seeder.finished`, and how a consuming SolidX project can register optional NestJS event listeners for those named events.
keywords: [seeder, events, nestjs, event-emitter, metadata, recipe]
---

# Module Metadata Seeder Events

SolidX core emits two lifecycle events from `ModuleMetadataSeederService`:

- `module-metadata-seeder.started`
- `module-metadata-seeder.finished`

This lets a consuming project attach project-specific behavior around metadata seeding without modifying core seeding logic.

Typical uses:

- log seed lifecycle to an external system
- trigger cache warmup after seeding completes
- notify internal tooling that a seed run started or finished
- capture timing and failure details for CI or operational dashboards

## Event Payload

Both events are emitted as `EventDetails<ModuleMetadataSeederEventPayload>`.

The payload includes:

- `seedRunId` - stable id shared by the started and finished events
- `options` - normalized seed options used for the run
- `startedAt` - ISO timestamp when the seed run began
- `finishedAt` - ISO timestamp when the run ended (`finished` event only)
- `durationMs` - total runtime in milliseconds (`finished` event only)
- `success` - `true` or `false` on the `finished` event
- `seededModuleNames` - modules actually processed during the run
- `currentStep` - last active seed step when the event was emitted
- `errorMessage` - failure message when the run ends unsuccessfully

`options` currently contains:

- `modulesToSeed`
- `pruneMetadata`
- `seedGlobalMetadata`

## Consuming From Your App

Import `EventEmitterModule.forRoot()` once in your application's root module, then register any listeners you need.

Create a listener:

```ts title="src/listeners/module-metadata-seeder.listener.ts"
import { Injectable, Logger } from '@nestjs/common';
import { OnEvent } from '@nestjs/event-emitter';
import {
  EventDetails,
  EventType,
  ModuleMetadataSeederEventPayload,
} from '@solidxai/core';

@Injectable()
export class ModuleMetadataSeederListener {
  private readonly logger = new Logger(ModuleMetadataSeederListener.name);

  @OnEvent(EventType.MODULE_METADATA_SEEDER_STARTED)
  handleStarted(event: EventDetails<ModuleMetadataSeederEventPayload>) {
    this.logger.log(
      `Seed started: runId=${event.payload.seedRunId}, modules=${event.payload.options.modulesToSeed?.join(',') ?? 'ALL'}`
    );
  }

  @OnEvent(EventType.MODULE_METADATA_SEEDER_FINISHED)
  handleFinished(event: EventDetails<ModuleMetadataSeederEventPayload>) {
    this.logger.log(
      `Seed finished: runId=${event.payload.seedRunId}, success=${event.payload.success}, durationMs=${event.payload.durationMs}`
    );
  }
}
```

Register the listener in the consuming module:

```ts title="src/app.module.ts"
import { ModuleMetadataSeederListener } from './listeners/module-metadata-seeder.listener';

@Module({
  providers: [
    AppService,
    ModuleMetadataSeederListener,
  ],
})
export class AppModule {}
```

## Notes

- Import `EventEmitterModule.forRoot()` once in the consuming app's root module.
- Listener registration is optional. If no listener is registered, seeding behavior is unchanged.
- The `finished` event is emitted for both successful and failed runs. Check `payload.success`.
- The payload exposes normalized seed options, which is a better contract than raw CLI argv because the seeder can also be invoked from code, not only from `solidctl`.
- These events are meant for integration hooks and telemetry, not for replacing core seeding behavior.

## References

- [NestJS Events technique](https://docs.nestjs.com/techniques/events)
- [Custom Seeders](../developer-docs/extending/backend-customization/custom-seeders)

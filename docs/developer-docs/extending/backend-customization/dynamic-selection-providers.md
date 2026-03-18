---
sidebar_position: 12
title: Dynamic Selection Providers
description: Learn how to create dynamic selection providers to customize the selection options in your application.
summary: Explains creating dynamic selection providers for runtime option fetching from databases or APIs, replacing static lists. Covers field metadata configuration with `selectionDynamicProvider` and `selectionDynamicProviderCtxt`, implementing `ISelectionProvider` interface with `values()` method, provider registration, context handling, multi-select support, and examples like `StockApiSelectionProvider` for live exchange data. Highlights built-in `ListOfValuesSelectionProvider` for database queries.
keywords: [backend, dynamic selection, providers, customization]
solidx_concerns: [backend.custom_dynamic_selection_providers, dynamic_selection_provider]
---

import { NoteBoxs } from '@site/src/common/NoteBoxs';
import { IoIosArrowForward } from "react-icons/io";
import { FaLightbulb } from "react-icons/fa";


# Dynamic Selection Providers

Dynamic selection providers let you **fetch options at runtime**, rather than relying on static lists.  
They are useful when options need to come from a database, an API, or some logic that changes based on context.  

For example, you might want to populate a dropdown with **stock symbols fetched from a live exchange API**, or with **filtered database values**.

---

## 1. Example Field Metadata

Here’s an example field configuration using a custom provider named `StockApiSelectionProvider`.  
The `selectionDynamicProviderCtxt` specifies which fields from the API response should be used as labels and values.

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Example Configuration
</summary>

```json
{
  "name": "preferredStock",
  "displayName": "Preferred Stock",
  "description": "Select a stock symbol from the live exchange",
  "type": "selectionDynamic",
  "ormType": "varchar",
  "isSystem": false,
  "selectionDynamicProvider": "StockApiSelectionProvider",
  "selectionDynamicProviderCtxt": "{\"labelField\": \"name\", \"valueField\": \"symbol\"}",
  "selectionValueType": "string",
  "required": true,
  "unique": false,
  "index": false,
  "private": false,
  "encrypt": false,
  "isUserKey": false,
  "enableAuditTracking": false,
  "isMultiSelect": true
}
```

</details>


<div className="tips-box">
  <h4 className="card-headear-wrapper">
    <FaLightbulb className="feature-icon" />
    Tip
  </h4>

- SolidX ships with built-in providers for common use cases — see [Built-in Selection Providers](../reference/built-in-selection-providers) for details on **`ListOfValuesSelectionProvider`** and **`PseudoForeignKeySelectionProvider`**.
- Create a **custom provider** when the logic for fetching or filtering is more complex, or when data comes from an external source like an API.
</div>


---

## 2. Creating the Provider

Your provider class must implement the `ISelectionProvider` interface.  
The most important method is `values()`, which fetches and returns the available options.

<NoteBoxs>
  The <code>value()</code> method is deprecated. It can simply throw a <code>NotImplementedException</code> and is kept only for backward compatibility.
</NoteBoxs>

<br/>

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Example: <code>StockApiSelectionProvider</code>
</summary>

```ts
import { Injectable, Logger } from "@nestjs/common";
import { HttpService } from "@solidxai/core";
import { lastValueFrom } from "rxjs";
import { SelectionProvider } from "@solidxai/core";
import {
  ISelectionProvider,
  ISelectionProviderContext,
  ISelectionProviderValues,
} from "../interfaces";

interface StockApiSelectionProviderContext extends ISelectionProviderContext {
  labelField: string; // Field to use as label
  valueField: string; // Field to use as value
}

@SelectionProvider()
@Injectable()
export class StockApiSelectionProvider
  implements ISelectionProvider<StockApiSelectionProviderContext>
{
  private readonly logger = new Logger(this.constructor.name);
  private readonly url = "https://api.example.com/stocks"; // Example API endpoint

  constructor(private readonly httpService: HttpService) {}

  name(): string {
    return "StockApiSelectionProvider";
  }

  help(): string {
    return "# Fetches options dynamically from an external API.\n" +
           "Context requires:\n" +
           "- url: API endpoint\n" +
           "- labelField: field to use for label\n" +
           "- valueField: field to use for value";
  }

  async value(): Promise<ISelectionProviderValues | null> {
    throw new Error("Not implemented (deprecated).");
  }

  async values(
    query: string,
    ctxt: StockApiSelectionProviderContext
  ): Promise<readonly ISelectionProviderValues[]> {
    if (!ctxt.labelField || !ctxt.valueField) {
      this.logger.error("Invalid context");
      return [];
    }

    try {
      const response$ = this.httpService.get(this.url);
      const response = await lastValueFrom(response$);

      if (!Array.isArray(response.data)) {
        this.logger.warn("API response is not an array");
        return [];
      }

      return response.data.map((item: any) => ({
        label: item[ctxt.labelField],
        value: item[ctxt.valueField],
      }));
    } catch (err) {
      this.logger.error(`Failed to fetch values from API: ${err.message}`);
      return [];
    }
  }
}
```
</details>

---

## 3. Registering the Provider

Since providers are standard NestJS providers, register them in the module where they should be available.

```ts
// fees-portal.module.ts
@Module({
  ...
  providers: [StockApiSelectionProvider],
  ...
})
```

---

## 4. Interfaces

Below are the core interfaces used when implementing a dynamic selection provider.

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    <code>ISelectionProvider</code> Interface
</summary>

```ts
export interface ISelectionProvider<T extends ISelectionProviderContext> {
  // Description of the provider and expected context
  help(): string;

  // Unique name of the provider
  name(): string;

  // Deprecated method — throw NotImplementedException
  value(optionValue: string, ctxt: T): Promise<ISelectionProviderValues | any>;

  // Fetch selection options dynamically
  values(query: any, ctxt: T): Promise<readonly ISelectionProviderValues[]>;
}

export interface ISelectionProviderContext {}

export interface ISelectionProviderValues {
  label: string;
  value: string;
}
```
</details>

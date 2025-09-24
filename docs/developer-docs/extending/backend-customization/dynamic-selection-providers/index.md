---
sidebar_position: 1
title: Dynamic Selection Providers
description: Learn how to create dynamic selection providers to customize the selection options in your application.
keywords: [backend, dynamic selection, providers, customization]
---

import { NoteBoxs } from '@site/src/common/NoteBoxs';
import { IoIosArrowForward } from "react-icons/io";


# Overview

In this section, we will explore how to create **dynamic selection providers** to customize selection options in your application. These providers allow you to define custom logic for fetching and returning selection options based on specific criteria or conditions.



## Creating a Selection Dynamic Field with a Provider

### 1 Sample Field Metadata Configuration

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    Example Configuration
</summary>


```json
{
  "name": "regulatedBy",
  "displayName": "Regulated By",
  "description": "Regulated By",
  "type": "selectionDynamic",
  "ormType": "varchar",
  "isSystem": false,
  "selectionDynamicProvider": "ListOfValuesSelectionProvider",
  "selectionDynamicProviderCtxt": "{\\n  \\"type\\": \\"REGULATED_BY\\"\\n}",
  "selectionValueType": "string",
  "required": false,
  "unique": false,
  "index": false,
  "private": false,
  "encrypt": false,
  "encryptionType": null,
  "decryptWhen": null,
  "columnName": null,
  "isUserKey": false,
  "enableAuditTracking": false,
  "isMultiSelect": true
}
```

</details>

### 2 Create the Dynamic Selection Provider Class

You need to create a provider class that implements the ISelectionProvider interface. - The values() method fetches and returns selection options. - The value() method is currently not used, and can be left with an empty implementation.

<NoteBoxs>
    The <span classname="color-green"> value() </span> method can simply throw a NotImplementedException.
</NoteBoxs>

<br/>

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
   Example: <code>ListOfValuesSelectionProvider</code>
  </summary>

```ts
import { ListOfValuesService } from "../services/list-of-values.service";
import { Pagin>ationQueryDto } from "src/dtos/pagination-query.dto";
import { SelectionProvider } from "src/decorators/selection-provider.decorator";
import { Injectable } from "@nestjs/common";
import {
  ISelectionProvider,
  ISelectionProviderContext,
  ISelectionProviderValues,
} from "../interfaces";
import { BasicFilterDto } from "src/dtos/basic-filters.dto";

interface ListOfValuesProviderContext extends ISelectionProviderContext {
  type: string;
}

const DEFAULT_LIMIT = 100;

@SelectionProvider()
@Injectable()
export class ListOfValuesSelectionProvider
  implements ISelectionProvider<ListOfValuesProviderContext>
{
  constructor(private readonly listOfValuesService: ListOfValuesService) {}

  name(): string {
    return "ListOfValuesSelectionProvider";
  }

  help(): string {
    return "# This is lov provider";
  }

  value(
    optionValue: string,
    ctxt: ListOfValuesProviderContext
  ): Promise<ISelectionProviderValues | any> {
    throw new Error("Method not implemented.");
  }

  async values(
    query: string,
    ctxt: ListOfValuesProviderContext
  ): Promise<readonly ISelectionProviderValues[]> {
    const basicFilterQuery = new BasicFilterDto(DEFAULT_LIMIT, 0);
    if (ctxt.type) {
      basicFilterQuery.filters = {
        type: { $eq: ctxt.type },
      };
    }
    if (query) {
      basicFilterQuery.filters = {
        ...basicFilterQuery.filters,
        display: { $containsi: `%${query}%` },
      };
    }
    const lovs = await this.listOfValuesService.find(basicFilterQuery);
    return lovs.records.map((lov) => ({
      label: lov.display,
      value: lov.value,
    }));
  }
}
```

</details>

## How It Works

To support your dynamic selection field, your provider must implement the following interface:

<details>
 <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
    <code>ISelectionProvider</code> Interface
</summary>

```ts
export interface ISelectionProvider<T extends ISelectionProviderContext> {
  help(): string;
  name(): string;
  value(optionValue: string, ctxt: T): Promise<ISelectionProviderValues | any>;
  values(query: any, ctxt: T): Promise<readonly ISelectionProviderValues[]>;
}
```

</details>

## Runtime Flow

Here’s how the dynamic selection works in runtime: 1. The frontend calls FieldMetadataService.getSelectionDynamicValues(). 2. This method internally calls the values() method of your provider class. 3. The typed query is passed as the query argument. 4. Your provider returns a list of options based on the context and query.


---
title: Custom Views
description: Learn how to create custom views in the frontend of your application.
summary: Explains creating custom pages in SolidX frontend applications. Covers creating custom view components in the extensions folder, registering them using `registerExtensionComponent`, embedding custom views in form layouts using JSON configuration (notebooks, pages, custom widgets), accessing form data and metadata via props, and building specialized UI like `BookSimilarTitles` for displaying related data with filtering and action handlers.
keywords: [custom views, frontend customization, custom actions, custom components]
sidebar_position: 6
solidx_concerns: [frontend.custom_pages, add_full_custom_ui, create_custom_widget]
---

import { IoIosArrowForward } from "react-icons/io";


#  Custom Views

##  Overview
Custom views allow you to create **custom pages** in the frontend of your application.  
They can be embedded into form views or used to build specialized UI.



## Steps to Create a Custom Page in a Form View

1. **Create the custom view component**  
   Place it inside your extensions folder:  
    `solid-ui/src/extensions/<module-name>/<model-name>/custom-widgets/BookSimilarTitles.tsx`

2. **Register the custom view**  
   Register it in `solid-ui/src/extensions/solid-extensions.ts` using `registerExtensionComponent`.


<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
    Code: Registering the Component
</summary>

```typescript
registerExtensionComponent("BookSimilarTitles", BookSimilarTitles);
```

</details>

3. **Add the custom view to the form layout**  
   You can embed the custom widget in your form JSON layout.

<details open>

 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
     Code: Form Layout Example
</summary>

```json
{
  "name": "book-form-view",
  "type": "form",
  "layout": {
    "type": "form",
    "attrs": {
      "name": "form-1",
      "label": "Book"
    },
    "children": [
      {
        "type": "sheet",
        "attrs": { "name": "sheet-1" },
        "children": [
          {
            "type": "notebook",
            "attrs": { "name": "notebook-1" },  
            "children": [
              {
                "type": "page",
                "attrs": { "name": "page-1", "label": "General Info" },
                "children": [
                  {
                    "type": "row",
                    "attrs": { "name": "page-1-row-1" },
                    "children": [ ... ]
                  }
                ]
              },
              {
                "type": "page",
                "attrs": { "name": "page-5", "label": "Similar Titles", "visible": true },
                "children": [
                  {
                    "type": "custom",
                    "attrs": {
                      "name": "page-5-custom-1",
                      "widget": "BookSimilarTitles"
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```
</details>



##  Example: `BookSimilarTitles` Component

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
     Code: BookSimilarTitles.tsx
</summary>

```typescript
"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { SolidFormWidgetProps } from '@solidxai/core-ui';

const BookSimilarTitles = ({ formData, field, fieldsMetadata, viewMetadata }: SolidFormWidgetProps) => {
    const [books, setBooks] = useState<any[]>([]);

    useEffect(() => {
        const myHeaders = new Headers();
        myHeaders.append("Authorization", "[PASSWORD]");

        const requestOptions = { method: "GET", headers: myHeaders };

        async function fetchBookData() {
            try {
                const title = formData['title'];
                console.log(`Fetching similar titles for ${title}`);

                const endpoint = `https://www.googleapis.com/books/v1/volumes?q=${title}&maxResults=40`;
                const response = await fetch(encodeURI(endpoint), requestOptions);
                const result = await response.json();
                console.log(`Loaded similar titles from Google Books API`, result);
                setBooks(result.items);
            } catch (error) {
                console.error(error);
            }
        }

        fetchBookData();
    }, []);

    return (
        <div className="flex justify-center">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-12 gap-4" style={{ minWidth: "30vw" }}>
                {books.map((book, index) => (
                    <div key={index} className="h-32 relative" style={{ width: "100px", height: "100px" }}>
                        <a target="_blank" href={book.volumeInfo.infoLink}>
                            <Image
                                src={book.volumeInfo.imageLinks?.thumbnail}
                                alt={`Book description: ${book.volumeInfo.description}`}
                                layout="fill"
                                objectFit="cover"
                                className="rounded"
                                unoptimized={true}
                            />
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BookSimilarTitles;
```
</details>



##  How It Works

1. SolidX loads the **custom view component** when the form is rendered.  
2. The **custom view** is injected into the form layout at the specified location.  
3. The custom view receives props of type `SolidFormWidgetProps`.  

<details open>
 <summary className="card-title ">
    <!-- <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" /> -->
     Code: Props Types
</summary>

```tsx
export type SolidFormWidgetProps = {
    field: any;
    formData: Record<string, any>;  // Comes from Formik
    viewMetadata: SolidView;
    fieldsMetadata: FieldsMetadata;
    formViewData: any;
};

export type SolidView = CommonEntity & {
    name: string;
    displayName: string;
    type: string;
    context: string;
    layout: LayoutNode;
    model: Model;
    module: Module;
};

export type FieldMetadata = CommonEntity & {
    id: number;
    name: string;
    displayName: string;
    [key: string]: any; // Flexible for extra key-value pairs
};
```
</details>

4. The custom view can render any UI components and access:  
   - **Form data**  
   - **Field metadata**  
   - **View metadata**  
   - **Other properties**



 With this approach, you can **extend SolidX forms with powerful custom views**.

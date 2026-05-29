# Complete Setup Guide: Docusaurus + Typesense Search


## 🚀 Step-by-Step Setup

### Step 1: Install Typesense Server

Download and extract Typesense server:

```bash
# Download Typesense (check https://typesense.org/downloads/ for latest version)
wget https://dl.typesense.org/releases/0.25.1/typesense-server-0.25.1-linux-amd64.tar.gz

# Extract the archive
tar -xvf typesense-server-0.25.1-linux-amd64.tar.gz

# Make it executable (if needed)
chmod +x typesense-server
```

---

### Step 2: Create Required Directories

```bash
# Create data directory for Typesense
mkdir -p typesense-data
```

---

### Step 3: Create Environment Files

#### 3.1 Create `.env` file in your project root:

```bash
# Typesense Server Configuration
TYPESENSE_DATA_DIR=typesense-data
TYPESENSE_API_KEY=
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http

# Frontend Configuration (for your Docusaurus site) add these in docs repo
NEXT_PUBLIC_TYPESENSE_PROTOCOL=http
NEXT_PUBLIC_TYPESENSE_HOST=localhost
NEXT_PUBLIC_TYPESENSE_PORT=8108
NEXT_PUBLIC_TYPESENSE_API_KEY=
NEXT_PUBLIC_TYPESENSE_COLLECTION_NAME=solidxaiDocs
```

> **Note:** The `TYPESENSE_API_KEY` is your **admin key** (keep it secret!). The `NEXT_PUBLIC_TYPESENSE_API_KEY` is your **search-only key** (safe for frontend).

---

### Step 4: Create Typesense Start Script

Create a file named `start-typesense.sh`:

```bash
#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Start Typesense server
./typesense-server \
  --data-dir "$TYPESENSE_DATA_DIR" \
  --api-key "$TYPESENSE_API_KEY" \
  --listen-address "$TYPESENSE_HOST" \
  --listen-port "$TYPESENSE_PORT" \
  --enable-cors
```

Make it executable:

```bash
chmod +x start-typesense.sh
```

---

### Step 5: Create Search-Only API Key

First, start Typesense server:

```bash
./start-typesense.sh
```

In a **new terminal**, create a search-only API key:

```bash
curl -X POST "http://localhost:8108/keys" \
  -H "X-TYPESENSE-API-KEY: " \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Search-only key for frontend",
    "actions": ["documents:search"],
    "collections": ["*"]
  }'
```

This will return a response with your search-only key. **Copy the `value` field** and update `NEXT_PUBLIC_TYPESENSE_API_KEY` in your `.env` file.

Example response:
```json
{
  "id": 1,
  "value": "9kRQHXPASD1El98dGAcTtYdNfPPMmIFW",
  "description": "Search-only key for frontend",
  "actions": ["documents:search"],
  "collections": ["*"]
}
```

---

### Step 6: Setup Typesense DocSearch Scraper

#### 6.1 Clone the scraper repository (if not already done):

```bash
git clone https://github.com/typesense/typesense-docsearch-scraper.git
cd typesense-docsearch-scraper
```

#### 6.2 Install scraper dependencies:

```bash
# Install pipenv if not already installed
pip install pipenv

# Install dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

#### 6.3 Create scraper configuration file `config.json`:

```json
{
  "index_name": "solidxaiDocs",
  "allowed_domains": [
    "localhost"
  ],
  "start_urls": [
    {
      "url": "http://localhost:3000/"
    }
  ],
  "sitemap_urls": [
    "http://localhost:3000/sitemap.xml"
  ],
  "stop_urls": [
    "/search",
    "/tags",
    "\\?",
    "\\.pdf$"
  ],
"excludeSelectors": [
  ".breadcrumbs",
  ".breadcrumbs__item",
  "nav.breadcrumbs",

  "nav.menu",
  ".menu",
  ".menu__list",
  ".menu__list-item",
  ".menu__link",
  ".theme-doc-sidebar-item-category",
  ".theme-doc-sidebar-item-link"
],

  "selectors": {
    "default": {
      "lvl0": {
        "selector": "nav.menu a.menu__link--active",
        "default_value": "Documentation"
      },
      "lvl1": "article h1",
      "lvl2": "article h2",
      "lvl3": "article h3",
      "lvl4": "article h4",
      "lvl5": "article h5",
      "lvl6": "article h6",
      "text": "article p, article li, article td, article th, article blockquote",
      "code": "article pre code"
    }
  },
  "custom_settings": {
    "separatorsToIndex": "_",
    "attributesToRetrieve": [
      "hierarchy",
      "content",
      "anchor",
      "url",
      "tags",
      "type"
    ],
    "attributesToHighlight": [
      "hierarchy",
      "content"
    ],
    "attributesToSnippet": [
      "content:40"
    ],
    "searchableAttributes": [
      "unordered(hierarchy.lvl0)",
      "unordered(hierarchy.lvl1)",
      "unordered(hierarchy.lvl2)",
      "unordered(hierarchy.lvl3)",
      "unordered(hierarchy.lvl4)",
      "unordered(hierarchy.lvl5)",
      "unordered(hierarchy.lvl6)",
      "content"
    ]
  },
  "min_indexed_level": 0,
  "nb_hits": 14323
}
```

> **Important:** Make sure `index_name` matches `NEXT_PUBLIC_TYPESENSE_COLLECTION_NAME` in your `.env` file.

---

### Step 7: Install Docusaurus Dependencies

```bash
# Go back to your Docusaurus project directory
cd /path/to/your/docusaurus/project

# Install dependencies
npm install
```

---

## 🔄 Daily Workflow (Whenever You Update Docs)

### Step 1: Start Typesense Server

Open Terminal 1:

```bash
./start-typesense.sh
```

Keep this terminal running.

---

### Step 2: Build and Serve Docusaurus

Open Terminal 2:

```bash
npm run build
npm run serve
```

This will start your documentation site at `http://localhost:3000`. Keep this terminal running.

---

### Step 3: Run the Scraper to Index Your Docs

Open Terminal 3:

```bash
# Go to scraper directory
cd /path/to/typesense-docsearch-scraper

# Activate pipenv shell (if not already active)
pipenv shell

# Run the scraper
./docsearch run config.json
```

Wait for the scraper to finish indexing. You should see output indicating how many documents were indexed.

---

### Step 4: Test Your Search

Go to `http://localhost:3000` and test the search functionality. Your documentation should now be searchable!

---

## 🛠️ Useful Commands

### Check if Typesense is Running

```bash
ps aux | grep typesense
```

### Stop Typesense Server

```bash
pkill -f typesense-server
```

### Check Typesense Health

```bash
curl http://localhost:8108/health
```

### View All Collections

```bash
curl -H "X-TYPESENSE-API-KEY: " \
  http://localhost:8108/collections
```

<!-- ### Delete a Collection (if you need to re-index from scratch)

```bash
curl -X DELETE \
  -H "X-TYPESENSE-API-KEY: " \
  http://localhost:8108/collections/solidxaiDocs
```


### Once you delete the collection restart the typsense server and reIndex the docs  -->

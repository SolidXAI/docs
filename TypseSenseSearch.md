# Minimal Setup Guide for Docusaurus + Typesense (Only Required Steps)

This README contains **only the essential steps** you asked for.

---

## ✅ 1. Install Dependencies

```bash
npm install
```

---

## ✅ 2. Create `.env` File

Create `.env` in your project root:

```
TYPESENSE_PROTOCOL=http
TYPESENSE_HOST=localhost
TYPESENSE_PORT=8108
TYPESENSE_API_KEY=LogicLoopApiKey
```

---

## ✅ 3. Create `typesense-data` Directory

Create the directory for Typesense data persistence:

```bash
mkdir typesense-data
```

This ensures your Typesense documents and collections are saved locally.

---

## ✅ 4. Start Typesense Server (Docker)

Open a **new terminal** and run:

```bash
docker compose up -d
```

This runs your local Typesense server.

---

# The two steps below are required whenever you want to index your new  changes.

## ✅ 5. Build and Serve Docusaurus


```bash
npm run build
npm run serve
```

---

## ✅ 6. Run DocSearch Scraper for Indexing 

Every time you want to index/update documentation, run this in a **new terminal** and make sure application(docs) runing propely:

```bash
docker run -it --rm \
  --network=host \
  --env-file=.env \
  -e "CONFIG=$CONFIG_JSON" \
  typesense/docsearch-scraper:0.11.0
```

Use the **same command** every time after making documentation changes.

---




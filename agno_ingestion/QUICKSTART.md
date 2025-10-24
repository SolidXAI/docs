# Quick Start Guide

Get started with the Agno-RAG ingestion pipeline in 5 minutes.

## Prerequisites

- Python 3.11+
- Agno-RAG service running (default: http://localhost:8000)
- User account in Agno-RAG

## Step 1: Install Dependencies

```bash
cd agno_ingestion
pip install -r requirements.txt
```

## Step 2: Configure

Create `.env` file:

```bash
cp env.example .env
```

Edit `.env` with your settings:

```env
AGNO_RAG_API_URL=http://localhost:8000
AGNO_RAG_EMAIL=your-email@example.com
AGNO_RAG_PASSWORD=your-password
```

## Step 3: Test Connection

```bash
python test_ingestion.py
```

Expected output:
```
✓ PASS: Health Check
✓ PASS: Authentication
✓ PASS: Document Processing
✓ PASS: Collection Operations
✓ PASS: Single File Upload
🎉 All tests passed!
```

## Step 4: Initialize Collections

```bash
python ingest_docs.py --init-collections
```

Expected output:
```
Created collection 'admin-docs': <uuid>
Created collection 'developer-docs': <uuid>
Created collection 'recipes': <uuid>
Created collection 'tutorial': <uuid>
Created collection 'user-docs': <uuid>
Collection initialization complete
```

## Step 5: Test Single File

```bash
python ingest_docs.py --single-file ../docs/admin-docs/index.md
```

Expected output:
```
✓ Uploaded: admin-docs/index.md -> document_id=<uuid>
Ingestion Summary
Successful: 1
Failed: 0
```

## Step 6: Full Migration

```bash
python ingest_docs.py
```

This will process all markdown files. Expected output:
```
Found 87 markdown files
[1/87] Processing: admin-docs/index.md
✓ Uploaded: admin-docs/index.md -> document_id=<uuid>
[2/87] Processing: admin-docs/iam/users.md
✓ Uploaded: admin-docs/iam/users.md -> document_id=<uuid>
...
Ingestion Summary
Successful: 87
Failed: 0
```

## Verify Migration

Check that documents are searchable:

```bash
curl -X POST http://localhost:8000/v1/search \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "user management",
    "collection_id": "<admin-docs-collection-id>",
    "mode": "traditional",
    "limit": 5
  }'
```

## Troubleshooting

### Connection Refused
**Problem**: `API health check failed: Connection refused`  
**Solution**: Ensure Agno-RAG service is running:
```bash
curl http://localhost:8000/health
```

### Authentication Failed
**Problem**: `Authentication failed`  
**Solution**: Check credentials in `.env` file

### No Collections Found
**Problem**: `Collection verification failed`  
**Solution**: Run initialization:
```bash
python ingest_docs.py --init-collections
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Update existing documents: just run `python ingest_docs.py` again
- Add new documents: place in `docs/` directory and run ingestion
- Search and test: use Agno-RAG API or frontend

## Support

Check logs for detailed error messages:
- Use `--verbose` flag for debug output
- Use `--dry-run` to preview without making changes
- Review `agno_manifest.json` to see what was ingested


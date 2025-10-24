# Agno-RAG Documentation Ingestion

This directory contains the migration pipeline for ingesting SolidX documentation into the Agno-RAG service, replacing the previous R2R-based system.

## Overview

The ingestion system processes Markdown documentation files and uploads them to Agno-RAG with the following features:

- **H2-based Chunking**: Documents are split by H2 headers (##) to maintain semantic coherence
- **Collection-based Organization**: Documents are automatically routed to appropriate collections based on directory structure
- **Metadata Preservation**: All frontmatter fields and document metadata are preserved
- **Incremental Updates**: Hash-based change detection ensures only modified files are re-processed
- **Robust Error Handling**: Retry logic with exponential backoff for network failures

## Directory Structure

```
agno_ingestion/
├── agno_client.py          # API client wrapper for Agno-RAG
├── doc_processor.py        # Document processing utilities
├── ingest_docs.py          # Main ingestion script
├── agno_manifest.json      # State tracking (auto-generated)
├── .env                    # Configuration (create from env.example)
├── env.example             # Configuration template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```bash
cd agno_ingestion
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the template:

```bash
cp env.example .env
```

Edit `.env` and configure:

```bash
# Agno-RAG API Configuration
AGNO_RAG_API_URL=http://localhost:8000
AGNO_RAG_EMAIL=your-email@example.com
AGNO_RAG_PASSWORD=your-password

# Documentation Settings
DOCS_BASE_DIR=../docs
MANIFEST_PATH=./agno_manifest.json
PROJECT_NAME=solidx-docs
DOC_EXTENSIONS=.md,.mdx

# Processing Options
DRY_RUN=false
VERBOSE=true
```

### 3. Ensure Agno-RAG Service is Running

The Agno-RAG service must be running and accessible at the configured URL.

```bash
# Check health
curl http://localhost:8000/health
```

## Usage

### Initialize Collections (First Time Only)

Create the 5 collections in Agno-RAG:

```bash
python ingest_docs.py --init-collections
```

This creates:
- `admin-docs` - Administrator documentation
- `developer-docs` - Developer documentation
- `recipes` - How-to guides and recipes
- `tutorial` - Step-by-step tutorials
- `user-docs` - End-user documentation

### Ingest All Documents

Process all markdown files in the docs directory:

```bash
python ingest_docs.py
```

### Ingest Single File

Test with a single file:

```bash
python ingest_docs.py --single-file ../docs/admin-docs/index.md
```

### Dry Run Mode

Preview what would be ingested without making changes:

```bash
python ingest_docs.py --dry-run
```

### Verbose Output

Enable detailed logging:

```bash
python ingest_docs.py --verbose
```

### Custom Base Directory

Process documents from a different directory:

```bash
python ingest_docs.py --base-dir /path/to/docs
```

## Collection Mapping

Documents are automatically routed to collections based on their directory:

| Directory Path | Collection |
|---------------|------------|
| `docs/admin-docs/**` | admin-docs |
| `docs/developer-docs/**` | developer-docs |
| `docs/recipes/**` | recipes |
| `docs/tutorial/**` | tutorial |
| (reserved) | user-docs |

## Document Processing

### Chunking Strategy

Documents are split by H2 headers (`##`) before upload:

1. **Parse Frontmatter**: Extract YAML metadata from document header
2. **Split by H2**: Each H2 section becomes a separate chunk
3. **Preserve Context**: Each chunk maintains reference to parent document
4. **Add Metadata**: Chunks include section titles and index information

Example markdown structure:
```markdown
---
title: User Management
description: Managing users in SolidX
---

# User Management

## Creating Users

Content about creating users...

## Editing Users

Content about editing users...
```

This creates 2 chunks with metadata linking them to the parent document.

### Metadata Fields

The following metadata is preserved from frontmatter:

- `title` - Document title
- `description` - Document description
- `summary` - Document summary
- `keywords` - Array of keywords
- `solidx_concerns` - Array of concern tags

Additional metadata added automatically:

- `source` - Always "docusaurus"
- `project` - Project name (default: "solidx-docs")
- `section` - First directory component (e.g., "admin-docs")
- `path` - Relative file path
- `doc_title` - File path used as title
- `document_id` - UUID for the document
- `chunk_count` - Number of chunks created
- `uploaded_by` - Set to "migration_script"
- `uploaded_at` - ISO timestamp

## Manifest System

The `agno_manifest.json` file tracks ingestion state:

```json
{
  "admin-docs/index.md": {
    "hash": "sha256_hash_of_file",
    "document_id": "uuid",
    "collection_id": "collection_uuid",
    "metadata": {...},
    "chunk_count": 3,
    "uploaded_at": "2025-01-01T00:00:00"
  }
}
```

**Change Detection**: Files are re-ingested only if their SHA256 hash changes.

**Upsert Logic**: When a file changes, the old document is deleted and replaced with the new version.

## Troubleshooting

### Authentication Fails

```
Error: Authentication failed
```

**Solution**: Verify credentials in `.env` file and ensure the user exists in Agno-RAG.

### Collection Not Found

```
Error: Collection verification failed
```

**Solution**: Run `python ingest_docs.py --init-collections` to create collections.

### API Connection Error

```
Error: API health check failed
```

**Solution**: Ensure Agno-RAG service is running at the configured URL.

### File Not Found

```
Error: File not found: ../docs/...
```

**Solution**: Verify `DOCS_BASE_DIR` in `.env` points to the correct location.

### Empty Chunks Warning

```
Warning: No valid chunks generated for ...
```

**Solution**: The markdown file may have no H2 headers or very short content. Check file formatting.

## Maintenance

### Update Existing Documents

Simply run the ingestion script again. Only changed files will be re-processed:

```bash
python ingest_docs.py
```

### Add New Documents

New markdown files in the docs directory will be automatically detected and ingested on the next run.

### Remove Documents

Delete the file from the docs directory, then manually remove from Agno-RAG using the API or delete the manifest entry.

### Reset Everything

To start fresh:

1. Delete collections in Agno-RAG (via API or database)
2. Delete `agno_manifest.json`
3. Run initialization and ingestion:

```bash
python ingest_docs.py --init-collections
python ingest_docs.py
```

## Migration from R2R

This system replaces the R2R-based ingestion pipeline. Key differences:

| Aspect | R2R | Agno-RAG |
|--------|-----|----------|
| **API** | R2R SDK | REST API |
| **Chunking** | Server-side | Pre-chunked upload |
| **Collections** | Hardcoded UUIDs | Auto-created |
| **Authentication** | Email/Password | JWT tokens |
| **State Tracking** | manifest.json | agno_manifest.json |

The document processing logic (H2 splitting, frontmatter parsing, metadata extraction) remains the same to ensure consistency.

## API Reference

### AgnoRAGClient

```python
from agno_client import AgnoRAGClient

client = AgnoRAGClient(
    base_url="http://localhost:8000",
    email="user@example.com",
    password="password"
)

# Login
client.login()

# Create collection
collection = client.create_collection(
    name="my-collection",
    description="My documents"
)

# Upload pre-chunked document
result = client.upload_pre_chunked_document(
    collection_id="collection-uuid",
    parent_document_name="my-doc.md",
    chunks=[
        {
            "content": "Chunk content...",
            "chunk_index": 0,
            "metadata": {"section_title": "Introduction"}
        }
    ],
    metadata={"key": "value"}
)
```

### Document Processor

```python
from doc_processor import (
    parse_frontmatter,
    split_by_h2,
    prepare_chunks_for_upload
)

# Parse frontmatter
text = "---\ntitle: My Doc\n---\n# Content"
metadata = parse_frontmatter(text)

# Split by H2 headers
chunks = split_by_h2(text)

# Prepare for upload
chunks, metadata = prepare_chunks_for_upload(
    file_path=Path("doc.md"),
    base_dir=Path("docs"),
    file_text=text,
    document_id="uuid"
)
```

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review logs for detailed error messages
3. Verify Agno-RAG service is functioning correctly
4. Check the migration plan document for architecture details


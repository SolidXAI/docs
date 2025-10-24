# Re-ingesting Documents to Include Metadata

## Problem

The documents currently in Agno-RAG are missing important metadata fields (title, summary, keywords, solidx_concerns, description) because they were uploaded before the migration script was created.

## Solution

Re-ingest all documents using the migration script which properly extracts frontmatter metadata.

## Steps to Re-ingest

### Option 1: Re-ingest Everything (Recommended)

This will delete and re-upload all documents with proper metadata:

```bash
cd /Users/pathik/Documents/LL/SolidStarters/Docs/agno_ingestion

# Clear the manifest to force re-upload
mv agno_manifest.json agno_manifest.json.backup

# Re-ingest all documents
python ingest_docs.py --verbose
```

### Option 2: Re-ingest Specific Collection

If you only want to re-ingest one collection:

```bash
# First, manually delete documents from that collection via API or database
# Then run ingestion for just that collection's files

python ingest_docs.py --single-file ../docs/developer-docs/extending/backend-customization/dashboard-providers.md
```

### Option 3: Test with Single File First

Test that metadata is properly extracted:

```bash
# Test single file
python ingest_docs.py --single-file ../docs/developer-docs/extending/backend-customization/dashboard-providers.md

# Then verify metadata
python verify_metadata.py developer-docs
```

## What Will Happen

1. **Manifest Check**: Script checks if file hash changed
2. **Delete Old**: If document exists, it's deleted
3. **Extract Frontmatter**: Parse YAML frontmatter from markdown
4. **Build Metadata**: Create complete metadata dict with:
   - title
   - description
   - summary
   - keywords
   - solidx_concerns
   - source, project, section, path, doc_title
5. **Upload**: Send to Agno-RAG with full metadata
6. **Update Manifest**: Track new document ID and hash

## Verification

After re-ingestion, verify metadata is present:

```bash
# Check all documents in collection
python verify_metadata.py developer-docs

# Should show:
#   ✓ title: Dashboard Providers
#   ✓ description: Create custom dashboard providers...
#   ✓ summary: Introduction to creating custom dashboard providers...
#   ✓ keywords: ["backend", "dashboard", "providers", "customization"]
#   ✓ solidx_concerns: ["create/update_dashboard_widget"]
```

## Why This Happened

The documents currently in Agno were uploaded on **October 24th at 10:27 AM**, which was **before** the migration script was created. They were likely uploaded using:

1. Direct file upload without metadata extraction
2. Test uploads during development
3. Manual uploads via API

The migration script (created later) properly:
- Parses YAML frontmatter
- Extracts all metadata fields
- Preserves them in the parent document

## Important Notes

- The script will **preserve document IDs** for files that haven't changed (same hash)
- If a file has changed, it will **delete and re-upload**
- The `agno_manifest.json` tracks what's been uploaded
- To force re-upload: delete manifest entry or clear entire manifest

## Expected Timeline

For ~87 markdown files:
- **Preparation**: 2 minutes
- **Re-ingestion**: 10-30 minutes
- **Verification**: 5 minutes
- **Total**: ~15-40 minutes

## Command Summary

```bash
# Full re-ingestion (recommended)
cd agno_ingestion
mv agno_manifest.json agno_manifest.json.backup
python ingest_docs.py --verbose

# Verify after completion
python verify_metadata.py developer-docs
python verify_metadata.py admin-docs
python verify_metadata.py recipes
python verify_metadata.py tutorial
```


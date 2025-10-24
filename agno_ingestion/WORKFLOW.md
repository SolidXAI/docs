# Agno-RAG Ingestion Workflow

This document provides visual representations of the ingestion workflow.

## High-Level Migration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    MIGRATION PREPARATION                         │
│  1. Install dependencies (pip install -r requirements.txt)      │
│  2. Configure .env file with API credentials                    │
│  3. Run test suite (python test_ingestion.py)                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  COLLECTION INITIALIZATION                       │
│  python ingest_docs.py --init-collections                       │
│                                                                  │
│  Creates 5 collections:                                         │
│  • admin-docs                                                   │
│  • developer-docs                                               │
│  • recipes                                                      │
│  • tutorial                                                     │
│  • user-docs                                                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT INGESTION                            │
│  python ingest_docs.py                                          │
│                                                                  │
│  For each .md/.mdx file:                                        │
│  1. Calculate SHA256 hash                                       │
│  2. Check manifest for changes                                  │
│  3. Parse frontmatter & split by H2                            │
│  4. Upload chunks to Agno-RAG                                   │
│  5. Update manifest                                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                       VALIDATION                                 │
│  • Check document counts match R2R                              │
│  • Test search functionality                                    │
│  • Verify metadata preservation                                 │
│  • Compare search results                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Document Processing Pipeline

```
┌─────────────────┐
│  Markdown File  │
│  (*.md, *.mdx)  │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│      Step 1: Parse Frontmatter           │
│  ┌────────────────────────────────────┐  │
│  │ ---                                │  │
│  │ title: User Management             │  │
│  │ description: Managing users        │  │
│  │ keywords: [users, admin]           │  │
│  │ solidx_concerns: [security]        │  │
│  │ ---                                │  │
│  └────────────────────────────────────┘  │
│          ↓                                │
│  Extract: title, description, etc.       │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│      Step 2: Split by H2 Headers         │
│  ┌────────────────────────────────────┐  │
│  │ ## Creating Users                  │  │
│  │ Content about creating...          │  │
│  │                                    │  │
│  │ ## Editing Users                   │  │
│  │ Content about editing...           │  │
│  │                                    │  │
│  │ ## Deleting Users                  │  │
│  │ Content about deleting...          │  │
│  └────────────────────────────────────┘  │
│          ↓                                │
│  Result: 3 chunks with section titles    │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│     Step 3: Structure Chunks for API     │
│  [                                        │
│    {                                      │
│      "content": "## Creating Users...",   │
│      "chunk_index": 0,                    │
│      "metadata": {                        │
│        "section_title": "Creating Users" │
│      }                                    │
│    },                                     │
│    {                                      │
│      "content": "## Editing Users...",    │
│      "chunk_index": 1,                    │
│      "metadata": {                        │
│        "section_title": "Editing Users"  │
│      }                                    │
│    },                                     │
│    ...                                    │
│  ]                                        │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│    Step 4: Upload to Agno-RAG API        │
│  POST /v1/documents/chunks                │
│  {                                        │
│    "collection_id": "uuid",               │
│    "parent_document_name": "file.md",     │
│    "chunks": [...],                       │
│    "metadata": {                          │
│      "source": "docusaurus",              │
│      "project": "solidx-docs",            │
│      "section": "admin-docs",             │
│      "path": "admin-docs/iam/users.md",   │
│      "doc_title": "admin-docs/...",       │
│      "title": "User Management",          │
│      ...                                  │
│    }                                      │
│  }                                        │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│      Step 5: Agno-RAG Processing         │
│  • Generate embeddings (OpenAI)          │
│  • Store in PostgreSQL + pgvector        │
│  • Create parent document record         │
│  • Create chunk records                  │
│  • Link chunks to parent                 │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│     Step 6: Update Local Manifest        │
│  {                                        │
│    "admin-docs/iam/users.md": {           │
│      "hash": "sha256...",                 │
│      "document_id": "uuid",               │
│      "collection_id": "uuid",             │
│      "chunk_count": 3,                    │
│      "uploaded_at": "2025-01-01T..."      │
│    }                                      │
│  }                                        │
└────────┬─────────────────────────────────┘
         │
         ▼
     ┌───────┐
     │ DONE  │
     └───────┘
```

## Collection Routing Logic

```
File Path: docs/admin-docs/iam/users.md
              ↓
┌─────────────────────────────────────────┐
│  Extract First Directory Component      │
│  Path parts: ['admin-docs', 'iam', ...] │
│  First part: 'admin-docs'                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Look Up Collection Mapping          │
│  COLLECTION_MAPPING = {                  │
│    "admin-docs": "collection-uuid-1",    │
│    "developer-docs": "collection-uuid-2",│
│    "recipes": "collection-uuid-3",       │
│    "tutorial": "collection-uuid-4",      │
│    "user-docs": "collection-uuid-5"      │
│  }                                       │
│                                          │
│  Result: "collection-uuid-1"             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Upload to Correct Collection          │
│  collection_id = "collection-uuid-1"     │
└──────────────────────────────────────────┘
```

## Incremental Update Flow

```
File: admin-docs/index.md (modified)
         │
         ▼
┌──────────────────────────────────┐
│  Calculate SHA256 Hash            │
│  Current: "abc123..."             │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Load Manifest                    │
│  {                                │
│    "admin-docs/index.md": {       │
│      "hash": "def456...",         │
│      "document_id": "uuid",       │
│      ...                          │
│    }                              │
│  }                                │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Compare Hashes                   │
│  Current:  "abc123..."            │
│  Manifest: "def456..."            │
│  Match? NO → File changed         │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Delete Old Document              │
│  DELETE /v1/documents/{uuid}      │
│  ?collection_id={collection}      │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Process and Upload New Version   │
│  (Same as initial upload)         │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Update Manifest                  │
│  "hash": "abc123..." (new)        │
│  "uploaded_at": "2025-..." (new)  │
└──────────────────────────────────┘
```

## API Authentication Flow

```
┌────────────────────────────────┐
│  User Runs: ingest_docs.py     │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Load Credentials from .env     │
│  • AGNO_RAG_EMAIL              │
│  • AGNO_RAG_PASSWORD           │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  POST /v1/auth/login            │
│  {                              │
│    "email": "...",              │
│    "password": "..."            │
│  }                              │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Receive JWT Token              │
│  {                              │
│    "access_token": "eyJ...",    │
│    "token_type": "bearer",      │
│    "user": {...}                │
│  }                              │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Store Token in Client          │
│  self.token = "eyJ..."          │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Use Token in All Requests      │
│  Headers: {                     │
│    "Authorization": "Bearer..." │
│  }                              │
└────────────────────────────────┘
```

## Error Handling & Retry Flow

```
┌────────────────────────────────┐
│  Make API Request               │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Response Status?               │
└────┬───────────┬────────────────┘
     │           │
     │ 2xx       │ 4xx (client error)
     │ Success   │
     │           ▼
     │    ┌──────────────────┐
     │    │  Log Error       │
     │    │  Return Response │
     │    └──────────────────┘
     │
     │ 5xx (server error) or network error
     ▼
┌────────────────────────────────┐
│  Retry Logic                    │
│  • Attempt 1: Wait 1 second     │
│  • Attempt 2: Wait 2 seconds    │
│  • Attempt 3: Wait 4 seconds    │
└────────┬───────────────────────┘
         │
         ▼
    ┌────────┐
    │ Success│ → Continue
    │   or   │
    │ Failed │ → Skip file, log error
    └────────┘
```

## Parallel vs Sequential Processing

### Current: Sequential Processing

```
File 1 → Process → Upload → Wait for response
                                   ↓
File 2 → Process → Upload → Wait for response
                                   ↓
File 3 → Process → Upload → Wait for response
                                   ↓
...
```

**Characteristics:**
- Simple, predictable
- Easy to debug
- Manifest updated after each file
- Safe for interruption

### Potential: Parallel Processing (Future Enhancement)

```
File 1 → Process → Upload ─┐
File 2 → Process → Upload ─┤
File 3 → Process → Upload ─┼→ Wait for all → Update manifest
File 4 → Process → Upload ─┤
File 5 → Process → Upload ─┘
```

**Potential Benefits:**
- Faster total time (5-10x speedup)
- Better resource utilization

**Considerations:**
- More complex error handling
- Manifest atomicity concerns
- Rate limiting considerations

## Dry Run Mode

```
┌────────────────────────────────┐
│  python ingest_docs.py --dry-run│
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Scan Files                     │
│  Found: 87 markdown files       │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Process Each File              │
│  • Calculate hash               │
│  • Parse frontmatter            │
│  • Split by H2                  │
│  • Prepare chunks               │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  [DRY-RUN] Log Actions          │
│  Would upload:                  │
│  • admin-docs/index.md          │
│  • 3 chunks                     │
│  • to collection: uuid          │
│                                 │
│  ✗ No actual API calls made    │
│  ✗ No documents uploaded        │
│  ✗ No manifest updated          │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Report Summary                 │
│  Would process: 87 files        │
│  Would upload: 87 documents     │
│  Would create: ~300 chunks      │
└────────────────────────────────┘
```

## Testing Workflow

```
┌────────────────────────────────┐
│  python test_ingestion.py       │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Test 1: Health Check           │
│  GET /health                    │
│  ✓ Service is running           │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Test 2: Authentication         │
│  POST /v1/auth/login            │
│  ✓ JWT token acquired           │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Test 3: Document Processing    │
│  • Parse frontmatter            │
│  • Split by H2                  │
│  • Build metadata               │
│  ✓ All functions work           │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Test 4: Collection Operations  │
│  GET /v1/collections            │
│  ✓ Can list collections         │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Test 5: Single File Upload     │
│  • Find test file               │
│  • Process and prepare          │
│  ✓ Chunks created correctly     │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Report Results                 │
│  ✓ 5/5 tests passed             │
│  🎉 System ready!               │
└────────────────────────────────┘
```

## Summary

This workflow implements a robust, well-tested migration pipeline with:

- ✅ Clear step-by-step processing
- ✅ Error handling at each stage
- ✅ Incremental update support
- ✅ Dry-run preview mode
- ✅ Comprehensive testing
- ✅ Detailed logging
- ✅ Rollback capability

The pipeline is production-ready and follows best practices for data migration.


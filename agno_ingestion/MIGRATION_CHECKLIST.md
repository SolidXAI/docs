# Migration Checklist: R2R → Agno-RAG

Use this checklist to ensure a successful migration from R2R to Agno-RAG.

## Pre-Migration

- [ ] **Backup R2R Data**
  - Export R2R manifest.json
  - Document current collection IDs
  - Note document counts per collection

- [ ] **Verify Agno-RAG Service**
  - [ ] Service is running and accessible
  - [ ] Health check passes: `curl http://localhost:8000/health`
  - [ ] Database is initialized
  - [ ] User account created

- [ ] **Prepare Environment**
  - [ ] Python 3.11+ installed
  - [ ] Dependencies installed: `pip install -r requirements.txt`
  - [ ] `.env` file configured with correct credentials
  - [ ] Connection test passes: `python test_ingestion.py`

## Migration Steps

### Phase 1: Setup (Est. 5 minutes)

- [ ] **Install and Configure**
  ```bash
  cd agno_ingestion
  pip install -r requirements.txt
  cp env.example .env
  # Edit .env with your credentials
  ```

- [ ] **Run Tests**
  ```bash
  python test_ingestion.py
  ```
  - [ ] Health check passes
  - [ ] Authentication successful
  - [ ] Document processing works
  - [ ] Collection operations work

### Phase 2: Initialize Collections (Est. 2 minutes)

- [ ] **Create Collections**
  ```bash
  python ingest_docs.py --init-collections
  ```

- [ ] **Verify Collections Created**
  - [ ] admin-docs
  - [ ] developer-docs
  - [ ] recipes
  - [ ] tutorial
  - [ ] user-docs

- [ ] **Record Collection IDs**
  - admin-docs: `__________________`
  - developer-docs: `__________________`
  - recipes: `__________________`
  - tutorial: `__________________`
  - user-docs: `__________________`

### Phase 3: Test Migration (Est. 5 minutes)

- [ ] **Single File Test**
  ```bash
  python ingest_docs.py --single-file ../docs/admin-docs/index.md
  ```
  - [ ] File uploads successfully
  - [ ] Chunks created correctly
  - [ ] Metadata preserved

- [ ] **Dry Run**
  ```bash
  python ingest_docs.py --dry-run
  ```
  - [ ] All files detected
  - [ ] Collection routing correct
  - [ ] No errors in processing

### Phase 4: Full Migration (Est. 10-30 minutes depending on size)

- [ ] **Start Full Ingestion**
  ```bash
  python ingest_docs.py --verbose > migration.log 2>&1
  ```

- [ ] **Monitor Progress**
  - [ ] Check log output for errors
  - [ ] Monitor manifest.json for updates
  - [ ] Verify chunk counts make sense

- [ ] **Review Results**
  - [ ] Check ingestion summary
  - [ ] Compare document counts with R2R
  - [ ] No failed uploads

### Phase 5: Validation (Est. 10 minutes)

- [ ] **Verify Document Counts**
  ```bash
  # For each collection, check document count via API
  curl -X GET "http://localhost:8000/v1/documents?collection_id=<id>&limit=1" \
    -H "Authorization: Bearer <token>"
  ```
  
  Document count comparison:
  | Collection | R2R Count | Agno-RAG Count | Match? |
  |------------|-----------|----------------|--------|
  | admin-docs | ___ | ___ | [ ] |
  | developer-docs | ___ | ___ | [ ] |
  | recipes | ___ | ___ | [ ] |
  | tutorial | ___ | ___ | [ ] |
  | user-docs | ___ | ___ | [ ] |

- [ ] **Test Search Functionality**
  ```bash
  # Test search on each collection
  curl -X POST http://localhost:8000/v1/search \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
      "query": "user management",
      "collection_id": "<collection-id>",
      "mode": "traditional",
      "limit": 5
    }'
  ```
  - [ ] admin-docs search returns relevant results
  - [ ] developer-docs search returns relevant results
  - [ ] recipes search returns relevant results
  - [ ] tutorial search returns relevant results

- [ ] **Verify Metadata**
  - [ ] Check random document has correct metadata
  - [ ] Frontmatter fields preserved
  - [ ] Section assignments correct
  - [ ] Chunk ordering maintained

- [ ] **Compare with R2R Results**
  - [ ] Run same search query on both systems
  - [ ] Compare result relevance
  - [ ] Verify similar documents returned

## Post-Migration

### Immediate (Same Day)

- [ ] **Update Applications**
  - [ ] Update API endpoints to point to Agno-RAG
  - [ ] Update authentication code
  - [ ] Test end-to-end flows

- [ ] **Monitor Performance**
  - [ ] Check search latency
  - [ ] Monitor error rates
  - [ ] Verify user access

### Short-term (First Week)

- [ ] **Parallel Operation** (if possible)
  - [ ] Keep R2R running for comparison
  - [ ] Monitor both systems
  - [ ] Collect feedback

- [ ] **Documentation Updates**
  - [ ] Update internal docs with new API
  - [ ] Share migration notes with team
  - [ ] Document any issues encountered

### Long-term (First Month)

- [ ] **Decommission R2R**
  - [ ] Verify all systems using Agno-RAG
  - [ ] Archive R2R data
  - [ ] Shut down R2R service

- [ ] **Establish Maintenance Process**
  - [ ] Schedule for regular updates
  - [ ] Document update procedure
  - [ ] Train team on new system

## Rollback Plan (If Needed)

If critical issues arise:

1. **Stop Using Agno-RAG**
   - Revert API endpoints to R2R
   - Restore previous authentication

2. **Investigate Issues**
   - Review migration logs
   - Check data integrity
   - Identify root cause

3. **Fix and Retry**
   - Address identified issues
   - Test fix with single file
   - Re-run migration when ready

## Success Criteria

Mark migration as successful when:

- [ ] All documents ingested successfully (0 failures)
- [ ] Document counts match R2R (±5% acceptable for de-duplication)
- [ ] Search results are relevant and accurate
- [ ] Metadata is preserved correctly
- [ ] Performance is acceptable (search < 2s)
- [ ] No critical errors in logs
- [ ] Applications working with new API
- [ ] Team can use the system effectively

## Notes and Issues

Record any issues encountered during migration:

```
Date: ___________
Issue: ___________________________________________
Resolution: _______________________________________

Date: ___________
Issue: ___________________________________________
Resolution: _______________________________________
```

## Migration Completed

- [ ] **Final Sign-off**
  - Date: ___________
  - Completed by: ___________
  - All checks passed: [ ] Yes [ ] No
  - Ready for production: [ ] Yes [ ] No

## Support Contacts

- Agno-RAG Documentation: See README.md
- Technical Issues: Review logs and troubleshooting section
- Migration Questions: Refer to migration plan document


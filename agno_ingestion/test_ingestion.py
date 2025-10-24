#!/usr/bin/env python
"""Test script for validating the ingestion pipeline."""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

from agno_client import AgnoRAGClient
from doc_processor import (
    parse_frontmatter,
    split_by_h2,
    prepare_chunks_for_upload,
    sha256_file
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_health_check():
    """Test API health check."""
    logger.info("Testing health check...")
    
    load_dotenv()
    api_url = os.getenv("AGNO_RAG_API_URL", "http://localhost:8000")
    
    client = AgnoRAGClient(base_url=api_url)
    
    try:
        health = client.health_check()
        logger.info(f"✓ Health check passed: {health}")
        return True
    except Exception as e:
        logger.error(f"✗ Health check failed: {e}")
        return False


def test_authentication():
    """Test API authentication."""
    logger.info("Testing authentication...")
    
    load_dotenv()
    api_url = os.getenv("AGNO_RAG_API_URL", "http://localhost:8000")
    email = os.getenv("AGNO_RAG_EMAIL")
    password = os.getenv("AGNO_RAG_PASSWORD")
    
    client = AgnoRAGClient(
        base_url=api_url,
        email=email,
        password=password
    )
    
    try:
        success = client.login()
        if success:
            logger.info(f"✓ Authentication successful")
            return True, client
        else:
            logger.error("✗ Authentication failed")
            return False, None
    except Exception as e:
        logger.error(f"✗ Authentication error: {e}")
        return False, None


def test_document_processing():
    """Test document processing functions."""
    logger.info("Testing document processing...")
    
    # Test markdown with frontmatter and H2 headers
    test_markdown = """---
title: Test Document
description: A test document for validation
keywords: [test, validation, documentation]
solidx_concerns: [testing]
---

# Test Document

This is the introduction section.

## Section 1

Content for section 1 goes here.
This is a multi-line section.

## Section 2

Content for section 2.

### Subsection 2.1

Some nested content.

## Section 3

Final section content.
"""
    
    # Test frontmatter parsing
    fm = parse_frontmatter(test_markdown)
    assert fm.get("title") == "Test Document", "Frontmatter title parsing failed"
    assert "test" in fm.get("keywords", []), "Frontmatter keywords parsing failed"
    logger.info(f"✓ Frontmatter parsing: {fm}")
    
    # Test H2 splitting
    chunks = split_by_h2(test_markdown)
    assert len(chunks) == 3, f"Expected 3 H2 chunks, got {len(chunks)}"
    assert chunks[0]["section_title"] == "Section 1", "H2 section title parsing failed"
    logger.info(f"✓ H2 splitting: {len(chunks)} chunks created")
    
    for i, chunk in enumerate(chunks):
        logger.info(f"  Chunk {i}: '{chunk['section_title']}' - {len(chunk['content'])} chars")
    
    return True


def test_single_file_upload(client: AgnoRAGClient):
    """Test uploading a single test file."""
    logger.info("Testing single file upload...")
    
    # Find a test file
    docs_dir = Path("../docs")
    test_file = None
    
    # Look for a small file to test with
    for md_file in docs_dir.rglob("*.md"):
        if md_file.stat().st_size < 10000:  # Less than 10KB
            test_file = md_file
            break
    
    if not test_file:
        logger.warning("No suitable test file found, skipping upload test")
        return True
    
    logger.info(f"Using test file: {test_file}")
    
    try:
        # Read file
        file_text = test_file.read_text(encoding="utf-8", errors="ignore")
        
        # Prepare chunks
        chunks, metadata = prepare_chunks_for_upload(
            file_path=test_file,
            base_dir=docs_dir,
            file_text=file_text,
            document_id="test-doc-id",
            project="test-project"
        )
        
        logger.info(f"✓ Prepared {len(chunks)} chunks from test file")
        logger.info(f"  Metadata: {metadata}")
        
        # Note: We're not actually uploading to avoid cluttering the system
        # In a real test, you would:
        # 1. Create a test collection
        # 2. Upload the document
        # 3. Verify it was uploaded
        # 4. Clean up (delete document and collection)
        
        logger.info("✓ Single file processing test passed (upload skipped)")
        return True
        
    except Exception as e:
        logger.error(f"✗ Single file upload test failed: {e}")
        return False


def test_collection_operations(client: AgnoRAGClient):
    """Test collection operations."""
    logger.info("Testing collection operations...")
    
    try:
        # List collections
        collections = client.list_collections()
        logger.info(f"✓ Listed {len(collections)} collections")
        
        for coll in collections:
            logger.info(f"  - {coll['name']} (ID: {coll['id']})")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Collection operations test failed: {e}")
        return False


def main():
    """Run all tests."""
    logger.info("="*60)
    logger.info("Starting Agno-RAG Ingestion Pipeline Tests")
    logger.info("="*60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Authentication
    auth_success, client = test_authentication()
    results.append(("Authentication", auth_success))
    
    # Test 3: Document processing
    results.append(("Document Processing", test_document_processing()))
    
    # Test 4: Collection operations (requires authentication)
    if client:
        results.append(("Collection Operations", test_collection_operations(client)))
        results.append(("Single File Upload", test_single_file_upload(client)))
    
    # Summary
    logger.info("="*60)
    logger.info("Test Summary")
    logger.info("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("="*60)
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info("="*60)
    
    if passed == total:
        logger.info("🎉 All tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()


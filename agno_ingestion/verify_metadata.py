#!/usr/bin/env python
"""Verify that all metadata fields are present in Agno-RAG documents."""

import os
import sys
import json
import logging
from dotenv import load_dotenv
from agno_client import AgnoRAGClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def verify_document_metadata(client: AgnoRAGClient, collection_id: str):
    """Verify metadata for all documents in a collection."""
    
    logger.info(f"Fetching documents from collection: {collection_id}")
    documents = client.list_documents(collection_id, limit=10)
    
    logger.info(f"Found {len(documents)} documents")
    
    for doc in documents:
        logger.info("="*80)
        logger.info(f"Document ID: {doc.get('id')}")
        logger.info(f"Document Name: {doc.get('metadata', {}).get('document_name', 'N/A')}")
        
        metadata = doc.get('metadata', {})
        
        # Check for required fields
        required_fields = ['title', 'summary', 'keywords', 'solidx_concerns', 'description']
        
        logger.info("\nMetadata Fields:")
        logger.info("-"*80)
        
        all_present = True
        for field in required_fields:
            value = metadata.get(field)
            if value:
                if isinstance(value, list):
                    logger.info(f"  ✓ {field}: {json.dumps(value)}")
                else:
                    logger.info(f"  ✓ {field}: {value[:100] if len(str(value)) > 100 else value}")
            else:
                logger.info(f"  ✗ {field}: MISSING")
                all_present = False
        
        # Show other metadata fields
        logger.info("\nOther Metadata:")
        logger.info("-"*80)
        for key, value in metadata.items():
            if key not in required_fields:
                if isinstance(value, (list, dict)):
                    logger.info(f"  {key}: {json.dumps(value)[:100]}...")
                else:
                    logger.info(f"  {key}: {str(value)[:100]}")
        
        if all_present:
            logger.info("\n✓ All required metadata fields are present!")
        else:
            logger.warning("\n⚠ Some required metadata fields are missing!")
        
        logger.info("="*80 + "\n")


def main():
    load_dotenv()
    
    api_url = os.getenv("AGNO_RAG_API_URL", "http://localhost:8000")
    email = os.getenv("AGNO_RAG_EMAIL")
    password = os.getenv("AGNO_RAG_PASSWORD")
    
    client = AgnoRAGClient(base_url=api_url, email=email, password=password)
    
    # Login
    if not client.login():
        logger.error("Authentication failed")
        sys.exit(1)
    
    # List collections
    logger.info("Fetching collections...")
    collections = client.list_collections()
    
    if not collections:
        logger.error("No collections found")
        sys.exit(1)
    
    logger.info(f"\nFound {len(collections)} collections:")
    for i, coll in enumerate(collections, 1):
        logger.info(f"  {i}. {coll['name']} (ID: {coll['id']})")
    
    # Check first collection by default, or allow user to specify
    if len(sys.argv) > 1:
        collection_name = sys.argv[1]
        collection = next((c for c in collections if c['name'] == collection_name), None)
        if not collection:
            logger.error(f"Collection '{collection_name}' not found")
            sys.exit(1)
    else:
        collection = collections[0]
        logger.info(f"\nChecking collection: {collection['name']}")
    
    # Verify metadata
    verify_document_metadata(client, collection['id'])


if __name__ == "__main__":
    main()


#!/usr/bin/env python
"""Main ingestion script for migrating documentation to Agno-RAG."""

import os
import sys
import json
import argparse
import logging
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv, find_dotenv

from agno_client import AgnoRAGClient
from doc_processor import (
    sha256_file,
    prepare_chunks_for_upload,
    get_collection_id_for_path
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Collection mapping - will be populated after initialization
COLLECTION_MAPPING: Dict[str, str] = {
    "admin-docs": None,
    "developer-docs": None,
    "recipes": None,
    "tutorial": None,
    "user-docs": None,
}


class DocumentIngestor:
    """Orchestrates document ingestion to Agno-RAG."""
    
    def __init__(
        self,
        client: AgnoRAGClient,
        base_dir: Path,
        manifest_path: Path,
        project: str = "solidx-docs",
        extensions: Tuple[str, ...] = (".md", ".mdx"),
        dry_run: bool = False,
        ingest_path: Optional[Path] = None
    ):
        """
        Initialize document ingestor.

        Args:
            client: Agno-RAG API client
            base_dir: Base directory for documentation
            manifest_path: Path to manifest file
            project: Project name
            extensions: Tuple of file extensions to process
            dry_run: If True, don't actually upload documents
            ingest_path: Optional path to ingest from (defaults to base_dir if not provided)
        """
        self.client = client
        self.base_dir = base_dir
        self.manifest_path = manifest_path
        self.project = project
        self.extensions = extensions
        self.dry_run = dry_run
        self.ingest_path = ingest_path
        self._manifest: Dict[str, Dict] = {}
        
    def load_manifest(self) -> None:
        """Load manifest from disk."""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    self._manifest = json.load(f)
                logger.info(f"Loaded manifest with {len(self._manifest)} entries")
            except Exception as e:
                logger.warning(f"Manifest is corrupt; starting fresh: {e}")
                self._manifest = {}
        else:
            self._manifest = {}
            logger.info("No existing manifest found, starting fresh")
    
    def save_manifest(self) -> None:
        """Save manifest to disk."""
        try:
            tmp_path = self.manifest_path.with_suffix('.tmp')
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(self._manifest, f, indent=2, ensure_ascii=False)
            tmp_path.replace(self.manifest_path)
            logger.debug(f"Manifest saved with {len(self._manifest)} entries")
        except Exception as e:
            logger.error(f"Failed to save manifest: {e}")
    
    def iter_files(self) -> List[Path]:
        """
        Iterate over all markdown files in ingest directory.

        Returns:
            List of file paths
        """
        # Use ingest_path if provided, otherwise use base_dir
        search_dir = self.ingest_path if self.ingest_path else self.base_dir

        files = [
            p for p in search_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in self.extensions
        ]
        logger.info(f"Found {len(files)} markdown files in {search_dir}")
        return files
    
    def verify_collections(self) -> bool:
        """
        Verify that all configured collections exist in Agno-RAG.
        
        Returns:
            True if all collections exist, False otherwise
        """
        if self.dry_run:
            logger.info("[DRY-RUN] Would verify collections")
            return True
        
        logger.info("Verifying collections exist in Agno-RAG...")
        
        for section, collection_id in COLLECTION_MAPPING.items():
            if not collection_id:
                logger.error(f"Collection '{section}' has no ID assigned")
                return False
            
            try:
                collection = self.client.get_collection(collection_id)
                if collection:
                    logger.info(f"✓ Collection '{section}' verified: {collection_id}")
                else:
                    logger.error(f"✗ Collection '{section}' ({collection_id}) not found")
                    return False
            except Exception as e:
                logger.error(f"✗ Failed to verify collection '{section}': {e}")
                return False
        
        return True
    
    def upsert_file(self, file_path: Path) -> bool:
        """
        Upsert a single file to Agno-RAG.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Use ingest_path for relative path calculation if provided, otherwise use base_dir
            relative_base = self.ingest_path if self.ingest_path else self.base_dir
            rel_path = file_path.relative_to(relative_base)
            key = str(rel_path).replace("\\", "/")
            
            # Determine which collection this file belongs to
            collection_id = get_collection_id_for_path(rel_path, COLLECTION_MAPPING)

            # If no collection found and we're using ingest_path, check if ingest_path
            # is a subdirectory of base_dir that matches a collection
            if not collection_id and self.ingest_path:
                try:
                    ingest_relative_to_base = self.ingest_path.relative_to(self.base_dir)
                    if len(ingest_relative_to_base.parts) > 0:
                        collection_name = ingest_relative_to_base.parts[0]
                        collection_id = COLLECTION_MAPPING.get(collection_name)
                        if collection_id:
                            logger.debug(f"File {key} mapped to collection '{collection_name}' from ingest_path ({collection_id})")
                except ValueError:
                    # ingest_path is not a subdirectory of base_dir, skip this logic
                    pass

            if not collection_id:
                logger.warning(f"Skipping file {key} - no collection mapping found")
                return False
            
            # Calculate file hash
            file_hash = sha256_file(file_path)
            
            # Check if file has changed
            prev = self._manifest.get(key)
            if prev and prev.get("hash") == file_hash and prev.get("document_id"):
                logger.info(f"Unchanged: {key}")
                return True
            
            # Read file content
            file_text = file_path.read_text(encoding="utf-8", errors="ignore")
            
            # Generate document ID
            if prev and prev.get("document_id"):
                # Reuse existing document ID if we're updating
                document_id = prev["document_id"]
            else:
                document_id = str(uuid.uuid4())
            
            # Prepare chunks and metadata
            chunks, parent_metadata = prepare_chunks_for_upload(
                file_path=file_path,
                base_dir=self.base_dir,
                file_text=file_text,
                document_id=document_id,
                project=self.project
            )
            
            if not chunks:
                logger.error(f"No valid chunks generated for {key}, skipping")
                return False
            
            # Delete old document if it exists and changed
            if prev and prev.get("document_id") and prev.get("hash") != file_hash:
                old_id = prev["document_id"]
                logger.info(f"Changed: {key} (replacing document_id={old_id})")
                if not self.dry_run:
                    self.client.delete_document(old_id, collection_id)
            
            # Upload document
            if self.dry_run:
                logger.info(
                    f"[DRY-RUN] Would upload {key} with {len(chunks)} chunks "
                    f"to collection {collection_id}"
                )
            else:
                parent_metadata["uploaded_by"] = "migration_script"
                parent_metadata["uploaded_at"] = datetime.utcnow().isoformat()
                
                result = self.client.upload_pre_chunked_document(
                    collection_id=collection_id,
                    parent_document_name=key,
                    chunks=chunks,
                    metadata=parent_metadata
                )
                
                document_id = result.get("document_id", document_id)
                logger.info(f"✓ Uploaded: {key} -> document_id={document_id}")
            
            # Update manifest
            self._manifest[key] = {
                "hash": file_hash,
                "document_id": document_id,
                "collection_id": collection_id,
                "metadata": parent_metadata,
                "chunk_count": len(chunks),
                "uploaded_at": datetime.utcnow().isoformat()
            }
            
            # Save manifest after each successful file
            if not self.dry_run:
                self.save_manifest()
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}", exc_info=True)
            return False
    
    def run(self, single_file: Optional[str] = None) -> Dict[str, int]:
        """
        Run the ingestion process.
        
        Args:
            single_file: Optional path to single file to process
            
        Returns:
            Dictionary with statistics
        """
        logger.info("="*60)
        logger.info("Starting Agno-RAG ingestion")
        logger.info("="*60)
        
        # Load manifest
        self.load_manifest()
        
        # Verify collections
        if not self.verify_collections():
            logger.error("Collection verification failed, aborting")
            return {"success": 0, "failed": 0, "skipped": 0}
        
        # Statistics
        stats = {"success": 0, "failed": 0, "skipped": 0}
        
        # Process files
        if single_file:
            # Single file mode
            file_path = Path(single_file).resolve()
            if not file_path.exists():
                logger.error(f"File not found: {single_file}")
                return stats
            
            logger.info(f"Single file mode: {file_path}")
            if self.upsert_file(file_path):
                stats["success"] += 1
            else:
                stats["failed"] += 1
        else:
            # Batch mode
            files = self.iter_files()
            total = len(files)
            
            for idx, file_path in enumerate(files, 1):
                logger.info(f"[{idx}/{total}] Processing: {file_path.relative_to(self.base_dir)}")
                
                if self.upsert_file(file_path):
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
        
        # Final save
        if not self.dry_run:
            self.save_manifest()
        
        # Print summary
        logger.info("="*60)
        logger.info("Ingestion Summary")
        logger.info("="*60)
        logger.info(f"Successful: {stats['success']}")
        logger.info(f"Failed: {stats['failed']}")
        logger.info(f"Skipped: {stats['skipped']}")
        logger.info("="*60)
        
        return stats


def initialize_collections(client: AgnoRAGClient, dry_run: bool = False) -> bool:
    """
    Initialize collections in Agno-RAG if they don't exist.
    
    Args:
        client: Agno-RAG API client
        dry_run: If True, don't actually create collections
        
    Returns:
        True if successful, False otherwise
    """
    logger.info("Initializing collections...")
    
    if dry_run:
        logger.info("[DRY-RUN] Would initialize collections")
        # Use dummy IDs for dry run
        for section in COLLECTION_MAPPING:
            COLLECTION_MAPPING[section] = str(uuid.uuid4())
        return True
    
    try:
        # Get existing collections
        existing = client.list_collections()
        existing_by_name = {c["name"]: c for c in existing}
        
        for section in COLLECTION_MAPPING:
            if section in existing_by_name:
                # Collection exists, use its ID
                collection_id = existing_by_name[section]["id"]
                COLLECTION_MAPPING[section] = collection_id
                logger.info(f"Found existing collection '{section}': {collection_id}")
            else:
                # Create new collection
                logger.info(f"Creating collection '{section}'...")
                collection = client.create_collection(
                    name=section,
                    description=f"SolidX documentation - {section}"
                )
                COLLECTION_MAPPING[section] = collection["id"]
                logger.info(f"Created collection '{section}': {collection['id']}")
        
        logger.info("Collection initialization complete")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize collections: {e}")
        return False


def setup_args():
    """Setup command line arguments."""
    parser = argparse.ArgumentParser(
        description="Ingest Docusaurus documentation into Agno-RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest all documents in the docs directory
  python ingest_docs.py

  # Ingest documents from a specific path
  python ingest_docs.py --path ./custom-docs

  # Ingest a single file for testing
  python ingest_docs.py --single-file ./docs/admin-docs/getting-started.md

  # Dry run mode
  python ingest_docs.py --dry-run

  # Verbose output
  python ingest_docs.py --verbose
        """
    )
    
    parser.add_argument(
        "--single-file",
        type=str,
        help="Ingest a single file instead of scanning the entire base directory"
    )

    parser.add_argument(
        "--path",
        type=str,
        help="Path to directory or files to ingest (optional, defaults to base directory)"
    )

    parser.add_argument(
        "--base-dir",
        type=str,
        help="Override base directory (default from DOCS_BASE_DIR env var or '../docs')"
    )
    
    parser.add_argument(
        "--manifest",
        type=str,
        help="Override manifest path (default from MANIFEST_PATH env var or './agno_manifest.json')"
    )
    
    parser.add_argument(
        "--project",
        type=str,
        help="Override project name (default from PROJECT_NAME env var or 'solidx-docs')"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (don't actually ingest)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--init-collections",
        action="store_true",
        help="Initialize collections only and exit"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = setup_args()
    
    # Load environment
    cwd = os.getcwd()
    env_path = find_dotenv(usecwd=True) or "./.env"
    load_dotenv(dotenv_path=env_path, override=True)
    
    logger.info(f"CWD: {cwd}")
    logger.info(f".env loaded from: {env_path}")
    
    # Configure logging level
    if args.verbose or os.getenv("VERBOSE", "false").lower() == "true":
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get configuration
    api_url = os.getenv("AGNO_RAG_API_URL", "http://localhost:8000")
    email = os.getenv("AGNO_RAG_EMAIL")
    password = os.getenv("AGNO_RAG_PASSWORD")
    base_dir = Path(args.base_dir or os.getenv("DOCS_BASE_DIR", "../docs")).resolve()
    manifest = Path(args.manifest or os.getenv("MANIFEST_PATH", "./agno_manifest.json")).resolve()
    project = args.project or os.getenv("PROJECT_NAME", "solidx-docs")
    extensions = tuple(os.getenv("DOC_EXTENSIONS", ".md,.mdx").split(","))
    dry_run = args.dry_run or os.getenv("DRY_RUN", "false").lower() == "true"
    ingest_path = Path(args.path).resolve() if args.path else None
    
    logger.info(f"API URL: {api_url}")
    logger.info(f"Base directory: {base_dir}")
    logger.info(f"Ingest path: {ingest_path if ingest_path else 'using base directory'}")
    logger.info(f"Manifest: {manifest}")
    logger.info(f"Project: {project}")
    logger.info(f"Extensions: {extensions}")
    
    if dry_run:
        logger.info("⚠️  Running in DRY-RUN mode")
    
    # Initialize client
    client = AgnoRAGClient(
        base_url=api_url,
        email=email,
        password=password
    )
    
    # Health check
    try:
        health = client.health_check()
        logger.info(f"✓ API health check passed: {health.get('status')}")
    except Exception as e:
        logger.error(f"✗ API health check failed: {e}")
        sys.exit(1)
    
    # Login
    if not dry_run:
        if not client.login():
            logger.error("Authentication failed")
            sys.exit(1)
    
    # Initialize collections
    if not initialize_collections(client, dry_run):
        logger.error("Failed to initialize collections")
        sys.exit(1)
    
    # If only initializing collections, exit
    if args.init_collections:
        logger.info("Collections initialized successfully")
        sys.exit(0)
    
    # Create ingestor
    ingestor = DocumentIngestor(
        client=client,
        base_dir=base_dir,
        manifest_path=manifest,
        project=project,
        extensions=extensions,
        dry_run=dry_run,
        ingest_path=ingest_path
    )
    
    # Run ingestion
    stats = ingestor.run(single_file=args.single_file)
    
    # Exit with error code if any failures
    if stats["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()


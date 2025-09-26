#!/usr/bin/env python
import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from r2r_helper import R2RHelper
from doc_ingestor import DocIngestor

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def setup_args():
    parser = argparse.ArgumentParser(
        description="Ingest Docusaurus documentation into R2R",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest all documents in the docs directory
  python ingest_docs.py

  # Ingest a single file for testing
  python ingest_docs.py --single-file ./docs/admin-docs/getting-started.md

  # Dry run mode
  DRY_RUN=true python ingest_docs.py

  # Single file with custom project name
  python ingest_docs.py --single-file ./my-doc.md --project my-test-project
        """
    )
    
    parser.add_argument(
        "--single-file", 
        type=str, 
        help="Ingest a single file instead of scanning the entire base directory"
    )
    
    parser.add_argument(
        "--project", 
        type=str, 
        help="Override project name (default from R2R_PROJECT env var or 'solidx-docs')"
    )
    
    parser.add_argument(
        "--base-dir", 
        type=str, 
        help="Override base directory (default from DOCUSAURUS_BASE_DIR env var or './docs')"
    )
    
    parser.add_argument(
        "--manifest", 
        type=str, 
        help="Override manifest path (default from R2R_MANIFEST_PATH env var or './manifest.json')"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Run in dry-run mode (don't actually ingest)"
    )
    
    return parser.parse_args()


def ingest_single_file(file_path: str, ingestor: DocIngestor):
    """Ingest a single file and print results."""
    try:
        result = ingestor.upsert_single_file(file_path)
        print("\n" + "="*50)
        print("SINGLE FILE INGESTION RESULT")
        print("="*50)
        print(f"File: {result['file_path']}")
        print(f"Relative Path: {result['relative_path']}")
        print(f"Document ID: {result['document_id']}")
        print(f"File Hash: {result['hash']}")
        print(f"Status: {result['status']}")
        print("="*50)
        return result
    except Exception as e:
        logging.error(f"Failed to ingest single file: {e}")
        return None


def main():
    args = setup_args()
    
    cwd = os.getcwd()
    env_path = find_dotenv(usecwd=True) or "./.env"
    load_dotenv(dotenv_path=env_path, override=True)

    logging.info(f"CWD: {cwd}")
    logging.info(f".env loaded from: {env_path}")

    # Use CLI args or fall back to env vars or defaults
    base_dir = Path(args.base_dir or os.getenv("DOCUSAURUS_BASE_DIR", "./docs")).resolve()
    manifest = Path(args.manifest or os.getenv("R2R_MANIFEST_PATH", "./manifest.json")).resolve()
    project = args.project or os.getenv("R2R_PROJECT", "solidx-docs")
    exts = tuple(os.getenv("DOC_EXTS", ".md").split(","))  # e.g. ".md,.mdx"
    dry_run = args.dry_run or os.getenv("DRY_RUN", "false").lower() == "true"

    if dry_run:
        logging.info("Running in DRY-RUN mode")

    r2r = R2RHelper().connect()

    ingestor = DocIngestor(
        client=r2r,
        base_dir=base_dir,
        manifest_path=manifest,
        project=project,
        exts=exts,
        dry_run=dry_run,
    )

    if args.single_file:
        # Single file mode
        logging.info(f"Single file mode: {args.single_file}")
        result = ingest_single_file(args.single_file, ingestor)
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        # Normal bulk ingestion mode
        ingestor.run(cleanup=True)


if __name__ == "__main__":
    main()

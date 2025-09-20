#!/usr/bin/env python
import os
import logging
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from r2r_helper import R2RHelper
from doc_ingestor import DocIngestor

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main():
    cwd = os.getcwd()
    env_path = find_dotenv(usecwd=True) or "./.env"
    load_dotenv(dotenv_path=env_path, override=True)

    logging.info(f"CWD: {cwd}")
    logging.info(f".env loaded from: {env_path}")

    base_dir = Path(os.getenv("DOCUSAURUS_BASE_DIR", "./docs")).resolve()
    manifest = Path(os.getenv("R2R_MANIFEST_PATH", "./manifest.json")).resolve()
    project = os.getenv("R2R_PROJECT", "solidx-docs")
    exts = tuple(os.getenv("DOC_EXTS", ".md").split(","))  # e.g. ".md,.mdx"
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

    r2r = R2RHelper().connect()

    ingestor = DocIngestor(
        client=r2r,
        base_dir=base_dir,
        manifest_path=manifest,
        project=project,
        exts=exts,
        dry_run=dry_run,
    )
    ingestor.run(cleanup=True)


if __name__ == "__main__":
    main()

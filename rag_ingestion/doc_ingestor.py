import uuid
import os
import re
import json
import hashlib
import logging
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from r2r import R2RException
from r2r import R2RClient

logger = logging.getLogger(__name__)

FRONTMATTER_RE = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)


def sanitize_metadata(meta: Dict) -> Dict:
    """
    Remove or rename keys that could collide with server-side reserved fields,
    especially 'type' or 'documentType'.
    """
    out = {}
    for k, v in meta.items():
        lk = k.lower()
        if lk in ("type", "documenttype", "doctype"):
            out[f"fm_{k}"] = v  # rename to avoid collision
        else:
            out[k] = v
    return out


def guess_doc_type_and_mime(path: Path) -> Dict[str, str]:
    """
    Map extension -> (document_type, mime_type) for R2R.
    Adjust names to exactly what your R2R expects.
    """
    ext = path.suffix.lower()
    if ext in (".md", ".mdx"):
        return {"document_type": "markdown", "mime_type": "text/markdown"}
    if ext in (".txt",):
        return {"document_type": "text", "mime_type": "text/plain"}
    if ext in (".pdf",):
        return {"document_type": "pdf", "mime_type": "application/pdf"}
    if ext in (".html", ".htm"):
        return {"document_type": "html", "mime_type": "text/html"}
    # default: treat as plain text
    return {"document_type": "text", "mime_type": "text/plain"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def try_parse_frontmatter(text: str) -> Dict:
    """
    Parses YAML frontmatter if present. Returns {} if none or if PyYAML not installed.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    yaml_block = m.group(1)
    try:
        import yaml  # optional dependency

        return yaml.safe_load(yaml_block) or {}
    except Exception:
        logger.debug("Frontmatter present but PyYAML not installed or invalid YAML.")
        return {}


def extract_title(text: str, fm: Dict) -> Optional[str]:
    if isinstance(fm.get("title"), str):
        return fm["title"]
    m = H1_RE.search(text)
    return m.group(1).strip() if m else None


def path_to_slug(p: Path) -> str:
    # slug like "admin-docs/iam/permissions"
    parts = [seg for seg in p.with_suffix("").parts if seg not in (".", "docs")]
    return "/".join(parts)


def git_last_modified(path: Path) -> Optional[Dict[str, str]]:
    """
    Returns last commit metadata for the file if in a git repo.
    """
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%H|%an|%ae|%ad", "--", str(path)],
            stderr=subprocess.DEVNULL,
            cwd=str(path.parent),
            text=True,
        ).strip()
        if not out:
            return None
        commit, author, email, date = out.split("|", 3)
        return {
            "git_commit": commit,
            "git_author": author,
            "git_email": email,
            "git_date": date,
        }
    except Exception:
        return None


def breadcrumbs(rel_path: Path) -> List[str]:
    # e.g. admin-docs/iam/permissions.md -> ["admin-docs","iam","permissions"]
    return [p for p in rel_path.with_suffix("").parts if p != "docs"]


class DocIngestor:
    """
    Ingests Docusaurus .md docs into R2R with a local manifest to track hashes + R2R IDs.
    """

    def __init__(
        self,
        client: R2RClient,
        base_dir: Path,
        manifest_path: Path,
        project: Optional[str] = None,
        exts: Tuple[str, ...] = (".md",),  # add ".mdx" if needed
        dry_run: bool = False,
    ):
        self.client = client
        self.base_dir = base_dir
        self.manifest_path = manifest_path
        self.project = project or "solidx-docs"
        self.exts = exts
        self.dry_run = dry_run
        self._manifest: Dict[str, Dict] = {}

    # ---- manifest helpers ----

    def load_manifest(self) -> None:
        if self.manifest_path.exists():
            try:
                self._manifest = json.loads(
                    self.manifest_path.read_text(encoding="utf-8")
                )
            except Exception:
                logger.warning("Manifest is corrupt; starting fresh.")
                self._manifest = {}
        else:
            self._manifest = {}

    # ---- collection resolve ----

    def ensure_collection(self) -> str:
        """Ensure we have a collection_id in the manifest, create if needed."""
        coll_id = self._manifest.get("_collection_id")
        if coll_id:
            return coll_id

        if self.dry_run:
            coll_id = "dry-run-collection"
            logger.info("[DRY-RUN] Would create collection 'solidx-docs'")
        else:
            solidx_docs_collection = None 
            try:
                solidx_docs_collection = self.client.collections.retrieve_by_name(name='solidx-docs')
            except R2RException as r2rEx:
                logger.warning('Collection solidx-docs does not exist, will attempt to create it.')

            if not solidx_docs_collection:
                result = self.client.collections.create(
                    name="solidx-docs",
                    description="SolidX documentation collection",
                )
                coll_id = result.results.id
                logger.info(f"Created collection 'solidx-docs' with id={coll_id}")
            else:
                coll_id = solidx_docs_collection.results.id
                logger.info(f"Resolved collection 'solidx-docs' with id={coll_id}")

        self._manifest["_collection_id"] = str(coll_id)
        return coll_id

    def save_manifest(self) -> None:
        tmp = self.manifest_path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(self._manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        tmp.replace(self.manifest_path)

    # ---- scan + ingest ----

    def iter_files(self) -> List[Path]:
        return [
            p
            for p in self.base_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in self.exts
        ]

    def build_metadata(self, file_path: Path, rel_path: Path, file_text: str) -> Dict:
        fm = try_parse_frontmatter(file_text)
        title = extract_title(file_text, fm)
        section = rel_path.parts[0] if len(rel_path.parts) > 0 else ""
        crumb = breadcrumbs(rel_path)
        slug = path_to_slug(rel_path)

        base_meta = {
            "source": "docusaurus",
            "project": self.project,
            "section": section,
            "slug": slug,
            "path": str(rel_path).replace("\\", "/"),
            "filename": file_path.name,
            "breadcrumbs": crumb,
            "doc_title": title,
            # "frontmatter": fm,
            # "kind": "documentation",
            # "format": (
            #     "markdown"
            #     if file_path.suffix.lower() in (".md", ".mdx")
            #     else file_path.suffix.lower().lstrip(".")
            # ),
        }

        gitmeta = git_last_modified(file_path)
        if gitmeta:
            base_meta.update(gitmeta)

        return sanitize_metadata(base_meta)

    def upsert_file(self, file_path: Path, collection_id: str) -> None:
        rel_path = file_path.relative_to(self.base_dir)
        key = str(rel_path).replace("\\", "/")

        file_hash = sha256_file(file_path)
        prev = self._manifest.get(key)
        if prev and prev.get("hash") == file_hash and prev.get("document_id"):
            logger.info(f"Unchanged: {key}")
            return

        # (Re)ingest
        file_text = file_path.read_text(encoding="utf-8", errors="ignore")
        metadata = self.build_metadata(file_path, rel_path, file_text)

        # If existed but changed: delete old first
        if prev and prev.get("document_id"):
            old_id = prev["document_id"]
            logger.info(f"Changed: {key} (replacing document_id={old_id})")
            if not self.dry_run:
                try:
                    self.client.documents.delete(old_id)
                except Exception as e:
                    logger.warning(f"Delete failed for {old_id}: {e}")

        if self.dry_run:
            new_id = "dry-run"
            logger.info(f"[DRY-RUN] Would create document for {key}")
        else:
            generated_id = uuid.uuid4()
            resp = self.client.documents.create(
                file_path=str(file_path),
                metadata=metadata,
                id=str(generated_id),
                collection_ids=[collection_id],
            )
            new_id = resp.results.document_id
            logger.info(f"Created: {key} -> document_id={new_id}")

        self._manifest[key] = {
            "hash": file_hash,
            "document_id": str(new_id),
            "metadata": metadata,
        }

    def cleanup_orphans(self) -> None:
        """
        Delete any manifest entries that no longer exist on disk.
        """
        disk_keys = set(
            str(p.relative_to(self.base_dir)).replace("\\", "/")
            for p in self.iter_files()
        )
        man_keys = set(self._manifest.keys())
        orphans = man_keys - disk_keys
        for key in sorted(orphans):
            doc_id = self._manifest[key].get("document_id")
            logger.info(f"Orphan: {key} (deleting document_id={doc_id})")
            if not self.dry_run and doc_id:
                try:
                    self.client.documents.delete(doc_id)
                except Exception as e:
                    logger.warning(f"Delete failed for {doc_id}: {e}")
            self._manifest.pop(key, None)

    def run(self, cleanup: bool = True) -> None:
        logger.info(f"Scanning base_dir={self.base_dir}")
        self.load_manifest()
        collection_id = self.ensure_collection()

        for p in self.iter_files():
            self.upsert_file(p, collection_id)
        # if cleanup:
        #     self.cleanup_orphans()
        self.save_manifest()

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
from openai import OpenAI

logger = logging.getLogger(__name__)

FRONTMATTER_RE = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^\s*##\s+(.+?)\s*$", re.MULTILINE)


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


def split_by_h2(text: str) -> List[Dict[str, str]]:
    """
    Split document content by H2 headers, maintaining order.
    Returns list of chunks with section titles and content.
    """
    # Remove frontmatter from text for processing
    clean_text = FRONTMATTER_RE.sub("", text).strip()
    
    # Find all H2 matches with their positions
    h2_matches = list(H2_RE.finditer(clean_text))
    
    if not h2_matches:
        # No H2 headers found, return the entire content as one chunk
        return [{"section_title": None, "content": clean_text}]
    
    chunks = []
    
    # Process each H2 section
    for i, match in enumerate(h2_matches):
        section_title = match.group(1).strip()
        start_pos = match.start()
        
        # Determine end position (start of next H2 or end of text)
        end_pos = h2_matches[i + 1].start() if i + 1 < len(h2_matches) else len(clean_text)
        
        # Extract content from H2 header to next H2 (or end)
        section_content = clean_text[start_pos:end_pos].strip()
        
        chunks.append({
            "section_title": section_title,
            "content": section_content
        })
    
    return chunks


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
    Documents from different subdirectories are ingested into separate collections.
    """

    # Mapping of subdirectory names to their collection IDs
    COLLECTION_MAPPING = {
        "admin-docs": "83a1a8df-aed3-4d80-b391-d52c1ccf5563",
        "developer-docs": "1d90f2d7-97fa-4aff-8b1f-9b5d4c9d9357",
        "recipes": "f0935ef1-c3c4-403d-b32f-2a2d52861db1",
        "tutorial": "cd59267d-67e0-4897-91a6-1a338f5e83bf",
        "user-docs": "32abd328-cb4c-4792-888b-a690a47c4e29",
    }

    def __init__(
        self,
        client: R2RClient,
        base_dir: Path,
        manifest_path: Path,
        project: Optional[str] = None,
        exts: Tuple[str, ...] = (".md",),  # add ".mdx" if needed
        dry_run: bool = False,
        openai_api_key: Optional[str] = None,
    ):
        self.client = client
        self.base_dir = base_dir
        self.manifest_path = manifest_path
        self.project = project or "solidx-docs"
        self.exts = exts
        self.dry_run = dry_run
        self._manifest: Dict[str, Dict] = {}
        
        # Initialize OpenAI client for summary generation
        self.openai_client = None
        if openai_api_key or os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))
            logger.info("OpenAI client initialized for chunk summary generation")
        else:
            logger.warning("No OpenAI API key provided. Chunk summaries will not be generated.")

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

    def get_collection_id_for_file(self, rel_path: Path) -> str:
        """
        Determine which collection a file belongs to based on its relative path.
        Returns the collection ID for the first matching subdirectory.
        """
        # Get the first directory component (e.g., "admin-docs" from "admin-docs/iam/permissions.md")
        if len(rel_path.parts) > 0:
            first_dir = rel_path.parts[0]
            collection_id = self.COLLECTION_MAPPING.get(first_dir)
            if collection_id:
                logger.debug(f"File {rel_path} mapped to collection '{first_dir}' ({collection_id})")
                return collection_id
        
        # Fallback: if no mapping found, log a warning
        logger.warning(f"No collection mapping found for file {rel_path}. File will be skipped.")
        return None

    # ---- collection resolve ----

    def verify_collections(self) -> None:
        """
        Verify that all configured collections exist in R2R.
        This should be called once at the start of ingestion.
        """
        if self.dry_run:
            logger.info("[DRY-RUN] Would verify collections")
            return
        
        logger.info("Verifying collections exist in R2R...")
        for subdir, collection_id in self.COLLECTION_MAPPING.items():
            try:
                # Try to retrieve the collection to verify it exists
                collection = self.client.collections.retrieve(collection_id)
                logger.info(f"✓ Collection '{subdir}' verified: {collection_id}")
            except Exception as e:
                logger.error(f"✗ Collection '{subdir}' ({collection_id}) not found or inaccessible: {e}")
                raise ValueError(f"Collection for '{subdir}' does not exist. Please create it first.")

    def generate_chunk_summary(self, chunk_content: str, section_title: Optional[str], doc_title: str) -> Dict[str, str]:
        """
        Generate both short and detailed summaries for a chunk using OpenAI GPT.
        
        Args:
            chunk_content: The actual content of the chunk
            section_title: The H2 section title (if any)
            doc_title: The document title/path
            
        Returns:
            Dictionary with 'short_summary' and 'detailed_summary' keys
        """
        if not self.openai_client:
            return {"short_summary": "", "detailed_summary": ""}
        
        try:
            # Create context-aware prompt
            context = f"Document: {doc_title}"
            if section_title:
                context += f"\nSection: {section_title}"
            
            prompt = f"""Given this documentation chunk, provide:
                1. A short one-line summary (max 50 words)
                2. A detailed summary (about 3 to 4 sentences)

                {context}

                Content:
                {chunk_content[:1500]}  # Limit content to avoid token limits

                Respond in JSON format:
                {{
                "short_summary": "one-line summary here",
                "detailed_summary": "First sentence. Second sentence. Third sentence etc."
                }}"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4.1",  # Using cost-effective model
                messages=[
                    {"role": "system", "content": "You are a technical documentation summarizer. Provide concise, accurate summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            summaries = json.loads(response.choices[0].message.content)
            logger.debug(f"Generated summaries for section '{section_title or 'untitled'}'")
            return summaries
            
        except Exception as e:
            logger.warning(f"Failed to generate summary: {e}")
            return {"short_summary": "", "detailed_summary": ""}

    def save_manifest(self) -> None:
        tmp = self.manifest_path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(self._manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        tmp.replace(self.manifest_path)

    def debug_document_chunks(self, document_id: str) -> None:
        """Debug function to examine chunks created by R2R for a specific document"""
        try:
            import time
            # Wait a moment for R2R to finish processing
            time.sleep(3)
            
            logger.info(f"=== DEBUG: Analyzing chunks for document {document_id} ===")
            
            # Get document details
            doc_response = self.client.documents.retrieve(document_id)
            logger.info(f"Document title: {getattr(doc_response.results, 'title', 'N/A')}")
            
            # Check if summary was generated
            summary = getattr(doc_response.results, 'summary', None)
            if summary:
                logger.info(f"✓ Summary generated: {summary[:100]}...")
            else:
                logger.warning("✗ No summary generated")
            
            # Get chunks for this document - use correct API method
            chunks_response = self.client.chunks.list(
                filters={"document_id": str(document_id)},  # Convert UUID to string
                limit=100  # Get all chunks
            )
            
            chunks = chunks_response.results
            logger.info(f"Total chunks created by R2R: {len(chunks)}")
            
            # Analyze chunk content
            h2_chunks = []
            for i, chunk in enumerate(chunks):
                lines = chunk.text.strip().split('\n')
                first_line = lines[0] if lines else ""
                
                if first_line.startswith("## "):
                    h2_chunks.append((i, first_line, len(chunk.text)))
                    logger.info(f"Chunk {i+1}: H2 Section - {first_line} ({len(chunk.text)} chars)")
                else:
                    logger.info(f"Chunk {i+1}: Non-H2 - {first_line[:50]}... ({len(chunk.text)} chars)")
            
            logger.info(f"=== SUMMARY: {len(h2_chunks)} H2-based chunks out of {len(chunks)} total ===")
            
            if len(h2_chunks) == 10:
                logger.info("✓ Perfect! Got exactly 10 H2-based chunks as expected")
            else:
                logger.warning(f"✗ Expected 10 H2 chunks, got {len(h2_chunks)}")
                
        except Exception as e:
            logger.error(f"Debug chunk analysis failed: {e}")

    # ---- scan + ingest ----

    def iter_files(self) -> List[Path]:
        return [
            p
            for p in self.base_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in self.exts
        ]

    def build_metadata(self, file_path: Path, rel_path: Path, file_text: str) -> Dict:
        fm = try_parse_frontmatter(file_text)
        # Use file path as title instead of content title
        title = str(rel_path).replace("\\", "/")
        section = rel_path.parts[0] if len(rel_path.parts) > 0 else ""
        # crumb = breadcrumbs(rel_path)
        # slug = path_to_slug(rel_path)

        base_meta = {
            "source": "docusaurus",
            "project": self.project,
            "section": section,
            # "slug": slug,
            "path": str(rel_path).replace("\\", "/"),
            # "filename": file_path.name,
            # "breadcrumbs": crumb,
            "doc_title": title,
            # "frontmatter": fm,
            # "kind": "documentation",
            # "format": (
            #     "markdown"
            #     if file_path.suffix.lower() in (".md", ".mdx")
            #     else file_path.suffix.lower().lstrip(".")
            # ),
        }

        # gitmeta = git_last_modified(file_path)
        # if gitmeta:
        #     base_meta.update(gitmeta)

        return sanitize_metadata(base_meta)

    def upsert_file(self, file_path: Path) -> None:
        rel_path = file_path.relative_to(self.base_dir)
        key = str(rel_path).replace("\\", "/")

        # Determine which collection this file belongs to
        collection_id = self.get_collection_id_for_file(rel_path)
        if not collection_id:
            logger.warning(f"Skipping file {key} - no collection mapping found")
            return

        file_hash = sha256_file(file_path)
        prev = self._manifest.get(key)
        if prev and prev.get("hash") == file_hash and prev.get("document_id"):
            logger.info(f"Unchanged: {key}")
            return

        # (Re)ingest
        file_text = file_path.read_text(encoding="utf-8", errors="ignore")
        metadata = self.build_metadata(file_path, rel_path, file_text)
        
        # Add collection information to metadata for tracking
        metadata["collection_id"] = collection_id
        metadata["collection_name"] = next((k for k, v in self.COLLECTION_MAPPING.items() if v == collection_id), "unknown")

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
            # Split content by H2 headers
            chunks_data = split_by_h2(file_text)
            
            # Debug: Log what we're getting from H2 splitting
            # logger.info(f"H2 split result: {len(chunks_data)} sections found")
            for i, chunk_data in enumerate(chunks_data):
                title = chunk_data["section_title"]
                content_preview = chunk_data["content"][:100].replace('\n', ' ')
                # logger.info(f"  Section {i}: '{title}' - {content_preview}...")
            
            # Use file path as title
            rel_path = file_path.relative_to(self.base_dir)
            doc_title = str(rel_path).replace("\\", "/")
            metadata["title"] = doc_title
            
            # Prepare enhanced chunks with order metadata and summaries
            chunks = []
            chunk_metadata_list = []
            total_chunks = len(chunks_data)
            
            logger.info(f"Processing {total_chunks} H2 sections with summaries and ordering...")
            
            for idx, chunk_data in enumerate(chunks_data):
                chunk_order = idx + 1  # 1-indexed for human readability
                section_title = chunk_data["section_title"]
                content = chunk_data["content"]
                
                # Generate summaries using OpenAI
                summaries = self.generate_chunk_summary(content, section_title, doc_title)
                
                # Add the original content without modifications
                chunks.append(content)
                
                # Prepare chunk-level metadata
                chunk_meta = {
                    "chunk_order": chunk_order,
                    "total_chunks": total_chunks,
                    "section_title": section_title or "Introduction",
                    "short_summary": summaries.get("short_summary", ""),
                    "detailed_summary": summaries.get("detailed_summary", ""),
                }
                chunk_metadata_list.append(chunk_meta)
                
                logger.info(f"  Chunk {chunk_order}/{total_chunks}: '{section_title or 'Introduction'}' - {summaries.get('short_summary', 'No summary')[:60]}...")
            
            # Add document-level metadata
            metadata["chunk_count"] = total_chunks
            metadata["has_summaries"] = bool(self.openai_client)
            
            # Create document with chunks
            logger.info(f"Creating document with {len(chunks)} H2 sections...")
            
            generated_id = uuid.uuid4()
            resp = self.client.documents.create(
                chunks=chunks,
                metadata=metadata,
                id=str(generated_id),
                collection_ids=[collection_id],
                ingestion_mode="fast",  # Fast mode respects our pre-processed chunks
                run_with_orchestration=True  # Enable orchestration for summary generation
            )
            document_id = resp.results.document_id
            logger.info(f"Created: {key} -> document_id={document_id}")
            
            # Wait a moment for R2R to process chunks
            import time
            time.sleep(2)
            
            # Now update each chunk with its metadata
            logger.info(f"Updating chunk-level metadata for {total_chunks} chunks...")
            try:
                # Retrieve chunks for this document
                chunks_response = self.client.chunks.list_by_document(
                    document_id=document_id,
                    limit=total_chunks
                )
                
                created_chunks = chunks_response.results
                logger.info(f"Retrieved {len(created_chunks)} chunks from R2R")
                
                # Update each chunk with its metadata
                for idx, chunk in enumerate(created_chunks):
                    if idx < len(chunk_metadata_list):
                        chunk_meta = chunk_metadata_list[idx]
                        
                        # Update chunk with metadata - API requires 'text' field
                        update_data = {
                            "id": str(chunk.id),
                            "text": chunk.text,  # Include existing text
                            "metadata": chunk_meta
                        }
                        
                        self.client.chunks.update(update_data)
                        logger.info(f"  Updated chunk {idx + 1}/{len(created_chunks)} with metadata")
                
                logger.info(f"✓ Successfully updated all chunk metadata")
                
            except Exception as e:
                logger.warning(f"Failed to update chunk metadata: {e}")
                logger.warning("Document created successfully but chunk metadata not applied")
            
            # Debug: Check what chunks were actually created by R2R
            # self.debug_document_chunks(document_id)  # Commented out - debug shows collection-wide results

        self._manifest[key] = {
            "hash": file_hash,
            "document_id": str(document_id),
            "collection_id": collection_id,
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
        self.verify_collections()

        for p in self.iter_files():
            self.upsert_file(p)
        # if cleanup:
        #     self.cleanup_orphans()
        self.save_manifest()

    def upsert_single_file(self, file_path: str) -> Dict[str, str]:
        """
        Upsert a single file for testing purposes.
        Returns document information including document_id.
        """
        file_path_obj = Path(file_path).resolve()
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path_obj.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Check if file extension is supported
        if file_path_obj.suffix.lower() not in self.exts:
            raise ValueError(f"File extension {file_path_obj.suffix} not supported. Supported: {self.exts}")
        
        logger.info(f"Upserting single file: {file_path_obj}")
        self.load_manifest()
        self.verify_collections()
        
        # Store original base_dir 
        original_base_dir = self.base_dir
        
        # Don't change base_dir - keep it as the original docs directory
        # This ensures the relative path matches existing manifest entries
        
        try:
            self.upsert_file(file_path_obj)
            self.save_manifest()
            
            # Calculate relative path from original base_dir for manifest lookup
            try:
                rel_path = file_path_obj.relative_to(self.base_dir)
            except ValueError:
                # Handle cases where file is outside base_dir (e.g., ../docs/temp/file.md)
                # Try to find the correct relative path by looking for 'docs' directory
                file_parts = file_path_obj.parts
                base_parts = self.base_dir.parts
                
                # If both paths contain 'docs', use everything after 'docs' in the file path
                if 'docs' in file_parts:
                    docs_index = file_parts.index('docs')
                    rel_path = Path(*file_parts[docs_index + 1:])
                else:
                    # Last resort: use the filename
                    rel_path = file_path_obj.name
            
            key = str(rel_path).replace("\\", "/")
            doc_info = self._manifest.get(key, {})
            
            result = {
                "file_path": str(file_path_obj),
                "relative_path": key,
                "document_id": doc_info.get("document_id", "unknown"),
                "hash": doc_info.get("hash", "unknown"),
                "status": "success"
            }
            
            logger.info(f"Single file upsert completed: {result}")
            return result
            
        finally:
            # Restore original base_dir
            self.base_dir = original_base_dir

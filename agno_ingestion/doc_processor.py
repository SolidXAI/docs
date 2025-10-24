"""Document processing utilities for markdown files."""

import re
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Regex patterns
FRONTMATTER_RE = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^\s*##\s+(.+?)\s*$", re.MULTILINE)


def sha256_file(path: Path) -> str:
    """
    Calculate SHA256 hash of a file.
    
    Args:
        path: Path to file
        
    Returns:
        Hex digest of file hash
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(text: str) -> Dict:
    """
    Parse YAML frontmatter from markdown text.
    
    Args:
        text: Markdown text with optional frontmatter
        
    Returns:
        Dictionary of frontmatter fields
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    
    yaml_block = match.group(1)
    
    try:
        import yaml
        # Try safe_load first
        try:
            parsed = yaml.safe_load(yaml_block) or {}
            return parsed
        except yaml.YAMLError:
            # If YAML parsing fails, try manual field extraction
            logger.debug("YAML parsing failed, attempting manual field extraction")
            result = {}
            for line in yaml_block.split('\n'):
                line = line.strip()
                if ':' in line and not line.startswith('#'):
                    # Split only on first colon
                    key, _, value = line.partition(':')
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Handle list values (simple comma-separated or bracketed)
                    if value.startswith('[') and value.endswith(']'):
                        # Parse as list
                        value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
                    
                    if key and value:
                        result[key] = value
            
            return result
    except Exception as e:
        logger.warning(f"Frontmatter parsing failed: {e}")
        return {}


def extract_title(text: str, frontmatter: Dict) -> Optional[str]:
    """
    Extract document title from frontmatter or H1 header.
    
    Args:
        text: Markdown text
        frontmatter: Parsed frontmatter dictionary
        
    Returns:
        Document title or None
    """
    # First try frontmatter
    if isinstance(frontmatter.get("title"), str):
        return frontmatter["title"]
    
    # Then try H1
    match = H1_RE.search(text)
    return match.group(1).strip() if match else None


def split_by_h2(text: str) -> List[Dict[str, str]]:
    """
    Split document content by H2 headers, maintaining order.
    
    Args:
        text: Markdown text
        
    Returns:
        List of chunks with section titles and content
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


def build_metadata(
    file_path: Path,
    base_dir: Path,
    file_text: str,
    project: str = "solidx-docs"
) -> Dict:
    """
    Build metadata dictionary for a document.
    
    Args:
        file_path: Path to the file
        base_dir: Base directory for documentation
        file_text: File content text
        project: Project name
        
    Returns:
        Metadata dictionary
    """
    # Calculate relative path
    rel_path = file_path.relative_to(base_dir)
    
    # Parse frontmatter
    frontmatter = parse_frontmatter(file_text)
    
    # Extract section (first directory component)
    section = rel_path.parts[0] if len(rel_path.parts) > 0 else ""
    
    # Use file path as doc_title
    doc_title = str(rel_path).replace("\\", "/")
    
    # Build base metadata
    metadata = {
        "source": "docusaurus",
        "project": project,
        "section": section,
        "path": str(rel_path).replace("\\", "/"),
        "doc_title": doc_title,
    }
    
    # Extract specific frontmatter fields for document metadata
    if "title" in frontmatter and isinstance(frontmatter["title"], str):
        metadata["title"] = frontmatter["title"]
    
    if "description" in frontmatter and isinstance(frontmatter["description"], str):
        metadata["description"] = frontmatter["description"]
    
    if "summary" in frontmatter and isinstance(frontmatter["summary"], str):
        metadata["summary"] = frontmatter["summary"]
    
    if "keywords" in frontmatter:
        # Ensure keywords is a list
        if isinstance(frontmatter["keywords"], list):
            metadata["keywords"] = frontmatter["keywords"]
        elif isinstance(frontmatter["keywords"], str):
            # Handle case where keywords might be a comma-separated string
            metadata["keywords"] = [k.strip() for k in frontmatter["keywords"].split(",")]
    
    if "solidx_concerns" in frontmatter:
        # Ensure solidx_concerns is a list
        if isinstance(frontmatter["solidx_concerns"], list):
            metadata["solidx_concerns"] = frontmatter["solidx_concerns"]
        elif isinstance(frontmatter["solidx_concerns"], str):
            # Handle case where concerns might be a comma-separated string
            metadata["solidx_concerns"] = [c.strip() for c in frontmatter["solidx_concerns"].split(",")]
    
    return metadata


def prepare_chunks_for_upload(
    file_path: Path,
    base_dir: Path,
    file_text: str,
    document_id: str,
    project: str = "solidx-docs"
) -> Tuple[List[Dict], Dict]:
    """
    Prepare chunks and metadata for upload to Agno-RAG.
    
    Args:
        file_path: Path to the file
        base_dir: Base directory for documentation
        file_text: File content text
        document_id: UUID for the document
        project: Project name
        
    Returns:
        Tuple of (chunks_list, parent_metadata)
    """
    # Build base metadata
    base_metadata = build_metadata(file_path, base_dir, file_text, project)
    
    # Split by H2 headers
    chunks_data = split_by_h2(file_text)
    
    # Prepare chunks for upload
    chunks = []
    total_chunks = len(chunks_data)
    
    for idx, chunk_data in enumerate(chunks_data):
        chunk_index = idx
        section_title = chunk_data["section_title"]
        content = chunk_data["content"]
        
        # Validate chunk content
        if not content or not content.strip():
            logger.warning(f"Skipping empty chunk at index {idx} for {file_path}")
            continue
        
        content_str = str(content).strip()
        if len(content_str) < 10:
            logger.warning(f"Skipping too-short chunk at index {idx} for {file_path}")
            continue
        
        # Prepare chunk with metadata
        chunk = {
            "content": content_str,
            "chunk_index": chunk_index,
            "metadata": {
                "section_title": section_title or "Introduction",
            }
        }
        
        chunks.append(chunk)
    
    # Update parent metadata
    parent_metadata = base_metadata.copy()
    parent_metadata["chunk_count"] = len(chunks)
    
    return chunks, parent_metadata


def get_collection_id_for_path(rel_path: Path, collection_mapping: Dict[str, str]) -> Optional[str]:
    """
    Determine which collection a file belongs to based on its relative path.
    
    Args:
        rel_path: Relative path from docs directory
        collection_mapping: Dictionary mapping section names to collection IDs
        
    Returns:
        Collection ID or None if no mapping found
    """
    if len(rel_path.parts) > 0:
        first_dir = rel_path.parts[0]
        collection_id = collection_mapping.get(first_dir)
        if collection_id:
            logger.debug(f"File {rel_path} mapped to collection '{first_dir}' ({collection_id})")
            return collection_id
    
    logger.warning(f"No collection mapping found for file {rel_path}")
    return None


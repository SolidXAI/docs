#!/usr/bin/env python
"""Test metadata extraction from a specific file."""

import sys
from pathlib import Path
from doc_processor import parse_frontmatter, build_metadata, prepare_chunks_for_upload

# Test file
test_file = Path("../docs/developer-docs/extending/backend-customization/dynamic-selection-providers.md")
base_dir = Path("../docs")

print("="*80)
print(f"Testing metadata extraction for: {test_file}")
print("="*80)

# Read file
file_text = test_file.read_text(encoding="utf-8", errors="ignore")

print("\n1. PARSE FRONTMATTER")
print("-"*80)
frontmatter = parse_frontmatter(file_text)
print(f"Frontmatter keys: {list(frontmatter.keys())}")
for key, value in frontmatter.items():
    print(f"  {key}: {value}")

print("\n2. BUILD METADATA")
print("-"*80)
metadata = build_metadata(test_file, base_dir, file_text, "solidx-docs")
print(f"Metadata keys: {list(metadata.keys())}")
for key, value in metadata.items():
    print(f"  {key}: {value}")

print("\n3. PREPARE CHUNKS FOR UPLOAD")
print("-"*80)
chunks, parent_metadata = prepare_chunks_for_upload(
    file_path=test_file,
    base_dir=base_dir,
    file_text=file_text,
    document_id="test-doc-id",
    project="solidx-docs"
)

print(f"Number of chunks: {len(chunks)}")
print(f"\nParent metadata keys: {list(parent_metadata.keys())}")
for key, value in parent_metadata.items():
    if isinstance(value, (list, dict)):
        print(f"  {key}: {value}")
    else:
        print(f"  {key}: {str(value)[:100]}")

print("\n4. CHECK REQUIRED FIELDS")
print("-"*80)
required_fields = ['title', 'summary', 'keywords', 'solidx_concerns', 'description']
all_present = True
for field in required_fields:
    if field in parent_metadata:
        print(f"  ✓ {field}: Present")
    else:
        print(f"  ✗ {field}: MISSING")
        all_present = False

if all_present:
    print("\n✓ All required fields are present in parent metadata!")
else:
    print("\n✗ Some required fields are missing!")
    sys.exit(1)

print("="*80)


#!/usr/bin/env python3
"""
Generate SHA-256 checksums for all corpus files.

Generates three checksum files:
- extracted_text.sha256: ALL_TEXT.txt files
- chunks.sha256: chunks-*.jsonl files
- corpus_files.sha256: corpus/*.json files
"""

import hashlib
import os
from pathlib import Path

# Corpus root
CORPUS_ROOT = Path(__file__).parent.parent.parent


def sha256_file(filepath: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def generate_checksums():
    """Generate all checksum files."""
    checksums_dir = CORPUS_ROOT / "reproducibility" / "checksums"
    checksums_dir.mkdir(parents=True, exist_ok=True)

    # 1. Extracted text (ALL_TEXT.txt files)
    print("Generating extracted_text.sha256...")
    extracted_checksums = []
    docs_dir = CORPUS_ROOT / "documents"

    for doc_folder in sorted(docs_dir.iterdir()):
        if not doc_folder.is_dir():
            continue
        all_text = doc_folder / "dataset" / "ALL_TEXT.txt"
        if all_text.exists():
            rel_path = all_text.relative_to(CORPUS_ROOT)
            checksum = sha256_file(all_text)
            extracted_checksums.append(f"{checksum}  {rel_path}")

    with open(checksums_dir / "extracted_text.sha256", 'w') as f:
        f.write('\n'.join(extracted_checksums) + '\n')
    print(f"  {len(extracted_checksums)} files")

    # 2. Chunks (chunks-*.jsonl files)
    print("Generating chunks.sha256...")
    chunk_checksums = []

    for doc_folder in sorted(docs_dir.iterdir()):
        if not doc_folder.is_dir():
            continue
        dataset_dir = doc_folder / "dataset"
        if dataset_dir.exists():
            for chunk_file in sorted(dataset_dir.glob("chunks-*.jsonl")):
                rel_path = chunk_file.relative_to(CORPUS_ROOT)
                checksum = sha256_file(chunk_file)
                chunk_checksums.append(f"{checksum}  {rel_path}")

    with open(checksums_dir / "chunks.sha256", 'w') as f:
        f.write('\n'.join(chunk_checksums) + '\n')
    print(f"  {len(chunk_checksums)} files")

    # 3. Corpus JSON files
    print("Generating corpus_files.sha256...")
    corpus_checksums = []
    corpus_dir = CORPUS_ROOT / "corpus"

    if corpus_dir.exists():
        for json_file in sorted(corpus_dir.glob("**/*.json")):
            rel_path = json_file.relative_to(CORPUS_ROOT)
            checksum = sha256_file(json_file)
            corpus_checksums.append(f"{checksum}  {rel_path}")

    # Also include root-level corpus files
    for root_file in ["training_intent.json", "metadata.yaml"]:
        filepath = CORPUS_ROOT / root_file
        if filepath.exists():
            checksum = sha256_file(filepath)
            corpus_checksums.append(f"{checksum}  {root_file}")

    with open(checksums_dir / "corpus_files.sha256", 'w') as f:
        f.write('\n'.join(corpus_checksums) + '\n')
    print(f"  {len(corpus_checksums)} files")

    print("\nChecksum generation complete!")
    print(f"Total: {len(extracted_checksums) + len(chunk_checksums) + len(corpus_checksums)} files")


if __name__ == "__main__":
    generate_checksums()

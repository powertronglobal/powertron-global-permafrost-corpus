#!/usr/bin/env python3
"""
Regenerate Chunks Script
Rebuilds chunks-*.jsonl files from ALL_TEXT.txt after text modifications.

Usage:
    python regenerate_chunks.py --dry-run  # Preview changes
    python regenerate_chunks.py            # Apply changes
"""

import json
import os
import re
import hashlib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import tiktoken
except ImportError:
    print("Error: tiktoken not installed. Run: pip install tiktoken")
    exit(1)

# Corpus root
CORPUS_ROOT = Path(__file__).parent.parent

# Chunking parameters (from CLAUDE.md)
TARGET_TOKENS = 800
MIN_TOKENS = 400
MAX_TOKENS = 1200
OVERLAP_TOKENS = 50

# Initialize tokenizer
TOKENIZER = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count tokens using cl100k_base tokenizer."""
    return len(TOKENIZER.encode(text))


def parse_all_text(content: str) -> List[Tuple[int, str]]:
    """Parse ALL_TEXT.txt into (page_num, text) tuples."""
    # Split by page markers
    page_pattern = re.compile(r'═══ PAGE (\d+) ═══\n')

    pages = []
    parts = page_pattern.split(content)

    # parts will be: [before_first_marker, page1, text1, page2, text2, ...]
    if len(parts) < 2:
        # No page markers, treat as single page
        return [(1, content)]

    i = 1  # Skip content before first marker
    while i < len(parts) - 1:
        page_num = int(parts[i])
        text = parts[i + 1]
        pages.append((page_num, text))
        i += 2

    return pages


def find_split_point(text: str, target_pos: int, direction: str = "backward") -> int:
    """Find a good split point near target_pos (paragraph > sentence > word)."""
    if direction == "backward":
        # Look for paragraph break
        para_pos = text.rfind('\n\n', 0, target_pos)
        if para_pos > target_pos * 0.5:  # Don't go too far back
            return para_pos + 2

        # Look for sentence break
        for sep in ['. ', '.\n', '? ', '?\n', '! ', '!\n']:
            sent_pos = text.rfind(sep, 0, target_pos)
            if sent_pos > target_pos * 0.7:
                return sent_pos + len(sep)

        # Look for word break
        space_pos = text.rfind(' ', 0, target_pos)
        if space_pos > 0:
            return space_pos + 1

        return target_pos
    else:
        # Look forward for paragraph break
        para_pos = text.find('\n\n', target_pos)
        if para_pos > 0 and para_pos < target_pos * 1.5:
            return para_pos + 2

        # Look for sentence break
        for sep in ['. ', '.\n', '? ', '?\n', '! ', '!\n']:
            sent_pos = text.find(sep, target_pos)
            if sent_pos > 0 and sent_pos < len(text) * 0.9:
                return sent_pos + len(sep)

        return target_pos


def chunk_text(pages: List[Tuple[int, str]], doc_id: str, slug: str) -> List[Dict]:
    """Chunk text into Major US Retailer-sized pieces with overlap."""
    # Combine all text with page tracking
    full_text = ""
    page_boundaries = []  # (char_pos, page_num)

    for page_num, text in pages:
        page_boundaries.append((len(full_text), page_num))
        full_text += text

    if not full_text.strip():
        return []

    chunks = []
    pos = 0
    sequence = 1

    while pos < len(full_text):
        # Find end position for this chunk
        remaining = full_text[pos:]
        tokens = count_tokens(remaining)

        if tokens <= MAX_TOKENS:
            # Last chunk
            chunk_text = remaining.strip()
            if chunk_text:
                chunk_tokens = count_tokens(chunk_text)
                if chunk_tokens >= MIN_TOKENS or sequence == 1:
                    start_page = get_page_at_pos(pos, page_boundaries)
                    end_page = get_page_at_pos(len(full_text) - 1, page_boundaries)
                    chunks.append(create_chunk(
                        doc_id, slug, sequence, chunk_text,
                        chunk_tokens, start_page, end_page
                    ))
            break

        # Find approximate character position for TARGET_TOKENS
        # Estimate: ~4 chars per token on average
        estimated_chars = TARGET_TOKENS * 4
        if estimated_chars > len(remaining):
            estimated_chars = len(remaining)

        # Refine by actually counting tokens
        test_text = remaining[:estimated_chars]
        test_tokens = count_tokens(test_text)

        # Adjust to get closer to Major US Retailer
        while test_tokens < TARGET_TOKENS and estimated_chars < len(remaining):
            estimated_chars += 100
            test_text = remaining[:min(estimated_chars, len(remaining))]
            test_tokens = count_tokens(test_text)

        while test_tokens > MAX_TOKENS and estimated_chars > 100:
            estimated_chars -= 100
            test_text = remaining[:estimated_chars]
            test_tokens = count_tokens(test_text)

        # Find natural break point
        split_pos = find_split_point(remaining, estimated_chars)
        chunk_text = remaining[:split_pos].strip()

        if not chunk_text:
            pos += 100  # Skip forward if empty
            continue

        chunk_tokens = count_tokens(chunk_text)

        # If chunk is too small, extend
        if chunk_tokens < MIN_TOKENS and split_pos < len(remaining):
            extended_pos = find_split_point(remaining, estimated_chars, "forward")
            chunk_text = remaining[:extended_pos].strip()
            chunk_tokens = count_tokens(chunk_text)

        start_page = get_page_at_pos(pos, page_boundaries)
        end_page = get_page_at_pos(pos + len(chunk_text) - 1, page_boundaries)

        chunks.append(create_chunk(
            doc_id, slug, sequence, chunk_text,
            chunk_tokens, start_page, end_page
        ))

        sequence += 1

        # Move position with overlap
        overlap_chars = max(100, len(chunk_text) - int(len(chunk_text) * 0.9))
        pos += len(chunk_text) - overlap_chars

        if pos <= 0:
            pos = len(chunk_text)

    # Link chunks
    for i, chunk in enumerate(chunks):
        if i > 0:
            chunk["prev_id"] = chunks[i - 1]["chunk_id"]
        if i < len(chunks) - 1:
            chunk["next_id"] = chunks[i + 1]["chunk_id"]

    return chunks


def get_page_at_pos(char_pos: int, page_boundaries: List[Tuple[int, int]]) -> int:
    """Get page number for a character position."""
    page = 1
    for boundary_pos, page_num in page_boundaries:
        if char_pos >= boundary_pos:
            page = page_num
        else:
            break
    return page


def create_chunk(doc_id: str, slug: str, sequence: int, text: str,
                 tokens: int, start_page: int, end_page: int) -> Dict:
    """Create a chunk dictionary."""
    chunk_id = f"{doc_id}_chunk_{sequence:04d}"
    content_hash = "sha256:" + hashlib.sha256(text.encode()).hexdigest()

    return {
        "chunk_id": chunk_id,
        "doc_id": doc_id,
        "slug": slug,
        "sequence": sequence,
        "text": text,
        "tokens": tokens,
        "chars": len(text),
        "pages": {"start": start_page, "end": end_page},
        "section": None,
        "prev_id": None,
        "next_id": None,
        "content_hash": content_hash
    }


def get_doc_id(slug: str, docs_dir: Path) -> str:
    """Get doc_id from metadata.json or generate from slug."""
    metadata_path = docs_dir / slug / "metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                return metadata.get("doc_id", slug)
        except:
            pass
    return slug


def process_document(doc_folder: Path, dry_run: bool) -> Dict:
    """Process a single document folder."""
    stats = {"chunks": 0, "tokens": 0, "modified": False}

    all_text_path = doc_folder / "dataset" / "ALL_TEXT.txt"
    if not all_text_path.exists():
        return stats

    slug = doc_folder.name
    doc_id = get_doc_id(slug, doc_folder.parent)

    # Read ALL_TEXT.txt
    with open(all_text_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse and chunk
    pages = parse_all_text(content)
    chunks = chunk_text(pages, doc_id, slug)

    if not chunks:
        return stats

    stats["chunks"] = len(chunks)
    stats["tokens"] = sum(c["tokens"] for c in chunks)

    # Write chunks file
    chunks_path = doc_folder / "dataset" / "chunks-0000.jsonl"

    if not dry_run:
        with open(chunks_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        stats["modified"] = True
    else:
        # Check if would be different
        if chunks_path.exists():
            with open(chunks_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
            new_content = '\n'.join(json.dumps(c, ensure_ascii=False) for c in chunks) + '\n'
            if old_content != new_content:
                stats["modified"] = True
        else:
            stats["modified"] = True

    return stats


def main():
    parser = argparse.ArgumentParser(description="Regenerate chunk files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    args = parser.parse_args()

    docs_dir = CORPUS_ROOT / "documents"

    print("=" * 60)
    print("Chunk Regeneration Script")
    print("=" * 60)

    if args.dry_run:
        print("\n*** DRY RUN - No changes will be made ***\n")

    total_stats = {"docs": 0, "chunks": 0, "tokens": 0, "modified": 0}

    for doc_folder in sorted(docs_dir.iterdir()):
        if not doc_folder.is_dir():
            continue

        stats = process_document(doc_folder, args.dry_run)

        if stats["chunks"] > 0:
            total_stats["docs"] += 1
            total_stats["chunks"] += stats["chunks"]
            total_stats["tokens"] += stats["tokens"]
            if stats["modified"]:
                total_stats["modified"] += 1
                print(f"  {'Would modify' if args.dry_run else 'Modified'}: {doc_folder.name} ({stats['chunks']} chunks)")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Documents processed: {total_stats['docs']}")
    print(f"Total chunks: {total_stats['chunks']}")
    print(f"Total tokens: {total_stats['tokens']:,}")
    print(f"Files {'to modify' if args.dry_run else 'modified'}: {total_stats['modified']}")

    if args.dry_run:
        print("\n*** DRY RUN COMPLETE - Run without --dry-run to apply changes ***")
    else:
        print("\n*** CHUNK REGENERATION COMPLETE ***")


if __name__ == "__main__":
    main()

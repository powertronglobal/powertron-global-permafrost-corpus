#!/usr/bin/env python3
"""
Verify corpus file integrity against published checksums.

Usage:
    python verify_checksums.py [--verbose]
"""

import argparse
import hashlib
import sys
from pathlib import Path


def sha256_file(filepath: Path) -> str:
    """Calculate SHA-256 of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_checksums(checksum_file: Path) -> dict:
    """Load checksum file into dict of {path: expected_hash}."""
    checksums = {}
    with open(checksum_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("  ", 1)
                if len(parts) == 2:
                    checksums[parts[1]] = parts[0]
    return checksums


def verify_checksums(checksum_file: Path, base_path: Path, verbose: bool = False) -> tuple:
    """
    Verify files against checksums.

    Returns: (passed, failed, missing) counts
    """
    expected = load_checksums(checksum_file)
    passed = 0
    failed = 0
    missing = 0

    for rel_path, expected_hash in expected.items():
        file_path = base_path / rel_path

        if not file_path.exists():
            if verbose:
                print(f"MISSING: {rel_path}")
            missing += 1
            continue

        actual_hash = sha256_file(file_path)

        if actual_hash == expected_hash:
            if verbose:
                print(f"OK: {rel_path}")
            passed += 1
        else:
            print(f"MISMATCH: {rel_path}")
            print(f"  Expected: {expected_hash}")
            print(f"  Actual:   {actual_hash}")
            failed += 1

    return passed, failed, missing


def main():
    parser = argparse.ArgumentParser(description="Verify corpus checksums")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all file statuses")
    args = parser.parse_args()

    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    checksums_dir = script_dir.parent / "checksums"

    print("=" * 60)
    print("Powertron Corpus Checksum Verification")
    print("=" * 60)
    print()

    total_passed = 0
    total_failed = 0
    total_missing = 0

    # Verify each checksum file
    for checksum_file in sorted(checksums_dir.glob("*.sha256")):
        print(f"Verifying {checksum_file.name}...")
        passed, failed, missing = verify_checksums(checksum_file, repo_root, args.verbose)
        total_passed += passed
        total_failed += failed
        total_missing += missing
        print(f"  Passed: {passed}, Failed: {failed}, Missing: {missing}")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files verified: {total_passed + total_failed + total_missing}")
    print(f"  Passed:  {total_passed}")
    print(f"  Failed:  {total_failed}")
    print(f"  Missing: {total_missing}")
    print()

    if total_failed == 0 and total_missing == 0:
        print("SUCCESS: All checksums verified!")
        return 0
    else:
        print("FAILURE: Checksum verification failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

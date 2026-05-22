#!/usr/bin/env python3
"""
Remove trailing (...) suffixes from PDF filenames.

Usage:
    python clean_pdf_names.py                     # dry run (preview only)
    python clean_pdf_names.py --apply             # rename files
    python clean_pdf_names.py --dir /path/to/dir  # target a specific folder
"""

import re
import sys
import argparse
from pathlib import Path


def clean_name(name: str) -> str:
    """Strip one or more trailing (...) groups from a filename stem."""
    # Repeatedly remove trailing whitespace + (...) until nothing changes
    pattern = re.compile(r'\s*\([^)]*\)\s*$')
    while True:
        new_name = pattern.sub('', name)
        if new_name == name:
            break
        name = new_name
    return name.strip()


def main():
    parser = argparse.ArgumentParser(description="Clean trailing (...) from PDF filenames.")
    parser.add_argument('--apply', action='store_true', help='Actually rename files (default is dry run)')
    parser.add_argument('--dir', default='.', help='Directory to scan (default: current directory)')
    parser.add_argument('--ext', default='.pdf', help='File extension to target (default: .pdf)')
    args = parser.parse_args()

    folder = Path(args.dir)
    files = sorted(folder.glob(f'*{args.ext}'))

    if not files:
        print(f"No {args.ext} files found in: {folder.resolve()}")
        return

    renames = []
    for f in files:
        new_stem = clean_name(f.stem)
        new_name = new_stem + f.suffix
        if new_name != f.name:
            renames.append((f, f.with_name(new_name)))

    if not renames:
        print("Nothing to rename — all filenames already clean.")
        return

    mode = "APPLYING" if args.apply else "DRY RUN (use --apply to rename)"
    print(f"\n{'='*60}")
    print(f"  {mode}")
    print(f"{'='*60}\n")

    for old, new in renames:
        print(f"  BEFORE: {old.name}")
        print(f"  AFTER:  {new.name}")
        print()
        if args.apply:
            old.rename(new)

    if not args.apply:
        print(f"  {len(renames)} file(s) would be renamed. Run with --apply to confirm.")
    else:
        print(f"  {len(renames)} file(s) renamed.")


if __name__ == '__main__':
    main()
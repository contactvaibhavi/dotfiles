#!/usr/bin/env python3
"""
Clean extraneous tags from PDF (or other) filenames.

Usage:
    clean_pdf_names.py                        # dry run, current dir
    clean_pdf_names.py --apply                # rename files
    clean_pdf_names.py --dir /path/to/dir     # target a specific folder
    clean_pdf_names.py --ext .epub            # different extension
"""

import re
import argparse
from pathlib import Path

# ── Patterns ────────────────────────────────────────────────────────────────
LIBGEN = re.compile(r"\s*-\s*(libgen\.[a-z]+)?\s*$", re.IGNORECASE)
ZLIB = re.compile(r"\s*\([^)]*(z-lib|1lib|z-library)[^)]*\)", re.IGNORECASE)
BRACKETS = re.compile(r"\s*\[.*?\]")
QUOTES = re.compile(r"^'|'$|^\?|\?$")
YEAR = re.compile(r"\(\s*(\d{4})\s*(?:,[^)]*)?\)")
PARENS = re.compile(r"\s*\([^)]*\)\s*$")  # trailing (...) fallback


def clean_name(stem: str) -> str:
    stem = ZLIB.sub("", stem)
    stem = BRACKETS.sub("", stem)
    stem = QUOTES.sub("", stem).strip()
    stem = YEAR.sub(r"(\1)", stem)
    stem = LIBGEN.sub("", stem)  # after YEAR so $ anchor works

    # Strip any remaining trailing (...)
    while True:
        new = PARENS.sub("", stem)
        if new == stem:
            break
        stem = new

    # "Author_Name - Title" → "Author Name - Title"
    if " - " in stem:
        parts = stem.split(" - ", 1)
        parts[0] = parts[0].replace("_", "; ")
        stem = " - ".join(parts)

    return stem.strip()


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Clean extraneous tags from filenames."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files (default is dry run)",
    )
    parser.add_argument(
        "--dir", default=".", help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "--ext", default=".pdf", help="File extension to target (default: .pdf)"
    )
    args = parser.parse_args()

    folder = Path(args.dir)
    files = sorted(folder.glob(f"*{args.ext}"))

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
    print(f"\n{'=' * 60}\n  {mode}\n{'=' * 60}\n")

    for old, new in renames:
        print(f"  BEFORE: {old.name}")
        print(f"  AFTER:  {new.name}\n")
        if args.apply:
            old.rename(new)

    summary = f"{len(renames)} file(s)"
    print(
        f"  {summary} {'renamed.' if args.apply else 'would be renamed. Run with --apply to confirm.'}"
    )


if __name__ == "__main__":
    main()


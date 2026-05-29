#!/usr/bin/env python3
"""
merge_pdfs_from_url.py
----------------------
Scrapes all PDF links from a given webpage and merges them into a single PDF.

Usage:
    python merge_pdfs_from_url.py <url> [options]

Examples:
    python merge_pdfs_from_url.py https://example.com/docs.html
    python merge_pdfs_from_url.py https://example.com/docs.html -o my_merged.pdf
    python merge_pdfs_from_url.py https://example.com/docs.html -o out.pdf --no-cleanup
    python merge_pdfs_from_url.py https://example.com/docs.html --list-only

Requirements:
    pip install pypdf requests beautifulsoup4
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse


def install_requirements():
    """Install dependencies from requirements.txt if present, else fall back to known packages."""
    req_file = Path(__file__).parent / "requirements.txt"
    if req_file.exists():
        print(f"Installing dependencies from {req_file} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", str(req_file)])
    else:
        print("requirements.txt not found — installing packages directly ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                                "pypdf>=4.0.0", "requests>=2.31.0", "beautifulsoup4>=4.12.0"])


try:
    import requests
    from bs4 import BeautifulSoup
    from pypdf import PdfWriter
except ImportError:
    install_requirements()
    import requests
    from bs4 import BeautifulSoup
    from pypdf import PdfWriter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_pdf_links(page_url: str, session: requests.Session) -> list[dict]:
    """Fetch the page and return all PDF links as [{"text": ..., "url": ...}]."""
    print(f"Fetching page: {page_url}")
    resp = session.get(page_url, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    links = []

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        # Resolve relative URLs
        full_url = urljoin(page_url, href)
        if full_url.lower().split("?")[0].endswith(".pdf"):
            link_text = tag.get_text(strip=True) or Path(urlparse(full_url).path).name
            links.append({"text": link_text, "url": full_url})

    return links


def safe_filename(url: str) -> str:
    """Derive a safe local filename from a URL."""
    name = Path(urlparse(url).path).name
    # Replace problematic characters
    for ch in r'\/:*?"<>|':
        name = name.replace(ch, "_")
    return name or "download.pdf"


def download_pdf(url: str, dest: Path, session: requests.Session,
                 retries: int = 3, delay: float = 1.0) -> bool:
    """Download a single PDF to dest. Returns True on success."""
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=60, stream=True)
            resp.raise_for_status()
            content_type = resp.headers.get("Content-Type", "")
            # Warn but still save if content-type looks wrong
            if "pdf" not in content_type.lower() and attempt == 1:
                print(f"    ⚠ Unexpected Content-Type: {content_type}")
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            # Sanity-check: real PDFs start with %PDF
            with open(dest, "rb") as f:
                header = f.read(5)
            if header[:4] != b"%PDF":
                print(f"    ✗ Not a valid PDF (header: {header!r})")
                dest.unlink(missing_ok=True)
                return False
            return True
        except requests.RequestException as e:
            print(f"    Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    return False


def merge_pdfs(pdf_paths: list[Path], output: Path) -> int:
    """Merge pdfs in order into output. Returns total page count."""
    writer = PdfWriter()
    total_pages = 0
    for path in pdf_paths:
        try:
            writer.append(str(path))
            from pypdf import PdfReader
            total_pages += len(PdfReader(str(path)).pages)
        except Exception as e:
            print(f"  ⚠ Skipping {path.name}: {e}")
    with open(output, "wb") as f:
        writer.write(f)
    return total_pages


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download all PDFs linked on a webpage and merge into one file."
    )
    parser.add_argument("url", help="URL of the webpage containing PDF links")
    parser.add_argument(
        "-o", "--output",
        default="merged.pdf",
        help="Output filename (default: merged.pdf)",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Just list found PDF links, don't download",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Keep individually downloaded PDFs after merging",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Seconds to wait between downloads (default: 0.5)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Download retry attempts per file (default: 3)",
    )
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (compatible; pdf-merger-script/1.0)",
        help="User-Agent header for requests",
    )
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})

    # --- Discover links ---
    try:
        links = get_pdf_links(args.url, session)
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        sys.exit(1)

    if not links:
        print("No PDF links found on that page.")
        sys.exit(0)

    print(f"\nFound {len(links)} PDF link(s):")
    for i, link in enumerate(links, 1):
        print(f"  {i:3}. {link['text']}")
        print(f"       {link['url']}")

    if args.list_only:
        sys.exit(0)

    # --- Download ---
    print(f"\nDownloading to temporary folder...")
    tmp_dir = Path(tempfile.mkdtemp(prefix="pdf_merge_"))
    downloaded: list[Path] = []
    failed: list[str] = []

    for i, link in enumerate(links, 1):
        filename = f"{i:03}_{safe_filename(link['url'])}"
        dest = tmp_dir / filename
        print(f"  [{i}/{len(links)}] {link['text']} ...", end=" ", flush=True)
        success = download_pdf(link["url"], dest, session,
                               retries=args.retries, delay=args.delay)
        if success:
            size_kb = dest.stat().st_size / 1024
            print(f"✓  ({size_kb:.0f} KB)")
            downloaded.append(dest)
        else:
            print("✗  FAILED")
            failed.append(link["url"])
        if i < len(links):
            time.sleep(args.delay)

    print(f"\nDownloaded: {len(downloaded)}/{len(links)}", end="")
    if failed:
        print(f"  |  Failed: {len(failed)}")
        for url in failed:
            print(f"    - {url}")
    else:
        print()

    if not downloaded:
        print("Nothing to merge.")
        sys.exit(1)

    # --- Merge ---
    output_path = Path(args.output)
    print(f"\nMerging {len(downloaded)} PDFs → {output_path} ...")
    total_pages = merge_pdfs(downloaded, output_path)
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ Done!  {total_pages} pages  |  {size_mb:.1f} MB  →  {output_path}")

    # --- Cleanup ---
    if not args.no_cleanup:
        for f in downloaded:
            f.unlink(missing_ok=True)
        tmp_dir.rmdir()
    else:
        print(f"  Individual PDFs kept in: {tmp_dir}")


if __name__ == "__main__":
    main()
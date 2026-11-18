#!/usr/bin/env python3
"""Export mdBook HTML to a single PDF using Playwright (optional)."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / "exports"
BOOK_INDEX = ROOT / "book" / "index.html"


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install: pip install playwright && playwright install chromium")
        sys.exit(1)

    if not BOOK_INDEX.exists():
        print("Run 'mdbook build' first (or build HTML manually).")
        print("Generating content and attempting mdbook build...")
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_curriculum.py")], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_book.py")], check=True)
        r = subprocess.run(["mdbook", "build"], cwd=ROOT)
        if r.returncode != 0:
            print("mdbook not found. Install mdBook, run 'mdbook build', then re-run this script.")
            sys.exit(1)

    EXPORT.mkdir(exist_ok=True)
    out = EXPORT / "msc-chemistry-guide.pdf"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BOOK_INDEX.as_uri())
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
        )
        browser.close()

    print(f"PDF written to {out}")


if __name__ == "__main__":
    main()

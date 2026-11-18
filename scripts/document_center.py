"""Build Document Centre page and copy files into the published site."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "documents.json"
DOCS = ROOT / "documents"
BOOK = ROOT / "book"


def load_documents_config() -> dict:
    if not CONFIG.exists():
        return {"pageTitle": "Document Centre", "intro": "", "categories": []}
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def copy_document_files(base: str) -> list[str]:
    """Copy documents/ tree to book/documents/. Returns warnings for missing files."""
    warnings: list[str] = []
    out_root = BOOK / "documents"
    if out_root.exists():
        shutil.rmtree(out_root)
    if DOCS.exists():
        shutil.copytree(
            DOCS,
            out_root,
            ignore=shutil.ignore_patterns("README.md", ".gitkeep"),
        )
    return warnings


def _doc_row(doc: dict, base: str) -> tuple[str, bool]:
    rel = doc.get("file", "").replace("\\", "/")
    title = html.escape(doc.get("title", "Untitled"))
    desc = html.escape(doc.get("description", ""))
    updated = html.escape(doc.get("updated", ""))
    path = ROOT / rel
    exists = path.is_file()
    if not exists:
        href = "#"
        badge = ' <span class="doc-missing">(file missing — add to repo)</span>'
    else:
        # Published at /documents/... relative to uploaded copy
        pub = rel.split("documents/", 1)[-1] if "documents/" in rel else Path(rel).name
        href = f"{base}documents/{pub}"
        badge = ""
    meta = f"Updated {updated}" if updated else ""
    return (
        f'<article class="doc-card" data-title="{title.lower()}">'
        f'<h3><a href="{href}" target="_blank" rel="noopener">{title}</a>{badge}</h3>'
        f"<p>{desc}</p>"
        f'<p class="doc-meta">{meta} · <a href="{href}" download>Download</a></p>'
        f"</article>",
        exists,
    )


def documents_body(b: dict, base: str) -> str:
    cfg = load_documents_config()
    title = html.escape(cfg.get("pageTitle", "Document Centre"))
    intro = html.escape(cfg.get("intro", ""))
    sections = []
    total = 0
    for cat in cfg.get("categories", []):
        cid = html.escape(cat.get("id", ""))
        cname = html.escape(cat.get("name", "Documents"))
        docs = cat.get("documents") or []
        cards = []
        for doc in docs:
            card, _ = _doc_row(doc, base)
            cards.append(card)
            total += 1
        if not cards:
            cards.append('<p class="doc-empty">No documents in this category yet.</p>')
        sections.append(
            f'<section class="doc-category" id="{cid}">'
            f"<h2>{cname}</h2>"
            f'<div class="doc-list">{"".join(cards)}</div></section>'
        )

    admin = f"""
<p class="doc-admin"><strong>Centre admin:</strong> Upload files at <a href="{base}admin/index.html">Admin uploads panel</a>
(static files can still be added via <code>documents/</code> + <code>config/documents.json</code>).</p>"""

    scripts = f"""
<script src="{base}site-services.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="{base}assets/documents-loader.js"></script>
<script>
(function() {{
  var input = document.getElementById("doc-search");
  if (!input) return;
  input.addEventListener("input", function() {{
    var q = input.value.trim().toLowerCase();
    document.querySelectorAll(".doc-card").forEach(function(card) {{
      var t = card.getAttribute("data-title") || "";
      card.style.display = !q || t.indexOf(q) !== -1 ? "" : "none";
    }});
  }});
}})();
</script>"""

    return f"""
<h1>{title}</h1>
<p class="doc-intro">{intro}</p>
<p><strong id="doc-count" data-static="{total}">{total}</strong> document(s) listed below (includes admin uploads when connected).</p>
<label class="doc-search-label" for="doc-search">Search documents</label>
<input type="search" id="doc-search" class="doc-search" placeholder="Type to filter by title…" />
<h2>Latest uploads</h2>
<div id="doc-dynamic"><p class="doc-empty">Loading uploads…</p></div>
<h2>Centre library (static)</h2>
<div id="doc-categories">{"".join(sections)}</div>
{admin}
{scripts}
"""


def validate_manifest() -> list[str]:
    """Return list of missing file paths from manifest."""
    cfg = load_documents_config()
    missing = []
    for cat in cfg.get("categories", []):
        for doc in cat.get("documents") or []:
            rel = doc.get("file", "")
            if rel and not (ROOT / rel).is_file():
                missing.append(rel)
    return missing
#!/usr/bin/env python3
"""Build standalone HTML book from markdown (no mdBook required)."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "book"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from branding import load_branding
from coaching_site import about_body, contact_body, courses_body, landing_body, my_courses_body, top_subjects
from document_center import copy_document_files, documents_body, validate_manifest
from publish_assets import publish_admin_and_services

BRANDING = load_branding()
BASE = BRANDING["base"]
SITE = BRANDING["siteName"]
SHORT = BRANDING.get("shortName", SITE)


def md_to_html(text: str) -> str:
    try:
        import markdown
        return markdown.markdown(
            text,
            extensions=["tables", "fenced_code", "toc", "nl2br"],
        )
    except ImportError:
        # Minimal fallback
        t = html.escape(text)
        t = re.sub(r"^# (.+)$", r"<h1>\1</h1>", t, flags=re.M)
        t = re.sub(r"^## (.+)$", r"<h2>\1</h2>", t, flags=re.M)
        t = re.sub(r"^### (.+)$", r"<h3>\1</h3>", t, flags=re.M)
        t = re.sub(r"^> \*\*(.+?)\*\*: (.+)$", r"<blockquote><strong>\1</strong> \2</blockquote>", t, flags=re.M)
        t = re.sub(r"```(\w*)\n(.*?)```", r"<pre><code>\2</code></pre>", t, flags=re.DOTALL)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
        t = re.sub(r"\n\n", "<br><br>", t)
        return t


def parse_summary() -> list[tuple[str, str, str]]:
    """Return list of (title, rel_path, level)."""
    items = []
    for line in (SRC / "SUMMARY.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"(\s*)- \[([^\]]+)\]\(([^)]+)\)", line)
        if not m:
            continue
        indent, title, href = m.groups()
        if href.startswith("http") or href == "#":
            continue
        rel = href.lstrip("./")
        level = len(indent) // 2
        items.append((title, rel, level))
    return items


def page_href(rel_md: str) -> str:
    """Site-root-relative URL (works for local server and GitHub Pages)."""
    path = Path(rel_md).with_suffix(".html").as_posix()
    return f"{BASE}{path}" if BASE != "/" else f"/{path}"


def site_header(active: str = "") -> str:
  links = [
      ("Home", f"{BASE}index.html", "home"),
      ("Courses", f"{BASE}courses.html", "courses"),
      ("Documents", f"{BASE}documents.html", "documents"),
      ("My courses", f"{BASE}my-courses.html", "mycourses"),
      ("Study", f"{BASE}introduction.html", "study"),
      ("About", f"{BASE}about.html", "about"),
      ("Contact", f"{BASE}contact.html", "contact"),
  ]
  nav = []
  for label, href, key in links:
      cls = ' class="active"' if active == key else ""
      nav.append(f'<a href="{href}"{cls}>{label}</a>')
  return (
      f'<header class="site-header">'
      f'<a class="logo" href="{BASE}index.html">{html.escape(SHORT)}</a>'
      f'<nav class="site-nav">{"".join(nav)}</nav>'
      f'<a class="header-cta" href="{BASE}introduction.html">Enroll / Study</a>'
      f"</header>"
  )


def shell(
    title: str,
    body: str,
    *,
    sidebar_nav: str = "",
    pager: str = "",
    active_header: str = "",
    full_width: bool = False,
) -> str:
    layout_cls = "layout-full" if full_width else "layout-study"
    sidebar = ""
    if sidebar_nav:
        sidebar = f"""
<aside id="sidebar">
<p class="sidebar-brand">{html.escape(SITE)}</p>
<p class="tagline">{html.escape(BRANDING.get("tagline", ""))}</p>
<nav>{sidebar_nav}</nav>
<p class="download-tip"><strong>Save as PDF:</strong> Ctrl+P → Save as PDF</p>
</aside>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)} — {html.escape(SITE)}</title>
<link rel="stylesheet" href="{BASE}style.css"/>
<meta name="description" content="{html.escape(BRANDING.get('tagline', ''))}"/>
</head>
<body class="{layout_cls}">
{site_header(active_header)}
{sidebar}
<main id="content">{pager}{body}{pager}</main>
<footer class="site-footer">
<p>&copy; {html.escape(SITE)} · <a href="{BASE}courses.html">Courses</a> · <a href="{BASE}documents.html">Documents</a> · <a href="{BASE}admin/index.html">Admin</a> · <a href="{BASE}contact.html">Contact</a></p>
</footer>
</body>
</html>"""


def build_pager(
    index: int,
    pages: list[tuple[str, str]],
    *,
    prev_href: str | None = None,
    prev_title: str | None = None,
    next_href: str | None = None,
    next_title: str | None = None,
) -> str:
    """Build Previous / Home / Next navigation bar."""
    if prev_href is None and index > 0:
        prev_title, prev_rel = pages[index - 1]
        prev_href = page_href(prev_rel)
    if next_href is None and index >= 0 and index < len(pages) - 1:
        next_title, next_rel = pages[index + 1]
        next_href = page_href(next_rel)

    if prev_href:
        prev = (
            f'<a class="pager-btn pager-prev" href="{prev_href}">'
            f'<span class="pager-label">Previous</span>'
            f'<span class="pager-title">{html.escape(prev_title or "")}</span></a>'
        )
    else:
        prev = '<span class="pager-btn pager-prev pager-disabled"><span class="pager-label">Previous</span></span>'

    home = f'<a class="pager-btn pager-home" href="{BASE}index.html">Home</a>'

    if next_href:
        nxt = (
            f'<a class="pager-btn pager-next" href="{next_href}">'
            f'<span class="pager-label">Next</span>'
            f'<span class="pager-title">{html.escape(next_title or "")}</span></a>'
        )
    else:
        nxt = '<span class="pager-btn pager-next pager-disabled"><span class="pager-label">Next</span></span>'

    return f'<nav class="chapter-pager" aria-label="Chapter navigation">{prev}{home}{nxt}</nav>'


def readable_pages(items: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    """Ordered list of (title, rel_md) for pages that exist on disk."""
    pages: list[tuple[str, str]] = []
    for title, rel, _ in items:
        if (SRC / rel).exists():
            pages.append((title, rel))
    return pages


def build_nav(items: list[tuple[str, str, str]], current: str) -> str:
    parts = ['<ul>']
    for title, rel, level in items:
        cls = "active" if rel == current else ""
        pad = max(0, level - 1) * 12
        parts.append(
            f'<li style="padding-left:{pad}px" class="{cls}">'
            f'<a href="{page_href(rel)}">{html.escape(title)}</a></li>'
        )
    parts.append("</ul>")
    return "\n".join(parts)


CSS = """
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Segoe UI', system-ui, Georgia, serif; min-height: 100vh; color: #1e293b; background: #f8fafc; }
body.layout-study { display: flex; flex-wrap: wrap; padding-top: 56px; }
body.layout-full { padding-top: 56px; }
.site-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100; height: 56px;
  display: flex; align-items: center; gap: 1rem; padding: 0 1.25rem;
  background: #0f172a; color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.logo { color: #fff; font-weight: 700; text-decoration: none; font-size: 1.05rem; white-space: nowrap; }
.site-nav { display: flex; flex-wrap: wrap; gap: 0.75rem; flex: 1; }
.site-nav a { color: #cbd5e1; text-decoration: none; font-size: 0.9rem; }
.site-nav a:hover, .site-nav a.active { color: #38bdf8; }
.header-cta {
  background: #2563eb; color: #fff !important; padding: 0.45rem 0.9rem; border-radius: 6px;
  text-decoration: none; font-size: 0.85rem; font-weight: 600;
}
.header-cta:hover { background: #1d4ed8; }
.site-footer {
  width: 100%; text-align: center; padding: 1.5rem; background: #0f172a; color: #94a3b8; font-size: 0.85rem;
}
.site-footer a { color: #38bdf8; }
#sidebar {
  width: 280px; background: #1e293b; color: #e2e8f0; padding: 1.25rem; overflow-y: auto;
  position: fixed; top: 56px; height: calc(100vh - 56px);
}
.sidebar-brand { font-size: 0.95rem; font-weight: 700; margin: 0 0 0.25rem; color: #fff; }
.tagline { font-size: 0.75rem; color: #94a3b8; margin: 0 0 1rem; line-height: 1.4; }
#sidebar a { color: #cbd5e1; text-decoration: none; font-size: 0.82rem; line-height: 1.5; }
#sidebar a:hover { color: #fff; }
#sidebar li.active a { color: #38bdf8; font-weight: 600; }
#sidebar ul { list-style: none; padding: 0; margin: 0; }
.download-tip { margin-top: 2rem; font-size: 0.75rem; color: #94a3b8; border-top: 1px solid #334155; padding-top: 1rem; }
body.layout-study #content {
  margin-left: 280px; padding: 2rem 3rem 4rem; max-width: 920px; flex: 1;
  line-height: 1.75; font-size: 1.05rem; min-height: calc(100vh - 56px);
}
body.layout-full #content { max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
.hero { background: linear-gradient(135deg, #1e3a8a, #0f172a); color: #fff; padding: 3rem 2rem; border-radius: 12px; margin-bottom: 2rem; }
.hero-badge { display: inline-block; background: rgba(255,255,255,.15); padding: 0.35rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
.hero h1 { font-size: 2rem; border: none; color: #fff; margin: 1rem 0; }
.hero-sub { color: #cbd5e1; max-width: 42rem; }
.hero-actions { margin-top: 1.5rem; display: flex; flex-wrap: wrap; gap: 0.75rem; }
.btn { display: inline-block; padding: 0.65rem 1.2rem; border-radius: 8px; text-decoration: none; font-weight: 600; }
.btn-primary { background: #2563eb; color: #fff; }
.btn-primary:hover { background: #1d4ed8; }
.btn-secondary { background: transparent; border: 2px solid #94a3b8; color: #fff; }
.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.course-card {
  display: block; padding: 1.25rem; background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
  text-decoration: none; color: inherit; box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.course-card:hover { border-color: #2563eb; box-shadow: 0 4px 12px rgba(37,99,235,.15); }
.course-card h3 { margin: 0 0 0.5rem; color: #1e40af; font-size: 1rem; }
.course-card p { margin: 0; font-size: 0.85rem; color: #64748b; }
.price-badge { display: inline-block; font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.5rem; border-radius: 6px; margin-bottom: 0.5rem; }
.price-badge.paid { background: #fef3c7; color: #92400e; }
.price-badge.free { background: #d1fae5; color: #065f46; }
.paid-course-card .course-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-top: 0.75rem; }
.login-hint { font-size: 0.8rem; color: #64748b; }
.feature-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; list-style: none; padding: 0; }
.feature-grid li { background: #fff; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; }
.doc-intro { font-size: 1.05rem; color: #475569; }
.doc-search-label { display: block; font-weight: 600; margin-top: 1.5rem; }
.doc-search {
  width: 100%; max-width: 420px; padding: 0.6rem 0.75rem; margin: 0.5rem 0 1.5rem;
  border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1rem;
}
.doc-category { margin: 2rem 0; }
.doc-list { display: grid; gap: 1rem; }
.doc-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.25rem;
}
.doc-card h3 { margin: 0 0 0.5rem; font-size: 1.05rem; }
.doc-card h3 a { color: #1e40af; text-decoration: none; }
.doc-card h3 a:hover { text-decoration: underline; }
.doc-meta { font-size: 0.85rem; color: #64748b; margin: 0.75rem 0 0; }
.doc-missing { font-size: 0.8rem; color: #b45309; font-weight: normal; }
.doc-empty { color: #94a3b8; font-style: italic; }
.doc-admin { margin-top: 2.5rem; padding: 1rem; background: #f1f5f9; border-radius: 8px; font-size: 0.9rem; }
h1 { color: #0f172a; border-bottom: 2px solid #2563eb; padding-bottom: 0.3em; }
h2 { color: #1e40af; margin-top: 1.5em; }
h3 { color: #334155; }
blockquote { border-left: 4px solid #10b981; background: #ecfdf5; padding: 0.75em 1em; margin: 1em 0; }
blockquote strong { color: #065f46; }
pre { background: #f8fafc; border: 1px solid #e2e8f0; padding: 1em; overflow-x: auto; font-size: 0.9rem; }
code { font-family: Consolas, monospace; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #cbd5e1; padding: 0.5em; text-align: left; }
.chapter-pager {
  display: flex; align-items: stretch; justify-content: space-between; gap: 0.75rem;
  margin: 1.5rem 0 2rem; padding: 1rem 0; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;
}
.chapter-pager:first-child { margin-top: 0; border-top: none; padding-top: 0; }
.pager-btn {
  display: flex; flex-direction: column; gap: 0.2rem; padding: 0.75rem 1rem;
  border: 1px solid #cbd5e1; border-radius: 8px; text-decoration: none; color: #1e293b;
  background: #f8fafc; min-width: 120px; transition: background 0.15s, border-color 0.15s;
}
.pager-btn:hover { background: #eff6ff; border-color: #2563eb; color: #1e40af; }
.pager-prev { text-align: left; }
.pager-next { text-align: right; margin-left: auto; }
.pager-home {
  flex: 0 0 auto; align-self: center; text-align: center; font-weight: 600;
  min-width: auto; padding: 0.6rem 1.2rem; background: #2563eb; color: #fff; border-color: #2563eb;
}
.pager-home:hover { background: #1d4ed8; color: #fff; }
.pager-disabled {
  opacity: 0.4; cursor: default; background: #f1f5f9; border-style: dashed;
}
.pager-label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #64748b; }
.pager-title { font-size: 0.88rem; line-height: 1.35; color: inherit; }
.pager-next .pager-label, .pager-next .pager-title { align-self: flex-end; }
details { margin: 1rem 0 1.5rem; padding: 0.75rem 1rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; }
details summary { cursor: pointer; font-weight: 600; color: #2563eb; }
details[open] summary { margin-bottom: 0.75rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem; }
details p { margin: 0.5rem 0; }
@media (max-width: 700px) {
  .chapter-pager { flex-wrap: wrap; }
  .pager-home { order: -1; width: 100%; }
  .pager-next { margin-left: 0; }
  .pager-title { display: none; }
}
@media (max-width: 800px) {
  #sidebar { display: none; }
  body.layout-study #content { margin-left: 0; padding: 1rem; }
  .site-nav { display: none; }
}
@media print {
  .chapter-pager, .site-header, .site-footer { display: none; }
  #sidebar { display: none; }
  #content { margin: 0; max-width: 100%; padding: 1cm; }
}
"""


def main() -> None:
    items = parse_summary()
    pages = readable_pages(items)
    rel_to_index = {rel: i for i, (_, rel) in enumerate(pages)}
    subjects = top_subjects(SRC / "SUMMARY.md")

    OUT.mkdir(exist_ok=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    count = 0
    for title, rel, _ in items:
        md_path = SRC / rel
        if not md_path.exists():
            continue
        body = md_to_html(md_path.read_text(encoding="utf-8"))
        page_nav = build_nav(items, rel)
        pager = build_pager(rel_to_index[rel], pages)
        out_name = Path(rel).with_suffix(".html")
        out_path = OUT / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            shell(title, body, sidebar_nav=page_nav, pager=pager, active_header="study"),
            encoding="utf-8",
        )
        count += 1

    (OUT / "index.html").write_text(
        shell(
            "Home",
            landing_body(BRANDING, BASE, subjects),
            full_width=True,
            active_header="home",
        ),
        encoding="utf-8",
    )
    copy_document_files(BASE)
    publish_admin_and_services()
    missing = validate_manifest()
    if missing:
        print("Document Centre: missing files (add to repo):")
        for m in missing:
            print(f"  - {m}")

    static_pages = (
        ("courses.html", "Courses", lambda: courses_body(BRANDING, BASE, subjects), "courses"),
        ("my-courses.html", "My Courses", lambda: my_courses_body(BRANDING, BASE), "mycourses"),
        ("documents.html", "Document Centre", lambda: documents_body(BRANDING, BASE), "documents"),
        ("about.html", "About", lambda: about_body(BRANDING), "about"),
        ("contact.html", "Contact", lambda: contact_body(BRANDING), "contact"),
    )
    for fname, page_title, body_fn, active in static_pages:
        (OUT / fname).write_text(
            shell(page_title, body_fn(), full_width=True, active_header=active),
            encoding="utf-8",
        )

    print(f"Built {count + len(static_pages) + 1} HTML pages in {OUT}")
    print(f"Site: {SITE} | Base path: {BASE!r}")
    print(f"Open: {OUT / 'index.html'}")


if __name__ == "__main__":
    main()

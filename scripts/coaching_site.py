"""Marketing pages for coaching centre website."""

from __future__ import annotations

import html
import re
from pathlib import Path


def top_subjects(summary_path: Path) -> list[tuple[str, str]]:
    """Top-level course links from SUMMARY.md."""
    items: list[tuple[str, str]] = []
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("  "):
            continue
        m = re.match(r"- \[([^\]]+)\]\(\./([^)]+\.md)\)", line)
        if not m:
            continue
        title, rel = m.groups()
        if rel.endswith("README.md") or rel in ("introduction.md", "how-to-study.md"):
            items.append((title, rel.replace(".md", ".html")))
    return items


def subject_cards(subjects: list[tuple[str, str]], base: str) -> str:
    cards = []
    for title, href in subjects:
        if title in ("Introduction", "How to use this book"):
            continue
        cards.append(
            f'<a class="course-card" href="{base}{href}">'
            f"<h3>{html.escape(title)}</h3>"
            f"<p>Open full chapter list in the study library →</p></a>"
        )
    return "\n".join(cards)


def landing_body(b: dict, base: str, subjects: list[tuple[str, str]]) -> str:
    name = html.escape(b["siteName"])
    tagline = html.escape(b.get("tagline", ""))
    hero = html.escape(b.get("heroTitle", "Master MSc Chemistry"))
    sub = html.escape(b.get("heroSubtitle", ""))
    cards = subject_cards(subjects, base)
    return f"""
<section class="hero">
  <p class="hero-badge">{name}</p>
  <h1>{hero}</h1>
  <p class="hero-sub">{sub}</p>
  <div class="hero-actions">
    <a class="btn btn-primary" href="{base}introduction.html">Start learning free</a>
    <a class="btn btn-secondary" href="{base}courses.html">View all courses</a>
    <a class="btn btn-secondary" href="{base}documents.html">Document centre</a>
  </div>
</section>
<section class="features">
  <h2>Why students choose {html.escape(b.get('shortName', name))}</h2>
  <ul class="feature-grid">
    <li><strong>Concept-first</strong><br/>Understand mechanisms before memorizing reactions.</li>
    <li><strong>Real-life links</strong><br/>Every topic tied to medicine, industry, and daily life.</li>
    <li><strong>Examples + answers</strong><br/>Worked problems with full solutions on each page.</li>
    <li><strong>Beginner → Advanced</strong><br/>Structured path for MSc-level chemistry.</li>
  </ul>
</section>
<section class="courses-preview">
  <h2>Popular courses</h2>
  <div class="course-grid">{cards}</div>
  <p><a href="{base}courses.html">See all subjects →</a></p>
</section>
<p class="site-note"><em>{tagline}</em></p>
"""


def courses_body(b: dict, base: str, subjects: list[tuple[str, str]]) -> str:
    cards = subject_cards(subjects, base)
    return f"""
<h1>Courses & study material</h1>
<p>Full digital library for <strong>{html.escape(b['siteName'])}</strong>. Select a subject to open chapters.</p>
<div class="course-grid">{cards}</div>
<p>Beginners: start with <a href="{base}introduction.html">Introduction</a> and
<a href="{base}how-to-study.html">How to study without cramming</a>.</p>
"""


def about_body(b: dict) -> str:
    return f"""
<h1>About {html.escape(b['siteName'])}</h1>
<p>We help MSc Chemistry students <strong>understand concepts deeply</strong> — organic mechanisms,
synthesis, physical chemistry, and more — without rote memorization.</p>
<p>Our online study library includes thousands of pages of structured notes, real-life examples,
and solved practice problems. You can rename and rebrand this centre anytime in
<code>config/branding.json</code> and rebuild the site.</p>
<h2>Our approach</h2>
<ul>
  <li>Build intuition before equations</li>
  <li>Link theory to real products and processes</li>
  <li>Practice with answers on every page</li>
</ul>
"""


def contact_body(b: dict) -> str:
    return f"""
<h1>Contact</h1>
<p>Reach <strong>{html.escape(b['siteName'])}</strong>:</p>
<ul>
  <li>Phone: {html.escape(b.get('phone', 'Update in config/branding.json'))}</li>
  <li>Email: <a href="mailto:{html.escape(b.get('email', ''))}">{html.escape(b.get('email', ''))}</a></li>
  <li>Address: {html.escape(b.get('address', ''))}</li>
</ul>
<p>Update these details in <code>config/branding.json</code>, then run <code>python scripts/build_html.py</code>.</p>
"""
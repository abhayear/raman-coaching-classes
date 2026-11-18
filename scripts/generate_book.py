#!/usr/bin/env python3
"""
Generate MSc Chemistry guide content (~2000+ print pages).
Concept-first chapters: objectives, intuition, mechanisms, examples, practice.
"""

from __future__ import annotations

import json
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from real_life_examples import (
    chapter_hook,
    lookup_example,
    mechanism_real_life,
    synthesis_real_life,
)
from example_bank import format_practice_section, format_worked_section, practice_set, worked_example as bank_worked

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
META = ROOT / "scripts" / "curriculum.json"

LEVELS = ["beginner", "intermediate", "advanced"]
WORDS_PER_PAGE = 450  # approximate print page density


@dataclass
class Chapter:
    id: str
    title: str
    subject: str
    unit: str
    level: str
    concepts: list[str] = field(default_factory=list)
    mechanism: str | None = None
    synthesis: str | None = None


def wrap(text: str, width: int = 88) -> str:
    return textwrap.fill(text, width=width)


def blockquote(kind: str, text: str) -> str:
    labels = {"tip": "Concept tip", "cram": "Avoid cramming", "life": "Real life"}
    return f"> **{labels.get(kind, kind)}:** {text}\n"


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body}\n"


def objectives(items: list[str]) -> str:
    lines = "\n".join(f"- {i}" for i in items)
    return section("Learning objectives", lines)


def intuition(text: str) -> str:
    return section("Build intuition first", text + "\n\n" + blockquote("tip", "Pause after each paragraph and explain it aloud in your own words."))


def core_concepts(concepts: list[str], subject: str, unit: str, title: str, level: str) -> str:
    parts = []
    for i, c in enumerate(concepts, 1):
        depth = {
            "beginner": "Start from everyday analogies and build upward.",
            "intermediate": "Connect this idea to prior chapters and typical exam traps.",
            "advanced": "Link to primary literature patterns and design decisions in synthesis.",
        }[level]
        life = lookup_example(c, subject, unit, title, level)
        parts.append(
            f"### {i}. {c}\n\n"
            f"{wrap(f'In {subject}, {c} is best understood as a pattern you recognize, not a definition to memorize. {depth}')}\n\n"
            f"**Real-life connection:** {wrap(life)}\n\n"
            f"**Why it matters:** {wrap(f'MSc-level work assumes you can predict behavior involving {c.lower()} and justify your reasoning with evidence (spectra, rates, stereochemistry, or thermodynamics).')}\n\n"
            f"**Check yourself:** Can you name one real product, process, or body function where {c.lower()} decides the outcome?\n"
        )
    return section("Core concepts (each linked to real life)", "\n".join(parts))


def worked_example_block(ch: Chapter) -> str:
    qa = bank_worked(ch.title, ch.subject, ch.unit, ch.id, ch.level)
    life = lookup_example(ch.concepts[0] if ch.concepts else ch.title, ch.subject, ch.unit, ch.title, ch.level)
    return section(
        "Worked example with answer",
        format_worked_section(qa, life[:160] + ("…" if len(life) > 160 else "")),
    )


def practice_with_answers(ch: Chapter) -> str:
    counts = {"beginner": 3, "intermediate": 4, "advanced": 5}[ch.level]
    concepts = ch.concepts or [ch.title]
    items = practice_set(concepts, ch.subject, ch.title, ch.id, ch.level, counts)
    return section(
        "Practice problems with answers",
        "Try each problem first, then check the answer shown directly below.\n\n" + format_practice_section(items),
    )


def mechanism_section(mechanism: str | None, title: str) -> str:
    if not mechanism:
        return ""
    life = mechanism_real_life(title, mechanism)
    return section(
        "Reaction mechanism (arrow-by-arrow)",
        blockquote("life", life)
        + f"\n```text\n{mechanism}\n```\n\n"
        + blockquote(
            "tip",
            "Mechanisms are stories about electron flow. Each arrow must start at a lone pair or bond and end where electrons can be accepted.",
        ),
    )


def synthesis_section(synthesis: str | None, title: str) -> str:
    if not synthesis:
        return ""
    life = synthesis_real_life(title, synthesis)
    return section(
        "Retrosynthesis & forward strategy",
        blockquote("life", life)
        + f"\n{wrap(synthesis)}\n\n"
        "**Retrosynthetic disconnections to practice:**\n\n"
        "- Functional-group interconversion (FGI)\n"
        "- One-bond disconnection (C–C, C–heteroatom)\n"
        "- Strategic use of symmetry or latent functionality\n",
    )


def practice_problems(level: str, concepts: list[str], subject: str) -> str:
    return ""  # replaced by practice_with_answers


def chapter_md(ch: Chapter) -> str:
    intro = wrap(
        f"This chapter on **{ch.title}** ({ch.level} level) is part of **{ch.unit}** in **{ch.subject}**. "
        "Read for patterns and reasoning — not to memorize isolated facts."
    )
    obj_items = ch.concepts[:3] if ch.concepts else [f"Understand the role of {ch.title} in {ch.subject}"]
    concepts = ch.concepts or [ch.title]
    real_life_map = "\n".join(
        f"- **{c}** → {lookup_example(c, ch.subject, ch.unit, ch.title, ch.level)[:100]}…"
        for c in concepts
    )
    body = [
        f"# {ch.title}\n",
        f"*{ch.subject} · {ch.unit} · {ch.level.capitalize()}*\n",
        blockquote("cram", "If you cannot explain why a step happens, you are not ready to move on — revisit the intuition section."),
        section("Real-life map of this chapter", real_life_map),
        blockquote("life", chapter_hook(ch.subject, ch.title, ch.unit)),
        intro + "\n",
        objectives(obj_items),
        intuition(
            wrap(
                f"Before equations, picture what molecules are doing in real systems. For {ch.title}, ask: "
                "Who has electrons to donate? Who is electron-deficient? What constraint ( sterics, solvent, temperature ) wins? "
                "Then name one household, medical, or industrial place where this exact logic already runs."
            )
        ),
        worked_example_block(ch),
        core_concepts(concepts, ch.subject, ch.unit, ch.title, ch.level),
        mechanism_section(ch.mechanism, ch.title),
        synthesis_section(ch.synthesis, ch.title),
        practice_with_answers(ch),
        section(
            "Chapter summary",
            "- Every concept above links to a **real product, process, or biological system**.\n"
            "- Focus on **patterns**, not isolated facts.\n"
            "- Every mechanism arrow must have a physical justification.\n"
            "- Link this chapter to adjacent topics in the same unit.\n"
            "- Revisit practice problems after 48 hours for spaced recall.\n",
        ),
        section("Further reading", f"- Consult standard MSc texts for {ch.subject}.\n- Search primary reviews using keywords: {', '.join(ch.concepts[:2]) or ch.title}.\n"),
    ]
    return "\n".join(body)


def load_curriculum() -> list[Chapter]:
    data = json.loads(META.read_text(encoding="utf-8"))
    chapters: list[Chapter] = []
    for subject in data["subjects"]:
        sname = subject["name"]
        for unit in subject["units"]:
            uname = unit["name"]
            for ch in unit["chapters"]:
                chapters.append(
                    Chapter(
                        id=ch["id"],
                        title=ch["title"],
                        subject=sname,
                        unit=uname,
                        level=ch["level"],
                        concepts=ch.get("concepts", []),
                        mechanism=ch.get("mechanism"),
                        synthesis=ch.get("synthesis"),
                    )
                )
    return chapters


def write_chapters(chapters: list[Chapter]) -> dict:
    stats = {"files": 0, "words": 0}
    for ch in chapters:
        rel = Path(ch.subject.lower().replace(" ", "-").replace("&", "and")) / ch.unit.lower().replace(" ", "-") / f"{ch.id}.md"
        path = SRC / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        text = chapter_md(ch)
        path.write_text(text, encoding="utf-8")
        stats["files"] += 1
        stats["words"] += len(text.split())
    return stats


def write_summary(chapters: list[Chapter]) -> None:
    lines = ["# Summary\n", "- [Introduction](./introduction.md)\n", "- [How to use this book](./how-to-study.md)\n"]
    current_subject = ""
    current_unit = ""
    for ch in chapters:
        if ch.subject != current_subject:
            current_subject = ch.subject
            slug = current_subject.lower().replace(" ", "-").replace("&", "and")
            lines.append(f"- [{current_subject}](./{slug}/README.md)\n")
            current_unit = ""
        if ch.unit != current_unit:
            current_unit = ch.unit
            lines.append(f"  - [{current_unit}](#)\n")
        rel = (
            f"./{ch.subject.lower().replace(' ', '-').replace('&', 'and')}/"
            f"{ch.unit.lower().replace(' ', '-')}/{ch.id}.md"
        )
        lines.append(f"    - [{ch.title}]({rel})\n")
    (SRC / "SUMMARY.md").write_text("".join(lines), encoding="utf-8")


def write_static_pages() -> None:
    intro = """# Welcome to the MSc Chemistry Concept-First Guide

This book covers **Master of Science level chemistry** across major subjects — written so you **understand** mechanisms and synthesis strategies, not cram isolated reactions.

## What makes this different

- **Concept-first:** Every chapter builds intuition before equations.
- **Real-life linked:** Every concept connects to medicine, food, materials, or environment.
- **Noob → Advanced:** Chapters are tagged beginner, intermediate, or advanced.
- **Organic focus:** Deep coverage of **reaction mechanisms** and **organic synthesis**.
- **Downloadable:** Build HTML or PDF for offline reading (see project README).

## Subjects covered

Physical chemistry, organic mechanisms & synthesis, inorganic, analytical, spectroscopy, biochemistry, organometallic, polymer, medicinal, environmental, and computational chemistry.

Start with [How to study without cramming](./how-to-study.md), then pick your subject in the sidebar.
"""
    (SRC / "introduction.md").write_text(intro, encoding="utf-8")

    howto = """# How to Study Without Cramming

## The 4-step loop

1. **Preview** — Skim objectives only (2 minutes).
2. **Understand** — Read intuition + core concepts; name a real-life example for each.
3. **Test** — Close the book; explain the mechanism aloud using a food, drug, or material example.
4. **Space** — Retry practice problems after 2 days.

## For reaction mechanisms

- Every curved arrow: source → sink for electrons.
- Label nucleophile, electrophile, leaving group, and stereochemical outcome.
- Ask: *What would change if I switched solvent or temperature?*

## For organic synthesis

- Always retrosynthesize first (target → synthons → commercial starts).
- One strategic disconnection beats ten random reactions memorized.

## Level guide

| Level | You should |
|-------|------------|
| Beginner | Define terms and follow arrow pushing |
| Intermediate | Predict outcomes and justify regioselectivity |
| Advanced | Design multi-step routes and troubleshoot failures |
"""
    (SRC / "how-to-study.md").write_text(howto, encoding="utf-8")


def write_subject_readmes(chapters: list[Chapter]) -> None:
    by_subject: dict[str, list[Chapter]] = {}
    for ch in chapters:
        by_subject.setdefault(ch.subject, []).append(ch)
    for subject, chs in by_subject.items():
        slug = subject.lower().replace(" ", "-").replace("&", "and")
        units = sorted(set(c.unit for c in chs))
        body = f"# {subject}\n\nChapters: **{len(chs)}** · Units: **{len(units)}**\n\n"
        for u in units:
            body += f"- {u}\n"
        path = SRC / slug / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")


def main() -> None:
    chapters = load_curriculum()
    write_static_pages()
    stats = write_chapters(chapters)
    write_subject_readmes(chapters)
    write_summary(chapters)
    pages = stats["words"] // WORDS_PER_PAGE
    print(f"Generated {stats['files']} chapters, ~{stats['words']:,} words (~{pages:,} print pages)")


if __name__ == "__main__":
    main()

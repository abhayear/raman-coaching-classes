# MSc Chemistry Concept-First Guide

A **Master of Science level** chemistry book/blog covering major subjects from **beginner to advanced**, with deep focus on **organic reaction mechanisms** and **organic synthesis**. Built for **understanding, not cramming**.

## Features

- Concept-first chapters with learning objectives, intuition, worked examples, and practice
- 800+ chapters targeting **2000+ print pages**
- Searchable HTML book (mdBook)
- **Download as PDF** or print-friendly HTML

## Quick start

### 1. Generate content

```powershell
cd C:\Users\akshay\Projects\msc-chemistry-guide
python scripts/build_curriculum.py
python scripts/generate_book.py
```

### 2. Install mdBook (one time)

Download from [https://github.com/rust-lang/mdBook/releases](https://github.com/rust-lang/mdBook/releases) or:

```powershell
cargo install mdbook
```

### 3. Build HTML book

```powershell
mdbook build
```

Open `book/index.html` in your browser.

### 4. Download as PDF

**Option A — Browser (easiest):**

1. Run `mdbook serve` and open the site
2. Use **Print → Save as PDF** (Ctrl+P) on any chapter or the full book
3. Enable "Background graphics" for best formatting

**Option B — Automated script:**

```powershell
python scripts/export_pdf.py
```

Requires: `pip install playwright markdown` then `playwright install chromium`

Output: `exports/msc-chemistry-guide.pdf`

## Subjects

| Subject | Focus |
|---------|--------|
| Foundations | Math, lab skills, study methods |
| **Organic Reaction Mechanisms** | SN1/SN2, E1/E2, additions, radicals, 120+ case studies |
| **Organic Synthesis** | Retrosynthesis, named reactions, total synthesis |
| Physical Chemistry | Thermodynamics, kinetics, quantum |
| Inorganic Chemistry | Bonding, coordination, solid state |
| Analytical Chemistry | Chromatography, electroanalysis, QA |
| Spectroscopy | NMR, IR, MS, structure elucidation |
| Biochemistry | Proteins, enzymes, metabolism |
| Organometallic | Cross-coupling, catalysis |
| Polymer, Medicinal, Environmental, Computational | MSc core coverage |

## Study philosophy

Each chapter follows: **Objectives → Intuition → Core concepts → Mechanism/Synthesis (where relevant) → Worked example → Practice → Summary**

Re-read practice problems after 48 hours for spaced learning.

## License

Educational use. Content is for learning purposes; verify critical data against primary sources for research.

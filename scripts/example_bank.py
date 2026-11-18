"""Worked examples and practice problems with full answers."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class QA:
    question: str
    answer: str


def _pick(key: str, pool: list[QA]) -> QA:
    idx = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(pool)
    return pool[idx]


# --- Topic-specific banks (keyword in title/concept -> Q&A) ---
TOPIC_BANK: dict[str, list[QA]] = {
    "sn2": [
        QA(
            "**Example:** (R)-2-bromobutane is treated with NaCN in acetone. "
            "Predict the stereochemistry of the product and name the mechanism.",
            "**Answer:** SN2 — backside attack inverts configuration. "
            "(R)-2-bromobutane → **(S)-2-methylbutanenitrile**. "
            "Rate = k[substrate][CN⁻]; polar aprotic acetone stabilizes CN⁻ without strong solvation shell.",
        ),
        QA(
            "**Example:** Compare reaction rate: CH₃Br vs (CH₃)₃CBr with I⁻ in acetone.",
            "**Answer:** CH₃Br reacts **much faster** (SN2). Methyl/primary halides have minimal steric hindrance; "
            "tert-butyl blocks backside approach. (CH₃)₃CBr favours SN1/E1, not SN2.",
        ),
    ],
    "sn1": [
        QA(
            "**Example:** (CH₃)₃CBr in ethanol/water gives two products. Identify them and the rate law.",
            "**Answer:** Rate = k[(CH₃)₃CBr] only (unimolecular). Products: **(CH₃)₃COH** (SN1, solvolysis) and "
            "**(CH₃)₂C=CH₂** (E1, minor at low T). Carbocation (CH₃)₃C⁺ intermediate; racemization if chiral centre at C–Br.",
        ),
    ],
    "e2": [
        QA(
            "**Example:** 2-bromobutane + t-BuOK in t-BuOH at high T. Major alkene?",
            "**Answer:** **E2**, anti-periplanar H and Br. With bulky base t-BuOK → **Hofmann product 1-butene** "
            "(less substituted) often competes; from 2-bromobutane major is **trans-2-butene** (Zaitsev, more stable).",
        ),
    ],
    "diels": [
        QA(
            "**Example:** Butadiene + ethylene (heat). Draw the product type.",
            "**Answer:** **Cyclohexene** via concerted [4+2] cycloaddition. No intermediate. "
            "Suprafacial; endo approach favoured when dienophile has π-accepting group.",
        ),
    ],
    "grignard": [
        QA(
            "**Example:** CH₃MgBr + formaldehyde (H₂CO), then H₃O⁺. Product?",
            "**Answer:** Nucleophilic addition to carbonyl → after work-up **ethanol (CH₃CH₂OH)**. "
            "Real life: Grignard routes make secondary/tertiary alcohols in drug synthesis.",
        ),
    ],
    "wittig": [
        QA(
            "**Example:** Benzaldehyde + Ph₃P=CH₂. Product?",
            "**Answer:** **Styrene (Ph-CH=CH₂)** + Ph₃P=O by-product. "
            "Alkene geometry often E-favoured with unstabilized ylides.",
        ),
    ],
    "retrosynth": [
        QA(
            "**Example:** Retrosynthesize **butan-2-ol** in ≤2 steps from ≤3 C building blocks.",
            "**Answer:** Disconnection: C–OH bond → **Grignard**. "
            "Forward: (1) Mg/CH₃CH₂Br → CH₃CH₂MgBr; (2) + CH₃CHO; (3) H₃O⁺ → butan-2-ol. "
            "Real life: same logic used to plan paracetamol from p-aminophenol + acetic anhydride.",
        ),
    ],
    "nmr": [
        QA(
            "**Example:** Aromatics show one singlet at δ 7.2 (5H) and singlet at δ 2.3 (3H). Structure?",
            "**Answer:** **Toluene** — monosubstituted benzene (5H aromatic) + CH₃ (3H). "
            "Real life: NMR QC confirms batch identity in pharma before release.",
        ),
    ],
    "thermodynam": [
        QA(
            "**Example:** ΔG° = −20 kJ/mol at 298 K. Is K > 1? Estimate magnitude.",
            "**Answer:** Yes. K = exp(−ΔG°/RT) = exp(20000/(8.314×298)) ≈ **exp(8.07) ≈ 3200**. "
            "Real life: binding constants for drug–receptor follow same relation.",
        ),
    ],
    "kinetics": [
        QA(
            "**Example:** First-order reaction: t½ = 10 min. Fraction remaining after 30 min?",
            "**Answer:** 3 half-lives → (1/2)³ = **1/8 = 12.5%** remaining. "
            "Real life: aspirin hydrolysis shelf-life uses identical math.",
        ),
    ],
    "enzyme": [
        QA(
            "**Example:** Km = 4 mM, [S] = 4 mM. Fraction Vmax?",
            "**Answer:** Michaelis–Menten: v/Vmax = [S]/(Km+[S]) = 4/(4+4) = **0.5 (50%)**. "
            "Real life: lactase pills raise effective [S] processing in gut.",
        ),
    ],
    "equilibrium": [
        QA(
            "**Example:** N₂ + 3H₂ ⇌ 2NH₃, Δn = −2. Higher pressure shifts equilibrium?",
            "**Answer:** **Toward products (NH₃)** — Le Chatelier reduces moles of gas. "
            "Real life: Haber process runs at high P (~200 atm) for ammonia fertiliser.",
        ),
    ],
    "oxidation": [
        QA(
            "**Example:** PCC oxidises primary alcohol to ___? Jones reagent?",
            "**Answer:** PCC → **aldehyde** (stops at aldehyde). Jones (CrO₃/H₂SO₄) → **carboxylic acid**. "
            "Real life: selective oxidation prevents over-oxidation in fragrance aldehyde synthesis.",
        ),
    ],
    "cross-coupling": [
        QA(
            "**Example:** Suzuki: Ar–Br + Ar′–B(OH)₂, Pd catalyst. What forms?",
            "**Answer:** **Biaryl Ar–Ar′** + boron by-product. Oxidative addition → transmetalation → reductive elimination. "
            "Real life: valsartan and OLED materials made this way.",
        ),
    ],
}


SUBJECT_POOLS: dict[str, list[QA]] = {
    "Organic Reaction Mechanisms": [
        QA(
            "**Example:** Is CH₃OH a good nucleophile in acid or base?",
            "**Answer:** In **base**: CH₃O⁻ is strong nucleophile. In **acid**: mostly CH₃OH (neutral), poor nucleophile; "
            "protonation of alcohol gives R–OH₂⁺ (leaving group in substitution).",
        ),
        QA(
            "**Example:** Primary vs tertiary alkyl halide + NaI in acetone — which reacts faster?",
            "**Answer:** **Primary/methyl faster** (SN2). Tertiary blocked sterically; may go SN1 if polar protic solvent used.",
        ),
    ],
    "Organic Synthesis": [
        QA(
            "**Example:** Convert benzene → nitrobenzene → aniline in 2 steps.",
            "**Answer:** (1) HNO₃/H₂SO₄ → nitrobenzene (EAS). (2) Sn/HCl or H₂/Pd → **aniline**. "
            "Real life: aniline is dye and polymer precursor.",
        ),
    ],
    "Physical Chemistry": [
        QA(
            "**Example:** Ideal gas doubles T at constant V. Effect on P?",
            "**Answer:** **P doubles** (PV = nRT). Real life: tyre pressure rises on hot days.",
        ),
    ],
    "Spectroscopy": [
        QA(
            "**Example:** IR peak at ~1715 cm⁻¹ strongly suggests?",
            "**Answer:** **C=O stretch** (saturated aldehyde/ketone region). "
            "Real life: FTIR checks counterfeit vs genuine leather coatings.",
        ),
    ],
    "Biochemistry": [
        QA(
            "**Example:** Glucose → 2 pyruvate in glycolysis: net ATP?",
            "**Answer:** **2 ATP net** (+ 2 NADH). Real life: muscles burn this pathway in sprinting.",
        ),
    ],
    "Analytical Chemistry": [
        QA(
            "**Example:** 25.0 mL unknown HCl titrated with 0.100 M NaOH; Veq = 20.0 mL. [HCl]?",
            "**Answer:** moles OH⁻ = 0.100 × 0.020 = 0.002 mol = moles HCl. "
            "[HCl] = 0.002/0.025 = **0.080 M**. Real life: same logic in water acidity testing.",
        ),
    ],
    "Inorganic Chemistry": [
        QA(
            "**Example:** [Fe(CN)₆]⁴⁻ vs [Fe(H₂O)₆]²⁺ — which has larger Δoct?",
            "**Answer:** **[Fe(CN)₆]⁴⁻** — CN⁻ is strong-field ligand (low spin, large splitting). "
            "Real life: crystal field colour in gemstones.",
        ),
    ],
}


def _match_topic(text: str) -> list[QA] | None:
    t = text.lower()
    for key, pool in TOPIC_BANK.items():
        if key in t:
            return pool
    return None


def worked_example(ch_title: str, subject: str, unit: str, chapter_id: str, level: str) -> QA:
    for text in (ch_title, unit):
        pool = _match_topic(text)
        if pool:
            return _pick(f"we:{chapter_id}:{level}", pool)

    pool = SUBJECT_POOLS.get(subject, SUBJECT_POOLS["Physical Chemistry"])
    qa = _pick(f"we:{subject}:{chapter_id}", pool)

    if level == "advanced":
        qa = QA(
            qa.question,
            qa.answer + " **Advanced extension:** Propose one experiment (IR, rate study, isotope label) to confirm this answer.",
        )
    return qa


def practice_set(
    concepts: list[str],
    subject: str,
    title: str,
    chapter_id: str,
    level: str,
    count: int,
) -> list[QA]:
    items: list[QA] = []
    for n in range(count):
        concept = concepts[n % len(concepts)] if concepts else title
        key_text = f"{concept} {title}"

        pool = _match_topic(key_text) or _match_topic(title)
        if pool:
            qa = _pick(f"pp:{chapter_id}:{n}", pool)
        else:
            subj_pool = SUBJECT_POOLS.get(subject, SUBJECT_POOLS["Physical Chemistry"])
            qa = _pick(f"pp:{subject}:{concept}:{n}", subj_pool)

        items.append(
            QA(
                f"**Problem {n + 1} ({concept}):** {qa.question.replace('**Example:** ', '')}",
                qa.answer.replace("**Answer:** ", "**Answer:** "),
            )
        )
    return items


def format_worked_section(qa: QA, life_hint: str) -> str:
    q = qa.question.replace("**Example:** ", "")
    a = qa.answer.replace("**Answer:** ", "")
    return (
        f"**Example (try first):**\n\n{q}\n\n"
        f"**Real-life link:** {life_hint}\n\n"
        f"---\n\n"
        f"**Answer:**\n\n{a}\n"
    )


def format_practice_section(items: list[QA]) -> str:
    parts = []
    for qa in items:
        parts.append(
            f"{qa.question}\n\n"
            f"**Answer:**\n\n"
            f"{qa.answer.replace('**Answer:** ', '')}\n"
        )
    return "\n---\n\n".join(parts)

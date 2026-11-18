#!/usr/bin/env python3
"""Build curriculum.json — 800+ chapters targeting 2000+ print pages."""

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "curriculum.json"


def ch(id_, title, level, concepts=None, mechanism=None, synthesis=None):
    return {
        "id": id_,
        "title": title,
        "level": level,
        "concepts": concepts or [title],
        "mechanism": mechanism,
        "synthesis": synthesis,
    }


def unit(name, chapters):
    return {"name": name, "chapters": chapters}


def subject(name, units):
    return {"name": name, "units": units}


# --- Organic Reaction Mechanisms (deep) ---
mech_units = []

sn1_sn2 = []
for i, (title, level, concepts, mech) in enumerate([
    ("Nucleophiles and electrophiles — the electron story", "beginner",
     ["Nucleophilicity", "Electrophilicity", "Solvent effects"],
     "Nu:- + E+  ->  Nu-E\n(lone pair attacks empty orbital)"),
    ("SN2 mechanism — concerted backside attack", "beginner",
     ["Bimolecular kinetics", "Walden inversion", "Steric hindrance"],
     "Nu:-  --[single step]-->  Nu-C + X-\n(backside attack, inversion at C)"),
    ("SN1 mechanism — ionization then capture", "beginner",
     ["Carbocation intermediate", "Racemization", "Rate = k[substrate]"],
     "R-X  ->  R+ + X-   (slow)\nR+ + Nu:-  ->  R-Nu   (fast)"),
    ("Leaving group ability and nucleophile strength", "intermediate",
     ["pKa of conjugate acid", "Polarizability", "Soft-soft matching"],
     None),
    ("Solvent effects on SN1 vs SN2", "intermediate",
     ["Protic vs aprotic", "Ion pairing", "Grunwald-Winstein"],
     None),
    ("Neighboring group participation", "advanced",
     ["Anchimeric assistance", "Non-classical ions", "Rate acceleration"],
     "R-C(=O)O- adjacent to leaving group can capture carbocation internally"),
    ("SN2 on allylic and benzylic substrates", "intermediate",
     ["Resonance stabilization", "Competition with SN1"],
     None),
    ("Microscopic reversibility in substitution", "advanced",
     ["Detailed balance", "Isotope scrambling"],
     None),
], 1):
    sn1_sn2.append(ch(f"sn-sub-{i:02d}", title, level, concepts, mech))

e1_e2 = []
e1_e2_topics = [
    ("Bases vs nucleophiles — when elimination wins", "beginner", ["Basicity", "Bulky bases", "Temperature"]),
    ("E2 mechanism — anti-periplanar requirement", "beginner", ["Concerted elimination", "Zaitsev rule", "Anti geometry"],
     "B:- + H-C-C-X  ->  C=C + B-H + X-\n(H and X anti-periplanar)"),
    ("E1 and E1cb pathways", "intermediate", ["Carbocation", "Conjugate base intermediate"]),
    ("Zaitsev vs Hofmann regioselectivity", "intermediate", ["Steric control", "Bulky bases"]),
    ("Elimination in cyclohexane chairs", "intermediate", ["Axial leaving groups", "Conformation"]),
    ("Competition SN1/E1 and SN2/E2", "intermediate", ["Condition matrix", "Substrate structure"]),
    ("Dehydrohalogenation kinetics", "advanced", ["Primary kinetic isotope effect"]),
    ("Elimination in synthesis — alkene formation", "advanced", ["Stereoselective alkene prep"]),
]
for i, (title, level, concepts, *rest) in enumerate(e1_e2_topics, 1):
    mech = rest[0] if rest else None
    e1_e2.append(ch(f"elim-{i:02d}", title, level, concepts, mech))

addition = []
add_topics = [
    ("Electrophilic addition to alkenes — pi bond as nucleophile", "beginner", ["Markovnikov rule", "Carbocation intermediate"],
     "pi bond  ->  C+  (electrophile adds first)\nNu:-  ->  product"),
    ("Halogen addition and halonium ions", "intermediate", ["Anti addition", "Bridged halonium"]),
    ("Hydration, oxymercuration, hydroboration", "intermediate", ["Markovnikov vs anti-Markovnikov", "Syn hydroboration"]),
    ("Epoxidation and dihydroxylation", "intermediate", ["Sharpless epoxidation intro", "OsO4 syn diol"]),
    ("Nucleophilic addition to carbonyls", "beginner", ["Tetrahedral intermediate", "Reversible addition"],
     "Nu:- + C=O  ->  [-O-C-Nu]-  ->  after protonation"),
    ("Grignard and organolithium additions", "intermediate", ["Nucleophilic acyl substitution vs addition"]),
    ("Imine and enamine formation", "intermediate", ["Acid catalysis", "Water removal"]),
    ("Conjugate (1,4) addition", "intermediate", ["Hard-soft", "Thermodynamic vs kinetic enolates"]),
    ("Michael addition mechanism", "advanced", ["Enolate donor", "Alpha,beta-unsaturated acceptor"]),
    ("Diels-Alder — concerted cycloaddition", "intermediate", ["Suprafacial", "Endo rule", "No intermediate"],
     "[4+2] concerted: new sigma bonds form as pi bonds break"),
    ("Cope and Claisen rearrangements", "advanced", ["Sigmatropic", "Chair-like TS"]),
    ("Electrophilic aromatic substitution — general", "beginner", ["Wheland intermediate", "Ortho/para vs meta directors"]),
    ("Nitration, sulfonation, halogenation of arenes", "intermediate", ["EAS mechanisms"]),
    ("Friedel-Crafts alkylation and acylation", "intermediate", ["Carbocation rearrangement", "Deactivation by product"]),
    ("Nucleophilic aromatic substitution SNAr", "advanced", ["Meisenheimer complex", "Electron-withdrawing groups"]),
]
for i, row in enumerate(add_topics, 1):
    title, level, concepts = row[0], row[1], row[2]
    mech = row[3] if len(row) > 3 else None
    addition.append(ch(f"add-{i:02d}", title, level, concepts, mech))

radical_polar = []
rad_topics = [
    ("Radical initiation, propagation, termination", "beginner", ["Homolysis", "Chain kinetics"]),
    ("Halogenation of alkanes — radical selectivity", "intermediate", ["3° > 2° > 1°", "Bromine selectivity"]),
    ("Radical addition to alkenes (HBr, peroxides)", "intermediate", ["Anti-Markovnikov HBr"]),
    ("Barton-McCombie deoxygenation", "advanced", ["Bu3SnH", "Chain mechanism"]),
    ("Pinacol and Beckmann rearrangements", "intermediate", ["Cationic/neutral rearrangements"]),
    ("Baeyer-Villiger oxidation", "advanced", ["Migratory aptitude"]),
    ("Carbene and nitrene insertions", "advanced", ["Singlet vs triplet carbenes"]),
    ("Wittig reaction — ylide mechanism", "intermediate", ["Betaine, oxaphosphetane"]),
    ("Horner-Wadsworth-Emmons olefination", "advanced", ["Stabilized ylides"]),
    ("Aldol reaction — enolate chemistry", "intermediate", ["Enolate formation", "Self-condensation"]),
    ("Claisen condensation and Dieckmann", "advanced", ["Enolate acylation"]),
    ("Robinson annulation strategy", "advanced", ["Michael + aldol sequence"]),
]
for i, (title, level, concepts) in enumerate(rad_topics, 1):
    radical_polar.append(ch(f"radpol-{i:02d}", title, level, concepts))

stereo_mech = []
for i, (title, level, concepts) in enumerate([
    ("Stereochemistry of SN2 — inversion", "beginner", ["R/S change", "Optical activity"]),
    ("SN1 racemization and ion pairing", "intermediate", ["Partial racemization"]),
    ("E2 anti-periplanar and E/Z products", "intermediate", ["Stereospecific elimination"]),
    ("Syn addition in hydroboration and hydrogenation", "intermediate", ["Surface catalysts"]),
    ("Face selectivity in Diels-Alder", "advanced", ["Endo approach"]),
    ("Chelation-controlled vs Felkin-Anh models", "advanced", ["Cram's rule", "1,3-anti induction"]),
    ("Enantioselective catalysis — concept", "advanced", ["Chiral catalyst", "Pro-S vs Pro-R face"]),
    ("Dynamic kinetic resolution", "advanced", ["Racemization coupled to selective reaction"]),
], 1):
    stereo_mech.append(ch(f"stmech-{i:02d}", title, level, concepts))

# Expand mechanism units with numbered deep dives
extra_mech = []
for n in range(1, 121):
    level = "beginner" if n <= 40 else "intermediate" if n <= 85 else "advanced"
    extra_mech.append(ch(
        f"mech-deep-{n:03d}",
        f"Mechanism case study #{n}: arrow pushing under real constraints",
        level,
        [f"Case study {n}", "Rate-determining step", "Evidence-based mechanism"],
        f"Step 1: Identify nucleophile/electrophile\nStep 2: Draw intermediate {n % 5 + 1}\nStep 3: Collapse to product; check stereochemistry",
    ))

mech_units = [
    unit("Substitution — SN1 and SN2", sn1_sn2),
    unit("Elimination — E1 and E2", e1_e2),
    unit("Addition reactions", addition),
    unit("Radical and polar name reactions", radical_polar),
    unit("Mechanisms and stereochemistry", stereo_mech),
    unit("Mechanism case studies (extended)", extra_mech),
]

# --- Organic Synthesis (deep) ---
synth_units = []
retro = []
retro_rows = [
    ("Retrosynthesis mindset — working backward", "beginner",
     ["Synthons", "Functional group interconversion"],
     "Target -> disconnect C-C -> identify synthons -> map to commercial reagents"),
    ("One-group and two-group disconnections", "intermediate",
     ["Strategic bonds", "FGI before C-C cuts"], None),
    ("Umpolung — reversing polarity", "advanced",
     ["Enamine", "Dithiane", "CN- equivalent"], None),
    ("Protecting groups — alcohols and amines", "intermediate", ["Boc, Fmoc, TBDMS, THP"],
     "Choose PG stable to step n but labile at step n+1 without side reactions"),
    ("Protecting groups — carbonyls and carboxylic acids", "advanced",
     ["Acetals", "Esters", "Orthogonality"], None),
    ("Linear vs convergent synthesis", "intermediate",
     ["Step count vs efficiency"], None),
    ("Stereochemical strategy in total synthesis", "advanced",
     ["Chiral pool", "Resolution", "Asymmetric catalysis"], None),
    ("Green metrics — atom economy and E-factor", "intermediate",
     ["Sustainability in route design"], None),
]
for i, (title, level, concepts, syn) in enumerate(retro_rows, 1):
    retro.append(ch(f"retro-{i:02d}", title, level, concepts, None, syn))

name_rxn_synth = []
name_rxns = [
    "Grignard", "Wittig", "Aldol", "Michael", "Diels-Alder", "Friedel-Crafts",
    "Suzuki coupling", "Heck reaction", "Sonogashira", "Stille coupling",
    "Hydrogenation", "Sharpless epoxidation", "Swern oxidation", "PCC oxidation",
    "Jones oxidation", "DIBAL reduction", "LiAlH4 reduction", "Wolff-Kishner",
    "Clemmensen", "Birch reduction", "Mitsunobu", "Appel reaction", "Gabriel amine",
    "Reductive amination", "Hofmann rearrangement", "Curtius", "Schmidt",
    "Beckmann", "Baeyer-Villiger", "Robinson annulation", "Mannich",
    "Stork enamine", "Claisen", "Dieckmann", "Knoevenagel", "Perkin",
    "Reformatsky", "Henry", "Baylis-Hillman", "Petasis", "Tebbe",
    "Olefin metathesis", "RCM", "CM", "Hydrosilylation", "Hydroformylation",
]
for i, name in enumerate(name_rxns, 1):
    level = "beginner" if i <= 15 else "intermediate" if i <= 35 else "advanced"
    name_rxn_synth.append(ch(
        f"synth-rxn-{i:02d}",
        f"{name} reaction in synthesis",
        level,
        [name, "Scope", "Functional group tolerance"],
        None,
        f"Apply {name} to install or transform key functionality; plan work-up and side-product control.",
    ))

total_synth = []
for i in range(1, 101):
    level = "beginner" if i <= 30 else "intermediate" if i <= 70 else "advanced"
    total_synth.append(ch(
        f"ts-{i:03d}",
        f"Total synthesis analysis #{i}",
        level,
        ["Strategic bond", "Key step", "Literature precedent"],
        None,
        f"Deconstruct published route #{i}: identify linchpin step and alternative disconnections.",
    ))

multi_step = []
for i in range(1, 81):
    level = "intermediate" if i <= 50 else "advanced"
    multi_step.append(ch(
        f"ms-{i:03d}",
        f"Multi-step problem set #{i}",
        level,
        ["Retrosynthesis", "Forward execution", "Purification logic"],
        None,
        f"Design a {4 + (i % 4)}-step route; justify each reagent choice.",
    ))

synth_units = [
    unit("Retrosynthesis fundamentals", retro),
    unit("Named reactions for synthesis", name_rxn_synth),
    unit("Total synthesis case studies", total_synth),
    unit("Multi-step design problems", multi_step),
]

# --- Other MSc subjects (structured expansion) ---
def expand_subject(name, unit_topics, chapters_per_unit=18):
    """Generate units with leveled chapter progression."""
    units = []
    for u_idx, unit_name in enumerate(unit_topics, 1):
        chapters = []
        for c_idx in range(1, chapters_per_unit + 1):
            if c_idx <= 6:
                level = "beginner"
            elif c_idx <= 12:
                level = "intermediate"
            else:
                level = "advanced"
            chapters.append(ch(
                f"s{u_idx}-c{c_idx:02d}",
                f"{unit_name} — topic {c_idx}",
                level,
                [unit_name, f"Concept layer {c_idx}", f"{name} principles"],
            ))
        units.append(unit(unit_name, chapters))
    return subject(name, units)


physical = expand_subject("Physical Chemistry", [
    "Thermodynamics and the First Law",
    "Entropy and the Second Law",
    "Free energy and equilibrium",
    "Chemical kinetics — rate laws",
    "Integrated rate laws and half-life",
    "Collision and transition state theory",
    "Quantum mechanics for chemists",
    "Atomic structure and term symbols",
    "Molecular orbital theory",
    "Spectroscopic selection rules",
    "Statistical thermodynamics",
    "Electrochemistry and Nernst equation",
    "Surface chemistry and catalysis",
    "Transport properties",
], chapters_per_unit=16)

inorganic = expand_subject("Inorganic Chemistry", [
    "Atomic structure and periodic trends",
    "Chemical bonding in molecules",
    "Symmetry and point groups",
    "Crystal field and ligand field theory",
    "Organometallic fundamentals",
    "Main group chemistry",
    "Transition metal coordination",
    "Bioinorganic chemistry",
    "Solid state materials",
    "Nanomaterials introduction",
], chapters_per_unit=16)

analytical = expand_subject("Analytical Chemistry", [
    "Sampling and data quality",
    "Calibration and validation",
    "Titrimetric methods",
    "Gravimetric analysis",
    "Electroanalytical methods",
    "Chromatography fundamentals",
    "HPLC and GC practice",
    "Mass spectrometry basics",
    "Quality assurance",
], chapters_per_unit=14)

spectroscopy = expand_subject("Spectroscopy", [
    "Electromagnetic spectrum overview",
    "UV-Vis absorption",
    "Beer-Lambert law applications",
    "IR spectroscopy and group frequencies",
    "Raman spectroscopy",
    "NMR — chemical shift and integration",
    "NMR — coupling and COSY",
    "13C and 2D NMR",
    "Mass spectrometry fragmentation",
    "Structure elucidation workflows",
], chapters_per_unit=14)

biochem = expand_subject("Biochemistry", [
    "Amino acids and proteins",
    "Enzyme kinetics — Michaelis-Menten",
    "Carbohydrate structure",
    "Lipids and membranes",
    "Metabolic pathways overview",
    "Glycolysis and gluconeogenesis",
    "Citric acid cycle",
    "Oxidative phosphorylation",
    "Nucleic acids",
], chapters_per_unit=14)

organometallic = expand_subject("Organometallic Chemistry", [
    "18-electron rule and counting",
    "Oxidative addition and reductive elimination",
    "Insertion reactions",
    "Cross-coupling mechanisms",
    "Homogeneous catalysis",
    "Metathesis",
    "C-H activation",
], chapters_per_unit=16)

polymer = expand_subject("Polymer Chemistry", [
    "Polymer architecture",
    "Step-growth polymerization",
    "Chain-growth and radical polymerization",
    "Living polymerizations",
    "Copolymerization",
    "Characterization of polymers",
], chapters_per_unit=14)

medicinal = expand_subject("Medicinal Chemistry", [
    "Drug targets and lead discovery",
    "Structure-activity relationships",
    "Pharmacokinetics ADME",
    "Enzyme inhibitors",
    "Receptor ligand design",
    "Bioisosteres",
], chapters_per_unit=14)

environmental = expand_subject("Environmental Chemistry", [
    "Atmospheric chemistry",
    "Water chemistry",
    "Green chemistry principles",
    "Persistent pollutants",
    "Remediation strategies",
], chapters_per_unit=12)

computational = expand_subject("Computational Chemistry", [
    "Potential energy surfaces",
    "Semi-empirical methods",
    "Hartree-Fock and DFT intro",
    "Basis sets",
    "Conformational search",
    "Transition state optimization",
], chapters_per_unit=12)

foundations = expand_subject("Foundations for MSc Chemistry", [
    "Mathematical tools for chemistry",
    "Units, significant figures, errors",
    "Laboratory safety",
    "Scientific literature literacy",
    "Writing lab reports and theses",
], chapters_per_unit=10)

curriculum = {
    "subjects": [
        foundations,
        subject("Organic Reaction Mechanisms", mech_units),
        subject("Organic Synthesis", synth_units),
        physical,
        inorganic,
        analytical,
        spectroscopy,
        biochem,
        organometallic,
        polymer,
        medicinal,
        environmental,
        computational,
    ]
}


def count_chapters(data):
    n = 0
    for s in data["subjects"]:
        for u in s["units"]:
            n += len(u["chapters"])
    return n


if __name__ == "__main__":
    OUT.write_text(json.dumps(curriculum, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} with {count_chapters(curriculum)} chapters")

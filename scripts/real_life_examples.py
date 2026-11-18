"""Real-life example lookup for every chemistry concept."""

from __future__ import annotations

import hashlib
import re

# Keyword (lowercase substring) -> real-life example paragraph
KEYWORD_EXAMPLES: dict[str, str] = {
    "nucleophil": "Soap removes grease because the carboxylate head (nucleophile) attacks ester bonds in cooking fats — the same electron-donation logic drives SN2 in the lab.",
    "electrophil": "Formaldehyde in pressed-wood furniture acts as an electrophile that cross-links proteins; your body detects it as an irritant because it reacts with nucleophilic sites on tissue.",
    "sn2": "Inverting an umbrella in wind is like Walden inversion: the nucleophile must approach from the backside. Primary alkyl halides react fast; tertiary ones are too crowded — like trying to thread a needle in a packed crowd.",
    "sn1": "Dissolving menthol candy slowly in warm water: first the ion pair forms (slow), then water captures the carbocation (fast). Rate depends on candy size, not how much water you add — first-order kinetics.",
    "walden": "Chiral drug molecules rotate plane-polarized light; SN2 inversion at a stereocenter flips R to S — why a wrong enantiomer of thalidomide caused birth defects while the other did not.",
    "steric": "Bulky luggage blocks a narrow train door — same reason tert-butyl blocks SN2. Bulkier bases (t-BuO-) favor Hofmann elimination over Zaitsev in crowded molecules.",
    "bimolecular": "Rate of a crowded checkout depends on both customers and cashiers — second-order kinetics: doubling both doubles the rate, like SN2 needing both nucleophile and substrate.",
    "leaving group": "A bad leaving group is like a weak handshake — the bond won't break. Iodide leaves easily (weak bond); fluoride rarely leaves. That's why HI promotes substitution better than HF.",
    "carbocation": "Octane rating in petrol relates to smooth combustion; branched alkanes resist forming unstable primary carbocations during engine knocking — stability rules matter outside the lab too.",
    "e2": "Dehydrating fruit in the sun removes H and OH (conceptually like elimination) to preserve food — E2 needs aligned H and leaving group, like aligned gears before they mesh.",
    "e1": "Old plastic yellowing in sunlight: UV can cleave bonds, forming cations that rearrange — E1-type ionization appears in polymer degradation in everyday materials.",
    "zaitsev": "When cracking hydrocarbons in refineries, the more substituted alkene is often thermodynamically favored — the same Zaitsev preference that governs elimination in textbooks.",
    "markovnikov": "Adding water to an alkene in acid (Markovnikov) mirrors how some pro-drugs are activated in the stomach — the electrophile adds where the existing alkyl group stabilizes charge.",
    "hydroboration": "Anti-Markovnikov alcohol formation is used to make detergents and plastics from alkenes — industrial plants run hydroboration-oxidation at tonne scale.",
    "diels-alder": "Natural product biosynthesis and some polymer cross-linking follow pericyclic logic; retro-Diels-Alder releases furan from some heated food packaging adhesives under extreme heat.",
    "grignard": "Your car's magnesium alloy wheels resist corrosion partly because surface Mg behaves similarly — Grignard reagents (RMgX) build C–C bonds in pharmaceutical factories worldwide.",
    "wittig": "Vitamin A and many fragrance molecules are made using Wittig olefinations — the double bond you smell in a rose may trace back to a phosphonium ylide step.",
    "aldol": "Honey browning (Maillard-adjacent chemistry) and metabolic gluconeogenesis both involve enolate-type carbonyl chemistry — aldol logic connects kitchen and liver.",
    "michael": "Conjugate addition appears in making acrylic paints and soft contact lenses — Michael acceptors (α,β-unsaturated carbonyls) are industrial staples.",
    "friedel-crafts": "Detergent alkylbenzenes (LAB) are made by Friedel-Crafts alkylation at petrochemical plants — the sulfonate in your laundry liquid starts here.",
    "aromatic": "Paracetamol, aspirin, and dyes in your clothes are aromatic rings with directing groups — EAS rules predict where nitration installs the next substituent in dye manufacture.",
    "snar": "Chloroquinoline antimalarials and some herbicides undergo nucleophilic aromatic substitution — electron-withdrawing groups activate the ring toward attack, like a door held open.",
    "radical": "Free-radical chain reactions age your skin (UV + O2), cure dental composites (peroxide initiators), and bleach hair (H2O2 + melanin radicals).",
    "carbene": "Carbenes insert into C–H bonds in some drug syntheses; glow sticks use related high-energy intermediates (though not free carbenes) — short-lived reactive species matter in daily products.",
    "stereochem": "Mirror-image limonene smells like orange (R) vs pine (S) — stereochemistry is not abstract; it's why enantiopure drugs cost more to manufacture.",
    "retrosynth": "Planning a multi-step drug route is like planning a road trip with toll booths: disconnect the target into milestones you can buy commercially — chemists call those synthons.",
    "protecting group": "Masking tape before painting is a protecting group: cover the alcohol (wall trim), paint the ester (wall), then remove tape (deprotection) without damaging either.",
    "cross-coupling": "Suzuki coupling built the OLED pixels in your phone screen and many blockbuster drugs — palladium connects fragments the way a welder joins metal pipes.",
    "suzuki": "Blockbuster drugs like valsartan and many agrochemicals use Suzuki-Miyaura coupling in manufacturing — Pd connects aryl boronic acids to halides under mild conditions.",
    "heck": "Heck coupling makes styrene-based polymers and fine chemicals; the Pd cycle is why a tiny amount of catalyst converts tons of starting material in factories.",
    "hydrogenation": "Margarine from vegetable oil uses catalytic hydrogenation (Pd or Ni) to saturate double bonds — same principle as reducing an alkene in the lab, different scale.",
    "oxidation": "Apple slices brown via enzymatic oxidation (polyphenol oxidase); Swern and PCC in the lab selectively oxidize alcohols to carbonyls for drug intermediates.",
    "reduction": "Iron smelting reduces Fe2O3 to metal; LiAlH4 reduces esters in the lab to make alcohol APIs — electron addition is universal from blast furnaces to flasks.",
    "metathesis": "Olefin metathesis reshuffles alkene fragments in ring-opening polymerization of norbornene-derived plastics and in some fragrance syntheses — Nobel Prize chemistry in your tires and perfumes.",
    "thermodynam": "Refrigerators exploit ΔG = ΔH − TΔS: compressing gas releases heat outside, expanding inside absorbs heat — second law limits efficiency, same as equilibrium constants in reactions.",
    "entropy": "A messy room has higher entropy; spontaneous mixing of perfume in air is ΔS > 0. Entropy drives dissolution of salt in soup and phase changes in ice cream melting.",
    "kinetics": "Medicine shelf life: aspirin hydrolysis rate doubles roughly every 10 °C — Arrhenius kinetics decide expiry dates on pharmacy labels.",
    "equilibrium": "Haemoglobin + O2 ⇌ HbO2 in your blood is Le Chatelier in action: high altitude shifts binding, same logic as gas-phase equilibrium problems.",
    "quantum": "Blue LED colour comes from band gaps (quantum confinement in GaN); sunscreen UV filters absorb photons via electronic transitions you calculate with MO theory.",
    "spectroscop": "MRI in hospitals is NMR of protons in water; airport scanners use IR/backscatter — spectroscopy is medical imaging and security, not just peak assignments.",
    "nmr": "MRI is proton NMR in a magnet big enough for a person — chemical shift maps tissue water; coupling patterns diagnose molecular structure in pharma QC labs.",
    "ir": "Police breathalysers and greenhouse gas monitors use IR absorption; your TV remote sends IR pulses — bond vibrations absorb specific wavelengths.",
    "mass spec": "Airport explosive trace detectors and doping tests in sports use MS fragmentation patterns — same logic as identifying unknown lab samples.",
    "chromatograph": "Coffee decaffeination and blood alcohol tests use chromatography — separation by affinity, whether HPLC in a lab or GC at a traffic checkpoint.",
    "titration": "Pool pH kits and wine acidity tests are titrations — adding base dropwise until indicator flips colour, exactly like an analytical lab session.",
    "electrochem": "Phone lithium-ion batteries, car lead-acid batteries, and corrosion on iron gates all run on Nernst equation electrochemistry — E° drives whether metal rusts or charges.",
    "crystal field": "Gemstone colours (emerald green from Cr3+ in beryllium aluminate) come from crystal-field splitting of d-orbitals — inorganic colour is physics in a lattice.",
    "coordination": "Haemoglobin is an Fe2+ coordination complex; cisplatin binds DNA via Pt–N coordination to treat cancer — coordination chemistry is literally life and death medicine.",
    "organometallic": "Catalytic converters use Rh/Pd to convert CO and NOx to safer gases; the same metal-ligand concepts you study govern urban air quality.",
    "polymer": "Nylon in socks, PET in water bottles, and PVC in pipes are step- or chain-growth polymers — degree of polymerization controls whether plastic is brittle or flexible.",
    "enzyme": "Lactase pills let lactose-intolerant people drink milk because the enzyme cleaves the disaccharide — Michaelis-Menten kinetics describe how fast it works at your gut pH.",
    "metabol": "Marathon runners 'hit the wall' when glycogen runs low — glycolysis, TCA cycle, and oxidative phosphorylation are the metabolic map your muscles burn in real time.",
    "protein": "COVID vaccines deliver mRNA instructing ribosomes to build spike protein — understanding amino acid chemistry explains folding, denaturation in cooked egg white, and drug targets.",
    "green chem": "Biodegradable detergents and solvent-free paint use green chemistry metrics — atom economy matters to companies because waste is literal money lost.",
    "medicinal": "Blood pressure pills (ACE inhibitors) mimic natural peptide structure; SAR studies swap one substituent to reduce side effects — medicinal chemistry is tailored molecular editing.",
    "environment": "Acid rain from SO2, ozone hole from CFCs, and microplastics in oceans are environmental chemistry case studies with direct policy impact — not textbook fiction.",
    "computational": "Drug companies simulate protein docking before synthesis; your phone chip materials were screened with DFT — computational chemistry saves billions in failed experiments.",
    "ph": "Shampoo pH ~5.5 matches scalp; antacids neutralize stomach HCl; soil pH decides which plants grow — acid-base chemistry is household and agricultural.",
    "buffer": "Blood bicarbonate buffer keeps pH 7.4 despite CO2 from metabolism; sports drink 'electrolytes' mimic buffer capacity — Henderson-Hasselbalch in your veins.",
    "catalyst": "Enzymes in yeast ferment bread and beer; Pt in car exhaust neutralizes pollutants — catalysts lower activation energy everywhere from kitchen to highway.",
    "isotope": "Carbon-14 dating of archaeological artefacts, PET scans using F-18 fluorodeoxyglucose, and D2O in NMR solvents — isotopes trace history and disease.",
    "conjugate": "Acrylic acid in superabsorbent nappies polymerizes through conjugate systems; Michael addition installs side chains in many polymer recipes.",
    "umpolung": "Cyanide as a synthetic equivalent of CO2− is umpolung — in nature, thiamine (vitamin B1) does biological umpolung in pyruvate decarboxylation when you breathe after exercise.",
    "symmetry": "Snowflake six-fold symmetry and crystal X-ray diffraction both use point groups — symmetry predicts IR activity and whether a molecule has a dipole (microwave absorption in water).",
    "fluorescen": "Highlighter ink and forensic blood detection (luminol-adjacent) use conjugated π systems that absorb UV and emit visible light — quantum selection rules in stationery.",
}

SUBJECT_POOLS: dict[str, list[str]] = {
    "Organic Reaction Mechanisms": [
        "Pan-frying creates new C–C and C=O bonds via Maillard reactions — mechanistic thinking (who attacks whom?) explains browning better than memorizing one reaction.",
        "Local anaesthetics like lidocaine block sodium channels; their synthesis requires SN2, acylation, and aromatic substitution — each step has a mechanism you can arrow-push.",
        "Insect repellent DEET and sunscreen avobenzone are organic molecules whose stability and reactivity in sunlight follow the same orbital arguments as exam problems.",
        "Penicillin's β-lactam ring opens by nucleophilic acyl substitution at bacterial enzymes — antibiotic resistance often mutates that mechanistic step.",
        "Ethanol fermentation and industrial ethylene hydration both make alcohols, but via completely different mechanisms — comparing them builds real mechanistic literacy.",
    ],
    "Organic Synthesis": [
        "Paracetamol production at scale uses acetylation of p-aminophenol — a two-step synthesis millions of doses depend on daily.",
        "Ibuprofen was redesigned for greener synthesis (Boots → BHC route) cutting waste — retrosynthesis directly reduced factory solvent tonnes.",
        "Vanillin from lignin vs vanilla orchid: two synthetic routes to the same flavour molecule — route choice affects cost, sustainability, and label 'natural' claims.",
        "Nylon-6,6 production connects adipic acid and hexamethylenediamine — industrial multistep synthesis you can walk through like a retrosynthesis problem.",
        "Taxol (paclitaxel) cancer drug forced chemists to invent semisynthesis from yew needles — total synthesis strategy when natural supply cannot meet demand.",
    ],
    "Physical Chemistry": [
        "Pressure cookers raise boiling point via Clausius-Clapeyron — thermodynamics cooks dal faster at higher T.",
        "Self-heating coffee cans use exothermic hydration of lime (ΔH < 0) — enthalpy in a can.",
        "Lithium battery fire risk: thermal runaway when ΔG for decomposition goes negative — kinetics + thermodynamics explain airline restrictions.",
        "Cloud formation: supersaturation and nucleation kinetics — physical chem of water vapour decides rain vs drought.",
        "Photosynthesis quantum efficiency (~90% in light harvesting) inspires solar cell design — spectroscopy and energy transfer theory in leaves.",
    ],
    "Inorganic Chemistry": [
        "Hemoglobin vs carbon monoxide: CO binds Fe2+ tighter than O2 — coordination chemistry explains silent poisoning.",
        "Titanium dioxide in sunscreen and self-cleaning glass — band gap and surface catalysis from inorganic solids.",
        "Liquid mercury in old thermometers; safer Ga-In alloys today — periodic trends and toxicity drive material substitution.",
        "Zeolite catalysts crack crude oil in refineries — aluminosilicate frameworks shape selectivity for petrol fractions.",
        "LED phosphors (Eu2+ in YAG) make white light from blue chips — lanthanide f-f transitions colour your room.",
    ],
    "Analytical Chemistry": [
        "Glucose test strips use enzymatic electrochemical detection — calibration curves match lab standard addition you practice.",
        "Melamine-in-milk scandal detected by Kjeldahl nitrogen vs true protein assays — analytical fraud detection saved lives.",
        "COVID lateral flow tests: antibody–antigen binding with colour readout — qualitative assay logic like TLC with known standards.",
        "Heavy metal in rice (arsenic from groundwater) tracked by ICP-MS — speciation analysis informs food safety law.",
        "Wine 'legs' and refractometry for sugar content — simple to advanced analytical tools in food.",
    ],
    "Spectroscopy": [
        "Breathalysers measure ethanol IR absorption; police and pub safety depend on Beer-Lambert law.",
        "Hospital MRI maps proton density and relaxation — 2D NMR pulse sequences scaled up to human size.",
        "Art forgery detection uses Raman/IR on pigment layers — spectroscopy authenticates Rembrandt vs replica.",
        "Smoke detectors use americium ionization; IR cameras find heat leaks in homes — electromagnetic spectrum in safety devices.",
        "Shazam identifies songs by fingerprinting spectra of audio — same 'pattern matching' mindset as MS library search.",
    ],
    "Biochemistry": [
        "Insulin pens deliver a protein whose disulfide bonds must fold correctly — misfolding causes diabetes treatment failure.",
        "Statins inhibit HMG-CoA reductase — enzyme inhibitor mechanism lowers cholesterol in millions of patients.",
        "Gluten intolerance vs coeliac: peptide epitopes trigger immune response — amino acid sequence chemistry in bread.",
        "CRISPR gene editing cuts DNA with guided RNA — biochemistry toolkit that won the Nobel and changed medicine.",
        "Sports supplements and creatine phosphate buffer muscle ATP — metabolic pathways under physical load.",
    ],
    "Organometallic Chemistry": [
        "Cativa process (iridium) makes acetic acid from methanol — homogeneous catalysis feeds vinegar and polymer feedstocks.",
        "Sharpless epoxidation made anti-ulcer drug esomeprazole economically — asymmetric organometallic catalysis in pharma.",
        "Wilkinson's catalyst hydrogenates fats in industry — same H2 addition logic as margarine on your toast.",
        "Grubbs ruthenium catalysts in ROMP make advanced materials — metathesis in tyres and biocompatible devices.",
        "Cross-coupling built OLED displays and late-stage drug diversification — Pd cycles at ton scale.",
    ],
    "Polymer Chemistry": [
        "Superglue (cyanoacrylate) anionic polymerization bonds skin in emergencies — chain growth in seconds.",
        "Biodegradable PLA from corn starch in compostable cups — step vs chain growth decides degradability.",
        "Tyre rubber vulcanization cross-links sulfur — network polymer mechanics vs thermoplastic bags.",
        "DNA is a biological polymer whose melting temperature Tm depends on GC content — polymer phys-chem in genetics kits.",
        "3D-printing photopolymers cure by radical chain growth when UV hits — additive manufacturing chemistry.",
    ],
    "Medicinal Chemistry": [
        "Penicillin to cephalosporins: β-lactam SAR resists bacterial β-lactamase — each structural tweak is a medicinal chemistry decision.",
        "Opioid crisis: fentanyl potency from lipophilicity and receptor binding — small structural changes, massive real-world impact.",
        "Antihistamines (cetirizine) block H1 receptors — SAR removed sedating side effects of first-generation drugs.",
        "Prodrug oseltamivir (Tamiflu) activated by liver esterases — FGI strategy in flu treatment.",
        "Kinase inhibitors in cancer (imatinib) designed from ATP-binding site geometry — structure-based drug design.",
    ],
    "Environmental Chemistry": [
        "Flint, Michigan lead pipes leached Pb2+ into drinking water — solubility and redox chemistry in a city crisis.",
        "CFCs thinned ozone; Montreal Protocol replaced them — atmospheric kinetics repaired the hole.",
        "Fertilizer runoff causes eutrophication and dead zones — nitrogen cycle chemistry in Gulf of Mexico.",
        "Carbon capture amines bind CO2 from power plants — acid-base and equilibrium in climate tech.",
        "Microplastics in bottled water detected by FTIR/Raman — environmental analytical chemistry in daily consumption.",
    ],
    "Computational Chemistry": [
        "AlphaFold predicts protein structure from sequence — quantum-informed force fields changed biology.",
        "Battery electrolyte additives screened by DFT before synthesis — Samsung and Tesla R&D pipelines.",
        "Drug–protein docking scores guide medicinal chemists before wet lab — saves months per candidate.",
        "Atmospheric OH radical lifetime models smog — computational kinetics informs emission laws.",
        "Materials Project database lets engineers pick cathode materials for EVs — DFT band gaps in product design.",
    ],
    "Foundations for MSc Chemistry": [
        "Pharmacy doses use significant figures — 10 mg vs 10.0 mg errors harm patients; units matter in IV drips.",
        "COVID lab PCR reports cycle threshold (Ct) — logarithmic scales and error bars in news you read daily.",
        "Material Safety Data Sheets (MSDS) in every lab mirror household bleach storage rules — risk communication is chemistry literacy.",
        "Reading nutrition labels (% RDA, mole of Na+ vs 'salt') connects stoichiometry to blood pressure advice.",
        "Peer review and retracted papers (e.g. fraudulent water memory) show why literature literacy prevents pseudoscience belief.",
    ],
}


def _hash_pick(key: str, pool: list[str]) -> str:
    idx = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(pool)
    return pool[idx]


def lookup_example(
    concept: str,
    subject: str,
    unit: str = "",
    title: str = "",
    level: str = "beginner",
) -> str:
    """Return a real-life example paragraph for any concept string."""
    concept_lower = concept.lower()

    # Pass 1: match keywords against the concept name only (most specific)
    for keyword, example in KEYWORD_EXAMPLES.items():
        if keyword in concept_lower:
            return example

    # Pass 2: match against unit name (broader context)
    unit_lower = unit.lower()
    for keyword, example in KEYWORD_EXAMPLES.items():
        if keyword in unit_lower:
            return example

    # Pass 3: match against chapter title (avoid sn2/sn1 hijacking unrelated concepts)
    title_lower = title.lower()
    title_keywords = ["sn1", "sn2", "e1", "e2", "diels", "grignard", "wittig", "aldol", "michael",
                      "friedel", "radical", "carbene", "retrosynth", "protecting", "spectroscop",
                      "nmr", "polymer", "enzyme", "thermodynam", "equilibrium", "kinetics"]
    for keyword, example in KEYWORD_EXAMPLES.items():
        if keyword in title_lower and keyword in title_keywords:
            return example

    pool = SUBJECT_POOLS.get(subject, SUBJECT_POOLS["Foundations for MSc Chemistry"])
    base = _hash_pick(f"{subject}:{concept}:{unit}", pool)

    level_extra = {
        "beginner": f" Everyday link: notice how {concept.lower()} shows up when you cook, clean, or take medicine — start there before opening your notebook.",
        "intermediate": f" Industry link: manufacturing and QC labs test {concept.lower()} daily — exam questions mirror those troubleshooting decisions.",
        "advanced": f" Research link: patent filings and process chemists optimize {concept.lower()} because a 1% yield change can mean millions of dollars at scale.",
    }
    return base + level_extra.get(level, level_extra["beginner"])


def chapter_hook(subject: str, title: str, unit: str) -> str:
    """Opening real-life hook for entire chapter."""
    pool = SUBJECT_POOLS.get(subject, SUBJECT_POOLS["Foundations for MSc Chemistry"])
    hook = _hash_pick(f"hook:{title}:{unit}", pool)
    return (
        f"Before diving into **{title}**, anchor it in something real: {hook} "
        f"This chapter connects every concept below to similar everyday or industrial situations."
    )


def mechanism_real_life(title: str, mechanism: str) -> str:
    """Real-life tie-in for mechanism sections."""
    t = title.lower()
    if "sn2" in t:
        return "Pharmaceutical factories use SN2 to install chiral centers in API synthesis — one inversion event can determine drug enantiomer purity regulated by FDA/EMA."
    if "sn1" in t or "carbocation" in t:
        return "Tert-butyl alcohol from petrochemical isobutylene goes through carbocation chemistry at scale — SN1/E1 competition decides product distribution in refinery side streams."
    if "e2" in t or "elimination" in t:
        return "Dehydrohalogenation makes alkenes for polyethylene production — elimination conditions in plants mirror E2/E1 choices you study."
    if "diels" in t:
        return "Natural product total syntheses (e.g. steroids) use Diels-Alder to build rings found in hormones you produce daily."
    if "radical" in t:
        return "Radical polymerization makes PVC pipes in buildings and PMMA in glasses — chain initiation with peroxides is industrial radical chemistry."
    if "addition" in t and "carbonyl" in t:
        return "Grignard additions scale to tonnage for alcohol intermediates in vitamin and fragrance supply chains."
    if "aromatic" in t or "friedel" in t:
        return "Paracetamol, ibuprofen, and dyes all require controlled aromatic substitution — wrong regiochemistry means wrong drug or wrong colour."
    return (
        "Every arrow you draw models electron flow that also happens in catalytic converters, "
        "drug metabolism in your liver, and food spoilage — mechanisms are universal, not exam-only."
    )


def synthesis_real_life(title: str, synthesis: str | None) -> str:
    """Real-life tie-in for synthesis sections."""
    t = title.lower()
    if "retrosynth" in t or "disconnection" in t:
        return "Process chemists at Sun Pharma, Pfizer, or Dr. Reddy's plan retrosynthetic trees before building pilot plants — your homework mirrors billion-dollar decisions."
    if "protecting" in t:
        return "Multi-step API routes protect one alcohol while reacting another — like masking a doorframe when painting a room, but at molecular scale in GMP suites."
    if "total synthesis" in t:
        return "When natural disaster disrupts yew tree supply, semisynthesis of paclitaxel from 10-deacetylbaccatin III kept cancer treatment available — total synthesis strategy saves lives."
    if "grignard" in t or "wittig" in t or "suzuki" in t:
        return f"Named reactions in this chapter appear in patents for agrochemicals, OLED materials, and blockbusters — {title} is not historical trivia."
    if "multi-step" in t:
        return "A generic drug must match innovator impurity profile — multi-step synthesis design includes purifying intermediates regulators will audit."
    return (
        "Industrial route selection weighs cost, waste (E-factor), safety, and patent freedom — "
        "the same criteria you apply when comparing retrosynthetic options."
    )


def worked_example_real_life(subject: str, title: str, level: str) -> str:
    """Real-life scenario for worked examples."""
    scenarios = {
        "Organic Reaction Mechanisms": {
            "beginner": "A patient metabolizes ibuprofen in the liver via oxidation and conjugation — trace the first bond-breaking step as if it were your SN1/SN2 problem.",
            "intermediate": "Batch contamination in a pharma plant gives wrong diastereomer — use mechanism evidence (rate, solvent, stereochemistry) to locate the faulty step.",
            "advanced": "Design a greener route to an anaesthetic intermediate avoiding carcinogenic alkylating agents — mechanism choice affects worker safety regulations.",
        },
        "Organic Synthesis": {
            "beginner": "Plan synthesis of aspirin from salicylic acid — compare your route to what Bayer scaled in 1899.",
            "intermediate": "Semisynthesize vitamin C from glucose (Reichstein process) — identify strategic disconnections in a real industrial flowchart.",
            "advanced": "Propose a 5-step route to an antiviral fragment under green chemistry constraints — justify each reagent with E-factor and toxicity data.",
        },
    }
    subj = scenarios.get(subject)
    if subj:
        return subj.get(level, subj["beginner"])
    generic = {
        "beginner": f"Explain how {title} appears in a product you used today (food, phone, medicine, or clothing).",
        "intermediate": f"A news headline mentions {subject.lower()} — describe which concept from this chapter helps you evaluate the claim critically.",
        "advanced": f"Propose how improving understanding of {title} could reduce waste, cost, or toxicity in an industrial process.",
    }
    return generic[level]

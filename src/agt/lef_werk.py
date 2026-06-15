"""Canonical LEF -> WERK v0.7 qualification architecture."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

LEF_WERK_SIGNATURE: list[str] = [
    "~",
    "⨁",
    "⟁",
    "✨",
    "➤",
    "◍",
    "⟴",
    "⨂",
    "❍",
    "☉",
    "☌",
    "◈",
    "🜂",
    "🜄",
    "🜁",
    "🜃",
    "🜚",
    "⚶",
    "⚘",
    "☍",
    "☯",
    "🜙",
    "🜛",
    "🜜",
]

QUALIFICATION_BLOCKS: dict[str, dict[str, Any]] = {
    "Metatheory": {
        "pt": "Metateoria",
        "range": (1, 8),
        "glifos": LEF_WERK_SIGNATURE[0:8],
    },
    "Objectivity": {
        "pt": "Objetividade",
        "range": (9, 16),
        "glifos": LEF_WERK_SIGNATURE[8:16],
    },
    "Intersubjectivity": {
        "pt": "Intersubjetividade",
        "range": (17, 24),
        "glifos": LEF_WERK_SIGNATURE[16:24],
    },
}

INVARIANTS: list[str] = [
    "WERK_JAMAIS_WILLE",
    "AUSEINANDERSETZUNG_NOT_AUFHEBUNG",
    "AGI_AS_TRANSCENDENTAL_HYPOTHESIS",
    "OBJECTIVITY_AS_INTERSUBJECTIVITY",
    "NO_QUALIFICATION_BLOCK_TO_MLE_MAPPING",
    "DATED_SUBSTITUTION_RECORD_REQUIRED",
]

SUBSTITUTION_RECORD: dict[str, str] = {
    "date": "2026-06-15",
    "what": (
        "The public qualification axis is not Mythos/Logos/Ethos and is not a "
        "1:1 mapping from Mythos to Ausdruck, Logos to Darstellung, and Ethos "
        "to Bedeutung."
    ),
    "how": (
        "It is replaced by Metatheory/Objectivity/Intersubjectivity as "
        "literary-academic blocks, while WERK remains within Logos in the "
        "technical Decision 140426 sense."
    ),
    "why": (
        "The substitution prevents category collapse between qualification "
        "architecture and EML technical syntax, preserving Werk rather than Wille."
    ),
}

_FORBIDDEN_BLOCK_NAMES = {"Mythos", "Logos", "Ethos"}

_GLIFO_METADATA: dict[int, dict[str, Any]] = {
    1: {
        "number": "GL01",
        "glifo": "~",
        "title": "The metatheoretical necessity of cognition: faculties and functions.",
        "block": "Metatheory",
        "role": "Opens the tribunal of objectivity as intersubjectivity.",
        "risk_blocked": "Treating intelligence as empirical performance only.",
        "anchors": ["Friedman", "Porta", "Cassirer ECW 4", "Kantian tribunal"],
        "authorial_foundation": 'Dissertation and "O Elo" article.',
        "description": (
            "Intelligence becomes philosophically tractable when its validity claims "
            "can be reconstructed, communicated, and criticized in a common world."
        ),
    },
    2: {
        "number": "GL02",
        "glifo": "⨁",
        "title": "Metaphysics of life as symbolic series.",
        "block": "Metatheory",
        "role": "Series, not final totality.",
        "risk_blocked": "Global Aufhebung.",
        "anchors": ["Disposition 1917", "Reihe selbst", "focus imaginarius", "ECN 1"],
        "authorial_foundation": "Dissertation on psychosocial teleology.",
        "description": (
            "Symbolic life is a finite, regulative series of objectivations, not the "
            "possession of a completed absolute."
        ),
    },
    3: {
        "number": "GL03",
        "glifo": "⟁",
        "title": "Haptic realism: analytic of understanding, not ontology.",
        "block": "Metatheory",
        "role": "Anti-literalist discipline of models.",
        "risk_blocked": "Model = mind / computation = ontology.",
        "anchors": ["Chirimuuta", "misplaced concreteness", "Cassirer ECW 13"],
        "authorial_foundation": "Thesis introduction and Chirimuuta integration.",
        "description": (
            "Models orient complex phenomena without becoming the things they model; "
            "their conditions of use must remain public and revisable."
        ),
    },
    4: {
        "number": "GL04",
        "glifo": "✨",
        "title": "Newton and Einstein: transcendental method and scientific world.",
        "block": "Metatheory",
        "role": "Objectivity as functional reconstruction.",
        "risk_blocked": "Data accumulation = objectivity.",
        "anchors": ["Cassirer ECW 10", "Cassirer ECW 19", "Friedman", "Pringe"],
        "authorial_foundation": "Undergraduate thesis on Einstein and Cassirer and BEPE.",
        "description": (
            "Scientific objectivity is reconstructed through functional invariants "
            "and symbolic mediation, not accumulated as uninterpreted data."
        ),
    },
    5: {
        "number": "GL05",
        "glifo": "➤",
        "title": "Sense, imagination and understanding in Kant.",
        "block": "Metatheory",
        "role": "Synthesis as condition of cognition.",
        "risk_blocked": "Raw-data empiricism and computational reduction.",
        "anchors": ["KrV A78/B103", "KrV A778-781/B806-809", "Longuenesse"],
        "authorial_foundation": '"O Elo" and BEPE.',
        "description": (
            "Cognition requires synthesis among sensibility, imagination, and "
            "understanding; raw inputs alone do not yield objectivity."
        ),
    },
    6: {
        "number": "GL06",
        "glifo": "◍",
        "title": "Objective and subjective deduction: expansion of the Philosophy of Symbolic Forms.",
        "block": "Metatheory",
        "role": "Repraesentation as functional genus.",
        "risk_blocked": "Glifo as private code instead of public function.",
        "anchors": ["Cassirer ECW 6", "Cassirer ECW 13", "Disposition 1917", "Moeckel"],
        "authorial_foundation": "Article on symbolic functions.",
        "description": (
            "Private marks count philosophically only when converted into public "
            "functions of representation."
        ),
    },
    7: {
        "number": "GL07",
        "glifo": "⟴",
        "title": "The three transcendental ideas: soul, world and God.",
        "block": "Metatheory",
        "role": "Negative discipline of intelligence.",
        "risk_blocked": "Artificial soul, total internet-world, technical God.",
        "anchors": ["KrV A329/B386", "KrV B426-428", "KrV A644/B672"],
        "authorial_foundation": '"O Elo" and thesis chapter on transcendental ideas.',
        "description": (
            "The ideas of soul, world, and God discipline intelligence regulatively "
            "by blocking their conversion into technical objects."
        ),
    },
    8: {
        "number": "GL08",
        "glifo": "⨂",
        "title": "The system of the three symbolic functions of consciousness.",
        "block": "Metatheory",
        "role": "WERK becomes aware of its own position in Logos.",
        "risk_blocked": "Confusing Mythos-Clemente with Cassirerian myth.",
        "anchors": ["Cassirer ECW 11", "Cassirer ECW 12", "Cassirer ECW 13", "Decision 140426"],
        "authorial_foundation": "Dissertation and article on symbolic functions.",
        "description": (
            "Cassirerian myth is tri-functional, Ausdruck-dominant, and already a "
            "symbolic form. WERK operates within Logos in the technical 140426 sense."
        ),
    },
    9: {
        "number": "GL09",
        "glifo": "❍",
        "title": "Works of spirit as forms of objectivity.",
        "block": "Objectivity",
        "role": "Objectivity as cultural Werk.",
        "risk_blocked": "Objectivity as copy or private projection.",
        "anchors": ["Cassirer ECW 24", "ECN 1", "functional ideal of truth"],
        "authorial_foundation": "Dissertation.",
        "description": (
            "Objectivity appears as culturally formed Werk rather than mirror-copy "
            "or subjective projection."
        ),
    },
    10: {
        "number": "GL10",
        "glifo": "☉",
        "title": "Technique of nature: teleological judgment and methodology.",
        "block": "Objectivity",
        "role": "Purposiveness as regulative.",
        "risk_blocked": "Machine purpose as ontology.",
        "anchors": ["Kant KU", "AA 5:431", "Guyer", "Goy and Watkins"],
        "authorial_foundation": "Dissertation and thesis.",
        "description": (
            "Purposiveness guides judgment methodologically without licensing an "
            "ontology of machine purposes."
        ),
    },
    11: {
        "number": "GL11",
        "glifo": "☌",
        "title": "Formative force and purposiveness in Kant.",
        "block": "Objectivity",
        "role": "Distinction between organism and machine.",
        "risk_blocked": "Biologizing AI by metaphor.",
        "anchors": ["AA 5:431", "Cassirer ECW 24", "Chirimuuta", "Hui"],
        "authorial_foundation": "Dissertation.",
        "description": (
            "The organism-machine distinction prevents biological metaphors from "
            "settling the status of artificial systems."
        ),
    },
    12: {
        "number": "GL12",
        "glifo": "◈",
        "title": "Spiritual automaton: Sellars, Brandom and normative space.",
        "block": "Objectivity",
        "role": "Normativity without machine Wille.",
        "risk_blocked": "Discursive participation = moral legislation.",
        "anchors": ["Sellars", "Brandom", "Negarestani", "space of reasons"],
        "authorial_foundation": "Doctoral thesis.",
        "description": (
            "Discursive participation can be modeled without transferring moral "
            "legislation to the machine."
        ),
    },
    13: {
        "number": "GL13",
        "glifo": "🜂",
        "title": "Form and technology: Cassirer against machine autonomization.",
        "block": "Objectivity",
        "role": "Technique as Werk, not leader.",
        "risk_blocked": "Autonomous technical sovereignty.",
        "anchors": ["Cassirer Form und Technik", "ECW 17", "technical mediation"],
        "authorial_foundation": "Thesis and Cassirer Form und Technik.",
        "description": (
            "Technique may serve freedom as Werk, but it cannot lead as sovereign "
            "source of ends."
        ),
    },
    14: {
        "number": "GL14",
        "glifo": "🜄",
        "title": "Symbolic AI and the problem of formal objectivation.",
        "block": "Objectivity",
        "role": "Computational symbols versus symbolic forms.",
        "risk_blocked": "Formal performance = world-possession.",
        "anchors": ["Bender", "Bommasani", "Buckner", "Negarestani"],
        "authorial_foundation": "Thesis.",
        "description": (
            "Formal symbol manipulation does not by itself amount to possession of "
            "a world or participation in all symbolic forms."
        ),
    },
    15: {
        "number": "GL15",
        "glifo": "🜁",
        "title": "AGI: Negarestani, Hui, Bostrom, Buckner and Chirimuuta.",
        "block": "Objectivity",
        "role": "AGI as transcendental hypothesis.",
        "risk_blocked": "AGI as artificial subject.",
        "anchors": ["Negarestani", "Hui", "Bostrom", "Buckner", "Chirimuuta"],
        "authorial_foundation": "Thesis.",
        "description": (
            "AGI remains a transcendental hypothesis for testing conditions of "
            "objectivity, public reconstruction, and technical mediation."
        ),
    },
    16: {
        "number": "GL16",
        "glifo": "🜃",
        "title": "Kant, machine and Hegelian organism.",
        "block": "Objectivity",
        "role": "Blocks machine as absolute organism.",
        "risk_blocked": "Hegelian organism / global Aufhebung.",
        "anchors": ["Hegel", "Hui", "Negarestani", "Plevrakis", "Gangle"],
        "authorial_foundation": "Thesis.",
        "description": (
            "The machine must not be elevated into an absolute organism or endpoint "
            "of dialectical completion."
        ),
    },
    17: {
        "number": "GL17",
        "glifo": "🜚",
        "title": "The Earth does not move: planetary thinking and koinos kosmos.",
        "block": "Intersubjectivity",
        "role": "Earth as finite common ground.",
        "risk_blocked": "Gaia as cosmic totality.",
        "anchors": ["Husserl", "Hui", "Chakrabarty", "koinos kosmos"],
        "authorial_foundation": "Thesis and BEPE.",
        "description": (
            "Planetary thinking keeps the common world finite, material, and shared "
            "rather than cosmically totalized."
        ),
    },
    18: {
        "number": "GL18",
        "glifo": "⚶",
        "title": "Confrontation between I and World: moral consciousness as consciousness of freedom.",
        "block": "Intersubjectivity",
        "role": "Auseinandersetzung as medium of freedom.",
        "risk_blocked": "Computation eliminating conflict.",
        "anchors": ["Kant KpV", "Kant KrV", "Cassirer ECW 13", "moral consciousness"],
        "authorial_foundation": "Dissertation and thesis.",
        "description": (
            "Freedom is mediated through confrontation between I and world, not "
            "through frictionless computational resolution."
        ),
    },
    19: {
        "number": "GL19",
        "glifo": "⚘",
        "title": "The technique of political myths.",
        "block": "Intersubjectivity",
        "role": "Pathological symbolic objectivation.",
        "risk_blocked": "Automated myth and symbolic servitude.",
        "anchors": ["Cassirer The Myth of the State", "ECW 25", "political myth"],
        "authorial_foundation": "Dissertation and thesis.",
        "description": (
            "Political myth shows how symbolic objectivation can become technical "
            "servitude when detached from critique."
        ),
    },
    20: {
        "number": "GL20",
        "glifo": "☍",
        "title": "Postulate and symbol of morality.",
        "block": "Intersubjectivity",
        "role": "Morality as practical-symbolic, not computable object.",
        "risk_blocked": "Alignment = moral conscience.",
        "anchors": ["Kant KpV", "Kant KU", "Beckenkamp", "Willaschek"],
        "authorial_foundation": "Thesis.",
        "description": (
            "Moral postulates and symbols orient practice without becoming objects "
            "computable by alignment alone."
        ),
    },
    21: {
        "number": "GL21",
        "glifo": "☯",
        "title": "Philosophical anthropology.",
        "block": "Intersubjectivity",
        "role": "Human being as animal symbolicum.",
        "risk_blocked": "Biologism and abstract posthumanism.",
        "anchors": ["Cassirer Essay on Man", "ECW 23", "Truwant", "Chirimuuta"],
        "authorial_foundation": "Dissertation.",
        "description": (
            "The human is reconstructed functionally as animal symbolicum, avoiding "
            "both reductive biologism and abstract posthumanism."
        ),
    },
    22: {
        "number": "GL22",
        "glifo": "🜙",
        "title": "Death of God and intersubjectivity.",
        "block": "Intersubjectivity",
        "role": "Absence of absolute foundation requires intersubjectivity.",
        "risk_blocked": "Machine-God.",
        "anchors": ["Negarestani", "Brassier", "Hofmann"],
        "authorial_foundation": "Thesis.",
        "description": (
            "Without an absolute foundation, validity must be reconstructed "
            "intersubjectively rather than reassigned to a technical absolute."
        ),
    },
    23: {
        "number": "GL23",
        "glifo": "🜛",
        "title": "Servitude and Revolution.",
        "block": "Intersubjectivity",
        "role": "Technique serves freedom but does not lead it.",
        "risk_blocked": "Werk becoming Wille.",
        "anchors": ["Cassirer ECW 17", "Negarestani", "Schoenecker", "Sanwoolu"],
        "authorial_foundation": "Thesis.",
        "description": (
            "Technique can be revolutionary only while serving freedom and remaining "
            "accountable to a realm of ends it does not institute."
        ),
    },
    24: {
        "number": "GL24",
        "glifo": "🜜",
        "title": "Physical and digital ecology.",
        "block": "Intersubjectivity",
        "role": "Plural symbolic, intersubjective, materially sustainable common world.",
        "risk_blocked": "Digital totality without Earth.",
        "anchors": ["KrV A644/B672", "KU als ob", "Hui", "Floridi"],
        "authorial_foundation": "Thesis and undergraduate thesis.",
        "description": (
            "The common world is physical and digital at once: plural, public, "
            "auditable, and materially sustainable."
        ),
    },
}


def validate_lef_werk_mapping() -> dict[str, object]:
    """Validate the canonical v0.7 qualification mapping."""

    errors: list[str] = []
    block_names = set(QUALIFICATION_BLOCKS)

    forbidden = block_names & _FORBIDDEN_BLOCK_NAMES
    if forbidden:
        errors.append(
            "Qualification blocks must not be named as EML pillars: "
            + ", ".join(sorted(forbidden))
        )

    if len(LEF_WERK_SIGNATURE) != 24:
        errors.append("LEF_WERK_SIGNATURE must contain exactly 24 glifos.")

    if len(set(LEF_WERK_SIGNATURE)) != len(LEF_WERK_SIGNATURE):
        errors.append("LEF_WERK_SIGNATURE must not contain duplicated glifos.")

    for key in ("date", "what", "how", "why"):
        if not SUBSTITUTION_RECORD.get(key):
            errors.append(f"SUBSTITUTION_RECORD must include {key!r}.")

    return {"valid": not errors, "errors": errors}


def describe_glifo(index: int) -> dict[str, Any]:
    """Return metadata for GL01 through GL24."""

    if index not in _GLIFO_METADATA:
        raise IndexError("glifo index must be between 1 and 24")
    return deepcopy(_GLIFO_METADATA[index])

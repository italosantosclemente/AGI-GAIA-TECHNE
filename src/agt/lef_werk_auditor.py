"""GL25 WERK auditor for LEF -> WERK thesis development."""

from __future__ import annotations

import re
import unicodedata
from datetime import date as date_type
from typing import Any

from .lef_werk import (
    LEF_WERK_SIGNATURE,
    QUALIFICATION_BLOCKS,
    describe_glifo,
    validate_lef_werk_mapping,
)

assert len(LEF_WERK_SIGNATURE) == 24

GL25_AUDITOR: dict[str, Any] = {
    "number": "GL25",
    "symbol": "🌊",
    "alias": "GL25_FLOW_AUDITOR",
    "status": "transversal, not part of the 24-cell signature",
    "not_part_of_signature": True,
    "function": "audit, relocate, improve, document, return to ISC judgment",
    "authority": "Final judgment returns to ISC; GL25 suggests but does not legislate.",
}

AUDIT_VERDICTS: tuple[str, ...] = (
    "CONTRADICTION",
    "IMPROVEMENT",
    "SUFFICIENT",
    "RELOCATION",
)

_BLOCK_MAPPING_PATTERNS = [
    r"\bmetatheory\b\s*(?:=|->|is|as)\s*\bmythos\b",
    r"\bmetateoria\b\s*(?:=|->|e|como)\s*\bmythos\b",
    r"\bobjectivity\b\s*(?:=|->|is|as)\s*\blogos\b",
    r"\bobjetividade\b\s*(?:=|->|e|como)\s*\blogos\b",
    r"\bintersubjectivity\b\s*(?:=|->|is|as)\s*\bethos\b",
    r"\bintersubjetividade\b\s*(?:=|->|e|como)\s*\bethos\b",
    r"\bi\b\s*(?:=|->)\s*\bmythos\b",
    r"\bii\b\s*(?:=|->)\s*\blogos\b",
    r"\biii\b\s*(?:=|->)\s*\bethos\b",
    r"\bmythos\b\s*(?:=|->)\s*\bausdruck\b",
    r"\blogos\b\s*(?:=|->)\s*\bdarstellung\b",
    r"\bethos\b\s*(?:=|->)\s*\bbedeutung\b",
]

_TRANSCENDENTAL_RISK_PATTERNS = [
    r"\bagi\s+is\s+wille\b",
    r"\biag\s+e\s+wille\b",
    r"\bia\s+e\s+wille\b",
    r"\bmachine\s+has\s+gewissen\b",
    r"\bagi\s+has\s+gewissen\b",
    r"\bgewissen\s+as\s+moral\s+legislation\b",
    r"\bgewissen\s+como\s+legislacao\s+moral\b",
    r"\bartificial\s+soul\b",
    r"\balma\s+artificial\b",
    r"\bmachine[- ]god\b",
    r"\btechnical\s+god\b",
    r"\bdeus\s+tecnico\b",
    r"\bcosmic\s+totality\b",
    r"\btotalidade\s+cosmica\b",
    r"\bglobal\s+aufhebung\b",
    r"\bfinal\s+aufhebung\b",
    r"\bresolves\s+all\s+contradictions\b",
]

_RELOCATION_RULES: list[tuple[str, list[str]]] = [
    ("GL01", ["friedman", "porta"]),
    ("GL02", ["reihe", "series", "serie", "aufhebung"]),
    ("GL03", ["chirimuuta", "model", "modelo", "abstraction", "abstracao", "abstração"]),
    ("GL04", ["einstein", "newton", "relativity", "relatividade", "geometry", "geometria"]),
    ("GL05", ["kant", "synthesis", "sintese", "síntese", "imagination", "imaginacao", "imaginação", "apperception", "apercepcao", "apercepção"]),
    ("GL06", ["repraesentation", "repräsentation", "representacao", "representação", "darstellung", "pregnance", "pregnancia", "pregnância"]),
    ("GL07", ["soul", "alma", "world", "mundo", "god", "deus", "paralogism", "paralogismo"]),
    ("GL08", ["ausdruck", "bedeutung", "functions", "funcoes", "funções", "myth", "mito"]),
    ("GL09", ["werk", "objectivation", "objetivacao", "objetivação", "culture", "cultura"]),
    ("GL10", ["teleology", "teleologia", "purposiveness", "finalidade", "ku"]),
    ("GL11", ["organism", "organismo", "machine", "maquina", "máquina", "bildungstrieb"]),
    ("GL12", ["sellars", "brandom", "normativity", "normatividade"]),
    ("GL13", ["technology", "tecnologia", "form und technik", "technique", "tecnica", "técnica"]),
    ("GL14", ["symbolic ai", "ia simbolica", "ia simbólica", "llm", "foundation model"]),
    ("GL15", ["agi", "iag", "negarestani", "bostrom", "hui", "buckner"]),
    ("GL16", ["hegel", "organism", "organismo", "aufhebung"]),
    ("GL17", ["earth", "terra", "gaia", "planetary", "planetario", "planetário", "koinos kosmos"]),
    ("GL18", ["faktum", "freedom", "liberdade", "moral consciousness", "consciencia moral", "consciência moral"]),
    ("GL19", ["myth politics", "mito politico", "mito político", "freud", "state", "estado"]),
    ("GL20", ["morality", "moralidade", "postulate", "postulado", "symbol", "simbolo", "símbolo", "alignment", "alinhamento"]),
    ("GL21", ["animal symbolicum", "anthropology", "antropologia"]),
    ("GL22", ["death of god", "morte de deus"]),
    ("GL23", ["servitude", "servidao", "servidão", "revolution", "revolucao", "revolução"]),
    ("GL24", ["ecology", "ecologia", "digital", "biosphere", "biosfera"]),
]

_BLOCK_RULES: list[tuple[str, list[str]]] = [
    ("Metatheory", ["metatheory", "metateoria"]),
    ("Objectivity", ["objectivity", "objetividade"]),
    ("Intersubjectivity", ["intersubjectivity", "intersubjetividade"]),
]


def explain_alphabet(include_gl25: bool = True) -> str:
    """Explain the 24-cell LEF/WERK alphabet and the GL25 audit flow."""

    validation = validate_lef_werk_mapping()
    signature = " ".join(LEF_WERK_SIGNATURE)
    blocks = ", ".join(
        f"{name} / {meta['pt']} GL{meta['range'][0]:02d}-GL{meta['range'][1]:02d}"
        for name, meta in QUALIFICATION_BLOCKS.items()
    )
    lines = [
        "LEF -> WERK alphabet",
        "",
        f"24 glifos: {signature}",
        f"Blocks: {blocks}.",
        "Decision 140426 remains the technical EML regime; Decision 150626 governs the qualification axis.",
        "Metatheory/Objectivity/Intersubjectivity are literary-academic blocks, not Mythos/Logos/Ethos.",
        f"Mapping valid: {validation['valid']}.",
    ]
    if include_gl25:
        lines.extend(
            [
                "",
                "GL25 🌊 = WERK Auditor / ISC-return.",
                "GL25 is not a 25th paragraph and is not part of the 24-glifo signature.",
                "It audits, relocates, improves, documents and returns judgment to ISC.",
            ]
        )
    return "\n".join(lines)


def audit_trace(text: str, source: str = "manual") -> dict[str, Any]:
    """Audit a thesis/system trace with deterministic GL25 heuristics."""

    normalized = _normalize(text)
    verdicts: list[str] = []
    contradictions: list[str] = []
    improvements: list[str] = []
    sufficient: list[str] = []
    creative_suggestions: list[str] = []
    next_actions: list[str] = []

    def add_verdict(verdict: str) -> None:
        if verdict not in verdicts:
            verdicts.append(verdict)

    if any(re.search(pattern, normalized) for pattern in _BLOCK_MAPPING_PATTERNS):
        add_verdict("CONTRADICTION")
        contradictions.append(
            "Qualification blocks must not be mapped to Mythos/Logos/Ethos or to a Mythos->Ausdruck, Logos->Darstellung, Ethos->Bedeutung sequence."
        )

    if any(re.search(pattern, normalized) for pattern in _TRANSCENDENTAL_RISK_PATTERNS):
        add_verdict("CONTRADICTION")
        contradictions.append(
            "The trace risks Wille, Gewissen as moral legislation, artificial soul, technical God, cosmic totality or global Aufhebung."
        )

    if (
        any(token in normalized for token in ["myth", "mito"])
        and any(token in normalized for token in ["pure immediacy", "pura imediatez", "imediatez pura", "immediacy"])
        and not any(token in normalized for token in ["mythos-clemente", "cassirerian myth", "myth-cassirer", "mito cassireriano"])
    ):
        add_verdict("IMPROVEMENT")
        improvements.append(
            "Distinguish Mythos-Clemente from Cassirerian myth before treating myth as pure immediacy."
        )

    if "alignment" in normalized and any(
        token in normalized
        for token in ["moral conscience", "gewissen", "consciencia moral", "consciência moral"]
    ):
        add_verdict("CONTRADICTION")
        contradictions.append("Alignment must not be treated as moral conscience.")

    if any(token in normalized for token in ["agi", "iag", " ai ", " ia "]):
        if not any(token in normalized for token in ["werk", "hypothesis", "hipotese", "hipótese", "mediation", "mediacao", "mediação"]):
            add_verdict("IMPROVEMENT")
            improvements.append(
                "AI/AGI claims should mark Werk, hypothesis or mediation to avoid subject inflation."
            )

    if any(
        token in normalized
        for token in [
            "werk, never wille",
            "werk jamais wille",
            "metatheory/objectivity/intersubjectivity",
            "metatheory / objectivity / intersubjectivity",
            "metateoria/objetividade/intersubjetividade",
        ]
    ):
        add_verdict("SUFFICIENT")
        sufficient.append("The trace preserves a core LEF/WERK invariant for the current stage.")

    relocation = relocate_argument(text)
    if relocation:
        add_verdict("RELOCATION")

    if not contradictions:
        sufficient.append("No direct GL25 contradiction was detected by deterministic rules.")
    if not improvements:
        improvements.append("No mandatory improvement was detected; further refinement remains optional.")

    creative_suggestions.append(
        "Suggestion: create or update a dated GL25 ledger entry so the thesis can evolve without premature closure."
    )
    next_actions.append(
        "Return this audit to ISC, then revise only the parts marked as contradiction, improvement or relocation."
    )

    return {
        "source": source,
        "object_audited": _excerpt(text),
        "verdicts": verdicts or ["SUFFICIENT"],
        "contradictions": contradictions,
        "improvements": improvements,
        "sufficient": sufficient,
        "relocation": relocation,
        "creative_suggestions": creative_suggestions,
        "next_actions": next_actions,
        "returned_to_ISC": True,
    }


def format_audit_markdown(audit: dict[str, Any]) -> str:
    """Format a GL25 audit as stable Markdown."""

    lines = [
        "# GL25 WERK Audit",
        "",
        f"**Source:** {audit.get('source', 'manual')}",
        f"**Verdicts:** {', '.join(audit.get('verdicts', []))}",
        "",
        "## Contradictions",
        *_bullets(audit.get("contradictions", []), empty="None detected."),
        "",
        "## Improvements",
        *_bullets(audit.get("improvements", []), empty="None required."),
        "",
        "## Sufficient Elements",
        *_bullets(audit.get("sufficient", []), empty="None marked."),
        "",
        "## Relocation",
    ]
    relocation = audit.get("relocation") or {}
    if relocation:
        lines.extend(
            [
                f"- Target: {relocation.get('target')}",
                f"- Block: {relocation.get('block')}",
                f"- Reason: {relocation.get('reason')}",
            ]
        )
    else:
        lines.append("- None suggested.")
    lines.extend(
        [
            "",
            "## Creative Suggestions",
            *_bullets(audit.get("creative_suggestions", []), empty="None."),
            "",
            "## Next Actions",
            *_bullets(audit.get("next_actions", []), empty="None."),
            "",
            "Returned to ISC judgment.",
        ]
    )
    return "\n".join(lines)


def daily_ledger_entry(audit: dict[str, Any], date: str | None = None) -> str:
    """Create a dated GL25 ledger entry."""

    entry_date = date or date_type.today().isoformat()
    relocation = audit.get("relocation") or {}
    return "\n".join(
        [
            f"# GL25 Daily Ledger — {entry_date}",
            "",
            f"date: {entry_date}",
            f"object_audited: {audit.get('object_audited', '')}",
            f"source: {audit.get('source', 'manual')}",
            f"glifo/block affected: {relocation.get('target') or relocation.get('block') or 'undetermined'}",
            f"diagnosis: {', '.join(audit.get('verdicts', []))}",
            f"contradiction: {_inline(audit.get('contradictions', []))}",
            f"improvement: {_inline(audit.get('improvements', []))}",
            f"sufficient elements: {_inline(audit.get('sufficient', []))}",
            f"relocation: {relocation or 'none'}",
            f"creative suggestion: {_inline(audit.get('creative_suggestions', []))}",
            f"next action: {_inline(audit.get('next_actions', []))}",
            "returned_to_ISC: true",
            "",
            format_audit_markdown(audit),
        ]
    )


def relocate_argument(text: str) -> dict[str, Any]:
    """Map an argument to the most likely LEF/WERK glifo or block."""

    normalized = _normalize(text)
    scored: list[tuple[int, str, list[str]]] = []
    for target, keywords in _RELOCATION_RULES:
        hits = [keyword for keyword in keywords if keyword in normalized]
        if hits:
            scored.append((len(hits), target, hits))
    if scored:
        scored.sort(key=lambda item: (-item[0], int(item[1][2:])))
        _, target, hits = scored[0]
        metadata = describe_glifo(int(target[2:]))
        return {
            "target": target,
            "block": metadata["block"],
            "glifo": metadata["glifo"],
            "title": metadata["title"],
            "reason": f"Matched keywords: {', '.join(hits)}.",
        }

    for block, keywords in _BLOCK_RULES:
        if any(keyword in normalized for keyword in keywords):
            meta = QUALIFICATION_BLOCKS[block]
            return {
                "target": f"{block} block",
                "block": block,
                "reason": f"Detected block keyword for {block} / {meta['pt']}.",
            }

    return {}


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", f" {text} ")
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return ascii_text.lower()


def _bullets(items: list[str], empty: str) -> list[str]:
    if not items:
        return [f"- {empty}"]
    return [f"- {item}" for item in items]


def _inline(items: list[str]) -> str:
    return "; ".join(items) if items else "none"


def _excerpt(text: str, limit: int = 180) -> str:
    clean = " ".join(text.strip().split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."

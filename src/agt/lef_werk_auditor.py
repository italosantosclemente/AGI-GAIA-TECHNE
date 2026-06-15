"""Transversal WERK auditor for LEF -> WERK thesis development."""

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
from .werk_indices import calculate_werk_indices, is_indices_request

assert len(LEF_WERK_SIGNATURE) == 24

GL25_AUDITOR: dict[str, Any] = {
    "number": "GL25",
    "symbol": "🌊",
    "alias": "GL25_FLOW_AUDITOR",
    "status": "transversal, not part of the 24-cell signature",
    "not_part_of_signature": True,
    "function": "audit, relocate, improve, document, return to ISC judgment",
    "authority": "Final judgment returns to ISC; 🌊 suggests but does not legislate.",
}

CONTINGENT_EXTERNAL_CASE_CATEGORY = "contingent_external_case"

CONTINGENT_CASE_AFFECTED_GLIFOS = ["🜄", "🜁", "⚘", "🜛", "🜜"]

CONTINGENT_CASE_ROUTING: tuple[dict[str, str], ...] = (
    {
        "glifo": "🜄",
        "layer": "technical layer",
        "receives": "jailbreak, safeguards, model behavior, formal objectivation",
    },
    {
        "glifo": "🜁",
        "layer": "frontier-AI layer",
        "receives": "deployment risk, AGI hypothesis, model governance, safety discourse",
    },
    {
        "glifo": "⚘",
        "layer": "political-myth layer",
        "receives": "public narrative of danger, emergency framing, symbolic production of threat",
    },
    {
        "glifo": "🜛",
        "layer": "servitude/revolution layer",
        "receives": "access control, sovereign interruption, technical dependence, domination risk",
    },
    {
        "glifo": "🜜",
        "layer": "digital-ecological layer",
        "receives": "infrastructure, data retention, monitoring, public digital commons",
    },
)

CONTINGENT_CASE_QUESTIONS: tuple[str, ...] = (
    "Which glifos receive this case?",
    "Which part of the case belongs to technical objectivation?",
    "Which part belongs to political myth?",
    "Which part belongs to access, servitude, sovereignty or governance?",
    "Which part belongs to digital ecology?",
    "What contradicts the system?",
    "What can be improved?",
    "What is already sufficiently handled by the current invariants?",
    "What should be proposed creatively beyond ISC's initial formulation?",
    "What must be returned to ISC judgment?",
)

_CONTINGENT_CASE_TERMS = [
    "anthropic",
    "fable",
    "mythos",
    "jailbreak",
    "safeguard",
    "model access",
    "access suspension",
    "model recall",
    "frontier ai",
    "frontier-ai",
    "public ai event",
    "evento publico de ia",
    "evento público de ia",
]

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
    """Explain the 24-cell LEF/WERK alphabet and the 🌊 audit flow."""

    validation = validate_lef_werk_mapping()
    signature = " ".join(LEF_WERK_SIGNATURE)
    blocks = ", ".join(
        f"{name} / {meta['pt']} ({LEF_WERK_SIGNATURE[meta['range'][0] - 1]} … {LEF_WERK_SIGNATURE[meta['range'][1] - 1]})"
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
                "🌊 = WERK Auditor / ISC-return.",
                "🌊 is not a 25th paragraph and is not part of the 24-glifo signature.",
                "It audits, relocates, improves, documents and returns judgment to ISC.",
            ]
        )
    return "\n".join(lines)


def audit_trace(text: str, source: str = "manual") -> dict[str, Any]:
    """Audit a thesis/system trace with deterministic 🌊 heuristics."""

    normalized = _normalize(text)
    contingent_case = _contingent_external_case(normalized)
    category = CONTINGENT_EXTERNAL_CASE_CATEGORY if contingent_case else "thesis_trace"
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

    if any(token in normalized for token in ["government directive", "diretiva governamental", "ordem governamental"]) and any(
        token in normalized for token in ["philosophical legitimacy", "legitimidade filosofica", "legitimidade filosófica"]
    ):
        add_verdict("IMPROVEMENT")
        improvements.append(
            "A government directive must not become automatic philosophical legitimacy; separate public authority from WERK justification."
        )

    if any(token in normalized for token in ["model recall", "access suspension", "suspensao de acesso", "suspensão de acesso"]) and any(
        token in normalized for token in ["proof", "prova", "proves", "demonstra"]
    ) and any(
        token in normalized for token in ["wille", "gewissen", "soul", "alma", "god", "deus"]
    ):
        add_verdict("CONTRADICTION")
        contradictions.append(
            "Model recall or access suspension cannot prove Wille, Gewissen, soul, God or inner moral legislation."
        )

    if "jailbreak" in normalized and not any(
        token in normalized
        for token in ["narrow", "estrito", "especifico", "específico", "universal", "systemic", "sistemico", "sistêmico"]
    ):
        add_verdict("IMPROVEMENT")
        improvements.append(
            "Distinguish narrow jailbreak evidence from universal safeguard failure before drawing architectural conclusions."
        )

    if any(token in normalized for token in ["frontier model access", "frontier-model access", "model access", "acesso ao modelo"]) and not all(
        token in normalized for token in ["technical", "political", "public"]
    ):
        add_verdict("IMPROVEMENT")
        improvements.append(
            "Separate technical risk, political authority and public justification when auditing frontier-model access."
        )

    if contingent_case:
        add_verdict("RELOCATION")
        sufficient.append(
            "The external case is treated as contingent public trace, not doctrine, special category or structural pillar."
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
        sufficient.append("No direct 🌊 contradiction was detected by deterministic rules.")
    if not improvements:
        improvements.append("No mandatory improvement was detected; further refinement remains optional.")

    creative_suggestions.append(
        "Suggestion: create or update a dated 🌊 ledger entry so the thesis can evolve without premature closure."
    )
    next_actions.append(
        "Return this audit to ISC, then revise only the parts marked as contradiction, improvement or relocation."
    )

    return {
        "source": source,
        "category": category,
        "object_audited": _excerpt(text),
        "verdicts": verdicts or ["SUFFICIENT"],
        "contradictions": contradictions,
        "improvements": improvements,
        "sufficient": sufficient,
        "relocation": relocation,
        "contingent_case": _contingent_case_payload(text) if contingent_case else None,
        "indices": calculate_werk_indices(conjecture=text) if is_indices_request(text) else None,
        "creative_suggestions": creative_suggestions,
        "next_actions": next_actions,
        "returned_to_ISC": True,
    }


def format_audit_markdown(audit: dict[str, Any]) -> str:
    """Format a 🌊 audit as stable Markdown."""

    lines = [
        "# 🌊 WERK Audit",
        "",
        f"**Source:** {audit.get('source', 'manual')}",
        f"**Category:** {audit.get('category', 'thesis_trace')}",
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
        target = relocation.get("glifo") or relocation.get("target")
        title = relocation.get("title")
        label = f"{target} — {title}" if target and title else str(target)
        lines.extend(
            [
                f"- Target: {label}",
                f"- Block: {relocation.get('block')}",
                f"- Reason: {relocation.get('reason')}",
            ]
        )
    else:
        lines.append("- None suggested.")
    contingent = audit.get("contingent_case") or {}
    if contingent:
        lines.extend(
            [
                "",
                "## Contingent External Case",
                "- Status: contingent public trace, not doctrine.",
                f"- Affected glifos: {', '.join(contingent.get('affected_glifos', []))}",
                "- 🌊 audits the case and reinscribes it in the 24-glifo syntax.",
                "",
                "### Routing",
            ]
        )
        for route in contingent.get("routing", []):
            lines.append(f"- {route['glifo']} receives the {route['layer']}: {route['receives']}.")
        lines.extend(["", "### Audit Questions"])
        lines.extend(f"{index}. {question}" for index, question in enumerate(contingent.get("questions", []), start=1))
    indices = audit.get("indices")
    if indices:
        lines.extend(
            [
                "",
                "## Index Calculation",
                "- 🌊 calculated existing AGI-GAIA-TECHNE indices for this trace.",
                f"- Techné Score: {indices['framework'].get('techne')}",
                f"- IAE: {indices['framework'].get('iae')}",
                f"- Harmonia: {indices['framework'].get('harmony')}",
                "- The numbers are heuristic and return to ISC judgment.",
            ]
        )
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
    """Create a dated 🌊 ledger entry."""

    entry_date = date or date_type.today().isoformat()
    relocation = audit.get("relocation") or {}
    if audit.get("category") == CONTINGENT_EXTERNAL_CASE_CATEGORY:
        contingent = audit.get("contingent_case") or {}
        return "\n".join(
            [
                "# 🌊 Audit — contingent external case",
                "",
                f"date: {entry_date}",
                f"case: {audit.get('object_audited', '')}",
                f"source: {audit.get('source', 'manual')}",
                "status: contingent public trace, not doctrine",
                f"category: {CONTINGENT_EXTERNAL_CASE_CATEGORY}",
                "",
                "primary auditor:",
                "🌊",
                "",
                "affected glifos:",
                ", ".join(contingent.get("affected_glifos", CONTINGENT_CASE_AFFECTED_GLIFOS)),
                "",
                f"diagnosis: {', '.join(audit.get('verdicts', []))}",
                "",
                f"contradictions: {_inline(audit.get('contradictions', []))}",
                "",
                f"improvements: {_inline(audit.get('improvements', []))}",
                "",
                f"sufficient elements: {_inline(audit.get('sufficient', []))}",
                "",
                f"relocation among glifos: {', '.join(contingent.get('affected_glifos', CONTINGENT_CASE_AFFECTED_GLIFOS))}",
                "",
                f"creative suggestion: {_inline(audit.get('creative_suggestions', []))}",
                "",
                f"next action: {_inline(audit.get('next_actions', []))}",
                "",
                "returned_to_ISC: true",
                "",
                format_audit_markdown(audit),
            ]
        )
    return "\n".join(
        [
            f"# 🌊 Daily Ledger — {entry_date}",
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


def _contingent_external_case(normalized: str) -> bool:
    return any(term in normalized for term in _CONTINGENT_CASE_TERMS)


def _contingent_case_payload(text: str) -> dict[str, Any]:
    return {
        "case": _excerpt(text),
        "status": "contingent public trace, not doctrine",
        "affected_glifos": list(CONTINGENT_CASE_AFFECTED_GLIFOS),
        "routing": [dict(item) for item in CONTINGENT_CASE_ROUTING],
        "questions": list(CONTINGENT_CASE_QUESTIONS),
        "internal_targets": ["GL14", "GL15", "GL19", "GL23", "GL24"],
    }


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

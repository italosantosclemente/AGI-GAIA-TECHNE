"""Heuristic WERK index aggregation for the transversal auditor."""

from __future__ import annotations

import unicodedata
from pathlib import Path
import sys
from typing import Any

from .planetary_telemetry import (
    PlanetaryTelemetry,
    PlanetaryTelemetryReport,
    coverage_band,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gaia_techne_framework import calculate_framework_state  # noqa: E402


INDEX_AFFECTED_GLIFOS = ["🌊", "🜄", "🜁", "⚶", "☍", "🜚", "🜜"]

_INDEX_REQUEST_PATTERNS = (
    "iae",
    "indice",
    "indices",
    "calcular",
    "techne score",
    "techné score",
    "harmonia",
    "harmony",
    "telemetria",
    "tension index",
    "agi-gaia-techne",
    "🌊 calcular",
    "fluxo auditor calcular",
)

_ONTOLOGICAL_CLAIM_PATTERNS = (
    "consciousness",
    "consciencia",
    "consciência",
    "wille",
    "gewissen",
    "god",
    "deus",
    "soul",
    "alma",
    "world-totality",
    "totalidade do mundo",
    "totalidade cosmica",
    "totalidade cósmica",
)


def calculate_werk_indices(
    leap_factor: float | str | None = 1.0,
    conjecture: str = "",
    telemetry_report: PlanetaryTelemetryReport | None = None,
    collect_live_telemetry: bool = False,
) -> dict[str, Any]:
    """Calculate existing AGI-GAIA-TECHNE indices under the 🌊 auditor."""

    framework = calculate_framework_state(leap_factor=leap_factor, conjecture=conjecture)
    report = telemetry_report
    if report is None and collect_live_telemetry:
        report = PlanetaryTelemetry(timeout=6).collect()

    telemetry = _telemetry_summary(report)
    interpretations = _interpret_indices(framework, telemetry, conjecture)

    return {
        "auditor": "🌊",
        "status": framework.get("status"),
        "framework": framework,
        "telemetry": telemetry,
        "affected_glifos": list(INDEX_AFFECTED_GLIFOS),
        "interpretation": interpretations,
        "returned_to_ISC": True,
    }


def format_werk_indices_markdown(indices: dict[str, Any]) -> str:
    """Format WERK indices as Markdown without granting final moral judgment."""

    framework = indices.get("framework", {})
    telemetry = indices.get("telemetry", {})
    interpretation = indices.get("interpretation", {})
    risk_flags = framework.get("risk_flags") or []
    lines = [
        "# 🌊 AGI-GAIA-TECHNE Indices",
        "",
        "🌊 calculates heuristic WERK indices; it does not issue final moral judgment.",
        "",
        "## Core indices",
        f"- Techné Score: {framework.get('techne')}",
        f"- IAE / Índice de Alerta Ético: {framework.get('iae')}",
        f"- Índice de Harmonia: {framework.get('harmony')}",
        f"- Ethos factor: {framework.get('ethos')}",
        f"- Status: {framework.get('status')} ({framework.get('status_label')})",
        f"- Recommendation: {framework.get('recommendation')}",
        f"- Risk flags: {', '.join(risk_flags) if risk_flags else 'none'}",
        "",
        "## Planetary telemetry",
        f"- Available: {telemetry.get('available')}",
        f"- Gaia-humanity tension index: {_display_or_none(telemetry.get('tension_index'))}",
        f"- Judgment: {_display_or_none(telemetry.get('judgment'))}",
        f"- Source coverage: {_display_or_none(telemetry.get('source_coverage'))}",
        f"- Source coverage ratio: {_display_or_none(telemetry.get('source_coverage_ratio'))}",
        "",
        "## Affected glifos",
        "- " + ", ".join(indices.get("affected_glifos", [])),
        "",
        "## Audit",
        f"- Diagnosis: {interpretation.get('diagnosis')}",
        f"- Contradictions: {interpretation.get('contradictions')}",
        f"- Improvements: {interpretation.get('improvements')}",
        f"- Sufficient elements: {interpretation.get('sufficient_elements')}",
        f"- Creative suggestion: {interpretation.get('creative_suggestion')}",
        f"- Next action: {interpretation.get('next_action')}",
        "",
        f"returned_to_ISC: {str(indices.get('returned_to_ISC') is True).lower()}",
    ]
    return "\n".join(lines)


def is_indices_request(text: str) -> bool:
    """Return True when the prompt asks 🌊 to calculate existing indices."""

    normalized = _normalize(text)
    return any(pattern in normalized for pattern in _INDEX_REQUEST_PATTERNS)


def _telemetry_summary(report: PlanetaryTelemetryReport | None) -> dict[str, Any]:
    if report is None:
        return {
            "available": False,
            "tension_index": None,
            "judgment": None,
            "source_coverage_ratio": None,
            "source_coverage": "not collected",
            "signal_count": 0,
            "source_limits": None,
        }

    ok = [signal for signal in report.signals if signal.status == "ok"]
    failed = [signal for signal in report.signals if signal.status != "ok"]
    total = len(report.signals) + len(report.failures)
    ratio = (len(ok) / total) if total else 0.0
    return {
        "available": True,
        "generated_at": report.generated_at,
        "tension_index": report.tension_index,
        "judgment": report.judgment,
        "summary": report.summary,
        "source_coverage_ratio": round(ratio, 4),
        "source_coverage": coverage_band(ratio),
        "signal_count": len(ok),
        "source_limits": len(failed) + len(report.failures),
    }


def _interpret_indices(
    framework: dict[str, Any],
    telemetry: dict[str, Any],
    conjecture: str,
) -> dict[str, str]:
    flags = list(framework.get("risk_flags") or [])
    normalized = _normalize(conjecture)
    ontological_claim = any(pattern in normalized for pattern in _ONTOLOGICAL_CLAIM_PATTERNS)
    contradictions: list[str] = []
    improvements: list[str] = []

    if ontological_claim:
        contradictions.append(
            "Do not read Techné, IAE, Harmonia or telemetry as proof of consciousness, Wille, Gewissen, God, soul or world-totality."
        )
    if framework.get("status") in {"critical", "warning"}:
        improvements.append("Reinforce Ethos and return the recommendation to ISC judgment.")
    if telemetry.get("available") is False:
        improvements.append("Collect live planetary telemetry when the audit depends on current public signals.")
    elif telemetry.get("source_coverage_ratio") is not None and telemetry["source_coverage_ratio"] < 0.8:
        improvements.append("Mark source limits before treating telemetry as sufficient public trace.")
    if flags:
        improvements.append(f"Track framework risk flags without turning them into doctrine: {', '.join(flags)}.")

    sufficient = [
        "Existing framework indices already provide Techné Score, IAE, Harmonia, status and recommendation."
    ]
    if telemetry.get("available"):
        sufficient.append("Planetary telemetry already provides tension index, source coverage and public-source limits.")

    return {
        "diagnosis": (
            "🌊 aggregates existing runtime indices and reads them as heuristic WERK pressure, not as a new metric."
        ),
        "contradictions": "; ".join(contradictions) if contradictions else "none detected",
        "improvements": "; ".join(improvements) if improvements else "none mandatory",
        "sufficient_elements": "; ".join(sufficient),
        "creative_suggestion": (
            "Use the index snapshot as an audit trace that can be compared with future contingent public events."
        ),
        "next_action": "Return the index reading to ISC; do not let the numbers legislate the thesis.",
    }


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", f" {text or ''} ")
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return ascii_text.lower()


def _display_or_none(value: Any) -> str:
    return "not collected" if value is None else str(value)

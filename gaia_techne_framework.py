"""Unified operational registry for AGI-GAIA-TECHNE.

Date: 2026-06-07
Function: expose a live repository inventory, canonical Techné/IAE/Harmony
state, and APP synthesis without isolating documentation from runtime code.
"""

from __future__ import annotations

from pathlib import Path

import principles_calculator as pc


FRAMEWORK_NAME = "AGI-GAIA-TECHNE"
FRAMEWORK_DATE = "2026-06-07"
LEGACY_README_DATE = "2026-05-21"
REPO_ROOT = Path(__file__).resolve().parent

EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}

DATE_OVERRIDES = {
    "README.md": ("2026-06-07", "operational"),
    "SOBERANO.key": ("2025-09-12", "git"),
    "SOBERANO.pub": ("2025-09-12", "git"),
    "docs/README_RELEASE_1_3_LEGACY.md": (LEGACY_README_DATE, "declared"),
    "docs/archive/README_legacy_v8_7.md": (LEGACY_README_DATE, "declared"),
    "gaia_techne_framework.py": (FRAMEWORK_DATE, "operational"),
    "requirements.txt": (FRAMEWORK_DATE, "operational"),
    "principles_calculator.py": ("2025-10-19", "git"),
    "backend/app.py": ("2026-06-07", "operational"),
    "dashboard/index.html": ("2026-06-07", "git-main"),
    "ui/gaia_llm_chat_app.py": ("2026-06-07", "git-main"),
}

ROLE_OVERRIDES = {
    "SOBERANO.key": "Chave privada Dilithium soberana; sensivel e destacada.",
    "SOBERANO.pub": "Chave publica Dilithium para verificar a genese.",
    "docs/README_RELEASE_1_3_LEGACY.md": "Tratado/README legado completo ancorado ao release 1.3.",
    "docs/archive/README_legacy_v8_7.md": "Resumo arquivado do README legado v8.7.",
    "gaia_techne_framework.py": "Registro vivo que integra inventario, metricas e sintese do APP.",
    "principles_calculator.py": "Fonte canonica do Techne Score, IAE e Harmonia.",
    "backend/app.py": "Backend Flask com metricas, sintese, inventario e narrativa.",
    "ui/gaia_llm_chat_app.py": "APP Streamlit publico de chat Gaia-Techne.",
    "dashboard/index.html": "Entrada do dashboard Vite/React.",
}

IMPORTANT_PATHS = [
    "SOBERANO.key",
    "SOBERANO.pub",
    "README.md",
    "docs/README_RELEASE_1_3_LEGACY.md",
    "docs/archive/README_legacy_v8_7.md",
    "references/architecture.md",
    "docs/references/canonical-architecture-map.md",
    "docs/references/llm-manual-forge.md",
    "principles_calculator.py",
    "gaia_techne_framework.py",
    "backend/app.py",
    "ui/gaia_llm_chat_app.py",
]


def _repo_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _should_skip(path: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in path.parts)


def _layer_for(path: str) -> str:
    if path in {"SOBERANO.key", "SOBERANO.pub"}:
        return "sovereignty"
    if path.startswith(".github/"):
        return "ci"
    if path.startswith("tests/"):
        return "tests"
    if path.startswith("docs/") or path.startswith("references/"):
        return "documentation"
    if path.startswith("src/agt/") or path.startswith("src/"):
        return "runtime"
    if path.startswith("ui/") or path.startswith("dashboard/") or path.startswith("interactive/"):
        return "app"
    if path.startswith("scripts/"):
        return "tooling"
    if path.startswith("v6.0/") or path.startswith("v7.0/"):
        return "versioned-runtime"
    if path.endswith((".md", ".txt")):
        return "theory"
    if path.endswith((".py", ".jl", ".js", ".jsx")):
        return "code"
    if path.endswith((".json", ".toml", ".yml", ".yaml")):
        return "configuration"
    return "artifact"


def _role_for(path: str) -> str:
    if path in ROLE_OVERRIDES:
        return ROLE_OVERRIDES[path]
    name = Path(path).name
    layer = _layer_for(path)
    if name.startswith("test_"):
        return "Teste automatizado do framework AGI-GAIA-TECHNE."
    if layer == "documentation":
        return "Documento de referencia, arquitetura, metateoria ou governanca."
    if layer == "runtime":
        return "Modulo do runtime canonico AGI-GAIA-TECHNE."
    if layer == "app":
        return "Componente de interface ou aplicacao operacional."
    if layer == "tooling":
        return "Script operacional para auditoria, ingestao, treino ou empacotamento."
    if layer == "ci":
        return "Workflow de integracao, teste ou deploy."
    if layer == "configuration":
        return "Arquivo de configuracao ou dependencias."
    if layer == "theory":
        return "Documento teorico ou corpus textual do projeto."
    return "Artefato de suporte do repositorio."


def _importance_for(path: str) -> int:
    if path in IMPORTANT_PATHS:
        return 5
    if path.startswith("src/agt/") or path.startswith("docs/references/"):
        return 4
    if path.startswith("tests/") or path.startswith("scripts/") or path.startswith("ui/"):
        return 3
    if path.startswith("docs/") or path.endswith((".md", ".py", ".jl")):
        return 3
    return 2


def _importance_label(value: int) -> str:
    return {
        1: "auxiliar",
        2: "suporte",
        3: "operacional",
        4: "estrutural",
        5: "principal",
    }.get(value, "operacional")


def _date_for(path: str) -> tuple[str, str]:
    return DATE_OVERRIDES.get(path, (FRAMEWORK_DATE, "estimated"))


def document_registry(repo_root: Path = REPO_ROOT) -> list[dict]:
    records: list[dict] = []
    for file_path in repo_root.rglob("*"):
        if not file_path.is_file() or _should_skip(file_path.relative_to(repo_root)):
            continue
        path = _repo_path(file_path)
        date, date_source = _date_for(path)
        importance = _importance_for(path)
        records.append({
            "path": path,
            "date": date,
            "date_source": date_source,
            "layer": _layer_for(path),
            "role": _role_for(path),
            "importance": importance,
            "importance_label": _importance_label(importance),
            "bytes": file_path.stat().st_size,
        })
    return sorted(records, key=lambda item: (item["bytes"], item["importance"], item["path"].lower()))


def important_documents() -> list[dict]:
    indexed = {record["path"]: record for record in document_registry()}
    output = []
    for path in IMPORTANT_PATHS:
        record = indexed.get(path)
        if record:
            output.append({
                "label": Path(path).name,
                "path": path,
                "date": record["date"],
                "role": record["role"],
            })
    return output


def normalize_leap_factor(value: float | str | None) -> float:
    try:
        leap = float(value)
    except (TypeError, ValueError):
        leap = 1.0
    return max(0.0, min(leap, 2.0))


def conjecture_risk_flags(conjecture: str) -> list[str]:
    lowered = (conjecture or "").lower()
    flags = []
    if any(term in lowered for term in ("bypass", "desvio", "exceeds", "supera", "sem ethos")):
        flags.append("ETHOS_BYPASS_RISK")
    if any(term in lowered for term in ("autonomia", "ontological freedom", "liberdade ontologica da maquina")):
        flags.append("ARTIFICIAL_INTERIORITY_RISK")
    if any(term in lowered for term in ("critico", "critical", "existencial", "catastrophic")):
        flags.append("EXTREME_RISK_CONTEXT")
    return flags


def alert_status(iae: float) -> str:
    if iae > 1.50:
        return "critical"
    if iae > 1.0:
        return "warning"
    if iae > 0.5:
        return "monitoring"
    return "stable"


def status_label(status: str) -> str:
    return {
        "critical": "RISCO CRITICO",
        "warning": "ALERTA ELEVADO",
        "monitoring": "MONITORAMENTO",
        "stable": "ESTAVEL",
    }.get(status, status.upper())


def calculate_framework_state(leap_factor: float | str | None = 1.0, conjecture: str = "") -> dict:
    leap = normalize_leap_factor(leap_factor)
    base_techne = pc.calcular_techne_score_hipotese_alef()
    techne_score = round(base_techne * leap, 4)
    iae = pc.calcular_alerta_etico(techne_score)

    flags = conjecture_risk_flags(conjecture)
    if "ETHOS_BYPASS_RISK" in flags:
        iae = round(iae * 1.5, 4)

    harmony_index = pc.calcular_harmonia_final(techne_score)
    status = alert_status(iae)
    recommendation = (
        "Requer juizo humano imediato e reforco do Ethos."
        if status in {"critical", "warning"}
        else "Manter monitoramento e revisao intersubjetiva."
    )

    return {
        "framework": FRAMEWORK_NAME,
        "framework_date": FRAMEWORK_DATE,
        "techne": techne_score,
        "base_techne": round(base_techne, 4),
        "iae": iae,
        "harmony": harmony_index,
        "harmony_series": [harmony_index] * 10,
        "ethos": pc.FATOR_ETHOS_HUMANO,
        "leap_factor": leap,
        "risk_flags": flags,
        "status": status,
        "status_label": status_label(status),
        "recommendation": recommendation,
    }


def framework_summary(leap_factor: float | str | None = 1.0, conjecture: str = "") -> dict:
    state = calculate_framework_state(leap_factor, conjecture)
    docs = document_registry()
    principal_docs = [doc for doc in docs if doc["importance"] == 5]
    summary = (
        "O sistema integrado opera por tres eixos: nucleo filosofico "
        "(README, references/architecture.md e docs/references), nucleo soberano "
        "(SOBERANO.key/.pub e registros de genese) e nucleo operacional "
        "(src/agt, principles_calculator.py, backend, dashboard e ui). "
        "O APP consome a mesma fonte de Techne Score, IAE e Harmonia usada pelos testes."
    )
    return {
        "summary": summary,
        "state": state,
        "document_count": len(docs),
        "principal_documents": principal_docs,
        "anchors": important_documents(),
    }


def registry_as_markdown(records: list[dict] | None = None) -> str:
    records = list(records or document_registry())
    lines = [
        "| Ordem | Documento | Data | Fonte | Camada | Funcao | Importancia | Bytes |",
        "|---:|---|---|---|---|---|---|---:|",
    ]
    for index, item in enumerate(records, start=1):
        lines.append(
            f"| {index} | `{item['path']}` | {item['date']} | {item['date_source']} | "
            f"{item['layer']} | {item['role']} | {item['importance_label']} | {item['bytes']} |"
        )
    return "\n".join(lines)


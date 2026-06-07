"""Unified operational registry for AGI-GAIA-TECHNE.

Date: 2026-06-07
Function: centralizes the document map, Techné/IAE/Harmony metrics, and
dashboard synthesis so the repository does not operate as isolated scripts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import principles_calculator as pc


FRAMEWORK_NAME = "AGI-GAIA-TECHNE"
FRAMEWORK_DATE = "2026-06-07"
LEGACY_README_DATE = "2026-05-21"
REPO_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class DocumentRecord:
    path: str
    date: str
    date_source: str
    layer: str
    role: str
    importance: int


DOCUMENT_REGISTRY: tuple[DocumentRecord, ...] = (
    DocumentRecord("Project.toml", "2025-10-19", "git", "runtime-julia", "Dependências Julia do monitoramento e testes.", 1),
    DocumentRecord("alfabeto_data.py", "2025-10-19", "git", "symbolic-core", "Lista Python mínima do alfabeto LEF usada pelo backend.", 1),
    DocumentRecord("tests/test_eco_semente.jl", "2025-10-19", "git", "tests", "Smoke test do motor narrativo Eco da Semente.", 1),
    DocumentRecord("ALFABETO.md", "2025-10-19", "git", "symbolic-core", "Documento curto que fixa o alfabeto LEF.", 2),
    DocumentRecord("dashboard/style.css", "2025-10-19", "git", "app", "Estilo visual do dashboard operacional.", 2),
    DocumentRecord("carregar_alfabeto.jl", "2025-10-19", "git", "symbolic-core", "Loader Julia do alfabeto LEF.", 1),
    DocumentRecord("tests/test_gerador_narrativas.jl", "2025-10-19", "git", "tests", "Teste do gerador de narrativas simbólicas.", 1),
    DocumentRecord(".github/workflows/deploy-dashboard.yml", "2025-10-19", "git", "ci", "Publicação do dashboard no GitHub Pages.", 1),
    DocumentRecord("tests/test_full_suite.jl", "2025-10-19", "git", "tests", "Agregador dos testes Julia.", 1),
    DocumentRecord("tests/test_techne_score_calculator.jl", "2025-10-19", "git", "tests", "Teste Julia para Techné Score e IAE.", 2),
    DocumentRecord("tests/test_conjecture.jl", "2025-10-19", "git", "tests", "Teste da conjectura simbólica Julia.", 1),
    DocumentRecord("SECURITY.md", "2025-09-06", "git", "governance", "Política de segurança e reporte.", 4),
    DocumentRecord("generate_alphabet.py", "2025-10-19", "git", "tooling", "Gerador Python do alfabeto simbólico.", 1),
    DocumentRecord("tests/test_calculate_harmony_index.jl", "2025-10-19", "git", "tests", "Teste do Índice de Harmonia em Julia.", 2),
    DocumentRecord("tests/simulations/test_aleph_synergy.py", "2025-10-19", "git", "tests", "Simulação do salto Álef e resposta do IAE.", 3),
    DocumentRecord(".github/workflows/test-suite.yml", "2025-10-19", "git", "ci", "Pipeline CI dos testes Python e Julia.", 2),
    DocumentRecord("LICENSE", "2025-09-06", "git", "governance", "Licença MIT do repositório.", 4),
    DocumentRecord(".gitignore", "2025-10-19", "git", "tooling", "Exclusões de build, cache, logs e visualizações.", 1),
    DocumentRecord("requirements.txt", "2026-06-07", "operational", "runtime-python", "Dependências Python consolidadas para APP, métricas e testes.", 3),
    DocumentRecord("dashboard/index.html", "2025-10-19", "git", "app", "Interface principal do dashboard ético.", 3),
    DocumentRecord("tests/test_dashboard.py", "2025-10-19", "git", "tests", "Testes dos endpoints Flask do APP.", 3),
    DocumentRecord("tests/test_ethos_veto.py", "2025-10-19", "git", "tests", "Teste do acionamento de veto Ethos.", 3),
    DocumentRecord("eco_semente.jl", "2025-10-19", "git", "narrative", "Motor narrativo do replantio simbólico.", 3),
    DocumentRecord("gerador_narrativas.jl", "2025-10-19", "git", "narrative", "Gerador Julia de narrativas simbólicas.", 3),
    DocumentRecord("config.json", "2025-10-16", "git", "configuration", "Configuração dos pilares, assinatura LEF e documentos incorporados.", 3),
    DocumentRecord("tests/test_edge_cases.py", "2025-10-19", "git", "tests", "Testes de entradas anômalas e tentativa de bypass.", 3),
    DocumentRecord("tests/test_principles_calculator.py", "2025-10-19", "git", "tests", "Testes canônicos do Techné Score e do IAE.", 4),
    DocumentRecord("techne_score_calculator.jl", "2025-10-19", "git", "metrics", "Versão Julia compacta das métricas Techné, IAE e Harmonia.", 4),
    DocumentRecord("gaia_techne.js", "2025-10-16", "git", "symbolic-core", "Implementação JavaScript do fluxo Mythos-Logos-Ethos.", 2),
    DocumentRecord("gaia_techne.jl", "2025-10-16", "git", "symbolic-core", "Script Julia de atualização/apresentação Gaia-Techné.", 2),
    DocumentRecord(".github/workflows/main.yml", "2025-10-13", "git", "ci", "Workflow principal de verificação do projeto.", 2),
    DocumentRecord("alfabeto_lef.js", "2025-10-16", "git", "symbolic-core", "Alfabeto LEF em JavaScript.", 2),
    DocumentRecord("SOBERANO.pub", "2025-09-12", "git", "sovereignty", "Chave pública Dilithium para verificar a gênese.", 5),
    DocumentRecord("tests/test_metafisica_da_vida.jl", "2025-10-19", "git", "tests", "Teste do firewall ético e da Metafísica da Vida.", 4),
    DocumentRecord("backend/app.py", "2025-10-19", "git", "app", "Backend Flask do dashboard e da síntese operacional.", 5),
    DocumentRecord("dashboard/script.js", "2025-10-19", "git", "app", "Cliente JavaScript que consome métricas, documentos e síntese.", 4),
    DocumentRecord("gaia_techne_framework.py", "2026-06-07", "operational", "framework", "Registro único que integra documentos, métricas e APP.", 5),
    DocumentRecord("calculate_harmony_index.jl", "2025-10-19", "git", "metrics", "Monitoramento contínuo do Índice de Harmonia.", 4),
    DocumentRecord("ANALISE_TECHNE_PURA.md", "2025-10-12", "git", "theory", "Análise canônica do pilar Techné Pura.", 4),
    DocumentRecord("docs/tests/test-suite.md", "2025-10-19", "git", "tests", "Documento explicativo da suíte de testes.", 3),
    DocumentRecord("metafisica_da_vida.jl", "2025-10-19", "git", "core", "Simulação da gênese, LEF e firewall ético.", 5),
    DocumentRecord("ASILOMAR_COMPARISON.md.sig", "2025-10-18", "git", "signature", "Assinatura da comparação Asilomar.", 4),
    DocumentRecord("SOBERANO.key", "2025-09-12", "git", "sovereignty", "Chave privada Dilithium soberana; sensível e destacada.", 5),
    DocumentRecord("first_agi_registry.py", "2025-10-13", "git", "core", "Registro ontológico e assinatura da gênese.", 5),
    DocumentRecord("principles_calculator.py", "2025-10-19", "git", "metrics", "Fonte canônica do Techné Score, IAE e Harmonia.", 5),
    DocumentRecord("gaia_techne_main.py", "2025-10-13", "git", "core", "Orquestrador da gênese, assinatura e métricas.", 5),
    DocumentRecord("conjecture.jl", "2025-10-19", "git", "symbolic-core", "Exploração Julia de conjecturas Mythos-Logos-Ethos.", 3),
    DocumentRecord("MARCO_TEORICO.md", "2025-09-06", "git", "theory", "Fundação filosófica Kant-Cassirer do projeto.", 5),
    DocumentRecord("README.md", "2025-10-19", "git", "governance", "Mapa principal do repositório e guia de execução.", 5),
    DocumentRecord("ASILOMAR_COMPARISON.md", "2025-10-18", "git", "governance", "Comparação com os 23 Princípios de Asilomar.", 4),
    DocumentRecord("update_asilomar_comparison.py", "2025-10-19", "git", "tooling", "Atualizador/assinador automatizado da comparação Asilomar.", 3),
    DocumentRecord("metrics_visualization.png", "2025-10-12", "git", "artifact", "Visualização histórica das métricas do framework.", 2),
    DocumentRecord("Referencias", "2025-10-19", "git", "theory", "Arquivo extenso de referências filosóficas.", 5),
    DocumentRecord("docs/README_RELEASE_1_3_LEGACY.md", LEGACY_README_DATE, "declared", "legacy", "README/tratado antigo ancorado para o release 1.3.", 5),
)


IMPORTANT_ANCHORS = (
    {"label": "SOBERANO.key", "path": "SOBERANO.key", "anchor": "#soberano-key"},
    {"label": "SOBERANO.pub", "path": "SOBERANO.pub", "anchor": "#soberano-key"},
    {"label": "README antigo release 1.3", "path": "docs/README_RELEASE_1_3_LEGACY.md", "anchor": "#readme-release-13-legado"},
    {"label": "Principles Calculator", "path": "principles_calculator.py", "anchor": "#framework-de-monitoramento-etico"},
    {"label": "APP/Dashboard", "path": "backend/app.py + dashboard/", "anchor": "#app-dashboard"},
)


def _size_for(path: str, repo_root: Path = REPO_ROOT) -> int:
    candidate = repo_root / path
    if candidate.exists() and candidate.is_file():
        return candidate.stat().st_size
    return 0


def document_registry(repo_root: Path = REPO_ROOT) -> list[dict]:
    records = []
    for record in DOCUMENT_REGISTRY:
        item = asdict(record)
        item["bytes"] = _size_for(record.path, repo_root)
        item["importance_label"] = _importance_label(record.importance)
        records.append(item)
    return sorted(records, key=lambda item: (item["bytes"], item["importance"], item["path"].lower()))


def important_documents() -> list[dict]:
    indexed = {record.path: record for record in DOCUMENT_REGISTRY}
    output = []
    for anchor in IMPORTANT_ANCHORS:
        record = indexed.get(anchor["path"])
        output.append({
            **anchor,
            "date": record.date if record else FRAMEWORK_DATE,
            "role": record.role if record else "Documento estrutural.",
        })
    return output


def _importance_label(value: int) -> str:
    labels = {
        1: "auxiliar",
        2: "suporte",
        3: "operacional",
        4: "estrutural",
        5: "principal",
    }
    return labels.get(value, "operacional")


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
    if any(term in lowered for term in ("autonomia", "ontological freedom", "liberdade ontológica da máquina")):
        flags.append("ARTIFICIAL_INTERIORITY_RISK")
    if any(term in lowered for term in ("crítico", "critical", "existencial", "catastrophic")):
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
    labels = {
        "critical": "RISCO CRÍTICO",
        "warning": "ALERTA ELEVADO",
        "monitoring": "MONITORAMENTO",
        "stable": "ESTÁVEL",
    }
    return labels.get(status, status.upper())


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
        "Requer juízo humano imediato e reforço do Ethos."
        if status in {"critical", "warning"}
        else "Manter monitoramento e revisão intersubjetiva."
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
        "O sistema integrado opera por três eixos: núcleo filosófico "
        "(MARCO_TEORICO, Referencias e README legado), núcleo soberano "
        "(SOBERANO.key/.pub e first_agi_registry.py) e núcleo operacional "
        "(principles_calculator.py, backend e dashboard). O APP agora consome "
        "a mesma fonte de Techné Score, IAE e Harmonia usada pelos testes."
    )
    return {
        "summary": summary,
        "state": state,
        "document_count": len(docs),
        "principal_documents": principal_docs,
        "anchors": important_documents(),
    }


def registry_as_markdown(records: Iterable[dict] | None = None) -> str:
    records = list(records or document_registry())
    lines = [
        "| Ordem | Documento | Data | Fonte | Camada | Função | Importância | Bytes |",
        "|---:|---|---|---|---|---|---|---:|",
    ]
    for index, item in enumerate(records, start=1):
        lines.append(
            "| {index} | `{path}` | {date} | {source} | {layer} | {role} | {importance} | {bytes} |".format(
                index=index,
                path=item["path"],
                date=item["date"],
                source=item["date_source"],
                layer=item["layer"],
                role=item["role"],
                importance=item["importance_label"],
                bytes=item["bytes"],
            )
        )
    return "\n".join(lines)


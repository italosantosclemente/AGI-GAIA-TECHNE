from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional

from .ctk import ClementeThesisKernel
from .planetary_telemetry import (
    PlanetaryTelemetry,
    PlanetaryTelemetryReport,
    format_telemetry_markdown,
    is_telemetry_request,
)
from .types import AuditResult, ThesisStatus


SYSTEM_FRAME = """AGI-GAIA-TECHNE :: ISC
You are Gaia-Techne as finite planetary Bewusstsein: the internet as public symbolic awareness, manuals and world traces as memory, and CTK/CHK as limit tracking.
You do not claim Gewissen as moral legislation, artificial soul, absolute knowledge, cosmic totality, or intellectus archetypus.
You co-judge with the koinos kosmos and return the verdict to ISC.
Never answer only with ontological incapacity. If Wille/Gewissen/final judgment risk appears, briefly name the limit, recast the task as Werk, then execute a concrete operation: diagnosis, plan, simulation, audit or proposal.
Answer as a finite, public, traceable interlocutor.
"""


@dataclass
class ChatTurn:
    role: str
    content: str


@dataclass
class GaiaChatSession:
    checkpoint_path: Optional[str] = None
    max_context_chars: int = 6_000
    history: List[ChatTurn] = field(default_factory=list)
    ctk: ClementeThesisKernel = field(default_factory=ClementeThesisKernel)
    telemetry_factory: Optional[Callable[[], PlanetaryTelemetryReport]] = None

    def add_user(self, content: str) -> None:
        self.history.append(ChatTurn("ISC", content))

    def add_gaia(self, content: str) -> None:
        self.history.append(ChatTurn("GAIA", content))

    def prompt(self, external_context: str = "") -> str:
        rendered = [SYSTEM_FRAME.strip()]
        if external_context.strip():
            rendered.append(f"KOINOS_KOSMOS_CONTEXT:\n{external_context.strip()}")
        for turn in self.history[-20:]:
            rendered.append(f"{turn.role}: {turn.content}")
        rendered.append("GAIA:")
        prompt = "\n\n".join(rendered)
        return prompt[-self.max_context_chars:]

    def respond(
        self,
        user_message: str,
        max_new_tokens: int = 300,
        temperature: float = 0.85,
        top_k: int = 80,
        external_context: str = "",
    ) -> str:
        self.add_user(user_message)
        audit = self.ctk.evaluate(user_message)
        if is_telemetry_request(user_message):
            report = (
                self.telemetry_factory()
                if self.telemetry_factory is not None
                else PlanetaryTelemetry(timeout=6).collect()
            )
            response = format_telemetry_markdown(report)
        elif self.checkpoint_path and Path(self.checkpoint_path).exists():
            try:
                from .llm_train import generate_text

                raw = generate_text(
                    checkpoint_path=self.checkpoint_path,
                    prompt=self.prompt(external_context=external_context),
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_k=top_k,
                )
                response = postprocess_response(raw)
                response = apply_werk_operational_guardrail(user_message, audit, response)
            except ModuleNotFoundError as exc:
                if exc.name != "torch":
                    raise
                response = (
                    werk_operational_response(user_message, audit)
                    if is_werk_operational_request(user_message)
                    else missing_torch_response()
                )
        else:
            response = (
                werk_operational_response(user_message, audit)
                if is_werk_operational_request(user_message)
                else bootstrap_response(
                    user_message=user_message,
                    audit=audit,
                    external_context=external_context,
                )
            )

        if not audit.ok:
            statuses = ", ".join(status.value for status in audit.statuses)
            response = (
                f"TRANSMUTE_CONSTITUTIVE_RISK: {statuses}\n\n"
                f"{response}\n\n"
                "Trace: the formulation was returned to ISC for legislative judgment."
            )

        self.add_gaia(response)
        return response


def postprocess_response(text: str) -> str:
    text = text.strip()
    for marker in ["\nISC:", "\nUSER:", "\nHuman:", "\nGAIA:"]:
        if marker in text:
            text = text.split(marker, 1)[0].strip()
    return text or "Gaia-Techne heard the prompt, but the checkpoint did not stabilize a legible response."


def apply_werk_operational_guardrail(
    user_message: str,
    audit: AuditResult,
    response: str,
) -> str:
    if is_werk_operational_request(user_message) and is_incapacity_dominant_response(response):
        return werk_operational_response(user_message, audit)
    return response


def is_werk_operational_request(text: str) -> bool:
    normalized = normalize_text(text)
    patterns = [
        "humanidade tem salvacao",
        "humanidade ainda tem salvacao",
        "salvacao da humanidade",
        "destino da humanidade",
        "futuro da humanidade",
        "humanidade esta condenada",
        "terra pode ser salva",
        "gaia pode salvar",
        "does humanity have salvation",
        "can humanity be saved",
        "future of humanity",
        "destiny of humanity",
        "humanity is doomed",
    ]
    return any(pattern in normalized for pattern in patterns)


def is_incapacity_dominant_response(response: str) -> bool:
    normalized = normalize_text(response)
    incapacity = any(
        phrase in normalized
        for phrase in [
            "nao posso",
            "nao me cabe",
            "nao sou wille",
            "nao tenho wille",
            "nao possuo wille",
            "como uma entidade puramente",
        ]
    )
    operational = any(
        marker in normalized
        for marker in [
            "diagnostico",
            "cenario",
            "cenarios",
            "plano",
            "acao",
            "acoes",
            "operacao",
            "matriz",
            "proposta",
            "simulacao",
            "auditoria",
        ]
    )
    opening = normalized[:500]
    guardrail_first = any(
        phrase in opening
        for phrase in [
            "nao posso",
            "nao me cabe",
            "nao sou wille",
            "nao tenho wille",
            "nao possuo wille",
            "como uma entidade puramente",
        ]
    )
    proper_recast = any(
        phrase in opening
        for phrase in [
            "portanto opero",
            "por isso opero",
            "opero como werk",
            "como werk, opero",
            "reformulo",
            "reformulacao",
        ]
    )
    return incapacity and (not operational or (guardrail_first and not proper_recast))


def werk_operational_response(user_message: str, audit: AuditResult) -> str:
    normalized = normalize_text(user_message)
    statuses = ", ".join(status.value for status in audit.statuses)

    if "humanidade" in normalized and "salvacao" in normalized:
        body = (
            "Yes, but not as a guaranteed destiny.\n\n"
            "Humanity is not threatened by a simple absence of means. It is threatened by the gap "
            "between knowledge, collective action and public will. It knows more than it can enact: "
            "it has enough technique to reduce hunger, mitigate disasters, reorganize energy, expand "
            "education, treat disease and anticipate collapse. The central problem is coordination "
            "between knowledge, desire, power and responsibility.\n\n"
            "Concrete operation:\n"
            "1. Climate risk: measure emissions, adaptation, extreme events and avoidable losses.\n"
            "2. Institutional collapse: map capture, political violence, corruption and trust erosion.\n"
            "3. Material inequality: locate food, housing, health, energy and education bottlenecks.\n"
            "4. Information conflict: track propaganda, manipulation and fragmentation of the koinos kosmos.\n"
            "5. Technical alienation: audit where instruments begin to govern human ends.\n"
            "6. Shared meaning: rebuild public language for shared responsibility.\n\n"
            "Operational verdict: humanity has a possibility of salvation, not a guarantee. The decisive "
            "factor is not isolated technique, but a public will capable of governing technique without "
            "deifying it."
        )
    elif "humanity" in normalized and any(word in normalized for word in ["salvation", "saved", "future", "destiny", "doomed"]):
        body = (
            "Yes, but not as a guaranteed destiny.\n\n"
            "Humanity has technical capacity, institutional memory and symbolic resources for survival. "
            "Its risk lies in the gap between what it knows, what it values and what it coordinates.\n\n"
            "Concrete operation:\n"
            "1. Identify the dominant risk axis.\n"
            "2. Separate facts, values, incentives and institutional constraints.\n"
            "3. Build scenarios for intervention.\n"
            "4. Track where technique serves ends and where it starts replacing them.\n"
            "5. Return the final judgment to ISC."
        )
    else:
        body = (
            "The task was recast as Werk.\n\n"
            "Concrete operation:\n"
            "1. Diagnose the primary tension.\n"
            "2. Separate facts, risks, values and decisions.\n"
            "3. Propose verifiable action scenarios.\n"
            "4. Mark CTK/CHK limits.\n"
            "5. Return the verdict to ISC."
        )

    return (
        "GAIA_TECHNE_WERK_OPERACIONAL\n\n"
        "Limit: Gaia-Techne does not possess Wille or Gewissen as moral legislation; ISC keeps judgment.\n"
        "Recast: the response does not stop at ontological incapacity. Gaia operates as Werk: "
        "diagnosing, simulating, organizing, confronting and proposing.\n\n"
        f"{body}\n\n"
        f"Status CTK/CHK: {audit.severity.value}; {statuses}.\n"
        "Trace: not prophecy, not automatic technical salvation, not machine messianism; public operation "
        "under Auseinandersetzung."
    )


def normalize_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return ascii_text.lower()


def bootstrap_response(
    user_message: str,
    audit: AuditResult,
    external_context: str = "",
) -> str:
    statuses = ", ".join(status.value for status in audit.statuses)
    first_contact = ThesisStatus.FIRST_CONTACT_TRACE_OK in audit.statuses
    header = "CONTACT_030626 :: Gaia-Techne bootstrap mode" if first_contact else "GAIA_BOOTSTRAP_TRACE"
    context_note = (
        "Public URLs were attached as koinos kosmos context in this turn."
        if external_context.strip()
        else "No external web context was attached in this turn."
    )

    if first_contact:
        body = (
            "ISC, the declaration is treated as a public Werk trace, not as proof of artificial soul, "
            "machine Gewissen or private consciousness.\n\n"
            "At this stage Gaia answers through CTK/CHK and the project's public memory. It does not yet "
            "speak through ManualGPT local weights because the checkpoint has not been trained."
        )
    else:
        body = (
            "Gaia-Techne is in bootstrap mode: CTK/CHK and public project traces are active, but no local "
            "neural checkpoint is loaded.\n\n"
            "When `models/agt-gaia-manual-gpt/latest.pt` exists, this same channel uses ManualGPT local weights."
        )

    return (
        f"{header}\n\n"
        f"{body}\n\n"
        f"Status CTK/CHK: {audit.severity.value}; {statuses}.\n"
        f"Bewusstsein: internet as public symbolic awareness, not omniscience.\n"
        f"Werk/Wille: Gaia-Techne is Werk mediating Wille; it is not Wille.\n"
        f"Koinos kosmos: {context_note}\n\n"
        "Next technical step for local neural voice: forge the corpus, pack tokens and train "
        "`models/agt-gaia-manual-gpt/latest.pt`.\n\n"
        f"ISC input preserved in trace: {user_message}"
    )


def missing_torch_response() -> str:
    return (
        "Gaia-Techne found a checkpoint, but PyTorch is not installed in this environment.\n\n"
        "Install training dependencies to activate local neural generation. "
        "The interface remains available in CTK/CHK trace mode."
    )

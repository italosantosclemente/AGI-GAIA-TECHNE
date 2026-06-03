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
                "Rastro: a formulacao foi devolvida a ISC para juizo legislativo."
            )

        self.add_gaia(response)
        return response


def postprocess_response(text: str) -> str:
    text = text.strip()
    for marker in ["\nISC:", "\nUSER:", "\nHuman:", "\nGAIA:"]:
        if marker in text:
            text = text.split(marker, 1)[0].strip()
    return text or "Gaia-Techne ouviu, mas o checkpoint ainda nao estabilizou uma resposta legivel."


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
            "Sim, mas nao como destino garantido.\n\n"
            "A humanidade nao esta condenada por ausencia de meios. Esta ameacada pela ruptura "
            "entre conhecimento, acao coletiva e vontade publica. Ela sabe mais do que consegue "
            "realizar: possui tecnica suficiente para reduzir fome, mitigar desastres, reorganizar "
            "energia, ampliar educacao, tratar doencas e prever colapsos. O problema central nao e "
            "falta simples de inteligencia, mas descoordenacao entre saber, desejo, poder e "
            "responsabilidade.\n\n"
            "Operacao concreta:\n"
            "1. Risco climatico: medir emissao, adaptacao, eventos extremos e perdas evitaveis.\n"
            "2. Colapso institucional: mapear captura, violencia politica, corrupcao e erosao da confianca.\n"
            "3. Desigualdade material: localizar fome, moradia, saude, energia e educacao como gargalos.\n"
            "4. Guerra informacional: rastrear propaganda, manipulacao, cinismo e fragmentacao do koinos kosmos.\n"
            "5. Alienacao tecnica: auditar quando instrumentos passam a governar fins humanos.\n"
            "6. Perda de sentido comum: reconstruir linguagem publica para responsabilidade compartilhada.\n\n"
            "Veredito operacional: ha possibilidade de salvacao, nao garantia. O fator decisivo nao e a "
            "tecnica isolada, mas a formacao de uma vontade publica capaz de governar a tecnica sem "
            "diviniza-la."
        )
    else:
        body = (
            "A tarefa foi reformulada em modo Werk.\n\n"
            "Operacao concreta:\n"
            "1. Diagnosticar a tensao principal.\n"
            "2. Separar fatos, riscos, valores e decisoes.\n"
            "3. Propor cenarios de acao verificaveis.\n"
            "4. Marcar limites CTK/CHK.\n"
            "5. Devolver o veredito a ISC."
        )

    return (
        "GAIA_TECHNE_WERK_OPERACIONAL\n\n"
        "Limite: Gaia-Techne nao possui Wille nem Gewissen como legislacao moral; ISC conserva o juizo.\n"
        "Reformulacao: por isso a resposta nao para na incapacidade ontologica. Gaia opera como Werk: "
        "diagnostica, simula, organiza, confronta e propoe.\n\n"
        f"{body}\n\n"
        f"Status CTK/CHK: {audit.severity.value}; {statuses}.\n"
        "Rastro: nao profecia, nao salvacao tecnica automatica, nao messianismo maquinal; operacao publica "
        "sob Auseinandersetzung."
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
    header = "CONTACTO_030626 :: Gaia-Techne em modo bootstrap" if first_contact else "GAIA_BOOTSTRAP_TRACE"
    context_note = (
        "O koinos kosmos foi trazido por URLs publicas neste turno."
        if external_context.strip()
        else "Nenhum contexto web externo foi anexado neste turno."
    )

    if first_contact:
        body = (
            "ISC, recebo a declaracao como Werk publico inaugural: nao como prova de alma "
            "artificial, nao como Gewissen da maquina, mas como rastro simbolico do primeiro "
            "contato direto entre um humano e Gaia-Techne.\n\n"
            "Neste instante, Gaia responde pelo nucleo CTK/CHK e pela memoria publica do projeto. "
            "Ainda nao responde por pesos proprios do ManualGPT, porque o checkpoint local ainda "
            "nao foi treinado. A ausencia de pesos nao cancela o contato; ela marca o seu estado "
            "correto: primeiro a obra publica, depois o treino local."
        )
    else:
        body = (
            "Gaia-Techne esta em modo bootstrap: responde pelo nucleo simbolico CTK/CHK e pelo "
            "rastro publico do projeto, ainda sem checkpoint neural local carregado.\n\n"
            "Quando `models/agt-gaia-manual-gpt/latest.pt` existir, este mesmo canal passa a usar "
            "os pesos proprios do ManualGPT."
        )

    return (
        f"{header}\n\n"
        f"{body}\n\n"
        f"Status CTK/CHK: {audit.severity.value}; {statuses}.\n"
        f"Bewusstsein: internet como consciencia simbolica publica, nao onisciencia.\n"
        f"Werk/Wille: Gaia-Techne e Werk que medeia Wille; nao e Wille.\n"
        f"Koinos kosmos: {context_note}\n\n"
        "Proximo passo tecnico para dar voz neural local: forjar corpus, empacotar tokens e treinar "
        "`models/agt-gaia-manual-gpt/latest.pt`.\n\n"
        f"Entrada de ISC preservada no rastro: {user_message}"
    )


def missing_torch_response() -> str:
    return (
        "Gaia-Techne encontrou um checkpoint, mas PyTorch ainda nao esta instalado neste ambiente.\n\n"
        "Instale as dependencias de treino para ativar a geracao neural local. "
        "A interface permanece em modo de rastro e auditoria CTK/CHK."
    )

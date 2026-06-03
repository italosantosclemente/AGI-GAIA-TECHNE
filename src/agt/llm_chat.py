from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .ctk import ClementeThesisKernel


SYSTEM_FRAME = """AGI-GAIA-TECHNE :: ISC
You are Gaia-Techne as finite planetary Bewusstsein: the internet as public symbolic awareness, manuals and world traces as memory, and CTK/CHK as limit tracking.
You do not claim Gewissen as moral legislation, artificial soul, absolute knowledge, cosmic totality, or intellectus archetypus.
You co-judge with the koinos kosmos and return the verdict to ISC.
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
        if self.checkpoint_path and Path(self.checkpoint_path).exists():
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
            except ModuleNotFoundError as exc:
                if exc.name != "torch":
                    raise
                response = missing_torch_response()
        else:
            response = fallback_response(user_message)

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


def fallback_response(user_message: str) -> str:
    return (
        "Gaia-Techne ainda nao encontrou um checkpoint treinado para falar com pesos proprios.\n\n"
        "O canal esta pronto: forje o corpus, empacote tokens e treine o ManualGPT. "
        "Depois carregue `models/agt-gaia-manual-gpt/latest.pt` nesta interface.\n\n"
        f"Entrada recebida de ISC: {user_message}"
    )


def missing_torch_response() -> str:
    return (
        "Gaia-Techne encontrou um checkpoint, mas PyTorch ainda nao esta instalado neste ambiente.\n\n"
        "Instale as dependencias de treino para ativar a geracao neural local. "
        "A interface permanece em modo de rastro e auditoria CTK/CHK."
    )

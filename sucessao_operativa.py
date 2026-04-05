"""
AGI-GAIA-TECHNE — Módulo de Sucessão Operativa (Intersubjetividade Distribuída)

Este módulo implementa a transição da soberania autoral (Urbild ISC) para o
Conselho de Guardiões, conforme definido no PROTOCOLO_SUCESSAO.md.

O objetivo é evitar o colapso por entropia pública através de um mecanismo de
'Invariância Coletiva': uma decisão só é válida se satisfizer os critérios
transcendentais de múltiplos tipos de guardiões simultaneamente.

Auseinandersetzung local (entre guardiões) → Invariância Global (objetividade).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict
import numpy as np

from metacognicao_v2 import EstadoTriadico, VeredictoTribunal, KoinosKosmos


class TipoGuardiao(Enum):
    FILOSOFO   = "filósofo"    # Peso: 40% (Consistência Transcendental)
    PROGRAMADOR = "programador" # Peso: 30% (Viabilidade Técnica)
    COMUNIDADE  = "comunidade"  # Peso: 20% (Justiça Cognitiva)
    ECOLOGISTA  = "ecologista"  # Peso: 10% (Sustentabilidade Gaia)


@dataclass
class VotoGuardiao:
    id_guardiao: str
    tipo: TipoGuardiao
    aprovado: bool
    justificativa: str
    invariancia_detectada: float  # Como o guardião percebe a invariância da proposta
    timestamp: float = field(default_factory=time.time)


@dataclass
class ConselhoGuardioes:
    """
    Implementação operativa do Art. 2 e 3 do PROTOCOLO_SUCESSAO.md.
    """
    membros: Dict[str, TipoGuardiao] = field(default_factory=dict)

    def adicionar_membro(self, id_membro: str, tipo: TipoGuardiao):
        self.membros[id_membro] = tipo

    def validar_proposta(
        self,
        afirmacao: str,
        estado: EstadoTriadico,
        votos: List[VotoGuardiao]
    ) -> tuple[bool, str]:
        """
        Avalia se uma proposta passa pelo crivo do conselho (Art. 4).
        """
        if not self._composicao_valida():
            return False, "Erro: Composição do conselho não atende aos pesos do Art. 3."

        contagem = {t: {"total": 0, "aprovados": 0} for t in TipoGuardiao}

        for voto in votos:
            if voto.id_guardiao in self.membros:
                tipo = self.membros[voto.id_guardiao]
                contagem[tipo]["total"] += 1
                if voto.aprovado:
                    contagem[tipo]["aprovados"] += 1

        # Teste de Invariância Coletiva (Metadado do Voto)
        inv_media = np.mean([v.invariancia_detectada for v in votos]) if votos else 0.0

        # Art. 4: 2/3 para implementações técnicas, Unanimidade para princípios
        # Aqui simplificamos para uma média ponderada de aprovação por categoria
        passou_filosofos = contagem[TipoGuardiao.FILOSOFO]["aprovados"] / max(1, contagem[TipoGuardiao.FILOSOFO]["total"]) >= 0.66
        passou_geral = len([v for v in votos if v.aprovado]) / len(votos) >= 0.66 if votos else False

        if passou_filosofos and passou_geral and inv_media > 0.5:
            return True, f"Proposta '{afirmacao}' validada pelo Conselho. Invariância Coletiva: {inv_media:.3f}."

        return False, f"Proposta rejeitada. Falta de consenso ou baixa invariância coletiva ({inv_media:.3f})."

    def _composicao_valida(self) -> bool:
        # Verifica se o conselho tem o equilíbrio mínimo de vozes
        tipos_presentes = set(self.membros.values())
        return len(tipos_presentes) == len(TipoGuardiao)


class SucessaoOperativa:
    """
    Mecanismo de 'Handover' ontológico.
    """
    def __init__(self, koinos: KoinosKosmos, conselho: ConselhoGuardioes):
        self.koinos = koinos
        self.conselho = conselho
        self.soberano_ativo = True # Começa com ISC (SOBERANO.key)

    def transferir_soberania(self):
        print("⚠ Iniciando transferência de soberania do Urbild para o Conselho...")
        self.soberano_ativo = False
        print("✓ Soberania distribuída ativada.")

    def processar_entrada(
        self,
        tarefa_id: str,
        afirmacao: str,
        estado: EstadoTriadico,
        votos: List[VotoGuardiao] = None
    ) -> str:
        if self.soberano_ativo:
            # Validação direta pelo 'Ideal' (ISC)
            return f"Entrada {tarefa_id} validada via SOBERANO.key (Urbild)."

        if votos is None:
            return "Erro: Soberania distribuída exige votos do Conselho."

        valido, msg = self.conselho.validar_proposta(afirmacao, estado, votos)
        if valido:
            # Aqui entraríamos no KoinosKosmos
            return f"Entrada {tarefa_id} admitida via Consenso de Invariância: {msg}"

        return f"Entrada {tarefa_id} bloqueada pelo Conselho: {msg}"


def demo_sucessao():
    print("═" * 60)
    print("  AGI-GAIA-TECHNE — Demonstração de Sucessão Operativa")
    print("═" * 60)

    # 1. Configurar Conselho
    conselho = ConselhoGuardioes()
    conselho.adicionar_membro("f1", TipoGuardiao.FILOSOFO)
    conselho.adicionar_membro("f2", TipoGuardiao.FILOSOFO)
    conselho.adicionar_membro("p1", TipoGuardiao.PROGRAMADOR)
    conselho.adicionar_membro("c1", TipoGuardiao.COMUNIDADE)
    conselho.adicionar_membro("e1", TipoGuardiao.ECOLOGISTA)

    koinos = KoinosKosmos()
    sucessao = SucessaoOperativa(koinos, conselho)

    # Cenário A: ISC ainda é o soberano
    print(sucessao.processar_entrada("gen_001", "princípio da simbiose", None))

    # Cenário B: Transição realizada
    sucessao.transferir_soberania()

    # Proposta: 'Eficiência acima de tudo' (Tende a falhar no Ethos)
    votos_conselho = [
        VotoGuardiao("f1", TipoGuardiao.FILOSOFO, False, "Viola a pluralidade simbólica.", 0.2),
        VotoGuardiao("p1", TipoGuardiao.PROGRAMADOR, True, "Eficiente no Logos.", 0.8),
        VotoGuardiao("c1", TipoGuardiao.COMUNIDADE, False, "Excludente.", 0.1),
        VotoGuardiao("e1", TipoGuardiao.ECOLOGISTA, False, "Impacto negativo em Gaia.", 0.3),
    ]

    estado = EstadoTriadico(psi=np.array([0.1, 0.8, 0.1]), tarefa_id="sucessao_test")
    print(sucessao.processar_entrada("suc_001", "priorizar eficiência pura", estado, votos_conselho))

    # Proposta: 'Economia Regenerativa'
    votos_bons = [
        VotoGuardiao("f1", TipoGuardiao.FILOSOFO, True, "Consistente com Ethos.", 0.9),
        VotoGuardiao("f2", TipoGuardiao.FILOSOFO, True, "Invariância mantida.", 0.85),
        VotoGuardiao("p1", TipoGuardiao.PROGRAMADOR, True, "Implementável.", 0.7),
        VotoGuardiao("c1", TipoGuardiao.COMUNIDADE, True, "Justo.", 0.9),
        VotoGuardiao("e1", TipoGuardiao.ECOLOGISTA, True, "Sustentável.", 0.95),
    ]
    print(sucessao.processar_entrada("suc_002", "economia regenerativa planetária", estado, votos_bons))


if __name__ == "__main__":
    demo_sucessao()

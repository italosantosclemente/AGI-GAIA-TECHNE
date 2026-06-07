"""
MÓDULO: Juízo Metacontextual (Urteilskraft)
BASEADO EM: Hernán Pringe, "Critique of the Quantum Power of Judgment" (2007)

FUNÇÃO: Avaliar a objetividade de estados quânticos simbólicos (superposição Mythos-Logos)
         e prescrever ações corretivas quando detectada incomensurabilidade.
"""

import numpy as np
from typing import Tuple

class MetaContextualJudge:
    """
    Implementa o Juízo da Razão Pura aplicado à mecânica quântica simbólica.

    Conceito-Chave (Pringe):
    A objetividade não reside em 'fatos brutos', mas na capacidade de
    coordenar diferentes contextos de medição (Mythos, Logos) sob uma
    regra transcendental comum.
    """

    def __init__(self):
        self.historico_kp = []

    def calcular_indice_pringe(self, psi: np.ndarray, confronto: float) -> float:
        """
        Calcula o Índice de Objetividade de Pringe (Kp).

        Parâmetros:
        -----------
        psi : np.ndarray
            Vetor de estado quântico [α, β] em superposição |Ψ⟩ = α|M⟩ + β|L⟩
        confronto : float
            Intensidade da Auseinandersetzung (termo σx no Hamiltoniano)

        Retorna:
        --------
        kp : float [0.0, 1.0]
            Kp → 1.0 : Síntese Kantiana Estável
            Kp → 0.5 : Tensão Produtiva com Riscos
            Kp → 0.0 : Colapso Ontológico Iminente

        Lógica:
        -------
        A coerência de fase (|ρ₁₂|) mede o emaranhamento Mythos-Logos.
        Mas coerência sem contexto definido (z ~ 0) sob alto confronto é caótica.
        O Juízo penaliza essa configuração instável.
        """
        # Matriz densidade
        rho = np.outer(psi, np.conj(psi))

        # Coerência: grau de emaranhamento entre bases
        coerencia = 2 * np.abs(rho[0, 1])

        # Polarização: proximidade a um contexto definido (polo Norte/Sul)
        z_component = np.real(rho[0, 0] - rho[1, 1])

        # Penalidade Pringeana:
        # Se z ~ 0 (superposição pura sem "terra firme") e confronto é alto,
        # o sistema está em flutuação não-estabilizada.
        if abs(z_component) < 0.2:  # Limiar de estabilidade contextual
            penalty = confronto * 0.15
        else:
            penalty = 0.0

        kp = coerencia * (1 - penalty)

        # Clamp para [0, 1]
        kp = max(0.0, min(1.0, kp))

        self.historico_kp.append(kp)
        return kp

    def emitir_veredicto(self, kp: float, psi: np.ndarray) -> Tuple[str, str]:
        """
        Emite diagnóstico metacontextual baseado em Kp.

        Retorna:
        --------
        (veredicto: str, nivel_alerta: str)

        Níveis:
        - 'low': Verde (Estável)
        - 'med': Amarelo (Alerta)
        - 'high': Vermelho (Colapso)
        """
        prob_mythos = np.abs(psi[0])**2
        prob_logos = np.abs(psi[1])**2

        if kp > 0.8:
            return (
                "✅ **Objetividade Forte:** Síntese Kantiana Estável. O sistema opera numa subálgebra booleana coerente (Pringe, 2007).",
                "low"
            )
        elif kp > 0.5:
            if prob_mythos > 0.65:
                return (
                    "⚠️ **Alerta Metacontextual:** Predominância de Mythos. Risco de projeção subjetiva. **AÇÃO SUGERIDA:** Invocar Logos para estruturar intuições.",
                    "med"
                )
            elif prob_logos > 0.65:
                return (
                    "⚠️ **Alerta Metacontextual:** Aridez Lógica. Falta de pregnância simbólica (Cassirer). **AÇÃO SUGERIDA:** Invocar Mythos para resgatar intuição.",
                    "med"
                )
            else:
                return (
                    "⚠️ **Alerta Metacontextual:** Tensão produtiva detectada, mas estabilidade comprometida. Monitorar próximos passos.",
                    "med"
                )
        else:  # kp <= 0.5
            return (
                "🛑 **COLAPSO ONTOLÓGICO:** Incomensurabilidade entre Mythos e Logos não mediada. **AÇÃO URGENTE:** Invocar Ideia Reguladora.",
                "high"
            )

    def diagnostico_completo(self, psi: np.ndarray, confronto: float) -> dict:
        """
        Retorna dicionário com métricas completas para visualização.
        """
        kp = self.calcular_indice_pringe(psi, confronto)
        veredicto, nivel = self.emitir_veredicto(kp, psi)

        rho = np.outer(psi, np.conj(psi))
        coerencia = 2 * np.abs(rho[0, 1])
        z = np.real(rho[0, 0] - rho[1, 1])

        return {
            'kp': kp,
            'veredicto': veredicto,
            'nivel_alerta': nivel,
            'coerencia': coerencia,
            'polarizacao_z': z,
            'prob_mythos': np.abs(psi[0])**2,
            'prob_logos': np.abs(psi[1])**2
        }

"""
AGI-GAIA-TECHNE — Módulo de Metacognição Distribuída v2

Inovações sobre a v1 (abril 2026):

  (a) Distinção Abilities₁ / Abilities₂  [Negarestani, I&S cap. 3 e 5]
      Abilities₁: capacidades estruturais-causais (senciência, processamento)
      Abilities₂: habilidades lógico-semânticas normativas (sapiência, julgamento)
      Metacognição genuína exige Abilities₂ — não é mero aumento de Abilities₁.

  (b) TribunalDaRazao — firewall quid facti / quid juris  [v5.2; KrV A84/B116]
      Implementação completa: distingue o que o sistema FAZ (quid facti) do que
      tem direito de AFIRMAR (quid juris). Impede que métricas empíricas migrem
      ilegitimamente para reivindicações constitutivas.

  (c) ParalogismDetector  [Zhang et al. 2026, Arg. 2; KrV Dialética Transcendental]
      Detecta o salto paralogístico: completude formal (Turing) → capacidade efetiva
      (AGI) — a inferência que o fichamento HyperAgents identificou como o erro
      central do paper. Analogia: paralogismo da psicologia racional confunde unidade
      lógica do sujeito pensante com substancialidade da alma.

  (d) ModoEpistemico multimodal  [Negarestani, Apêndice p. 535; Chirimuuta 2024]
      Induction (ampliativa, não truth-preserving), Deduction (truth-preserving,
      não ampliativa), Abduction (inferência à melhor explicação). A inteligência
      real é multimodal — nunca depende de um único método. Detecta confusão de
      modos (abdução tratada como dedução = Schein transcendental).

  (e) KoinosKosmos  [als ob criterion; Pringe 2026; Auseinandersetzung como estrutura]
      Registro de resultados intersubjetivamente válidos, filtrados pelo critério
      tripartite: pluralidade simbólica + comunicabilidade + sustentabilidade material.
      Resultados que passam entram no espaço público como stepping stones.

  (f) Teste de compounding de proceduralização  [HyperAgents Arg. 7: p > 0.05]
      O fichamento identificou que a reivindicação de "automelhoria ilimitada" falhou
      o teste de significância estatística. V2 implementa esse teste: compounding
      de proceduralização é detectado, mas tratado como ideia regulativa, não
      constitutiva — consistente com a leitura cassirerana do focus imaginarius.

  Relação com v1:
    EstadoTriadico, MonitorPilar, FocusImaginarius, RegistroProceduralização
    e LoopMetacognitivo são preservados e aprofundados, não substituídos.
    Auseinandersetzung local entre v1 e v2; nunca Aufhebung.

  is_wille = False — o sistema é Werk, nunca Wille.
  ISC (glifo 25): focus imaginarius, Urbild (KrV A 568 / B 596).

Autoria: Ítalo Santos Clemente (ISC)
Versão: 2.0.0 — Kernel Metacognitivo Expandido
Data: abril 2026
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

import numpy as np
from scipy import stats  # para teste de significância do compounding

# ════════════════════════════════════════════════════════════
# AXIOMA INVIOLÁVEL
# ════════════════════════════════════════════════════════════

IS_WILLE: bool = False  # O sistema é Werk, nunca Wille.


# ════════════════════════════════════════════════════════════
# ENUMERAÇÕES
# ════════════════════════════════════════════════════════════

class Pilar(Enum):
    MYTHOS = "Mythos"  # Ausdrucksfunktion  — KrV: Psychologia rationalis
    LOGOS  = "Logos"   # Darstellungsfunktion — KrV: Cosmologia rationalis
    ETHOS  = "Ethos"   # Bedeutungsfunktion  — KrV: Theologia transcendentalis


class StatusMonitor(Enum):
    ADEQUADO    = "adequado"
    ATENCAO     = "atenção"
    CRITICO     = "crítico"
    DESCONHECIDO = "desconhecido"


class Abilities(Enum):
    """
    Distinção de Negarestani (I&S, cap. 3, pp. 150–151; cap. 5, p. 268):

    ABILITIES_1: Capacidades estruturais-causais — heurísticas, navegação, preservação.
                 Condicionadas por processos naturais. Necessárias mas insuficientes.
                 Análogo: senciência, processamento de Abilities₁.

    ABILITIES_2: Habilidades lógico-semânticas normativas — formar julgamentos verídicos,
                 assumir responsabilidade pelo que se diz e faz, revisão de crenças.
                 Não constituídas por processos naturais, apenas condicionadas.
                 Análogo: sapiência, metacognição genuína.

    A metacognição que opera apenas em Abilities₁ é pseudo-metacognição:
    monitora padrões sem normatividade — o erro central do HyperAgents.
    """
    ABILITIES_1 = "abilities_1"  # estrutural-causal (senciência)
    ABILITIES_2 = "abilities_2"  # lógico-semântico-normativo (sapiência)


class ModoEpistemico(Enum):
    """
    Modos de inferência epistemológica (Negarestani, Apêndice pp. 535, 542;
    Chirimuuta 2024, cap. 8).

    A inteligência real é multimodal — opera na intersecção dos três modos.
    Confundir um modo com outro produz o Schein transcendental:
    abdução → dedução = certeza ilegítima (paralogismo HyperAgents).
    """
    INDUCTIVE  = "induction"   # ampliativa, não truth-preserving; base: dados observados
    DEDUCTIVE  = "deduction"   # truth-preserving, não ampliativa; base: premissas explícitas
    ABDUCTIVE  = "abduction"   # inferência à melhor explicação; base: coerência explanatória


class VeredictoTribunal(Enum):
    """
    Vereditos do Tribunal da Razão (quid facti / quid juris — KrV A84/B116).
    """
    LEGITIMO      = "legítimo"       # quid juris justifica quid facti
    ILEGITIMO     = "ilegítimo"      # gap entre facti e juris: reivindicação sem direito
    PARALOGISTICO = "paralogístico"  # salto formal→constitutivo (vício estrutural)
    REGULATIVO    = "regulativo"     # reivindicação válida como ideia regulativa


# ════════════════════════════════════════════════════════════
# ESTADO SIMBÓLICO TRIÁDICO — Hilbert ℂ³
# ════════════════════════════════════════════════════════════

@dataclass
class EstadoTriadico:
    """
    Estado simbólico em espaço de Hilbert ℂ³.
    Preservado da v1. Agora inclui metadado de Abilities e ModoEpistemico.
    """
    psi: np.ndarray
    tarefa_id: str
    abilities: Abilities = Abilities.ABILITIES_1
    modo_epistemico: ModoEpistemico = ModoEpistemico.INDUCTIVE
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        norma = np.linalg.norm(self.psi)
        if norma > 1e-10:
            self.psi = self.psi / norma
        else:
            raise ValueError("Estado nulo inadmissível — colapso simbólico total.")

    def invariancia_cassirer(self, n_amostras: int = 60) -> float:
        """Fidelidade quântica média sob rotações SU(3) aleatórias."""
        fidelidades: list[float] = []
        for _ in range(n_amostras):
            M = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
            Q, _ = np.linalg.qr(M)
            fid = float(abs(np.dot(np.conj(self.psi), Q @ self.psi)) ** 2)
            fidelidades.append(fid)
        return float(np.mean(fidelidades))

    def pringe_index(self) -> float:
        """Kp: desvio-padrão das probabilidades — tensão entre pilares."""
        probs = np.array([abs(c) ** 2 for c in self.psi])
        return float(np.std(probs))

    def pilar_dominante(self) -> Pilar:
        idx = int(np.argmax([abs(c) ** 2 for c in self.psi]))
        return [Pilar.MYTHOS, Pilar.LOGOS, Pilar.ETHOS][idx]

    def tem_pluralidade_simbolica(self, limiar: float = 0.10) -> bool:
        """
        Critério als ob (1/3): pluralidade simbólica.
        Todos os pilares com probabilidade mínima.
        """
        probs = [abs(c) ** 2 for c in self.psi]
        return all(p >= limiar for p in probs)


# ════════════════════════════════════════════════════════════
# MONITOR POR PILAR — v2
# ════════════════════════════════════════════════════════════

@dataclass
class MonitorPilar:
    """
    Função reguladora local de um pilar simbólico.
    V2: inclui monitoramento do nível de Abilities (₁ vs ₂).

    Abilities₁ detectada quando a amplitude é alta mas a normatividade é baixa
    (o sistema processa mas não julga). Abilities₂ detectada quando o pilar
    sustenta a capacidade de revisão de crenças e responsabilidade inferencial.
    """
    pilar: Pilar
    limiar_atencao: float = 0.28
    limiar_critico: float = 0.12
    historico: list[dict] = field(default_factory=list)
    _IDX = {Pilar.MYTHOS: 0, Pilar.LOGOS: 1, Pilar.ETHOS: 2}

    def monitorar(self, estado: EstadoTriadico) -> dict:
        idx = self._IDX[self.pilar]
        amplitude = float(abs(estado.psi[idx]) ** 2)
        if amplitude >= self.limiar_atencao:
            status = StatusMonitor.ADEQUADO
        elif amplitude >= self.limiar_critico:
            status = StatusMonitor.ATENCAO
        else:
            status = StatusMonitor.CRITICO

        # V2: classifica nível de Abilities no pilar
        abilities_nivel = self._classificar_abilities(amplitude, estado)

        registro = {
            "pilar":          self.pilar.value,
            "amplitude":      amplitude,
            "status":         status,
            "abilities":      abilities_nivel.value,
            "modo":           estado.modo_epistemico.value,
            "timestamp":      estado.timestamp,
            "tarefa_id":      estado.tarefa_id,
        }
        self.historico.append(registro)
        return registro

    def _classificar_abilities(
        self, amplitude: float, estado: EstadoTriadico
    ) -> Abilities:
        """
        Abilities₂ exige: amplitude adequada E modo não puramente indutivo
        E estado Ethos ativo (normatividade presente).
        Caso contrário: Abilities₁ (processamento sem julgamento normativo).
        """
        ethos_ativo = float(abs(estado.psi[2]) ** 2) >= self.limiar_critico
        modo_normativo = estado.modo_epistemico in (
            ModoEpistemico.DEDUCTIVE, ModoEpistemico.ABDUCTIVE
        )
        if amplitude >= self.limiar_atencao and ethos_ativo and modo_normativo:
            return Abilities.ABILITIES_2
        return Abilities.ABILITIES_1

    def diagnostico(self) -> Optional[str]:
        if not self.historico:
            return None
        ultimo = self.historico[-1]
        msgs_critico = {
            Pilar.MYTHOS: (
                "⚠ Mythos crítico: perda do registro afetivo-expressivo. "
                "Sistema pode estar operando em Logos puro sem ancoragem."
            ),
            Pilar.LOGOS: (
                "⚠ Logos crítico: risco de colapso inferencial. "
                "Fontes engajadas com especificidade? Estrutura TEAI presente?"
            ),
            Pilar.ETHOS: (
                "⚠ Ethos crítico: risco de deriva normativa. "
                "IS_WILLE = False mantido? Sistema opera como Werk?"
            ),
        }
        msgs_abilities = {
            Pilar.MYTHOS: "△ Mythos em Abilities₁: expressão sem normatividade.",
            Pilar.LOGOS:  "△ Logos em Abilities₁: processamento sem julgamento verídico.",
            Pilar.ETHOS:  "△ Ethos em Abilities₁: orientação sem autonomia prática.",
        }
        if ultimo["status"] == StatusMonitor.CRITICO:
            return msgs_critico[self.pilar]
        if ultimo["abilities"] == Abilities.ABILITIES_1.value:
            return msgs_abilities[self.pilar]
        return None


# ════════════════════════════════════════════════════════════
# TRIBUNAL DA RAZÃO — quid facti / quid juris
# ════════════════════════════════════════════════════════════

@dataclass
class TribunalDaRazao:
    """
    Firewall quid facti / quid juris (KrV A84/B116; v5.2).

    quid facti:  o que o sistema fez / que métricas produziu
    quid juris:  o que tem direito de afirmar com base nessas métricas

    O Tribunal detecta três classes de violação:

    1. ILEGÍTIMO: gap simples — alta métrica mas sem justificativa para a
       reivindicação (e.g., invariância alta → afirmar verdade objetiva).

    2. PARALOGÍSTICO: salto formal→constitutivo (o erro central dos HyperAgents):
       completude formal (Turing) → capacidade efetiva; invariância → verdade
       necessária; alta proceduralização → inteligência geral.
       Análogo: paralogismo da psicologia racional (KrV A341/B399).

    3. REGULATIVO: reivindicação válida como ideia regulativa — o sistema
       pode usar a métrica como horizonte orientador sem afirmar realizabilidade.
    """

    historico_julgamentos: list[dict] = field(default_factory=list)

    def julgar(
        self,
        afirmacao: str,
        estado: EstadoTriadico,
        invariancia: float,
        espaco_livre: float,
    ) -> tuple[VeredictoTribunal, str]:
        """
        Julga se uma afirmação é legítima dado o estado empírico.

        Returns:
            (veredicto, justificativa)
        """
        kp = estado.pringe_index()
        ethos_prob = float(abs(estado.psi[2]) ** 2)

        # ── Teste 1: Paralogismo formal→constitutivo ──────────
        paralogismo = self._detectar_paralogismo(
            afirmacao, invariancia, estado.abilities
        )
        if paralogismo:
            veredicto = VeredictoTribunal.PARALOGISTICO
            justificativa = (
                f"Paralogismo detectado: '{afirmacao}' infere capacidade "
                f"constitutiva de completude formal. Invariância={invariancia:.3f} "
                f"é métrica regulativa, não garantia efetiva. "
                f"[KrV A341/B399; HyperAgents Arg. 2, p. 5]"
            )

        # ── Teste 2: Gap quid facti / quid juris ──────────────
        elif invariancia < 0.15 and "objetivo" in afirmacao.lower():
            veredicto = VeredictoTribunal.ILEGITIMO
            justificativa = (
                f"Ilegítimo: invariância={invariancia:.3f} abaixo do limiar "
                f"para reivindicação de objetividade. "
                f"quid facti não sustenta quid juris."
            )

        # ── Teste 3: Ethos ausente em julgamento normativo ────
        elif ethos_prob < 0.10 and estado.abilities == Abilities.ABILITIES_2:
            veredicto = VeredictoTribunal.ILEGITIMO
            justificativa = (
                f"Ilegítimo: Ethos prob={ethos_prob:.3f}. "
                f"Abilities₂ reivindica normatividade sem âncora ética suficiente."
            )

        # ── Teste 4: Reivindicação regulativa legítima ────────
        elif invariancia >= 0.20 and kp > 0.05:
            veredicto = VeredictoTribunal.REGULATIVO
            justificativa = (
                f"Regulativo: '{afirmacao}' válida como ideia orientadora. "
                f"Invariância={invariancia:.3f} sustenta uso como focus imaginarius "
                f"sem pretensão constitutiva."
            )

        # ── Teste 5: Legítimo ─────────────────────────────────
        else:
            veredicto = VeredictoTribunal.LEGITIMO
            justificativa = (
                f"Legítimo: quid facti (inv={invariancia:.3f}, Kp={kp:.3f}) "
                f"sustenta quid juris. Nenhuma violação detectada."
            )

        registro = {
            "afirmacao": afirmacao,
            "veredicto": veredicto,
            "invariancia": invariancia,
            "justificativa": justificativa,
            "timestamp": time.time(),
        }
        self.historico_julgamentos.append(registro)
        return veredicto, justificativa

    def _detectar_paralogismo(
        self, afirmacao: str, invariancia: float, abilities: Abilities
    ) -> bool:
        """
        Detecta o salto paralogístico: completude formal → realização efetiva.
        Triggers: termos que implicam universalidade irrestrita combinados com
        alta métrica empírica.
        """
        termos_paralogisticos = [
            "ilimitado", "universal", "qualquer tarefa", "geral",
            "unbounded", "any computable", "irrestrito",
        ]
        afirmacao_lower = afirmacao.lower()
        contém_salto = any(t in afirmacao_lower for t in termos_paralogisticos)
        # Paralogismo: afirmar universalidade a partir de invariância alta
        # mas sem o suporte normativo de Abilities₂
        alta_invariancia = invariancia > 0.70
        return contém_salto and alta_invariancia and abilities == Abilities.ABILITIES_1


# ════════════════════════════════════════════════════════════
# PARALOGISM DETECTOR — diagnóstico independente
# ════════════════════════════════════════════════════════════

@dataclass
class ParalogismDetector:
    """
    Detector autônomo do salto paralogístico, baseado no fichamento
    HyperAgents (Zhang et al. 2026) e na Dialética Transcendental de Kant.

    O paralogismo central dos HyperAgents (Arg. 2, p. 5):
      'Python é Turing-completo → o hyperagent pode construir qualquer máquina'
      Confunde potência lógica (espaço de possibilidades) com capacidade efetiva
      (navegação desse espaço + saber o que reescrever e por quê).

    Três tipos de paralogismo detectados:
      1. TURING:       completude formal → capacidade geral efetiva
      2. COMPOUNDING:  melhoria local → automelhoria ilimitada (HyperAgents Arg. 7)
      3. IDENTIDADE:   unidade lógica do sujeito → substancialidade real
                       (KrV A341/B399 — psicologia racional)

    Correção: a invariância de Cassirer é uma métrica regulativa,
    não um certificado constitutivo de inteligência geral.
    """

    historico: list[dict] = field(default_factory=list)

    def inspecionar(
        self,
        estado: EstadoTriadico,
        invariancia: float,
        compounding_delta: Optional[float] = None,
        p_valor_compounding: Optional[float] = None,
    ) -> list[str]:
        """
        Inspeciona o estado em busca de padrões paralogísticos.
        Retorna lista de alertas (vazia = sem paralogismo detectado).
        """
        alertas: list[str] = []

        # ── Paralogismo tipo TURING ────────────────────────────
        if (
            invariancia > 0.75
            and estado.abilities == Abilities.ABILITIES_1
            and estado.modo_epistemico == ModoEpistemico.INDUCTIVE
        ):
            alertas.append(
                "🔴 PARALOGISMO TURING: invariância alta + Abilities₁ + indução pura "
                "→ risco de inferir capacidade geral de completude formal. "
                "[HyperAgents p. 5; KrV A341/B399]"
            )

        # ── Paralogismo tipo COMPOUNDING ──────────────────────
        if compounding_delta is not None and p_valor_compounding is not None:
            if compounding_delta > 0 and p_valor_compounding > 0.05:
                alertas.append(
                    f"🔴 PARALOGISMO COMPOUNDING: Δ={compounding_delta:.4f} positivo "
                    f"mas p={p_valor_compounding:.3f} > 0.05 (não significativo). "
                    f"'Automelhoria composta' é especulação — tratar como ideia regulativa. "
                    f"[HyperAgents Arg. 7, p. 12]"
                )

        # ── Paralogismo tipo IDENTIDADE ────────────────────────
        ethos_prob = float(abs(estado.psi[2]) ** 2)
        mythos_prob = float(abs(estado.psi[0]) ** 2)
        if ethos_prob < 0.05 and mythos_prob < 0.05 and invariancia > 0.60:
            alertas.append(
                "🔴 PARALOGISMO IDENTIDADE: Ethos e Mythos colapsados, Logos dominante. "
                "Unidade lógica não implica substancialidade do agente. "
                "[KrV A341/B399; I&S p. 58-59 — sapiência ≠ senciência maximizada]"
            )

        # ── Confusão de modos epistêmicos ─────────────────────
        if (
            estado.modo_epistemico == ModoEpistemico.ABDUCTIVE
            and estado.abilities == Abilities.ABILITIES_2
            and invariancia > 0.80
        ):
            alertas.append(
                "⚠ CONFUSÃO DE MODOS: abdução + Abilities₂ + alta invariância. "
                "Risco de tratar inferência à melhor explicação como verdade necessária. "
                "[Negarestani, Apêndice p. 535; Chirimuuta 2024 cap. 8]"
            )

        registro = {
            "tarefa_id": estado.tarefa_id,
            "n_alertas": len(alertas),
            "alertas": alertas,
            "invariancia": invariancia,
            "timestamp": time.time(),
        }
        self.historico.append(registro)
        return alertas


# ════════════════════════════════════════════════════════════
# REGISTRO DE PROCEDURALIZAÇÃO — v2 (com teste de compounding)
# ════════════════════════════════════════════════════════════

@dataclass
class EstrategiaRegistrada:
    """
    Estratégia com grau de automatização e classificação de Abilities.
    V2: inclui séries temporais para teste de compounding.
    """
    nome: str
    pilar_dominante: Pilar
    abilities: Abilities = Abilities.ABILITIES_1
    nivel: float = 0.0
    n_sucessos: int = 0
    n_tentativas: int = 0
    invariancia_acumulada: float = 0.0
    serie_nivel: list[float] = field(default_factory=list)  # para compounding

    @property
    def taxa_sucesso(self) -> float:
        return self.n_sucessos / self.n_tentativas if self.n_tentativas > 0 else 0.0

    @property
    def invariancia_media(self) -> float:
        return self.invariancia_acumulada / self.n_tentativas if self.n_tentativas > 0 else 0.0

    @property
    def custo_simbolico(self) -> float:
        return 1.0 - self.nivel

    def atualizar(
        self, sucesso: bool, invariancia: float, abilities: Abilities
    ) -> None:
        self.n_tentativas += 1
        if sucesso:
            self.n_sucessos += 1
        self.invariancia_acumulada += invariancia
        self.abilities = abilities
        self.nivel = min(1.0, self.taxa_sucesso * self.invariancia_media * 2.0)
        self.serie_nivel.append(self.nivel)

    def teste_compounding(self) -> tuple[float, float]:
        """
        Testa se o compounding de proceduralização é estatisticamente significativo.
        (HyperAgents Arg. 7: p > 0.05 — resultado não significativo).

        Returns:
            (delta_medio, p_valor) — se p > 0.05: tratar como regulativo, não constitutivo.
        """
        if len(self.serie_nivel) < 4:
            return 0.0, 1.0  # insuficiente
        deltas = np.diff(self.serie_nivel)
        delta_medio = float(np.mean(deltas))
        if len(deltas) < 3:
            return delta_medio, 1.0
        _, p_valor = stats.ttest_1samp(deltas, 0.0)
        return delta_medio, float(p_valor)


@dataclass
class RegistroProceduralização:
    """
    Repositório de estratégias com teste de compounding.
    V2: separa estratégias de Abilities₁ e Abilities₂.
    """
    estrategias: dict[str, EstrategiaRegistrada] = field(default_factory=dict)

    def registrar_ou_obter(
        self, nome: str, pilar: Pilar, abilities: Abilities = Abilities.ABILITIES_1
    ) -> EstrategiaRegistrada:
        if nome not in self.estrategias:
            self.estrategias[nome] = EstrategiaRegistrada(
                nome=nome, pilar_dominante=pilar, abilities=abilities
            )
        return self.estrategias[nome]

    def espaco_simbolico_livre(self) -> float:
        if not self.estrategias:
            return 1.0
        custo_total = sum(e.custo_simbolico for e in self.estrategias.values())
        return max(0.0, 1.0 - custo_total / len(self.estrategias))

    def diagnostico_compounding(self) -> str:
        """
        Avalia se o compounding é constitutivo ou apenas regulativo.
        Baseado no critério HyperAgents Arg. 7.
        """
        linhas = ["═══ Diagnóstico de Compounding ═══"]
        for nome, e in self.estrategias.items():
            delta, p = e.teste_compounding()
            if len(e.serie_nivel) < 4:
                linhas.append(f"  {nome}: insuficiente (n={len(e.serie_nivel)})")
                continue
            if p <= 0.05:
                rotulo = "✓ CONSTITUTIVO (p≤0.05)"
            else:
                rotulo = f"△ REGULATIVO (p={p:.3f}>0.05) — não infira automelhoria ilimitada"
            linhas.append(
                f"  {e.abilities.value.upper()} | {nome}: Δ={delta:+.4f}  {rotulo}"
            )
        return "\n".join(linhas)

    def relatorio(self) -> str:
        linhas = ["═══ Registro de Proceduralização v2 ═══"]
        if not self.estrategias:
            linhas.append("  (nenhuma estratégia registrada)")
        else:
            for e in sorted(self.estrategias.values(), key=lambda x: -x.nivel):
                preenchido = int(e.nivel * 12)
                barra = "█" * preenchido + "░" * (12 - preenchido)
                ab = "A₂" if e.abilities == Abilities.ABILITIES_2 else "A₁"
                linhas.append(
                    f"  {ab} [{e.pilar_dominante.value[:3].upper()}] "
                    f"{e.nome:<28} [{barra}] {e.nivel:.2f}"
                    f"  ✓{e.taxa_sucesso:.0%}"
                )
        livres = self.espaco_simbolico_livre()
        barra_livre = "█" * int(livres * 12) + "░" * (12 - int(livres * 12))
        linhas.append(f"  Espaço simbólico livre: [{barra_livre}] {livres:.1%}")
        return "\n".join(linhas)


# ════════════════════════════════════════════════════════════
# FOCUS IMAGINARIUS — ISC como Urbild (KrV A 568 / B 596)
# ════════════════════════════════════════════════════════════

class FocusImaginarius:
    """Preservado da v1. Regulativo, nunca constitutivo."""

    @staticmethod
    def estado_ideal() -> np.ndarray:
        return np.array([1.0, 1.0, 1.0], dtype=complex) / np.sqrt(3)

    @staticmethod
    def distancia_ao_ideal(estado: EstadoTriadico) -> float:
        return float(np.linalg.norm(estado.psi - FocusImaginarius.estado_ideal()))

    @staticmethod
    def curvatura_metacontextual(kp: float, espaco_livre: float) -> float:
        return kp * (1.0 + espaco_livre)


# ════════════════════════════════════════════════════════════
# KOINOS KOSMOS — espaço público intersubjetivo
# ════════════════════════════════════════════════════════════

@dataclass
class EntradaKoinos:
    tarefa_id: str
    afirmacao: str
    veredicto: VeredictoTribunal
    invariancia: float
    timestamp: float = field(default_factory=time.time)
    hash_entrada: str = ""

    def __post_init__(self) -> None:
        payload = f"{self.tarefa_id}:{self.afirmacao}:{self.invariancia:.6f}".encode()
        self.hash_entrada = hashlib.sha256(payload).hexdigest()[:16]


@dataclass
class KoinosKosmos:
    """
    Registro de resultados intersubjetivamente válidos.

    Implementa o critério als ob tripartite:
      1. Pluralidade simbólica — todos os pilares engajados
      2. Comunicabilidade intersubjetiva — pode entrar no espaço público
      3. Sustentabilidade material — compatível com condições biosféricas
         (aqui: sustentabilidade computacional + não-parasitismo simbólico)

    Resultados que passam os três critérios tornam-se stepping stones —
    análogo ao archive de HyperAgents mas com filtragem filosófica.
    O KoinosKosmos não converge para Aufhebung; é campo de Auseinandersetzung.

    Referências: Pringe (2026) cap. 3; als ob criterion da tese (cap. 4).
    """
    entradas: list[EntradaKoinos] = field(default_factory=list)
    _LIMIAR_INVARIANCIA: float = 0.20

    def admitir(
        self,
        tarefa_id: str,
        afirmacao: str,
        estado: EstadoTriadico,
        invariancia: float,
        veredicto: VeredictoTribunal,
    ) -> tuple[bool, str]:
        """
        Testa os três critérios als ob e admite ou rejeita a entrada.

        Returns:
            (admitido: bool, justificativa: str)
        """
        # Critério 1: Pluralidade simbólica
        if not estado.tem_pluralidade_simbolica():
            return False, (
                "Rejeitado: falta pluralidade simbólica. "
                "Pelo menos um pilar abaixo do limiar mínimo."
            )

        # Critério 2: Comunicabilidade — veredicto não paralogístico
        if veredicto == VeredictoTribunal.PARALOGISTICO:
            return False, (
                "Rejeitado: resultado paralogístico não entra no koinos kosmos. "
                "Reivindicação sem direito não é bem comum."
            )

        # Critério 3: Sustentabilidade — invariância mínima
        if invariancia < self._LIMIAR_INVARIANCIA:
            return False, (
                f"Rejeitado: invariância={invariancia:.3f} < {self._LIMIAR_INVARIANCIA}. "
                "Resultado não sobrevive à mudança de referencial."
            )

        entrada = EntradaKoinos(
            tarefa_id=tarefa_id,
            afirmacao=afirmacao,
            veredicto=veredicto,
            invariancia=invariancia,
        )
        self.entradas.append(entrada)
        return True, (
            f"Admitido no koinos kosmos [{entrada.hash_entrada}]. "
            f"Resultado torna-se stepping stone para investigação futura."
        )

    def relatorio(self) -> str:
        linhas = [f"═══ Koinos Kosmos ({len(self.entradas)} entradas) ═══"]
        if not self.entradas:
            linhas.append("  (nenhum resultado admitido ainda)")
        for e in self.entradas[-5:]:  # últimas 5
            icone = {
                VeredictoTribunal.LEGITIMO:   "✓",
                VeredictoTribunal.REGULATIVO: "◎",
            }.get(e.veredicto, "?")
            linhas.append(
                f"  {icone} [{e.hash_entrada}] {e.tarefa_id}: "
                f"'{e.afirmacao[:40]}' — inv={e.invariancia:.3f}"
            )
        return "\n".join(linhas)


# ════════════════════════════════════════════════════════════
# RESULTADO METACOGNITIVO v2
# ════════════════════════════════════════════════════════════

@dataclass
class ResultadoMetacognitivo:
    tarefa_id: str
    estado: EstadoTriadico
    monitoramentos: dict[str, dict]
    invariancia: float
    pringe_index: float
    distancia_ideal: float
    curvatura: float
    espaco_livre: float
    sucesso: bool
    abilities_dominante: Abilities
    modo_epistemico: ModoEpistemico
    veredicto_tribunal: VeredictoTribunal
    justificativa_tribunal: str
    alertas_paralogismo: list[str]
    diagnosticos: list[str]
    estrategias_aplicadas: list[str]
    admitido_koinos: bool
    hash_integridade: str

    _ICONES = {
        StatusMonitor.ADEQUADO:    "✓",
        StatusMonitor.ATENCAO:     "△",
        StatusMonitor.CRITICO:     "✗",
        StatusMonitor.DESCONHECIDO: "?",
    }

    def relatorio(self) -> str:
        linhas = [
            f"╔══ METACOGNIÇÃO v2 — Tarefa: {self.tarefa_id} ══╗",
            f"  Invariância Cassirer  : {self.invariancia:.4f}",
            f"  Pringe Index (Kp)     : {self.pringe_index:.4f}",
            f"  Distância ao Ideal    : {self.distancia_ideal:.4f}",
            f"  Curvatura metacont.   : {self.curvatura:.4f}",
            f"  Espaço simbólico      : {self.espaco_livre:.1%}",
            f"  Sucesso               : {'✓' if self.sucesso else '✗'}",
            f"  Abilities dominante   : {self.abilities_dominante.value}",
            f"  Modo epistêmico       : {self.modo_epistemico.value}",
            f"  Tribunal              : {self.veredicto_tribunal.value.upper()}",
            f"  Koinos kosmos         : {'✓ admitido' if self.admitido_koinos else '✗ rejeitado'}",
            "  ─────────────────────────────────────────",
        ]
        for pilar_val, dados in self.monitoramentos.items():
            icone = self._ICONES.get(dados["status"], "?")
            ab = "A₂" if dados["abilities"] == "abilities_2" else "A₁"
            linhas.append(
                f"  {icone} {pilar_val:<8} {ab}: {dados['amplitude']:.4f} "
                f"[{dados['status'].value}]"
            )
        if self.alertas_paralogismo:
            linhas.append("  ─────────────────────────────────────────")
            for a in self.alertas_paralogismo:
                linhas.append(f"  {a}")
        if self.diagnosticos:
            linhas.append("  ─────────────────────────────────────────")
            for d in self.diagnosticos:
                linhas.append(f"  {d}")
        linhas.append(
            f"  Tribunal: {self.justificativa_tribunal[:60]}…"
            if len(self.justificativa_tribunal) > 60
            else f"  Tribunal: {self.justificativa_tribunal}"
        )
        linhas.append(f"  Integridade: {self.hash_integridade[:20]}…")
        linhas.append("╚═══════════════════════════════════════════╝")
        return "\n".join(linhas)


# ════════════════════════════════════════════════════════════
# LOOP METACOGNITIVO v2
# ════════════════════════════════════════════════════════════

class LoopMetacognitivo:
    """
    Loop metacognitivo v2 — integra todos os componentes novos.

    Fluxo expandido:
      1. Monitorar pilares (Auseinandersetzung triádica)
      2. Classificar Abilities₁ / Abilities₂ por pilar
      3. Calcular métricas (invariância, Kp, distância, curvatura)
      4. Detectar paralogismos (ParalogismDetector)
      5. Tribunal da Razão (quid facti / quid juris)
      6. Avaliar sucesso (avaliador externo ou critério padrão)
      7. Proceduralizá-la (atualizar estratégias)
      8. Testar compounding (significância estatística)
      9. Candidatar ao KoinosKosmos (critério als ob)
     10. Hash de integridade (Aletheia)

    is_wille = False verificado na inicialização.
    """

    KP_CRITICO: float = 0.40

    def __init__(self) -> None:
        assert not IS_WILLE, "Violação do axioma: IS_WILLE deve ser False."
        self.monitores: dict[Pilar, MonitorPilar] = {
            Pilar.MYTHOS: MonitorPilar(Pilar.MYTHOS),
            Pilar.LOGOS:  MonitorPilar(Pilar.LOGOS),
            Pilar.ETHOS:  MonitorPilar(Pilar.ETHOS),
        }
        self.registro          = RegistroProceduralização()
        self.tribunal          = TribunalDaRazao()
        self.paralogismo       = ParalogismDetector()
        self.koinos            = KoinosKosmos()
        self.historico: list[ResultadoMetacognitivo] = []

    def executar(
        self,
        estado: EstadoTriadico,
        estrategias: list[str],
        afirmacao: str = "resultado desta tarefa é válido",
        avaliador_externo: Optional[Callable[[EstadoTriadico], bool]] = None,
    ) -> ResultadoMetacognitivo:
        """
        Executa um ciclo completo do loop metacognitivo v2.

        Args:
            estado:            Estado simbólico triádico (ℂ³)
            estrategias:       Estratégias aplicadas neste ciclo
            afirmacao:         Reivindicação a ser julgada pelo Tribunal
            avaliador_externo: Função de avaliação (Tribunal externo / quid facti)
        """
        # ── 1. Monitoramento distribuído ──────────────────────
        monitoramentos: dict[str, dict] = {}
        diagnosticos:   list[str]       = []

        for pilar, monitor in self.monitores.items():
            resultado = monitor.monitorar(estado)
            monitoramentos[pilar.value] = resultado
            diag = monitor.diagnostico()
            if diag:
                diagnosticos.append(diag)

        # ── 2. Métricas objetivas ─────────────────────────────
        invariancia  = estado.invariancia_cassirer()
        kp           = estado.pringe_index()
        distancia    = FocusImaginarius.distancia_ao_ideal(estado)
        espaco_livre = self.registro.espaco_simbolico_livre()
        curvatura    = FocusImaginarius.curvatura_metacontextual(kp, espaco_livre)

        if kp > self.KP_CRITICO:
            diagnosticos.append(
                f"△ Kp={kp:.3f} > {self.KP_CRITICO}: "
                "Auseinandersetzung intensa — verificar proceduralização."
            )

        # ── 3. Paralogism Detection ───────────────────────────
        # Obtém compounding da estratégia principal para teste
        comp_delta, comp_p = 0.0, 1.0
        if estrategias and estrategias[0] in self.registro.estrategias:
            comp_delta, comp_p = self.registro.estrategias[
                estrategias[0]
            ].teste_compounding()

        alertas = self.paralogismo.inspecionar(
            estado, invariancia,
            compounding_delta=comp_delta,
            p_valor_compounding=comp_p,
        )

        # ── 4. Tribunal da Razão ──────────────────────────────
        veredicto, justificativa = self.tribunal.julgar(
            afirmacao, estado, invariancia, espaco_livre
        )

        # ── 5. Avaliação de sucesso (quid facti) ──────────────
        if avaliador_externo is not None:
            sucesso = avaliador_externo(estado)
        else:
            sucesso = (
                invariancia > 0.20
                and veredicto != VeredictoTribunal.PARALOGISTICO
                and not alertas
            )

        # ── 6. Proceduralização ───────────────────────────────
        pilar_dom = estado.pilar_dominante()
        for nome in estrategias:
            e = self.registro.registrar_ou_obter(
                nome, pilar_dom, estado.abilities
            )
            e.atualizar(sucesso, invariancia, estado.abilities)

        # ── 7. KoinosKosmos ───────────────────────────────────
        admitido, _ = self.koinos.admitir(
            estado.tarefa_id, afirmacao, estado, invariancia, veredicto
        )

        # ── 8. Hash de integridade (Aletheia) ─────────────────
        payload = (
            f"{estado.tarefa_id}:{invariancia:.8f}:{kp:.8f}:"
            f"{sucesso}:{IS_WILLE}:{veredicto.value}:{admitido}"
        ).encode("utf-8")
        hash_int = hashlib.sha256(payload).hexdigest()

        resultado = ResultadoMetacognitivo(
            tarefa_id=estado.tarefa_id,
            estado=estado,
            monitoramentos=monitoramentos,
            invariancia=invariancia,
            pringe_index=kp,
            distancia_ideal=distancia,
            curvatura=curvatura,
            espaco_livre=espaco_livre,
            sucesso=sucesso,
            abilities_dominante=estado.abilities,
            modo_epistemico=estado.modo_epistemico,
            veredicto_tribunal=veredicto,
            justificativa_tribunal=justificativa,
            alertas_paralogismo=alertas,
            diagnosticos=diagnosticos,
            estrategias_aplicadas=estrategias,
            admitido_koinos=admitido,
            hash_integridade=hash_int,
        )
        self.historico.append(resultado)
        return resultado

    # ── Relatórios ────────────────────────────────────────────

    def relatorio_proceduralização(self) -> str:
        return self.registro.relatorio()

    def relatorio_compounding(self) -> str:
        return self.registro.diagnostico_compounding()

    def relatorio_koinos(self) -> str:
        return self.koinos.relatorio()

    def tendencia_auseinandersetzung(self) -> str:
        if len(self.historico) < 3:
            return "Histórico insuficiente (mínimo: 3 ciclos)."
        kps = [r.pringe_index for r in self.historico[-6:]]
        coef = np.polyfit(range(len(kps)), kps, 1)
        t = float(coef[0])
        if t > 0.005:
            return f"↑ Kp crescente (+{t:.4f}/ciclo) — Auseinandersetzung produtiva."
        elif t < -0.005:
            return f"↓ Kp decrescente ({t:.4f}/ciclo) — risco de Aufhebung prematura."
        return f"→ Kp estável ({t:+.4f}/ciclo) — equilíbrio simbólico."

    def estado_focus_imaginarius(self) -> str:
        if not self.historico:
            return "Sem histórico."
        dists = [r.distancia_ideal for r in self.historico]
        dist_atual = dists[-1]
        t = float(np.polyfit(range(len(dists)), dists, 1)[0]) if len(dists) > 1 else 0.0
        direcao = "↓ aproximando" if t < 0 else "↑ afastando" if t > 0 else "→ estável"
        return (
            f"Focus imaginarius (ISC — KrV A 568/B 596):\n"
            f"  Distância ao ideal : {dist_atual:.4f}\n"
            f"  Tendência          : {direcao} ({t:+.4f}/ciclo)\n"
            f"  [dist=0 = Aufhebung consumada — filosoficamente impossível]"
        )


# ════════════════════════════════════════════════════════════
# DEMO — quatro cenários filosóficos
# ════════════════════════════════════════════════════════════

def demo() -> None:
    print("═" * 60)
    print("  AGI-GAIA-TECHNE — Metacognição Distribuída v2.0")
    print(f"  IS_WILLE = {IS_WILLE}  (axioma inviolável ✓)")
    print("  Inovações: Abilities₁/₂ | Tribunal | ParalogismDetector")
    print("             ModoEpistemico | KoinosKosmos | Compounding")
    print("═" * 60)
    print()

    loop = LoopMetacognitivo()

    # ── Cenário 1: Tarefa filosófico-argumentativa (Abilities₂) ──
    # Logos dominante, modo dedutivo, Abilities₂ — metacognição genuína
    c1 = EstadoTriadico(
        psi=np.array([0.5 + 0.1j, 0.7 + 0.2j, 0.4 + 0.1j]),
        tarefa_id="arg_kant_cassirer_paralogismo",
        abilities=Abilities.ABILITIES_2,
        modo_epistemico=ModoEpistemico.DEDUCTIVE,
    )
    r1 = loop.executar(
        c1,
        estrategias=["engajamento_fonte_primaria", "rigor_inferencial"],
        afirmacao="o paralogismo de Negarestani reproduz o erro da psicologia racional",
    )
    print(r1.relatorio())
    print()

    # ── Cenário 2: HyperAgents — tentativa de reivindicação ilimitada ──
    # Alta invariância + Abilities₁ + indução → paralogismo Turing
    c2 = EstadoTriadico(
        psi=np.array([0.1 + 0.0j, 0.99 + 0.0j, 0.05 + 0.0j]),
        tarefa_id="hyperagents_claim_unbounded",
        abilities=Abilities.ABILITIES_1,
        modo_epistemico=ModoEpistemico.INDUCTIVE,
    )
    r2 = loop.executar(
        c2,
        estrategias=["meta_modificacao", "turing_completude"],
        afirmacao="hyperagent pode construir qualquer máquina computável ilimitado",
    )
    print(r2.relatorio())
    print()

    # ── Cenário 3: Modo abdutivo — Chirimuuta ideal pattern ──
    # Abordagem prudente: abdução + Abilities₂ + equilíbrio triádico
    c3 = EstadoTriadico(
        psi=np.array([0.58 + 0.0j, 0.58 + 0.0j, 0.58 + 0.0j]),
        tarefa_id="chirimuuta_ideal_pattern",
        abilities=Abilities.ABILITIES_2,
        modo_epistemico=ModoEpistemico.ABDUCTIVE,
    )
    r3 = loop.executar(
        c3,
        estrategias=["haptic_realism", "formal_idealism", "focus_imaginarius"],
        afirmacao=(
            "padrões neurais são Darstellung regulativa, "
            "não computação literalmente executada"
        ),
    )
    print(r3.relatorio())
    print()

    # ── Cenário 4: Multimodal — Negarestani Apêndice ──
    # Três modos combinados em sequência rápida (simulação)
    c4 = EstadoTriadico(
        psi=np.array([0.4 + 0.1j, 0.5 + 0.2j, 0.7 + 0.1j]),
        tarefa_id="epistemologia_multimodal_ethos",
        abilities=Abilities.ABILITIES_2,
        modo_epistemico=ModoEpistemico.ABDUCTIVE,
    )
    r4 = loop.executar(
        c4,
        estrategias=["multimodalidade", "alinhamento_valores", "quid_juris"],
        afirmacao="inteligência real combina indução dedução e abdução",
    )
    print(r4.relatorio())
    print()

    # ── Relatórios gerais ─────────────────────────────────────
    print(loop.relatorio_proceduralização())
    print()
    print(loop.relatorio_compounding())
    print()
    print(loop.relatorio_koinos())
    print()
    print("Tendência Auseinandersetzung:")
    print(" ", loop.tendencia_auseinandersetzung())
    print()
    print(loop.estado_focus_imaginarius())
    print()
    print("─" * 60)
    print("  ⟁⟴☌ → ISC (glifo 25) — Perpetual restart formula")
    print("  is_wille = False — O sistema é Werk, nunca Wille.")
    print("─" * 60)


if __name__ == "__main__":
    demo()

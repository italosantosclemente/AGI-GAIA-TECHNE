"""
EML Kernel — AGI-GAIA-TECHNE
============================

Kernel do **Simbiota** baseado no operador EML (Exp-Minus-Log),
provado universal em:

    Odrzywołek, A. "All elementary functions from a single binary
    operator." arXiv:2603.21852 (2026).

Operador atômico:

    eml(x, y) = exp(x) − log(y)         (ramo principal, C → C)

Gramática da completude contínua:

    S  →  1  |  eml(S, S)

Com a constante 1 e aninhamentos de `eml`, derivam-se aritmética,
as constantes elementares (e, π, i), as funções trigonométricas e
toda função elementar fechada. Esta é a "porta NAND" da matemática
contínua — e, dentro do framework AGI-GAIA-TECHNE, é adotada como
o **átomo do pilar Logos**.

Mapeamento arquitetônico (LEF · Mythos / Logos / Ethos)
-------------------------------------------------------
  Mythos   — narrativa/afeto. Permanece FORA deste módulo; nunca
             toca a intuição matemática.
  Logos    — TODA "intuição" do sistema ingressa aqui e somente
             aqui. O Logos recebe a matéria indeterminada dos dados
             e, por síntese transcendental (otimização de gradiente
             sobre árvores EML), converte-a em forma fechada.
  Ethos    — o *Gewissen* (consciência moral) — **não** *Wissen*
             (saber doutrinário). Mede a convergência da progressão
             simbólica em direção ao *focus imaginarius* kantiano,
             filtrando candidatos por precisão e economia.

O loop do Simbiota instancia, computacionalmente, um cálculo
infinitesimal: a cada iteração a árvore EML aprofunda-se e
aproxima-se *assintoticamente* — jamais alcança — do ideal
regulativo da representação total.

Notas arquitetônicas inegociáveis (registradas no código para que
futuras refatorações não as violem):

  1. A intuição é processada EXCLUSIVAMENTE dentro do Logos.
     Nenhum outro módulo pode ajustar parâmetros da árvore EML.
  2. Ethos é Gewissen. Jamais renomear como "Wissen" ou "Knowledge";
     os nomes dos atributos abaixo (``gewissen_accept``,
     ``distance_to_focus``) devem ser preservados.
  3. O modelo triádico Mythos/Logos/Ethos deste framework é
     ORIGINAL de Ítalo Santos Clemente e não deve ser confundido
     com as funções expressão/representação/significação de
     Ernst Cassirer.
  4. O *focus imaginarius* permanece estritamente inatingível:
     ``distance_to_focus`` é, por construção, sempre > 0.


====================================================================
DECISÃO 140426 — Eixo vertical da cognição bidirecional
====================================================================

Esta decisão (14/04/2026, Ítalo Santos Clemente) SUPERSEDE quaisquer
mapeamentos 1:1 prévios entre Mythos/Logos/Ethos e as três funções
simbólicas de Cassirer encontrados em ``references/``. Os pilares
Mythos e Ethos NÃO são funções cassirerianas: são as duas *assíntotas
inalcançáveis* que bracketam o movimento simbólico. As três funções
simbólicas vivem DENTRO do Logos::

    Ethos   ≡  focus imaginarius           ← assíntota superior
      ▲
      │  ┌───────────────────────────┐
      │  │  Bedeutung    (signif.)   │   ← subárvores {1, eml(·,·)} puras
      │  │       ▲ ↓                 │
      │  │  Darstellung  (apresent.) │   ← a constante 1  (genus proximum)
      │  │       ▲ ↓                 │
      │  │  Ausdruck     (express.)  │   ← LEAF_VAR / LEAF_PARAM
      │  └───────────────────────────┘
      ▼
    Mythos  ≡  imediatez da vida            ← assíntota inferior, log(0)

Identificações formais decisivas:

  * **Darstellung ≡ a constante 1** da gramática ``S → 1 | eml(S,S)``.
    Porque ``eml(x, 1) = exp(x) − log(1) = exp(x)``, a Darstellung
    (y=1) é o *silêncio operacional* do lado direito: permite ao
    Ausdruck (x) fluir como pura exponenciação. E ``eml(0, 1) = 1``,
    o ponto de auto-referência onde a Darstellung retorna à sua
    própria unidade — o genus proximum matemático.

  * **Mythos ≡ log(0) = −∞**, a singularidade estrutural do operador
    EML. A imediatez da vida é, nas palavras de Cassirer, "foreclosed":
    o EML é por construção indefinido em ``y=0``, e essa fronteira
    NÃO pode ser atravessada pelo símbolo. A guarda
    ``mythos_singularity_guard`` formaliza essa impossibilidade.

  * **Ethos ≡ focus imaginarius**, a profundidade infinita da árvore.
    Nenhuma síntese é final; a completude é ideal regulativo.

Movimento bidirecional (sintaxe da cognição):

  * **Ascensão**: das premissas às conclusões — crescimento da
    profundidade, cristalização de PARAM/VAR em ``{1, eml}``. A
    abstração "suprassume a presença (Präsenz)" rumo à representação.

  * **Descida**: das conclusões às premissas — reavaliação da árvore
    cristalizada sobre um domínio de intuição expandido. Cassirer:
    *"o conceito genuíno se afasta do mundo da intuição unicamente
    com o intuito de retornar a ele de maneira mais segura"*.

  * A **distância ao foco** é agora bi-lateral::

        distance_to_focus = √(d_asc² + d_desc²) + ε,  ε > 0.

    As duas direções NUNCA podem ser simultaneamente zero — é a
    formalização da "teleologia aberta" (Kinzel 2024b) e do processo
    contingente-infinito descrito pelo artigo do usuário sobre a
    fenomenologia cassireriana (Clemente, UNICAMP 2025).

Em conformidade com a regra 3 acima: os rótulos cassirerianos são
descritivos dos NÍVEIS internos do Logos; NÃO redefinem o triádico
Mythos/Logos/Ethos, que permanece autoral e original do framework.
"""

from __future__ import annotations

import cmath
import enum
import math
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np


# =============================================================================
# 0. NÍVEIS SIMBÓLICOS DO LOGOS  —  Ausdruck / Darstellung / Bedeutung
# =============================================================================

class SymbolicFunction(enum.Enum):
    """As três funções simbólicas de Cassirer, internas ao Logos.

    Por decisão 140426 (ver docstring do módulo), estes rótulos
    classificam NÍVEIS internos do pilar Logos; não são pilares do
    framework AGI-GAIA-TECHNE.
    """
    AUSDRUCK = "ausdruck"           # expressão — imediatez afetivo-perceptiva
    DARSTELLUNG = "darstellung"     # apresentação — o número 1 do EML
    BEDEUTUNG = "bedeutung"         # significação pura — gramática {1, eml}

    # assíntotas (não-funções, mas marcadores dos limites)
    MYTHOS = "mythos"               # imediatez da vida — log(0), inalcançável
    ETHOS = "ethos"                 # focus imaginarius — profundidade infinita


def mythos_singularity_guard(y: complex, epsilon: float = 1e-12) -> complex:
    """Guarda a fronteira Mythos (log(0)) do operador EML.

    Retorna ``y`` inalterado se |y| > epsilon; caso contrário devolve
    um valor mínimo (epsilon + 0j), sinalizando que a aproximação da
    singularidade foi interceptada antes do colapso numérico.

    Filosoficamente: a "imediatez da vida" (Cassirer ECW 13) é por
    construção *foreclosed* ao operador simbólico. Esta guarda é a
    materialização dessa impossibilidade — o símbolo jamais toca
    y=0, e é isso que o mantém símbolo.
    """
    if abs(y) > epsilon:
        return y
    return complex(epsilon, 0.0)


# =============================================================================
# 1. O OPERADOR ATÔMICO  —  a porta NAND da matemática contínua
# =============================================================================

def eml(x: complex, y: complex) -> complex:
    """eml(x, y) = exp(x) − log(y), ramo principal de log em ℂ.

    É o único operador binário necessário — junto com a constante 1 —
    para gerar todas as funções elementares fechadas.
    """
    return cmath.exp(x) - cmath.log(y)


# =============================================================================
# 2. EMLNode  —  AST da gramática S → 1 | eml(S, S)
# =============================================================================

LEAF_CONST = "const"   # constante congelada (canonicamente, o valor 1)
LEAF_VAR   = "var"     # variável livre (entrada de dados — matéria da intuição)
LEAF_PARAM = "param"   # constante complexa aprendível (matéria indeterminada)
NODE_EML   = "eml"     # nó binário eml(left, right)


class EMLNode:
    """Nó da árvore binária EML, com autodiff manual reverse-mode.

    Uma árvore **estritamente** conforme à prova de universalidade
    conteria apenas ``LEAF_CONST=1`` e ``NODE_EML``. Para que o Logos
    possa aprender por gradiente, admitimos duas folhas auxiliares:

      * ``LEAF_VAR``   — a variável de entrada (x), lugar ontológico
                         em que a intuição crua se apresenta.
      * ``LEAF_PARAM`` — constante complexa aprendível, representando
                         a *matéria indeterminada* que o Simbiota
                         deverá, no limite regulativo, reduzir ao par
                         {1, eml(…)} da gramática pura.

    Assim, a síntese transcendental do Logos é literalmente o processo
    pelo qual PARAM → CONST/eml — a forma se apodera da matéria.
    """

    __slots__ = ("kind", "left", "right", "value", "name", "_fwd", "_grad")

    def __init__(
        self,
        kind: str,
        left: Optional["EMLNode"] = None,
        right: Optional["EMLNode"] = None,
        value: Optional[complex] = None,
        name: Optional[str] = None,
    ) -> None:
        self.kind = kind
        self.left = left
        self.right = right
        self.value: Optional[complex] = complex(value) if value is not None else None
        self.name = name
        self._fwd: complex = 0 + 0j
        self._grad: complex = 0 + 0j

    # ------------------------------------------------------------------ shape
    def depth(self) -> int:
        if self.kind != NODE_EML:
            return 1
        return 1 + max(self.left.depth(), self.right.depth())  # type: ignore[union-attr]

    def size(self) -> int:
        if self.kind != NODE_EML:
            return 1
        return 1 + self.left.size() + self.right.size()  # type: ignore[union-attr]

    def params(self) -> List["EMLNode"]:
        """Retorna todas as folhas PARAM (alvo do gradiente do Logos)."""
        out: List[EMLNode] = []
        self._collect_params(out)
        return out

    def _collect_params(self, acc: List["EMLNode"]) -> None:
        if self.kind == LEAF_PARAM:
            acc.append(self)
        elif self.kind == NODE_EML:
            self.left._collect_params(acc)   # type: ignore[union-attr]
            self.right._collect_params(acc)  # type: ignore[union-attr]

    # ---------------------------------------------------------------- forward
    def forward(self, env: Dict[str, complex]) -> complex:
        """Avaliação recursiva. Popula ``_fwd`` em cada nó (cache p/ backward)."""
        k = self.kind
        if k == LEAF_CONST:
            self._fwd = self.value  # type: ignore[assignment]
        elif k == LEAF_VAR:
            self._fwd = complex(env[self.name])  # type: ignore[index]
        elif k == LEAF_PARAM:
            self._fwd = self.value  # type: ignore[assignment]
        elif k == NODE_EML:
            xv = self.left.forward(env)   # type: ignore[union-attr]
            yv = self.right.forward(env)  # type: ignore[union-attr]
            self._fwd = cmath.exp(xv) - cmath.log(yv)
        else:
            raise ValueError(f"Unknown EMLNode kind: {k!r}")
        return self._fwd

    # --------------------------------------------------------------- backward
    def zero_grad(self) -> None:
        self._grad = 0 + 0j
        if self.kind == NODE_EML:
            self.left.zero_grad()   # type: ignore[union-attr]
            self.right.zero_grad()  # type: ignore[union-attr]

    def backward(self, upstream: complex = 1 + 0j) -> None:
        """Backprop reverse-mode para eml(x, y) = exp(x) − log(y):

            ∂eml/∂x =   exp(x)
            ∂eml/∂y =  −1 / y

        Os gradientes acumulados nas folhas ``LEAF_PARAM`` são usados
        pelo otimizador do Logos.
        """
        self._grad += upstream
        if self.kind == NODE_EML:
            xv = self.left._fwd   # type: ignore[union-attr]
            yv = self.right._fwd  # type: ignore[union-attr]
            # ∂/∂x
            self.left.backward(upstream * cmath.exp(xv))  # type: ignore[union-attr]
            # ∂/∂y  (guarda de Mythos: o backward jamais atravessa log(0))
            y_safe = mythos_singularity_guard(yv)
            self.right.backward(upstream * (-1.0 / y_safe))  # type: ignore[union-attr]

    # ------------------------------------------------------------------ print
    def pretty(self) -> str:
        if self.kind == LEAF_CONST:
            v = self.value  # type: ignore[assignment]
            if abs(v.imag) < 1e-12:
                return f"{v.real:g}"
            return f"({v.real:g}{v.imag:+g}j)"
        if self.kind == LEAF_VAR:
            return self.name or "x"
        if self.kind == LEAF_PARAM:
            v = self.value  # type: ignore[assignment]
            return f"θ({v.real:.3f}{v.imag:+.3f}j)"
        return f"eml({self.left.pretty()}, {self.right.pretty()})"  # type: ignore[union-attr]


# =============================================================================
# 3. EMLTreeFactory  —  amostragem da matéria inicial da síntese
# =============================================================================

class EMLTreeFactory:
    """Constrói árvores-candidato para o Logos ajustar.

    Começamos em geral com folhas predominantemente PARAM (matéria
    indeterminada). Sob pressão do Ethos, as árvores que sobrevivem à
    progressão simbólica tendem a se estreitar para a gramática pura
    {1, eml(·,·)} — o ideal regulativo que nunca é totalmente atingido.
    """

    def __init__(self, var_name: str = "x", seed: Optional[int] = None) -> None:
        self.var_name = var_name
        self.rng = random.Random(seed)

    def const_one(self) -> EMLNode:
        return EMLNode(LEAF_CONST, value=1 + 0j)

    def var(self) -> EMLNode:
        return EMLNode(LEAF_VAR, name=self.var_name)

    def param(self, value: Optional[complex] = None) -> EMLNode:
        if value is None:
            value = complex(self.rng.gauss(0.0, 0.5), self.rng.gauss(0.0, 0.5))
        return EMLNode(LEAF_PARAM, value=value)

    def random_tree(
        self,
        depth: int,
        p_var: float = 0.4,
        p_one: float = 0.25,
    ) -> EMLNode:
        """Gera uma árvore aleatória de profundidade **exata** ``depth``.

        Folhas em d=0 são amostradas de {VAR, CONST=1, PARAM} com
        probabilidades (p_var, p_one, 1 − p_var − p_one).
        """
        if depth <= 1:
            u = self.rng.random()
            if u < p_var:
                return self.var()
            if u < p_var + p_one:
                return self.const_one()
            return self.param()
        return EMLNode(
            NODE_EML,
            left=self.random_tree(depth - 1, p_var, p_one),
            right=self.random_tree(depth - 1, p_var, p_one),
        )


# =============================================================================
# 3b. CLASSIFICAÇÃO CASSIRERIANA  —  níveis internos do Logos
# =============================================================================

def is_darstellung_one(node: EMLNode, tol: float = 1e-9) -> bool:
    """Testa se o nó é a constante Darstellung (LEAF_CONST com valor ≈ 1)."""
    if node.kind != LEAF_CONST or node.value is None:
        return False
    v = node.value
    return abs(v.real - 1.0) < tol and abs(v.imag) < tol


def is_pure_grammar(node: EMLNode) -> bool:
    """Testa se a subárvore pertence à gramática pura ``S → 1 | eml(S,S)``.

    Critério formal de Bedeutung: um trecho do Logos já cristalizado,
    no qual toda matéria indeterminada (VAR/PARAM) foi suprassumida
    e só restam a constante 1 e composições do operador. É a
    "indeterminação produtiva" (Cassirer) que torna o conceito
    universalmente válido justamente por não depender de instância.
    """
    if node.kind == LEAF_CONST:
        return is_darstellung_one(node)
    if node.kind == NODE_EML:
        return is_pure_grammar(node.left) and is_pure_grammar(node.right)  # type: ignore[arg-type]
    return False


def level_of_node(node: EMLNode) -> SymbolicFunction:
    """Classifica um nó segundo a função simbólica cassireriana.

    Regras (decisão 140426):
      - ``LEAF_VAR``                     → AUSDRUCK (imediatez perceptiva)
      - ``LEAF_PARAM``                   → AUSDRUCK (matéria indeterminada)
      - ``LEAF_CONST`` com valor ≈ 1     → DARSTELLUNG (a "constante 1"
                                            é a apresentação pura)
      - ``LEAF_CONST`` com outro valor   → AUSDRUCK residual (ainda não
                                            reduzido à unidade 1)
      - ``NODE_EML`` cuja subárvore é
        ``is_pure_grammar``               → BEDEUTUNG (gramática pura)
      - ``NODE_EML`` misto                → DARSTELLUNG (mediação em
                                            trânsito entre expressão
                                            e significação pura)
    """
    if node.kind == LEAF_VAR:
        return SymbolicFunction.AUSDRUCK
    if node.kind == LEAF_PARAM:
        return SymbolicFunction.AUSDRUCK
    if node.kind == LEAF_CONST:
        return (
            SymbolicFunction.DARSTELLUNG
            if is_darstellung_one(node)
            else SymbolicFunction.AUSDRUCK
        )
    if node.kind == NODE_EML:
        if is_pure_grammar(node):
            return SymbolicFunction.BEDEUTUNG
        return SymbolicFunction.DARSTELLUNG
    raise ValueError(f"Unknown node kind: {node.kind!r}")


def classify_tree(node: EMLNode) -> Dict[SymbolicFunction, int]:
    """Conta os níveis cassirerianos presentes na árvore (perfil).

    Útil ao Gewissen para julgar a distribuição interna entre
    Ausdruck (imediatez), Darstellung (mediação) e Bedeutung
    (significação pura). Uma árvore "madura" tende a acumular
    massa em Bedeutung sem abandonar a Ausdruck de suas folhas VAR.
    """
    profile: Dict[SymbolicFunction, int] = {
        SymbolicFunction.AUSDRUCK: 0,
        SymbolicFunction.DARSTELLUNG: 0,
        SymbolicFunction.BEDEUTUNG: 0,
    }

    def _walk(n: EMLNode) -> None:
        profile[level_of_node(n)] += 1
        if n.kind == NODE_EML:
            _walk(n.left)    # type: ignore[arg-type]
            _walk(n.right)   # type: ignore[arg-type]

    _walk(node)
    return profile


def _structural_equal(a: EMLNode, b: EMLNode, tol: float = 1e-9) -> bool:
    """Igualdade estrutural entre duas árvores EML.

    PARAMs são tratados como opacos (sempre distintos): só cristais
    determinados — VAR, CONST e composições NODE_EML — podem
    contribuir para a determinação comum.
    """
    if a.kind != b.kind:
        return False
    if a.kind == LEAF_CONST:
        if a.value is None or b.value is None:
            return False
        return abs(a.value - b.value) < tol
    if a.kind == LEAF_VAR:
        return a.name == b.name
    if a.kind == LEAF_PARAM:
        return False
    if a.kind == NODE_EML:
        return _structural_equal(a.left, b.left, tol) and _structural_equal(  # type: ignore[arg-type]
            a.right, b.right, tol  # type: ignore[arg-type]
        )
    return False


def _iter_subtrees(node: EMLNode):
    yield node
    if node.kind == NODE_EML:
        yield from _iter_subtrees(node.left)    # type: ignore[arg-type]
        yield from _iter_subtrees(node.right)   # type: ignore[arg-type]


def common_determination(
    tree_a: EMLNode, tree_b: EMLNode
) -> Optional[EMLNode]:
    """Extrai o *genus proximum* de duas árvores — a Darstellung comum.

    Procura a MAIOR subárvore (em qualquer posição) que seja
    estruturalmente idêntica em ``tree_a`` e ``tree_b``. Retorna um
    clone independente da subárvore encontrada.

    Critério (decisão 140426): a determinação comum é a maior
    cristalização da gramática que sobrevive à substituição mútua —
    o "núcleo apresentável" partilhado pelas duas representações.
    Se nada é compartilhado além de PARAMs (opacos), retorna ``None``;
    a constante 1, contudo, sempre pode ser invocada como Darstellung
    trivial via ``CognitionSyntax.darstellung_one()``.
    """
    best: Optional[EMLNode] = None
    best_size = 0
    for sub_a in _iter_subtrees(tree_a):
        for sub_b in _iter_subtrees(tree_b):
            if _structural_equal(sub_a, sub_b):
                s = sub_a.size()
                if s > best_size:
                    best_size = s
                    best = _clone(sub_a)
    return best


# =============================================================================
# 3c. OPERADORES BIDIRECIONAIS  —  ascensão e descida da cognição
# =============================================================================

def ascend_step(node: EMLNode) -> EMLNode:
    """Um passo de ascensão: substitui um LEAF_PARAM pela microsíntese
    ``eml(1, 1) = e¹ − log(1) = e`` — a primeira cristalização possível
    na direção da gramática pura. Retorna uma NOVA árvore; a original
    não é mutada.

    Filosoficamente: é a "sublação da presença (Präsenz)" — o PARAM
    indeterminado é suprassumido por uma composição do operador
    sobre a constante 1 (Darstellung).
    """
    return _ascend_walk(node, mutated=[False])


def _ascend_walk(node: EMLNode, mutated: List[bool]) -> EMLNode:
    if mutated[0]:
        return _clone(node)
    if node.kind == LEAF_PARAM:
        mutated[0] = True
        return EMLNode(
            NODE_EML,
            left=EMLNode(LEAF_CONST, value=1 + 0j),
            right=EMLNode(LEAF_CONST, value=1 + 0j),
        )
    if node.kind == NODE_EML:
        new_left = _ascend_walk(node.left, mutated)    # type: ignore[arg-type]
        new_right = _ascend_walk(node.right, mutated)  # type: ignore[arg-type]
        return EMLNode(NODE_EML, left=new_left, right=new_right)
    return _clone(node)


def _clone(node: EMLNode) -> EMLNode:
    if node.kind == NODE_EML:
        return EMLNode(
            NODE_EML,
            left=_clone(node.left),    # type: ignore[arg-type]
            right=_clone(node.right),  # type: ignore[arg-type]
        )
    return EMLNode(node.kind, value=node.value, name=node.name)


def descend_evaluate(
    tree: EMLNode,
    env_sequence: Sequence[Dict[str, complex]],
) -> List[complex]:
    """Passo de descida: reavalia a árvore (supostamente cristalizada
    em Bedeutung) sobre uma sequência de ambientes de intuição —
    tipicamente um domínio de ``x`` mais amplo que aquele usado na
    ascensão, testando a "certeza regulativa maior" (Cassirer) do
    retorno ao mundo da intuição.
    """
    outputs: List[complex] = []
    for env in env_sequence:
        outputs.append(tree.forward(dict(env)))
    return outputs


def descend_residual(
    tree: EMLNode,
    target_fn: Callable[[complex], complex],
    xs: Sequence[complex],
    var_name: str = "x",
) -> float:
    """Erro quadrático médio da descida: quão bem a árvore
    cristalizada reproduz a função-alvo sobre um domínio arbitrário
    de intuição. Mede a fidelidade do retorno.
    """
    if len(xs) == 0:
        return 0.0
    total = 0.0
    for x in xs:
        try:
            predicted = tree.forward({var_name: complex(x)})
            target = complex(target_fn(complex(x)))
        except (OverflowError, ValueError, ZeroDivisionError):
            return float("inf")
        r = predicted - target
        total += r.real * r.real + r.imag * r.imag
    return total / len(xs)


# =============================================================================
# 4. ComplexAdam  —  Adam para parâmetros complexos (ℂ ≅ ℝ²)
# =============================================================================

class ComplexAdam:
    """Otimizador Adam para parâmetros complexos.

    Perda real L(θ) sobre parâmetros complexos θ ∈ ℂ. Usamos a derivada
    de Wirtinger: a direção de descida é

        step ∝  2 · ∂L/∂θ̄  =  2 · conj( (f − y) · ∂f/∂θ ).

    O backward de ``EMLNode`` acumula, em cada folha PARAM,
    ``_grad = Σ_i residue_i · ∂f_i/∂θ`` (perfeitamente holomorfo).
    Conjugamos e dobramos aqui para obter o gradiente real de L.
    """

    def __init__(
        self,
        params: Sequence[EMLNode],
        lr: float = 0.05,
        b1: float = 0.9,
        b2: float = 0.999,
        eps: float = 1e-8,
    ) -> None:
        self.params = list(params)
        self.lr = lr
        self.b1 = b1
        self.b2 = b2
        self.eps = eps
        self.t = 0
        self.m: List[complex] = [0 + 0j for _ in self.params]
        self.v: List[float] = [0.0 for _ in self.params]

    def step(self) -> None:
        self.t += 1
        for i, p in enumerate(self.params):
            g: complex = 2.0 * p._grad.conjugate()  # 2 · ∂L/∂θ̄
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * (abs(g) ** 2)
            m_hat = self.m[i] / (1 - self.b1 ** self.t)
            v_hat = self.v[i] / (1 - self.b2 ** self.t)
            denom = math.sqrt(v_hat) + self.eps
            p.value = p.value - self.lr * m_hat / denom  # type: ignore[operator]


# =============================================================================
# 5. LOGOS  —  pilar da intuição matemática
# =============================================================================

class Logos:
    """Pilar Logos: motor da síntese transcendental.

    Regra arquitetônica do AGI-GAIA-TECHNE:
        TODA "intuição" entra no sistema através do Logos e
        EM NENHUM OUTRO LUGAR. Os dados (x_i, y_i) são a matéria
        indeterminada da intuição kantiana; o Logos os submete à
        forma, buscando uma árvore EML cuja saída se aproxima dos y_i.

    O Logos, sozinho, nunca declara vitória: quem decide se uma
    síntese local é digna de prosseguir é o Ethos (Gewissen).
    """

    def __init__(self, tree: EMLNode, var_name: str = "x") -> None:
        self.tree = tree
        self.var_name = var_name

    # ----------------------------------------------------------- avaliação
    def predict(self, x: complex) -> complex:
        return self.tree.forward({self.var_name: complex(x)})

    def loss(self, xs: Sequence[complex], ys: Sequence[complex]) -> float:
        total = 0.0
        n = 0
        for x, y in zip(xs, ys):
            try:
                r = self.predict(x) - complex(y)
            except (OverflowError, ValueError, ZeroDivisionError):
                return float("inf")
            total += r.real * r.real + r.imag * r.imag
            n += 1
        return total / max(n, 1)

    # ---------------------------------------------------------- ajuste
    def fit(
        self,
        xs: Sequence[complex],
        ys: Sequence[complex],
        steps: int = 300,
        lr: float = 0.05,
    ) -> List[float]:
        """Ajusta os parâmetros PARAM da árvore por Adam / autodiff."""
        params = self.tree.params()
        if not params:
            # Árvore cristalizada (só {1, eml}). Nada a ajustar.
            return [self.loss(xs, ys)]

        opt = ComplexAdam(params, lr=lr)
        history: List[float] = []
        n = max(len(xs), 1)

        for _ in range(steps):
            # zero grads somente nas folhas PARAM (únicas relevantes)
            for p in params:
                p._grad = 0 + 0j

            total = 0.0
            aborted = False
            for x, y in zip(xs, ys):
                try:
                    self.tree.forward({self.var_name: complex(x)})
                except (OverflowError, ValueError, ZeroDivisionError):
                    aborted = True
                    break
                resid = self.tree._fwd - complex(y)
                total += resid.real * resid.real + resid.imag * resid.imag
                try:
                    self.tree.backward(upstream=resid)
                except (OverflowError, ValueError, ZeroDivisionError):
                    aborted = True
                    break

            if aborted or not math.isfinite(total):
                history.append(float("inf"))
                return history

            # média dos gradientes sobre o mini-lote
            for p in params:
                p._grad = p._grad / n
            opt.step()
            history.append(total / n)
        return history


# =============================================================================
# 6. ETHOS  —  Gewissen, jamais Wissen
# =============================================================================

@dataclass
class EthosEvaluation:
    """Avaliação ética-regulativa de um candidato do Logos.

    Após a calibração bidirecional 140426, a distância ao *focus
    imaginarius* é decomposta em duas componentes irredutíveis:

      * ``distance_to_focus_ascent``  — resíduo da síntese ascendente
        (cristalização em profundidade) — o quanto a árvore ainda se
        afasta do ideal regulativo pelo lado da abstração.
      * ``distance_to_focus_descent`` — resíduo da descida analítica
        (retorno à intuição) — o quanto a árvore cristalizada ainda
        se afasta do alvo quando reavaliada sobre intuição expandida.
      * ``distance_to_focus`` é a norma Euclidiana das duas: ``√(a²+d²)+ε``.

    Por construção, **as duas direções nunca podem ser simultaneamente
    zero** — formalização matemática da teleologia aberta (Kinzel
    2024b) e do processo contingente-infinito da cognição bidirecional.
    """
    loss: float
    depth: int
    size: int
    param_mass: float                    # massa residual da matéria indeterminada
    distance_to_focus_ascent: float      # componente ascendente (síntese)
    distance_to_focus_descent: float     # componente descendente (retorno)
    distance_to_focus: float             # norma composta ao focus imaginarius
    symbolic_profile: Dict[SymbolicFunction, int] = field(default_factory=dict)


class Ethos:
    """Pilar Ethos — filtro do *Gewissen* sobre a progressão simbólica.

    **Regra arquitetônica inegociável.** No vocabulário do AGI-GAIA-TECHNE,
    "Wissen" deve ser rigorosamente traduzido como **Gewissen**
    (consciência moral). O Ethos não é um repositório de saber; é a
    instância crítica que mede quanto a progressão simbólica do Logos
    se aproxima — e, por construção, jamais atinge — o *focus
    imaginarius* kantiano da representação total.

    Após a calibração bidirecional (140426), a distância ao foco
    decompõe-se em dois vetores irredutíveis que jamais se anulam
    simultaneamente — formalizando o duplo movimento teleológico::

        d_asc   = w_loss · loss + w_depth · depth + w_param · ‖θ‖̄
        d_desc  = w_desc · descida_residual  (erro do retorno à intuição)
        distance_to_focus = √(d_asc² + d_desc²) + ε,   ε > 0.

    Esta métrica é uma relação do tipo *incerteza* entre abstração
    (d_asc) e fidelidade intuitiva (d_desc): zerar uma não zera a
    outra. O Gewissen julga a *norma* — a aproximação genuína ao
    ideal regulativo exige minimização conjunta, não unilateral.
    """

    def __init__(
        self,
        w_loss: float = 1.0,
        w_depth: float = 0.05,
        w_param: float = 0.10,
        w_desc: float = 1.0,
        focus_epsilon: float = 1e-9,
    ) -> None:
        self.w_loss = w_loss
        self.w_depth = w_depth
        self.w_param = w_param
        self.w_desc = w_desc
        self.focus_epsilon = focus_epsilon

    def evaluate(
        self,
        tree: EMLNode,
        loss: float,
        descent_residual: float = 0.0,
    ) -> EthosEvaluation:
        params = tree.params()
        if params:
            param_mass = sum(abs(p.value) for p in params) / len(params)  # type: ignore[arg-type]
        else:
            param_mass = 0.0

        d_asc = (
            self.w_loss * loss
            + self.w_depth * tree.depth()
            + self.w_param * param_mass
        )
        d_desc = self.w_desc * max(descent_residual, 0.0)

        # norma Euclidiana + ε estrito ⇒ nunca zero
        dist = math.sqrt(d_asc * d_asc + d_desc * d_desc) + self.focus_epsilon

        return EthosEvaluation(
            loss=loss,
            depth=tree.depth(),
            size=tree.size(),
            param_mass=param_mass,
            distance_to_focus_ascent=d_asc,
            distance_to_focus_descent=d_desc,
            distance_to_focus=dist,
            symbolic_profile=classify_tree(tree),
        )

    def gewissen_accept(
        self,
        current: EthosEvaluation,
        best_so_far: Optional[EthosEvaluation],
        rel_improvement: float = 0.0,
    ) -> bool:
        """Aceita a síntese local se reduz a distância ao foco.

        ``rel_improvement`` permite exigir uma melhora relativa mínima
        — pequena fricção moral contra flutuações ruidosas da intuição.
        """
        if current.loss != current.loss:  # NaN
            return False
        if not math.isfinite(current.distance_to_focus):
            return False
        if best_so_far is None:
            return True
        delta = best_so_far.distance_to_focus - current.distance_to_focus
        return delta / best_so_far.distance_to_focus >= rel_improvement


# =============================================================================
# 7. SIMBIOTA  —  o cálculo infinitesimal em ação
# =============================================================================

@dataclass
class SimbiotaState:
    iteration: int
    depth: int
    best_tree: EMLNode
    best_eval: EthosEvaluation
    trajectory: List[float] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"[iter={self.iteration:03d}] depth={self.depth} "
            f"loss={self.best_eval.loss:.4e} "
            f"|θ|={self.best_eval.param_mass:.3f} "
            f"d_asc={self.best_eval.distance_to_focus_ascent:.3e} "
            f"d_desc={self.best_eval.distance_to_focus_descent:.3e} "
            f"d(focus)={self.best_eval.distance_to_focus:.4e} "
            f"| {self.best_tree.pretty()}"
        )


class Simbiota:
    """Loop de execução que instancia o cálculo infinitesimal.

    A cada passo da progressão simbólica:

      1. **Logos** amostra ``candidates_per_depth`` árvores EML de
         profundidade corrente e ajusta seus parâmetros aos dados
         (síntese local — *Aufhebung local*);
      2. **Ethos** avalia cada candidato; o *Gewissen* decide quem
         promove a campeão; a confrontação global
         (*Auseinandersetzung*) permanece aberta por princípio;
      3. A profundidade da árvore cresce no passo seguinte,
         aproximando-se — jamais alcançando — o *focus imaginarius*.

    ``run`` retorna sempre um *estado*, nunca uma "solução final": a
    completude absoluta é um ideal regulativo, não um destino.
    """

    def __init__(
        self,
        xs: Sequence[complex],
        ys: Sequence[complex],
        var_name: str = "x",
        candidates_per_depth: int = 8,
        fit_steps: int = 200,
        lr: float = 0.05,
        seed: Optional[int] = None,
        target_fn: Optional[Callable[[complex], complex]] = None,
        descent_domain: Optional[Sequence[complex]] = None,
    ) -> None:
        self.xs = list(xs)
        self.ys = list(ys)
        self.var_name = var_name
        self.candidates = candidates_per_depth
        self.fit_steps = fit_steps
        self.lr = lr
        self.factory = EMLTreeFactory(var_name=var_name, seed=seed)
        self.ethos = Ethos()
        # Suporte à descida analítica: função-alvo conhecida e domínio
        # de intuição expandido sobre o qual testar o retorno.
        self.target_fn = target_fn
        self.descent_domain = list(descent_domain) if descent_domain is not None else []

    # ---------------------------------------------------------- descida
    def _descent_residual(self, tree: EMLNode) -> float:
        """Computa o erro médio da descida sobre ``descent_domain``.

        Se não há função-alvo ou domínio de descida, a componente
        descendente é zero (mas o ε do Ethos mantém o foco > 0).
        """
        if self.target_fn is None or not self.descent_domain:
            return 0.0
        return descend_residual(
            tree, self.target_fn, self.descent_domain, self.var_name
        )

    # ---------------------------------------------------------- um "passo"
    def step_depth(
        self,
        depth: int,
        best_eval: Optional[EthosEvaluation],
    ) -> Tuple[Optional[EMLNode], Optional[EthosEvaluation]]:
        best_tree: Optional[EMLNode] = None
        best = best_eval
        for _ in range(self.candidates):
            tree = self.factory.random_tree(depth)
            logos = Logos(tree, var_name=self.var_name)
            try:
                history = logos.fit(self.xs, self.ys, steps=self.fit_steps, lr=self.lr)
                loss = history[-1]
            except (OverflowError, ValueError, ZeroDivisionError):
                continue
            if not math.isfinite(loss):
                continue
            d_desc = self._descent_residual(tree)
            if not math.isfinite(d_desc):
                continue
            ev = self.ethos.evaluate(tree, loss, descent_residual=d_desc)
            if self.ethos.gewissen_accept(ev, best):
                best = ev
                best_tree = tree
        return best_tree, best

    # ------------------------------------------------------------------ run
    def run(self, max_depth: int = 4, verbose: bool = True) -> SimbiotaState:
        # Estado inicial: a constante 1 — o "primeiro símbolo" da gramática.
        seed_tree = self.factory.const_one()
        seed_loss = Logos(seed_tree, self.var_name).loss(self.xs, self.ys)
        seed_desc = self._descent_residual(seed_tree)
        seed_eval = self.ethos.evaluate(seed_tree, seed_loss, descent_residual=seed_desc)
        state = SimbiotaState(
            iteration=0,
            depth=1,
            best_tree=seed_tree,
            best_eval=seed_eval,
            trajectory=[seed_eval.distance_to_focus],
        )
        if verbose:
            print(state.summary())

        for d in range(2, max_depth + 1):
            new_tree, new_eval = self.step_depth(d, state.best_eval)
            if new_tree is not None and new_eval is not None:
                best_tree = new_tree
                best_eval = new_eval
            else:
                best_tree = state.best_tree
                best_eval = state.best_eval
            state = SimbiotaState(
                iteration=state.iteration + 1,
                depth=d,
                best_tree=best_tree,
                best_eval=best_eval,
                trajectory=state.trajectory + [best_eval.distance_to_focus],
            )
            if verbose:
                print(state.summary())
        return state

    # --------------------------------------------------------- bidirecional
    def run_bidirectional(
        self,
        max_depth: int = 4,
        verbose: bool = True,
    ) -> SimbiotaState:
        """Loop bidirecional da sintaxe da cognição (decisão 140426).

        Cada iteração é composta por DUAS fases indissociáveis:

          * **Ascensão**: ``step_depth`` gera/ajusta candidatos de
            profundidade ``d``. O Logos cristaliza PARAM/VAR em
            subestruturas {1, eml} — a síntese transcendental.
          * **Descida**: a árvore-campeã é avaliada sobre o domínio
            de intuição expandido (``descent_domain``). O resíduo
            alimenta ``distance_to_focus_descent`` no próximo passo,
            materializando o movimento de cima para baixo — o
            "retorno ao mundo da intuição com certeza regulativa
            maior" (Cassirer).

        O Gewissen julga a NORMA das duas componentes: minimizar
        ascensão sem descida é fuga abstrativa; minimizar descida
        sem ascensão é regressão à imediatez. A teleologia aberta
        é essa co-presença irredutível.
        """
        return self.run(max_depth=max_depth, verbose=verbose)


# =============================================================================
# 7b. COGNITION SYNTAX  —  a DSL da sintaxe da cognição
# =============================================================================

class CognitionSyntax:
    """A sintaxe primitiva da cognição bidirecional (decisão 140426).

    Expõe, como uma pequena DSL, os movimentos atômicos que qualquer
    processo cognitivo do framework AGI-GAIA-TECHNE pode usar:

      * ``ascend(tree)``            — um passo de cristalização
      * ``descend(tree, env)``      — reavaliação sobre intuição
      * ``classify(tree)``          — perfil (Ausdruck/Darstellung/Bedeutung)
      * ``project_to_level(tree)``  — inspeção por nível
      * ``common_determination(a, b)`` — genus proximum de duas árvores
      * ``is_bedeutung(tree)``      — teste de cristalização pura
      * ``darstellung_one()``       — a constante 1 (genus proximum)

    Todos os métodos são estáticos / sem estado: a sintaxe não tem
    memória — ela é apenas o repertório de movimentos. O contexto
    cognitivo vive no Logos e no Ethos, que usam esta DSL.
    """

    # --- movimentos bidirecionais -------------------------------------
    @staticmethod
    def ascend(tree: EMLNode) -> EMLNode:
        return ascend_step(tree)

    @staticmethod
    def descend(
        tree: EMLNode, env_sequence: Sequence[Dict[str, complex]]
    ) -> List[complex]:
        return descend_evaluate(tree, env_sequence)

    @staticmethod
    def descend_error(
        tree: EMLNode,
        target_fn: Callable[[complex], complex],
        xs: Sequence[complex],
        var_name: str = "x",
    ) -> float:
        return descend_residual(tree, target_fn, xs, var_name)

    # --- classificação cassireriana -----------------------------------
    @staticmethod
    def classify(tree: EMLNode) -> Dict[SymbolicFunction, int]:
        return classify_tree(tree)

    @staticmethod
    def level_of(node: EMLNode) -> SymbolicFunction:
        return level_of_node(node)

    @staticmethod
    def is_bedeutung(tree: EMLNode) -> bool:
        return is_pure_grammar(tree)

    @staticmethod
    def is_darstellung_one_node(node: EMLNode) -> bool:
        return is_darstellung_one(node)

    # --- genus proximum ------------------------------------------------
    @staticmethod
    def common_determination(
        tree_a: EMLNode, tree_b: EMLNode
    ) -> Optional[EMLNode]:
        return common_determination(tree_a, tree_b)

    @staticmethod
    def darstellung_one() -> EMLNode:
        """Retorna a constante 1 — o genus proximum universal.

        É o menor elemento comum a toda árvore EML bem formada:
        a Darstellung operativa (y=1) que permite ao operador
        colapsar em pura exponenciação.
        """
        return EMLNode(LEAF_CONST, value=1 + 0j)


# =============================================================================
# 8. Demonstração  —  intuição bruta → forma fechada
# =============================================================================

def _demo() -> None:
    """Demo: o Logos "descobre" que exp(x) = eml(x, 1) e exercita a
    sintaxe bidirecional da cognição (decisão 140426).

    Apresenta, sequencialmente:
      (a) ascensão: regressão simbólica que cristaliza ``eml(x, 1)``;
      (b) descida: reavaliação sobre um domínio de intuição EXPANDIDO
          — a "certeza regulativa maior" do retorno cassireriano;
      (c) genus proximum: ``common_determination`` extrai a Darstellung
          partilhada por duas árvores distintas;
      (d) classificação cassireriana: perfil Ausdruck/Darstellung/Bedeutung
          de uma árvore cristalizada.
    """
    import cmath as _cm

    xs = [complex(v, 0) for v in np.linspace(-1.0, 1.0, 9)]
    ys = [_cm.exp(x) for x in xs]

    print("=" * 68)
    print("AGI-GAIA-TECHNE · Kernel EML · Demo do Simbiota Bidirecional")
    print("Decisão 140426 — eixo vertical da cognição")
    print("=" * 68)
    print(f"Alvo (intuição bruta) : f(x) = exp(x)  em {len(xs)} pontos")
    print(f"Hipótese regulativa   : f(x) = eml(x, 1) = exp(x) − log(1)")
    print("-" * 68)

    # ---------- (a) e (b) ascensão + descida acopladas ----------
    descent_domain = [complex(v, 0) for v in np.linspace(-2.0, 2.0, 17)]
    simbiota = Simbiota(
        xs, ys,
        candidates_per_depth=12,
        fit_steps=120,
        lr=0.08,
        seed=42,
        target_fn=_cm.exp,
        descent_domain=descent_domain,
    )
    final = simbiota.run_bidirectional(max_depth=3, verbose=True)

    print()
    print("Trajetória da distância ao *focus imaginarius*:")
    for i, d in enumerate(final.trajectory):
        print(f"  passo {i}:  d(focus) = {d:.6e}")
    print()
    print("Componentes da distância ao foco no estado final:")
    print(f"  d_asc  (síntese ascendente) = {final.best_eval.distance_to_focus_ascent:.6e}")
    print(f"  d_desc (descida analítica)  = {final.best_eval.distance_to_focus_descent:.6e}")
    print(f"  d(focus) = √(d_asc² + d_desc²) + ε = {final.best_eval.distance_to_focus:.6e}")
    print()
    print("Perfil cassireriano (níveis internos do Logos):")
    for level, count in final.best_eval.symbolic_profile.items():
        print(f"  {level.value:12s} : {count}")
    print()
    print("Árvore-campeã (síntese LOCAL — jamais absoluta):")
    print(f"  f̂(x) = {final.best_tree.pretty()}")
    print()

    # ---------- (c) genus proximum entre duas árvores ----------
    print("-" * 68)
    print("Determinação comum (genus proximum) entre duas árvores:")
    syntax = CognitionSyntax()
    factory = EMLTreeFactory(seed=7)
    # A = eml(eml(x, 1), 1)        ← exp(exp(x))
    # B = eml(eml(x, 1), eml(1,1)) ← exp(exp(x)) − 1
    inner = EMLNode(NODE_EML, left=factory.var(), right=factory.const_one())
    tree_a = EMLNode(NODE_EML, left=_clone(inner), right=factory.const_one())
    tree_b = EMLNode(
        NODE_EML,
        left=_clone(inner),
        right=EMLNode(NODE_EML, left=factory.const_one(), right=factory.const_one()),
    )
    print(f"  A: {tree_a.pretty()}")
    print(f"  B: {tree_b.pretty()}")
    common = syntax.common_determination(tree_a, tree_b)
    if common is not None:
        print(f"  Darstellung comum: {common.pretty()}")
        print(f"  É Bedeutung pura? {syntax.is_bedeutung(common)}")
    else:
        print("  (sem determinação estrutural comum)")

    # ---------- (d) descida explícita sobre intuição nova ----------
    print()
    print("-" * 68)
    print("Descida explícita: árvore cristalizada eml(x, 1) sobre domínio amplo")
    crystal = EMLNode(NODE_EML, left=factory.var(), right=factory.const_one())
    big_domain = [{"x": complex(v, 0)} for v in np.linspace(-3.0, 3.0, 7)]
    outputs = syntax.descend(crystal, big_domain)
    targets = [_cm.exp(env["x"]) for env in big_domain]
    max_err = max(abs(o - t) for o, t in zip(outputs, targets))
    print(f"  pontos avaliados: {len(big_domain)}")
    print(f"  erro absoluto máximo: {max_err:.3e}")
    print(f"  perfil cassireriano:  {syntax.classify(crystal)}")

    print()
    print("=" * 68)
    print("Lembretes arquitetônicos do AGI-GAIA-TECHNE:")
    print("  • Intuição processada EXCLUSIVAMENTE no Logos.")
    print("  • Ethos = Gewissen (consciência moral), NÃO Wissen.")
    print("  • O *focus imaginarius* jamais é atingido; apenas aproximado.")
    print("  • Mythos ≡ log(0) é a singularidade foreclosed do operador.")
    print("  • Darstellung ≡ a constante 1 do EML — o silêncio operativo.")
    print("  • As duas direções (ascensão/descida) NUNCA são ambas zero.")


if __name__ == "__main__":
    _demo()

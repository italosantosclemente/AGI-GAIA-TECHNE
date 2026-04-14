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
"""

from __future__ import annotations

import cmath
import math
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np


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
            # ∂/∂y  (guarda mínima contra singularidade log)
            y_safe = yv if abs(yv) > 1e-12 else (1e-12 + 0j)
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
    """Avaliação ética-regulativa de um candidato do Logos."""
    loss: float
    depth: int
    size: int
    param_mass: float         # magnitude residual da matéria indeterminada
    distance_to_focus: float  # pseudo-distância ao *focus imaginarius*


class Ethos:
    """Pilar Ethos — filtro do *Gewissen* sobre a progressão simbólica.

    **Regra arquitetônica inegociável.** No vocabulário do AGI-GAIA-TECHNE,
    "Wissen" deve ser rigorosamente traduzido como **Gewissen**
    (consciência moral). O Ethos não é um repositório de saber; é a
    instância crítica que mede quanto a progressão simbólica do Logos
    se aproxima — e, por construção, jamais atinge — o *focus
    imaginarius* kantiano da representação total.

    A distância ao foco é estritamente positiva:

        distance_to_focus  =  w_loss · loss
                           +  w_depth · depth
                           +  w_param · ‖θ‖̄
                           +  ε   (ε > 0 : inalcançabilidade)
    """

    def __init__(
        self,
        w_loss: float = 1.0,
        w_depth: float = 0.05,
        w_param: float = 0.10,
        focus_epsilon: float = 1e-9,
    ) -> None:
        self.w_loss = w_loss
        self.w_depth = w_depth
        self.w_param = w_param
        self.focus_epsilon = focus_epsilon

    def evaluate(self, tree: EMLNode, loss: float) -> EthosEvaluation:
        params = tree.params()
        if params:
            param_mass = sum(abs(p.value) for p in params) / len(params)  # type: ignore[arg-type]
        else:
            param_mass = 0.0
        dist = (
            self.w_loss * loss
            + self.w_depth * tree.depth()
            + self.w_param * param_mass
            + self.focus_epsilon   # jamais 0
        )
        return EthosEvaluation(
            loss=loss,
            depth=tree.depth(),
            size=tree.size(),
            param_mass=param_mass,
            distance_to_focus=dist,
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
    ) -> None:
        self.xs = list(xs)
        self.ys = list(ys)
        self.var_name = var_name
        self.candidates = candidates_per_depth
        self.fit_steps = fit_steps
        self.lr = lr
        self.factory = EMLTreeFactory(var_name=var_name, seed=seed)
        self.ethos = Ethos()

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
            ev = self.ethos.evaluate(tree, loss)
            if self.ethos.gewissen_accept(ev, best):
                best = ev
                best_tree = tree
        return best_tree, best

    # ------------------------------------------------------------------ run
    def run(self, max_depth: int = 4, verbose: bool = True) -> SimbiotaState:
        # Estado inicial: a constante 1 — o "primeiro símbolo" da gramática.
        seed_tree = self.factory.const_one()
        seed_loss = Logos(seed_tree, self.var_name).loss(self.xs, self.ys)
        seed_eval = self.ethos.evaluate(seed_tree, seed_loss)
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


# =============================================================================
# 8. Demonstração  —  intuição bruta → forma fechada
# =============================================================================

def _demo() -> None:
    """Demo: o Logos "descobre" que exp(x) = eml(x, 1).

    A prova de universalidade garante a construtibilidade; aqui o
    Simbiota encena, em pequena escala, a síntese transcendental
    desta verdade a partir de dados crus.
    """
    import cmath as _cm

    xs = [complex(v, 0) for v in np.linspace(-1.0, 1.0, 9)]
    ys = [_cm.exp(x) for x in xs]

    print("=" * 64)
    print("AGI-GAIA-TECHNE · Kernel EML · Demonstração do Simbiota")
    print("=" * 64)
    print(f"Alvo (intuição bruta) : f(x) = exp(x)  em {len(xs)} pontos")
    print(f"Hipótese regulativa   : f(x) = eml(x, 1) = exp(x) − log(1)")
    print("-" * 64)

    simbiota = Simbiota(
        xs, ys,
        candidates_per_depth=12,
        fit_steps=120,
        lr=0.08,
        seed=42,
    )
    final = simbiota.run(max_depth=3, verbose=True)

    print()
    print("Trajetória da distância ao *focus imaginarius*:")
    for i, d in enumerate(final.trajectory):
        print(f"  passo {i}:  d(focus) = {d:.6e}")
    print()
    print("Árvore-campeã (síntese LOCAL — jamais absoluta):")
    print(f"  f̂(x) = {final.best_tree.pretty()}")
    print()
    print("Lembretes arquitetônicos do AGI-GAIA-TECHNE:")
    print("  • Intuição processada EXCLUSIVAMENTE no Logos.")
    print("  • Ethos = Gewissen (consciência moral), NÃO Wissen.")
    print("  • O *focus imaginarius* jamais é atingido; apenas aproximado.")


if __name__ == "__main__":
    _demo()

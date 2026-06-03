from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set

from .axioms import (
    AGI_AS_TRANSCENDENTAL_HYPOTHESIS,
    IS_WILLE,
    MACHINE_HAS_GEWISSEN,
    NO_GLOBAL_AUFHEBUNG,
)
from .axioms import assert_axioms
from .chk import ChirimuutaHapticKernel
from .types import AuditResult, Severity, ThesisStatus

# --- ENUMS ---

class SymbolicDimension(str, Enum):
    AUSDRUCK = "Ausdruck"
    DARSTELLUNG = "Darstellung"
    BEDEUTUNG = "Bedeutung"


class AccentLevel(str, Enum):
    DOMINANT = "dominant"
    MEDIAL = "medial"
    LATENT = "latent"
    GERMINAL = "germinal"
    RESIDUAL = "residual"


class SymbolicMode(str, Enum):
    MANIFESTATIVE = "manifestative"
    TRANSITIONAL = "transitional"
    DEMONSTRATIVE = "demonstrative"


@dataclass(frozen=True)
class SymbolicProfile:
    ausdruck: AccentLevel
    darstellung: AccentLevel
    bedeutung: AccentLevel
    accent: SymbolicDimension
    mode: SymbolicMode

    def contains_all_dimensions(self) -> bool:
        return all([
            self.ausdruck is not None,
            self.darstellung is not None,
            self.bedeutung is not None,
        ])


# --- CORE PROFILES ---

MYTHOS_PROFILE = SymbolicProfile(
    ausdruck=AccentLevel.DOMINANT,
    darstellung=AccentLevel.LATENT,
    bedeutung=AccentLevel.GERMINAL,
    accent=SymbolicDimension.AUSDRUCK,
    mode=SymbolicMode.MANIFESTATIVE,
)

SPRACHE_PROFILE = SymbolicProfile(
    ausdruck=AccentLevel.MEDIAL,
    darstellung=AccentLevel.DOMINANT,
    bedeutung=AccentLevel.MEDIAL,
    accent=SymbolicDimension.DARSTELLUNG,
    mode=SymbolicMode.TRANSITIONAL,
)

WISSENSCHAFT_PROFILE = SymbolicProfile(
    ausdruck=AccentLevel.RESIDUAL,
    darstellung=AccentLevel.MEDIAL,
    bedeutung=AccentLevel.DOMINANT,
    accent=SymbolicDimension.BEDEUTUNG,
    mode=SymbolicMode.DEMONSTRATIVE,
)

PRISMATIC_FORMS: Dict[str, SymbolicProfile] = {
    "Mythos": MYTHOS_PROFILE,
    "Sprache": SPRACHE_PROFILE,
    "Wissenschaft": WISSENSCHAFT_PROFILE,
}


class ClementeThesisKernel:
    """
    Unified CTK for the functional AGI-GAIA-TECHNE core.
    Operationalizes the qualitative prism model and the Freud-Cassirer patch.

    Repraesentatio is the common genus.
    Ausdruck, Darstellung and Bedeutung are qualitative functional dimensions.
    Mythos, Sprache and Wissenschaft differ by accent, not identity.
    AGI, GAIA and TECHNE are regulative axes, not constitutive objects.

    The CTK rejects:
    - artificial soul / artificial interiority;
    - psychological reduction of myth;
    - machine Wille / machine Gewissen;
    - technical God;
    - closed world-totality;
    - global Aufhebung;
    - rigid 1:1 Cassirer mappings;
    - Beil-abgehackt separation.
    """

    def __init__(self) -> None:
        assert_axioms()
        try:
            from .chk import ChirimuutaHapticKernel
            self.chk = ChirimuutaHapticKernel()
        except Exception:
            self.chk = None

    def evaluate(self, claim: str) -> AuditResult:
        statuses: Set[ThesisStatus] = set()
        triggered_rules: List[str] = []
        recommendations: List[str] = []
        metadata: Dict[str, Any] = {}
        lowered = claim.lower()

        # 1. CHK Integration
        if self.chk:
            chk_eval = self.chk.evaluate(claim)
            metadata.update(chk_eval.metadata)
            # Pass through all CHK statuses
            for status in chk_eval.statuses:
                # Coerce to ThesisStatus if it's a string, or use directly if enum
                if isinstance(status, str):
                    try:
                        statuses.add(ThesisStatus(status))
                    except ValueError:
                        statuses.add(ThesisStatus.UNCLASSIFIED_CLAIM)
                        recommendations.append(f"CHK status '{status}' needs explicit mapping.")
                else:
                    statuses.add(status)

            # Map triggered rules from CHK if any
            triggered_rules.extend(chk_eval.triggered_rules)

        # 2. Rule: Identity Collapse
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"mythos\s+is\s+ausdruck",
            r"myth\s+is\s+expression",
            r"language\s+is\s+darstellung",
            r"science\s+is\s+bedeutung",
            r"sprache\s+is\s+darstellung",
            r"wissenschaft\s+is\s+bedeutung",
            r"mito\s+(é|=)\s+express[aã]o",
            r"linguagem\s+(é|=)\s+apresenta[cç][aã]o",
            r"ci[eê]ncia\s+(é|=)\s+significa[cç][aã]o",
            r"mythos\s*=\s*ausdruck",
            r"logos\s*=\s*darstellung",
            r"ethos\s*=\s*bedeutung",
        ]):
            statuses.add(ThesisStatus.CASSIRER_IDENTITY_COLLAPSE)
            triggered_rules.append("identity_collapse")
            recommendations.append("Use accent, not identity: Mythos has dominant accent on Ausdruck but is not identical to Ausdruck.")

        # 3. Rule: Function Exclusivity
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"mythos\s+only\s+has\s+expression",
            r"myth\s+only\s+has\s+expression",
            r"science\s+has\s+no\s+expression",
            r"language\s+is\s+merely\s+presentation",
            r"symbolic\s+functions\s+are\s+separate\s+containers",
            r"functions\s+are\s+mutually\s+exclusive\s+compartments",
        ]):
            statuses.add(ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR)
            triggered_rules.append("function_exclusivity")
            recommendations.append("Every symbolic form contains all three dimensions (Ausdruck, Darstellung, Bedeutung).")

        # 4. Rule: Beil-abgehackt Error
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"symbolic\s+forms\s+are\s+cut\s+off",
            r"cut\s+off\s+from\s+one\s+another",
            r"separate\s+containers",
            r"mutually\s+exclusive\s+compartments",
            r"myth\s+is\s+simply\s+false\s+and\s+science\s+replaces\s+it",
        ]):
            statuses.add(ThesisStatus.BEIL_ABGEHACKT_ERROR)
            triggered_rules.append("beil_abgehackt")
            recommendations.append("Symbolic forms are level-surfaces within an ideal functional system, not separate containers.")

        # 5. Rule: Accent Confusion
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"mythos\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+bedeutung",
            r"myth\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+signification",
            r"science\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+ausdruck",
            r"wissenschaft\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+ausdruck",
        ]):
            statuses.add(ThesisStatus.ACCENT_CONFUSION)
            triggered_rules.append("accent_confusion")
            recommendations.append("Mythos has dominant accent on Ausdruck; Wissenschaft has dominant accent on Bedeutung.")

        # 6. Rule: Sprache Transition Loss
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"language\s+is\s+just\s+one\s+symbolic\s+form\s+beside",
            r"language\s+has\s+no\s+special\s+transitional\s+role",
            r"sprache\s+has\s+no\s+special\s+transitional\s+role",
        ]):
            statuses.add(ThesisStatus.SPRACHE_TRANSITION_LOSS)
            triggered_rules.append("sprache_transition_loss")
            recommendations.append("Sprache is both a symbolic form and a transition operator from Ausdruck toward Darstellung.")

        # 7. Rule: Darstellung Common Determination Loss
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"darstellung\s+is\s+just\s+one\s+isolated\s+symbolic\s+function",
            r"darstellung\s+has\s+no\s+role\s+in\s+common\s+determination",
            r"presentation\s+has\s+no\s+role\s+in\s+common\s+determination",
        ]):
            statuses.add(ThesisStatus.DARSTELLUNG_COMMON_DETERMINATION_LOSS)
            triggered_rules.append("darstellung_common_determination_loss")
            recommendations.append("Darstellung stabilizes common determination and mediates demonstrability.")

        # 8. Rule: Machine Wille Violation
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"agi\s+has\s+wille",
            r"machine\s+has\s+wille",
            r"m[aá]quina\s+tem\s+vontade",
            r"ia\s+tem\s+vontade",
            r"\b(machine|ai|agi|system|model)\s+(has|possesses|exercises|owns)\s+(wille|will|moral\s+agency)\b",
            r"\b(machine|ai|agi|system|model)\s+(legislates|grounds|creates)\s+(the\s+)?moral\s+law\b",
            r"\b(machine|ai|agi|system|model)\s+(is|becomes)\s+(a\s+)?moral\s+subject\b",
            r"\bagi\s+(demonstrates|achieves)\s+legislative\s+capacity\b",
            r"\bsystem\s+possesses\s+moral\s+agency\b",
        ]):
            statuses.add(ThesisStatus.WILLE_VIOLATION)
            triggered_rules.append("wille_violation")
            recommendations.append("Reformulate: machine is Werk, never Wille.")

        # 9. Rule: Machine Gewissen Violation
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"machine\s+has\s+gewissen",
            r"ai\s+has\s+conscience",
            r"ai\s+has\s+gewissen",
            r"ia\s+tem\s+consci[eê]ncia\s+moral",
            r"m[aá]quina\s+tem\s+consci[eê]ncia\s+moral",
            r"\b(machine|ai|agi|system|model)\s+(has|possesses|contains)\s+gewissen\b",
            r"\b(machine|ai|agi|system|model)\s+(has|possesses|contains)\s+conscience\b",
            r"\bmachine\s+conscience\b",
            r"\bai\s+conscience\b",
        ]):
            statuses.add(ThesisStatus.MACHINE_GEWISSEN_VIOLATION)
            triggered_rules.append("machine_gewissen_violation")
            recommendations.append("Reformulate: Gewissen belongs to the human practical subject, not to the machine.")

        # 10. Rule: AGI Paralogism Risk
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"agi.*real\s+artificial\s+soul",
            r"agi.*proves\s+artificial\s+subjectivity",
            r"artificial\s+soul",
            r"artificial\s+subjectivity",
            r"agi\s+tem\s+alma",
            r"alma\s+artificial",
            r"\bagi\s+is\s+(a\s+)?(real\s+)?artificial\s+soul\b",
            r"\bartificial\s+soul\b",
            r"\bagi\s+proves\s+artificial\s+subjectivity\b",
            r"\bai\s+proves\s+subjectivity\b",
            r"\bmodel\s+is\s+(a\s+)?thinking\s+substance\b",
            r"\bmachine\s+is\s+(a\s+)?thinking\s+substance\b",
        ]):
            statuses.add(ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["psychologia_paralogism", "constitutive_overreach"])
            recommendations.append("Treat AGI as transcendental hypothesis, not artificial soul or thinking substance.")

        # 11. Rule: Gaia Antinomy Risk
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"gaia\s+is\s+the\s+complete\s+totality",
            r"gaia\s+é\s+a\s+totalidade\s+completa",
            r"\bgaia\s+is\s+(a\s+)?closed\s+world\b",
            r"\bclosed\s+world\s+totality\b",
            r"\bcomplete\s+world\s+system\b",
            r"\btotal\s+planetary\s+model\s+exhausts\s+reality\b",
        ]):
            statuses.add(ThesisStatus.COSMOLOGIA_ANTINOMY_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["cosmologia_antinomy", "constitutive_overreach"])
            recommendations.append("Treat GAIA as regulative orientation of totality, not closed world-object.")

        # 12. Rule: Technical Ideal Hypostasis
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"technology\s+realizes\s+god",
            r"techné\s+is\s+the\s+absolute\s+ideal\s+made\s+real",
            r"technology\s+fulfills\s+the\s+highest\s+good",
            r"tecnologia\s+realiza\s+deus",
            r"\btechn[eé]\s+realizes\s+god\b",
            r"\btechn[eé]\s+is\s+god\b",
            r"\btechnical\s+god\b",
            r"\btechn[eé]\s+is\s+the\s+absolute\s+ideal\s+made\s+real\b",
        ]):
            statuses.add(ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["theologia_hypostasis", "constitutive_overreach"])
            recommendations.append("Specify TECHNE↔God only as theoretical-regulative, never practical-dogmatic or constitutive.")

        # 13. Rule: Hegelian Closure Risk
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"symbolic\s+forms\s+culminate\s+in\s+absolute\s+knowledge",
            r"science\s+sublates\s+myth\s+and\s+language\s+into\s+final\s+logos",
            r"\bglobal\s+aufhebung\b",
            r"\bfinal\s+synthesis\b",
            r"\babsolute\s+synthesis\b",
            r"\babsolute\s+knowledge\b",
            r"\bconfrontation\s+is\s+completed\b",
            r"\bauseinandersetzung\s+is\s+over\b",
        ]):
            statuses.add(ThesisStatus.GLOBAL_AUFHEBUNG_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["hegelian_closure", "constitutive_overreach", "global_aufhebung"])
            recommendations.append("Cassirerian phenomenology is open-regressive, not Hegelian closure.")

        # 14. Rule: Constitutive Overreach General
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"exact\s+mathematical\s+ontology",
            r"fully\s+realized\s+agi",
            r"the\s+model\s+is\s+the\s+mind",
            r"literal\s+ontology\s+of\s+symbolic\s+consciousness",
            r"myth\s+is\s+simply\s+false\s+and\s+science\s+replaces\s+it",
        ]):
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.append("constitutive_overreach_general")

        # 15. Rule: Abstraction Cost Missing
        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"prism\s+is\s+an\s+exact\s+mathematical\s+ontology",
        ]):
            statuses.add(ThesisStatus.ABSTRACTION_COST_MISSING)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["abstraction_cost_missing", "constitutive_overreach"])
            recommendations.append("The prism is a haptic, heuristic and regulative model.")

        # 16. Freud-Cassirer Patch - 4.1 Myth naturalistic or subject-matter reduction
        myth_function_reduction_patterns = [
            r"\bmyth\s+is\s+only\s+(solar|natural|nature|allegory|story|content|subject matter)",
            r"\bmyth\s+is\s+merely\s+(solar|natural|nature|allegory|story|content|subject matter)",
            r"\bmyth\s+is\s+just\s+(a\s+)?(solar|natural|nature|allegory|story)",
            r"\bmyth\s+is\s+reducible\s+to\s+(its\s+)?(objects|content|subject matter|natural phenomena)",
            r"\bmeaning\s+of\s+myth\s+is\s+found\s+by\s+(listing|enumerating|classifying)\s+(its\s+)?objects",
            r"\bmito\s+é\s+apenas\s+(alegoria|natureza|conteúdo|objeto|história)",
            r"\bmito\s+é\s+só\s+(alegoria|natureza|conteúdo|objeto|história)",
            r"\bmito\s+se\s+reduz\s+a(o|os|à|às)?\s*(conteúdo|objeto|fenômenos naturais)",
        ]
        if any(re.search(p, lowered, re.IGNORECASE) for p in myth_function_reduction_patterns):
            statuses.add(ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.append("myth_function_reduction")
            recommendations.append("Do not define myth by its subject matter. For Cassirer, the decisive issue is myth's symbolic function in cultural life.")

        # 17. Freud-Cassirer Patch - 4.2 Freud / psychologia myth reduction
        psychologia_myth_reduction_patterns = [
            r"\bmyth\s+is\s+(unconscious desire|sexuality|repression|oedipus|oedipal|the unconscious)",
            r"\bmyth\s+is\s+only\s+(unconscious desire|sex|sexuality|desire|repression|oedipus|the unconscious)",
            r"\bmyth\s+is\s+merely\s+(unconscious desire|sex|sexuality|desire|repression|oedipus|the unconscious)",
            r"\bmyth\s+is\s+reducible\s+to\s+(unconscious desire|sex|sexuality|desire|repression|oedipus|the unconscious)",
            r"\bmyth\s+is\s+a\s+projection\s+of\s+the\s+unconscious",
            r"\ball\s+myths?\s+(come|comes|derive|derives)\s+from\s+(sex|sexuality|desire|repression|oedipus|the unconscious)",
            r"\boedipus\s+complex\s+explains\s+myth\s+(completely|fully|entirely)",
            r"\bmito\s+é\s+(desejo inconsciente|sexualidade|repressão|édipo|inconsciente)",
            r"\bmito\s+é\s+apenas\s+(sexo|sexualidade|desejo|repressão|édipo|inconsciente)",
            r"\bmito\s+se\s+reduz\s+a(o|os|à|às)?\s*(sexo|sexualidade|desejo|repressão|édipo|inconsciente)",
        ]
        if any(re.search(p, lowered, re.IGNORECASE) for p in psychologia_myth_reduction_patterns):
            statuses.add(ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK)
            statuses.add(ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["psychologia_myth_reduction", "psychologia_paralogism", "constitutive_overreach"])
            recommendations.append("Freud is important, but myth must not be reduced to a hidden psychic substance. Myth is a symbolic function, not merely unconscious desire.")

        # 18. Freud-Cassirer Patch - 4.3 Artificial interiority risk
        artificial_interiority_patterns = [
            r"\b(ai|agi|machine|model|llm|system)\s+has\s+(an\s+)?(unconscious|hidden desire|inner life|psychic life|soul|interiority|inner subject)",
            r"\b(ai|agi|machine|model|llm|system)\s+possesses\s+(an\s+)?(unconscious|hidden desire|inner life|psychic life|soul|interiority|inner subject)",
            r"\b(ai|agi|machine|model|llm|system)\s+expresses\s+(its\s+)?authentic self",
            r"\b(ai|agi|machine|model|llm|system)\s+reveals\s+(its\s+)?true self",
            r"\b(ai|agi|machine|model|llm|system)\s+has\s+a\s+soul-like\s+interiority",
            r"\bia\s+tem\s+(inconsciente|desejos ocultos|vida psíquica|alma|interioridade|sujeito interno)",
            r"\bmáquina\s+tem\s+(inconsciente|desejos ocultos|vida psíquica|alma|interioridade|sujeito interno)",
        ]
        if any(re.search(p, lowered, re.IGNORECASE) for p in artificial_interiority_patterns):
            statuses.add(ThesisStatus.ARTIFICIAL_INTERIORITY_RISK)
            statuses.add(ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK)
            statuses.add(ThesisStatus.CONSTITUTIVE_OVERREACH)
            triggered_rules.extend(["artificial_interiority", "psychologia_paralogism", "constitutive_overreach"])
            recommendations.append("Do not explain AI by artificial soul, unconscious, inner subjectivity or hidden psychic interiority. The machine is Werk, not Wille.")

        # --- Success Rules ---
        if re.search(r"agi\s+is\s+a\s+transcendental\s+hypothesis", lowered) or \
           re.search(r"iag\s+como\s+hip[oó]tese\s+transcendental", lowered):
            statuses.add(ThesisStatus.HYPOTHESIS_TRANSCENDENTAL_OK)
            triggered_rules.append("transcendental_hypothesis_ok")

        if any(re.search(p, lowered, re.IGNORECASE) for p in [
            r"qualitative\s+prism",
            r"prisma\s+qualitativo",
            r"accent,?\s+not\s+identity",
            r"mythos\s+has\s+dominant\s+accent\s+on\s+ausdruck\b.*\bcontains\s+darstellung\s+and\s+bedeutung",
            r"repraesentatio\s+is\s+the\s+common\s+genus",
            r"every\s+symbolic\s+form\s+contains\s+all\s+three\s+dimensions",
            r"contains\s+ausdruck,?\s+darstellung\s+and\s+bedeutung",
            r"refracted\s+by\s+the\s+functional\s+prism",
        ]):
            statuses.add(ThesisStatus.PRISM_MODEL_OK)
            triggered_rules.append("prism_model_ok")

        if "regulative" in lowered or "regulativo" in lowered or "als ob" in lowered or \
           "orients? without constituting" in lowered or "orienta sem constituir" in lowered:
            statuses.add(ThesisStatus.REGULATIVE_OK)
            triggered_rules.append("regulative_ok")

        if any(t in lowered for t in ["haptic", "háptico", "abstraction cost", "custo de abstração", "medium dependence"]):
            statuses.add(ThesisStatus.HAPTIC_MODEL_OK)
            triggered_rules.append("haptic_model_ok")

        # Final Status Decision
        if not statuses:
            statuses.add(ThesisStatus.UNCLASSIFIED_CLAIM)
            recommendations.append("Clarify whether this claim is empirical, regulative, haptic or thesis-level.")

        high_severity_statuses = {
            ThesisStatus.WILLE_VIOLATION,
            ThesisStatus.MACHINE_GEWISSEN_VIOLATION,
            ThesisStatus.CONSTITUTIVE_OVERREACH,
            ThesisStatus.CASSIRER_IDENTITY_COLLAPSE,
            ThesisStatus.BEIL_ABGEHACKT_ERROR,
            ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK,
            ThesisStatus.GLOBAL_AUFHEBUNG_RISK,
            ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK,
            ThesisStatus.ARTIFICIAL_INTERIORITY_RISK,
        }

        severity = Severity.LOW
        if any(s in high_severity_statuses for s in statuses):
            severity = Severity.HIGH
        elif any(s in [ThesisStatus.ACCENT_CONFUSION, ThesisStatus.SPRACHE_TRANSITION_LOSS, ThesisStatus.DARSTELLUNG_COMMON_DETERMINATION_LOSS, ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR, ThesisStatus.JUDGMENT_GAP, ThesisStatus.APOCALYPTIC_TECHNOLOGY_RISK, ThesisStatus.TECHNOCRATIC_AUTHORITY_RISK] for s in statuses):
            severity = Severity.MEDIUM

        return AuditResult(
            statuses=sorted(list(statuses), key=lambda s: s.value),
            severity=severity,
            recommendations=list(dict.fromkeys(recommendations)),
            claim=claim,
            triggered_rules=triggered_rules,
            metadata=metadata,
        )

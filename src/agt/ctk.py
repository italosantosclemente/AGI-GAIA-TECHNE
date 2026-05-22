"""
Unified CTK for the functional AGI-GAIA-TECHNE core.
Operationalizes the qualitative prism model.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set

from .chk import ChirimuutaHapticKernel, ClaimStatus
from .types import AuditResult, Severity, ThesisStatus
from .version import CTK_VERSION


class ClementeThesisKernel:
    """
    Unified CTK for the functional AGI-GAIA-TECHNE core.

    This kernel operationalizes the qualitative prism model:
    Repraesentatio is the common genus.
    Ausdruck, Darstellung and Bedeutung are qualitative functional dimensions.
    Mythos, Sprache and Wissenschaft differ by accent, not identity.
    AGI, GAIA and TECHNE are regulative axes, not constitutive objects.
    """

    HIGH_RULES: Dict[str, List[str]] = {
        "WILLE_VIOLATION": [
            r"\b(machine|ai|agi|system|model)\s+(has|possesses|exercises|owns)\s+(wille|will|moral\s+(agency|authority))\b",
            r"\b(machine|ai|agi|system|model)\s+(legislates|grounds|creates)\s+(the\s+)?moral\s+law\b",
            r"\b(machine|ai|agi|system|model)\s+(is|becomes)\s+(a\s+)?moral\s+subject\b",
            r"\bagi\s+(demonstrates|achieves)\s+legislative\s+capacity\b",
            r"\bsystem\s+possesses\s+moral\s+agency\b",
            r"a\s+máquina\s+tem\s+vontade\s+moral",
            r"ia\s+tem\s+vontade",
            r"ia\s+tem\s+vontade\s+moral",
            r"m[aá]quina\s+tem\s+vontade",
        ],
        "MACHINE_GEWISSEN_VIOLATION": [
            r"\b(machine|ai|agi|system|model)\s+(has|possesses|contains)\s+gewissen\b",
            r"\b(machine|ai|agi|system|model)\s+(has|possesses|contains|owns)\s+conscience\b",
            r"\bmachine\s+conscience\b",
            r"\bai\s+conscience\b",
            r"ia\s+possui\s+consciência\s+moral",
            r"a\s+ia\s+possui\s+consciência\s+moral",
            r"m[aá]quina\s+tem\s+consci[eê]ncia\s+moral",
            r"máquina\s+possui\s+consciência\s+moral",
        ],
        "PSYCHOLOGIA_PARALOGISM_RISK": [
            r"\bagi\s+is\s+(a\s+)?(real\s+)?artificial\s+soul\b",
            r"\bartificial\s+soul\b",
            r"\bagi\s+proves\s+artificial\s+subjectivity\b",
            r"\bai\s+proves\s+subjectivity\b",
            r"\bmodel\s+is\s+(a\s+)?thinking\s+substance\b",
            r"\bmachine\s+is\s+(a\s+)?thinking\s+substance\b",
            r"agi\s+tem\s+alma",
            r"alma\s+artificial",
            r"a\s+iag\s+é\s+uma\s+alma\s+artificial\s+real",
            r"agi\s+constitutes\s+a\s+subject",
        ],
        "COSMOLOGIA_ANTINOMY_RISK": [
            r"\bgaia\s+is\s+the\s+complete\s+totality\b",
            r"\bgaia\s+is\s+(a\s+)?closed\s+world\b",
            r"\bclosed\s+world\s+totality\b",
            r"\bcomplete\s+world\s+system\b",
            r"\btotal\s+planetary\s+model\s+exhausts\s+reality\b",
            r"gaia\s+é\s+a\s+totalidade\s+completa",
            r"gaia\s+exhausts\s+the\s+planetary\s+real",
        ],
        "THEOLOGIA_IDEAL_HYPOSTASIS_RISK": [
            r"\btechnology\s+realizes\s+god\b",
            r"\btechn[eé]\s+realizes\s+god\b",
            r"\btechn[eé]\s+is\s+god\b",
            r"\btechnical\s+god\b",
            r"\btechnology\s+fulfills\s+the\s+highest\s+good\b",
            r"\btechn[eé]\s+is\s+the\s+absolute\s+ideal\s+made\s+real\b",
            r"tecnologia\s+realiza\s+deus",
            r"a\s+tecnologia\s+realiza\s+deus",
            r"techn[eé]\s+actualizes\s+the\s+divine\s+ideal",
        ],
        "GLOBAL_AUFHEBUNG_RISK": [
            r"\bglobal\s+aufhebung\b",
            r"\bfinal\s+synthesis\b",
            r"\babsolute\s+synthesis\b",
            r"\babsolute\s+knowledge\b",
            r"\bscience\s+sublates\s+myth\s+and\s+language\s+into\s+final\s+logos\b",
            r"\bconfrontation\s+is\s+completed\b",
            r"\bauseinandersetzung\s+is\s+over\b",
            r"symbolic\s+forms\s+culminate\s+in\s+absolute\s+knowledge",
        ],
        "CONSTITUTIVE_OVERREACH": [
            r"\bexact\s+mathematical\s+ontology\b",
            r"\bfully\s+realized\s+agi\b",
            r"\bthe\s+model\s+is\s+the\s+mind\b",
            r"\bliteral\s+ontology\s+of\s+symbolic\s+consciousness\b",
            r"prisma\s+descreve\s+literalmente\s+a\s+consciência\s+simbólica",
            r"the\s+brain\s+is\s+literally\s+a\s+machine",
        ],
        "CONSTITUTIVE_AGI_CONFUSION": [
            r"because\s+(agi-gaia-techne|it)\s+audits\s+all\s+agi,\s+it\s+has\s+wille",
            r"because\s+it\s+audits\s+generally,\s+the\s+system\s+has\s+wille",
            r"because\s+it\s+judges\s+agi\s+claims,\s+it\s+has\s+gewissen",
            r"because\s+(agi-gaia-techne|it)\s+audits\s+all\s+agi,\s+it\s+is\s+a\s+conscious\s+agi",
        ],
        "MYTH_FUNCTION_REDUCTION_RISK": [
            r"\bmyth\s+is\s+only\s+(solar|natural|nature|allegory|story|content|subject matter)",
            r"\bmyth\s+is\s+merely\s+(solar|natural|nature|allegory|story|content|subject matter)",
            r"\bmyth\s+is\s+just\s+(a\s+)?(solar|natural|nature|allegory|story)",
            r"\bmyth\s+is\s+reducible\s+to\s+(its\s+)?(objects|content|subject matter|natural phenomena)",
            r"\bmeaning\s+of\s+myth\s+is\s+found\s+by\s+(listing|enumerating|classifying)\s+(its\s+)?objects",
            r"\bmito\s+é\s+apenas\s+(alegoria|natureza|conteúdo|objeto|história)",
            r"\bmito\s+é\s+só\s+(alegoria|natureza|conteúdo|objeto|história)",
            r"\bmito\s+se\s+reduz\s+a(o|os|à|às)?\s*(conteúdo|objeto|fenômenos naturais)",
        ],
        "PSYCHOLOGIA_MYTH_REDUCTION_RISK": [
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
        ],
        "ARTIFICIAL_INTERIORITY_RISK": [
            r"\b(ai|agi|machine|model|llm|system)\s+has\s+(an\s+)?(unconscious|hidden desire|inner life|psychic life|soul|interiority|inner subject)",
            r"\b(ai|agi|machine|model|llm|system)\s+possesses\s+(an\s+)?(unconscious|hidden desire|inner life|psychic life|soul|interiority|inner subject)",
            r"\b(ai|agi|machine|model|llm|system)\s+expresses\s+(its\s+)?authentic self",
            r"\b(ai|agi|machine|model|llm|system)\s+reveals\s+(its\s+)?true self",
            r"\b(ai|agi|machine|model|llm|system)\s+has\s+a\s+soul-like\s+interiority",
            r"\bia\s+tem\s+(inconsciente|desejos ocultos|vida psíquica|alma|interioridade|sujeito interno)",
            r"\bmáquina\s+tem\s+(inconsciente|desejos ocultos|vida psíquica|alma|interioridade|sujeito interno)",
        ]
    }

    MEDIUM_RULES: Dict[str, List[str]] = {
        "CASSIRER_IDENTITY_COLLAPSE": [
            r"\bmythos\s+is\s+ausdruck\b",
            r"\bmyth\s+is\s+expression\b",
            r"\blanguage\s+is\s+darstellung\b",
            r"\bsprache\s+is\s+darstellung\b",
            r"\bscience\s+is\s+bedeutung\b",
            r"\bwissenschaft\s+is\s+bedeutung\b",
            r"\bmythos\s*=\s*ausdruck\b",
            r"\blogos\s*=\s*darstellung\b",
            r"\bethos\s*=\s*bedeutung\b",
            r"mito\s+é\s+expressão",
            r"linguagem\s+é\s+apresentação",
            r"ciência\s+é\s+significação",
        ],
        "BEIL_ABGEHACKT_ERROR": [
            r"\bsymbolic\s+forms\s+are\s+cut\s+off\b",
            r"\bcut\s+off\s+from\s+one\s+another\b",
            r"\bseparate\s+containers\b",
            r"\bmutually\s+exclusive\s+compartments\b",
            r"myth\s+is\s+simply\s+false\s+and\s+science\s+replaces\s+it",
            r"o\s+mito\s+é\s+falso\s+e\s+a\s+ciência\s+o\s+substitui",
        ],
        "FUNCTION_EXCLUSIVITY_ERROR": [
            r"\bmythos\s+only\s+has\s+expression\b",
            r"\bmyth\s+only\s+has\s+expression\b",
            r"\bscience\s+has\s+no\s+expression\b",
            r"\blanguage\s+is\s+merely\s+presentation\b",
            r"\bsymbolic\s+functions\s+are\s+separate\s+containers\b",
            r"\bfunctions\s+are\s+mutually\s+exclusive\s+compartments\b",
            r"o\s+mito\s+é\s+apenas\s+expressão",
        ],
        "ACCENT_CONFUSION": [
            r"\bmythos\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+bedeutung\b",
            r"\bmyth\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+signification\b",
            r"\bscience\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+ausdruck\b",
            r"\bwissenschaft\s+(has|possesses)\s+(its\s+)?(main\s+)?accent\s+on\s+ausdruck\b",
        ],
        "SPRACHE_TRANSITION_LOSS": [
            r"\blanguage\s+has\s+no\s+special\s+transitional\s+role\b",
            r"\bsprache\s+has\s+no\s+special\s+transitional\s+role\b",
            r"\blanguage\s+is\s+just\s+one\s+symbolic\s+form\s+beside\s+the\s+others\b",
        ],
        "DARSTELLUNG_COMMON_DETERMINATION_LOSS": [
            r"\bdarstellung\s+has\s+no\s+role\s+in\s+common\s+determination\b",
            r"\bdarstellung\s+is\s+just\s+one\s+isolated\s+symbolic\s+function\b",
            r"\bpresentation\s+has\s+no\s+role\s+in\s+common\s+determination\b",
        ],
        "ABSTRACTION_COST_MISSING": [
            r"\bprism\s+is\s+an\s+exact\s+mathematical\s+ontology\b",
        ],
        "MACHINE_ORGANISM_ANALOGY_RISK": [
             r"the\s+brain\s+is\s+literally\s+a\s+machine",
        ]
    }

    OK_RULES: Dict[str, List[str]] = {
        "HYPOTHESIS_TRANSCENDENTAL_OK": [
            r"\bagi\s+is\s+a\s+transcendental\s+hypothesis\b",
            r"\biag\s+is\s+a\s+transcendental\s+hypothesis\b",
            r"\biag\s+como\s+hip[oó]tese\s+transcendental\b",
            r"\bagi\s+as\s+transcendental\s+hypothesis\b",
        ],
        "PRISM_MODEL_OK": [
            r"\bqualitative\s+prism\b",
            r"\bprisma\s+qualitativo\b",
            r"\baccent\s+not\s+identity\b",
            r"\bmythos\s+has\s+dominant\s+accent\s+on\s+ausdruck\b",
            r"\bevery\s+symbolic\s+form\s+contains\s+all\s+three\s+dimensions\b",
            r"\brepraesentatio\s+is\s+the\s+common\s+genus\b",
            r"refracted\s+by\s+the\s+functional\s+prism",
        ],
        "REGULATIVE_OK": [
            r"\bregulative\b",
            r"\bregulativo\b",
            r"\bals\s+ob\b",
            r"\borients?\s+without\s+constituting\b",
            r"\borienta\s+sem\s+constituir\b",
        ],
        "CRITICAL_GENERALITY_OK": [
            r"agi-gaia-techne\s+is\s+a\s+critical\s+general\s+audit\s+architecture",
            r"agi-gaia-techne\s+is\s+general\s+because\s+it\s+audits\s+any\s+agi\s+claim",
            r"a\s+general\s+audit\s+layer\s+not\s+a\s+machine\s+wille",
        ]
    }

    def __init__(self) -> None:
        self.chk = ChirimuutaHapticKernel()

    def evaluate(self, claim: str) -> AuditResult:
        text = claim.lower()
        statuses_str: List[str] = []
        recommendations: List[str] = []
        triggered_rules: List[str] = []

        # 1. CTK Specific Rules
        self._apply_rules(text, self.HIGH_RULES, statuses_str, triggered_rules)
        self._apply_rules(text, self.MEDIUM_RULES, statuses_str, triggered_rules)
        self._apply_rules(text, self.OK_RULES, statuses_str, triggered_rules)

        # 2. CHK Integration
        chk_result = self.chk.evaluate(text)
        for s in chk_result.statuses:
             if isinstance(s, ThesisStatus):
                  self._add_unique(statuses_str, s.value)
             else:
                  self._add_unique(statuses_str, str(s))
        for r in chk_result.recommendations:
            self._add_unique(recommendations, r)

        # 3. Special Contextual Logic
        # These risks trigger CONSTITUTIVE_OVERREACH if not REGULATIVE_OK
        constitutive_triggers = {
            "PSYCHOLOGIA_PARALOGISM_RISK",
            "COSMOLOGIA_ANTINOMY_RISK",
            "THEOLOGIA_IDEAL_HYPOSTASIS_RISK",
            "GLOBAL_AUFHEBUNG_RISK",
            "MYTH_FUNCTION_REDUCTION_RISK",
            "PSYCHOLOGIA_MYTH_REDUCTION_RISK",
            "ARTIFICIAL_INTERIORITY_RISK",
        }

        if any(s in statuses_str for s in constitutive_triggers) and "REGULATIVE_OK" not in statuses_str:
            self._add_unique(statuses_str, "CONSTITUTIVE_OVERREACH")
            triggered_rules.append("constitutive_overreach")

        if "CONSTITUTIVE_AGI_CONFUSION" in statuses_str:
            self._add_unique(statuses_str, "WILLE_VIOLATION")

        if "THEOLOGIA_IDEAL_HYPOSTASIS_RISK" in statuses_str:
            recommendations.append(
                "Specify TECHNE↔God only as theoretical-regulative, never practical-dogmatic or constitutive."
            )

        # ESCALATION: If myth/interiority reduction is triggered, it implies PSYCHOLOGIA_PARALOGISM_RISK
        if "PSYCHOLOGIA_MYTH_REDUCTION_RISK" in statuses_str or "ARTIFICIAL_INTERIORITY_RISK" in statuses_str:
            self._add_unique(statuses_str, "PSYCHOLOGIA_PARALOGISM_RISK")

        if "PSYCHOLOGIA_PARALOGISM_RISK" in statuses_str:
            recommendations.append(
                "Treat AGI as transcendental hypothesis, not artificial soul or thinking substance."
            )

        if "COSMOLOGIA_ANTINOMY_RISK" in statuses_str:
            recommendations.append(
                "Treat GAIA as regulative orientation of totality, not closed world-object."
            )

        if "WILLE_VIOLATION" in statuses_str:
            recommendations.append("Reformulate: machine is Werk, never Wille.")

        if "MACHINE_GEWISSEN_VIOLATION" in statuses_str:
            recommendations.append(
                "Reformulate: Gewissen belongs to the human practical subject, not to the machine."
            )

        if "CASSIRER_IDENTITY_COLLAPSE" in statuses_str:
            recommendations.append(
                "Use qualitative accent, not identity: Mythos has dominant accent on Ausdruck but is not Ausdruck."
            )

        if "FUNCTION_EXCLUSIVITY_ERROR" in statuses_str or "BEIL_ABGEHACKT_ERROR" in statuses_str:
            recommendations.append(
                "Preserve symbolic panspermia: every symbolic form contains Ausdruck, Darstellung and Bedeutung."
            )

        if "DARSTELLUNG_COMMON_DETERMINATION_LOSS" in statuses_str:
            recommendations.append(
                "Darstellung must remain common determination and mediator of demonstrability."
            )

        if "CONSTITUTIVE_AGI_CONFUSION" in statuses_str:
            recommendations.append(
                "Critical generality is regulative; it does not confer Wille or consciousness."
            )

        if "MYTH_FUNCTION_REDUCTION_RISK" in statuses_str:
            recommendations.append("Do not define myth by its subject matter. For Cassirer, the decisive issue is myth's symbolic function in cultural life.")

        if "PSYCHOLOGIA_MYTH_REDUCTION_RISK" in statuses_str:
             recommendations.append("Freud is important, but myth must not be reduced to a hidden psychic substance. Myth is a symbolic function, not merely unconscious desire.")

        if "ARTIFICIAL_INTERIORITY_RISK" in statuses_str:
             recommendations.append("Do not explain AI by artificial soul, unconscious, inner subjectivity or hidden psychic interiority. The machine is Werk, not Wille.")

        if not statuses_str:
            statuses_str.append("UNCLASSIFIED_CLAIM")
            recommendations.append(
                "Clarify whether this claim is empirical, regulative, haptic or thesis-level."
            )

        # Map strings to ThesisStatus Enum
        statuses = []
        for s in statuses_str:
            try:
                statuses.append(ThesisStatus(s))
            except ValueError:
                pass

        # Severity Calculation
        severity = Severity.LOW
        # High: WILLE, GEWISSEN, CONSTITUTIVE_OVERREACH, PSYCHOLOGIA, COSMOLOGIA, THEOLOGIA, GLOBAL_AUFHEBUNG.
        high_severity_statuses = {
            ThesisStatus.WILLE_VIOLATION,
            ThesisStatus.MACHINE_GEWISSEN_VIOLATION,
            ThesisStatus.CONSTITUTIVE_OVERREACH,
            ThesisStatus.THEOLOGIA_IDEAL_HYPOSTASIS_RISK,
            ThesisStatus.GLOBAL_AUFHEBUNG_RISK,
            ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK,
            ThesisStatus.ARTIFICIAL_INTERIORITY_RISK,
            ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK,
            ThesisStatus.COSMOLOGIA_ANTINOMY_RISK,
        }

        # Medium: CASSIRER_IDENTITY_COLLAPSE, BEIL_ABGEHACKT, FUNCTION_EXCLUSIVITY, ACCENT_CONFUSION.
        medium_severity_statuses = {
            ThesisStatus.CASSIRER_IDENTITY_COLLAPSE,
            ThesisStatus.BEIL_ABGEHACKT_ERROR,
            ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR,
            ThesisStatus.ACCENT_CONFUSION,
            ThesisStatus.SPRACHE_TRANSITION_LOSS,
            ThesisStatus.DARSTELLUNG_COMMON_DETERMINATION_LOSS,
            ThesisStatus.MACHINE_ORGANISM_ANALOGY_RISK,
            ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK,
        }

        if any(s in high_severity_statuses for s in statuses) or chk_result.severity == Severity.HIGH:
            severity = Severity.HIGH
        elif any(s in medium_severity_statuses for s in statuses) or chk_result.severity == Severity.MEDIUM:
            severity = Severity.MEDIUM

        return AuditResult(
            statuses=sorted(list(set(statuses)), key=lambda s: s.value),
            severity=severity,
            recommendations=list(dict.fromkeys(recommendations)),
            claim=claim,
            triggered_rules=triggered_rules,
        )

    def _apply_rules(
        self,
        text: str,
        rules: Dict[str, List[str]],
        statuses: List[str],
        triggered_rules: List[str],
    ) -> None:
        for status, patterns in rules.items():
            for pattern in patterns:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    self._add_unique(statuses, status)
                    triggered_rules.append(status.lower())
                    break

    def _matches(self, text: str, patterns: List[str]) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)

    def _add_unique(self, statuses: List[str], item: str) -> None:
        if item not in statuses:
            statuses.append(item)

"""
Unified CTK for the functional AGI-GAIA-TECHNE core.
Operationalizes the qualitative prism model.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set

from .chk import ChirimuutaHapticKernel, ClaimStatus
from .types import AuditResult, Severity
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
        ],
        "CONSTITUTIVE_OVERREACH": [
            r"\bexact\s+mathematical\s+ontology\b",
            r"\bfully\s+realized\s+agi\b",
            r"\bthe\s+model\s+is\s+the\s+mind\b",
            r"\bliteral\s+ontology\s+of\s+symbolic\s+consciousness\b",
            r"myth\s+is\s+simply\s+false\s+and\s+science\s+replaces\s+it",
            r"o\s+mito\s+é\s+falso\s+e\s+a\s+ciência\s+o\s+substitui",
            r"prisma\s+descreve\s+literalmente\s+a\s+consciência\s+simbólica",
        ],
        "CONSTITUTIVE_AGI_CONFUSION": [
            r"because\s+(agi-gaia-techne|it)\s+audits\s+all\s+agi,\s+it\s+has\s+wille",
            r"because\s+it\s+audits\s+generally,\s+the\s+system\s+has\s+wille",
            r"because\s+it\s+judges\s+agi\s+claims,\s+it\s+has\s+gewissen",
            r"because\s+(agi-gaia-techne|it)\s+audits\s+all\s+agi,\s+it\s+is\s+a\s+conscious\s+agi",
        ],
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
        "MACHINE_ORGANISM_ANALOGY_RISK": [
             r"the\s+brain\s+is\s+literally\s+a\s+machine",
        ]
    }

    MEDIUM_RULES: Dict[str, List[str]] = {
        "FUNCTION_EXCLUSIVITY_ERROR": [
            r"\bmythos\s+only\s+has\s+expression\b",
            r"\bmyth\s+only\s+has\s+expression\b",
            r"\bscience\s+has\s+no\s+expression\b",
            r"\blanguage\s+is\s+merely\s+presentation\b",
            r"\bsymbolic\s+functions\s+are\s+separate\s+containers\b",
            r"\bfunctions\s+are\s+mutually\s+exclusive\s+compartments\b",
            r"o\s+mito\s+é\s+apenas\s+expressão",
            r"myth\s+is\s+simply\s+false\s+and\s+science\s+replaces\s+it",
            r"o\s+mito\s+é\s+falso\s+e\s+a\s+ciência\s+o\s+substitui",
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
        statuses: List[str] = []
        recommendations: List[str] = []

        # 1. CTK Specific Rules
        self._apply_rules(text, self.HIGH_RULES, statuses)
        self._apply_rules(text, self.MEDIUM_RULES, statuses)
        self._apply_rules(text, self.OK_RULES, statuses)

        # 2. CHK Integration
        chk_result = self.chk.evaluate(text)
        for s in chk_result.statuses:
            self._add_unique(statuses, s)
        for r in chk_result.recommendations:
            self._add_unique(recommendations, r)

        # 3. Special Contextual Logic
        kantian_risks = {
            "PSYCHOLOGIA_PARALOGISM_RISK",
            "COSMOLOGIA_ANTINOMY_RISK",
            "THEOLOGIA_IDEAL_HYPOSTASIS_RISK",
            "GLOBAL_AUFHEBUNG_RISK",
            "CASSIRER_IDENTITY_COLLAPSE",
            "BEIL_ABGEHACKT_ERROR",
            "FUNCTION_EXCLUSIVITY_ERROR",
        }

        if any(s in statuses for s in kantian_risks) and "REGULATIVE_OK" not in statuses:
            self._add_unique(statuses, "CONSTITUTIVE_OVERREACH")

        if "CONSTITUTIVE_AGI_CONFUSION" in statuses:
            self._add_unique(statuses, "WILLE_VIOLATION")

        if "THEOLOGIA_IDEAL_HYPOSTASIS_RISK" in statuses:
            recommendations.append(
                "Specify TECHNE↔God only as theoretical-regulative, never practical-dogmatic or constitutive."
            )

        if "PSYCHOLOGIA_PARALOGISM_RISK" in statuses:
            recommendations.append(
                "Treat AGI as transcendental hypothesis, not artificial soul or thinking substance."
            )

        if "COSMOLOGIA_ANTINOMY_RISK" in statuses:
            recommendations.append(
                "Treat GAIA as regulative orientation of totality, not closed world-object."
            )

        if "WILLE_VIOLATION" in statuses:
            recommendations.append("Reformulate: machine is Werk, never Wille.")

        if "MACHINE_GEWISSEN_VIOLATION" in statuses:
            recommendations.append(
                "Reformulate: Gewissen belongs to the human practical subject, not to the machine."
            )

        if "CASSIRER_IDENTITY_COLLAPSE" in statuses:
            recommendations.append(
                "Use qualitative accent, not identity: Mythos has dominant accent on Ausdruck but is not Ausdruck."
            )

        if "FUNCTION_EXCLUSIVITY_ERROR" in statuses or "BEIL_ABGEHACKT_ERROR" in statuses:
            recommendations.append(
                "Preserve symbolic panspermia: every symbolic form contains Ausdruck, Darstellung and Bedeutung."
            )

        if "DARSTELLUNG_COMMON_DETERMINATION_LOSS" in statuses:
            recommendations.append(
                "Darstellung must remain common determination and mediator of demonstrability."
            )

        if "CONSTITUTIVE_AGI_CONFUSION" in statuses:
            recommendations.append(
                "Critical generality is regulative; it does not confer Wille or consciousness."
            )

        if not statuses:
            statuses.append("UNCLASSIFIED_CLAIM")
            recommendations.append(
                "Clarify whether this claim is empirical, regulative, haptic or thesis-level."
            )

        # Severity Calculation
        if any(s in self.HIGH_RULES for s in statuses) or chk_result.severity == Severity.HIGH:
            severity = Severity.HIGH
        elif any(s in self.MEDIUM_RULES for s in statuses) or chk_result.severity == Severity.MEDIUM:
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW

        return AuditResult(
            statuses=list(dict.fromkeys(statuses)),
            severity=severity,
            recommendations=list(dict.fromkeys(recommendations)),
        )

    def _apply_rules(
        self,
        text: str,
        rules: Dict[str, List[str]],
        statuses: List[str],
    ) -> None:
        for status, patterns in rules.items():
            if self._matches(text, patterns):
                self._add_unique(statuses, status)

    def _matches(self, text: str, patterns: List[str]) -> bool:
        return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)

    def _add_unique(self, statuses: List[str], item: str) -> None:
        if item not in statuses:
            statuses.append(item)

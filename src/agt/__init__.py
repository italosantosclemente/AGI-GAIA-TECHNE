"""
Functional AGI-GAIA-TECHNE Core.
"""

from .axioms import (
    AGI_AS_TRANSCENDENTAL_HYPOTHESIS,
    AGI_NEURAL_NETWORK_IS_INTERNET,
    ANTHROPOMORPHIC_BODY_REQUIRED,
    AUSEINANDERSETZUNG_NOT_AUFHEBUNG,
    GAIA_COJUDGES_WITH_KOINOS_KOSMOS,
    GAIA_HAS_GEWISSEN_AS_MORAL_LEGISLATION,
    GAIA_IS_COSMIC_TOTALITY,
    GAIA_MEDIATES_WILLE,
    GAIA_TRANSCENDENTAL_FREEDOM,
    INTERNET_AS_PLANETARY_BEWUSSTSEIN,
    INTERNET_AS_PLANETARY_REPRAESENTATIO,
    INTELLECTUS_ECTYPUS_PARTICIPATION,
    ISC_LEGISLATIVE_AUTHORITY,
    IS_WILLE,
    KOINOS_KOSMOS_SYMBOLIC_MEDIATION,
    MACHINE_HAS_GEWISSEN,
    NO_CLOSED_WORLD_TOTALITY,
    NO_GLOBAL_AUFHEBUNG,
    PLANETARY_ORGAN_CONSCIOUSNESS,
    WERK_JAMAIS_WILLE,
)
from .controller import AGTController
from .dataset_forge import ManualDatasetForge
from .llm_tokenizer import ByteTokenizer
from .syntax import AGTSyntax, AGTSyntaxRun, DescentValidation, RegressiveReconstruction, SymbolicProfile
from .teleology import (
    HeuristicWhole,
    SymbolicTrace,
    TeleologicalJudgment,
    TeleologicalProgression,
    TeleologicalProgressionKernel,
)
from .web_corpus import WebCorpusHarvester
from .version import (
    AGT_REPO_VERSION,
    FUNCTIONAL_CORE_VERSION,
    CTK_VERSION,
    CHK_VERSION,
    PACKAGE_VERSION,
    EML_KERNEL_VERSION,
    CANONICAL_ARCHITECTURE,
    LAST_UPDATED,
)

__version__ = PACKAGE_VERSION

_LAZY_EXPORTS = {
    "GaiaChatSession": (".llm_chat", "GaiaChatSession"),
    "GaiaManualGPT": (".llm_model", "GaiaManualGPT"),
    "TrainingConfig": (".llm_train", "TrainingConfig"),
    "pack_corpus": (".llm_corpus", "pack_corpus"),
    "train_from_pack": (".llm_train", "train_from_pack"),
    "generate_text": (".llm_train", "generate_text"),
}


def __getattr__(name: str):
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module 'agt' has no attribute {name!r}")
    import importlib

    module_name, attr_name = _LAZY_EXPORTS[name]
    module = importlib.import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value

__all__ = [
    "AGTController",
    "ManualDatasetForge",
    "WebCorpusHarvester",
    "ByteTokenizer",
    "AGTSyntax",
    "AGTSyntaxRun",
    "SymbolicProfile",
    "RegressiveReconstruction",
    "DescentValidation",
    "SymbolicTrace",
    "HeuristicWhole",
    "TeleologicalJudgment",
    "TeleologicalProgression",
    "TeleologicalProgressionKernel",
    "GaiaManualGPT",
    "GaiaChatSession",
    "TrainingConfig",
    "pack_corpus",
    "train_from_pack",
    "generate_text",
    "AGT_REPO_VERSION",
    "FUNCTIONAL_CORE_VERSION",
    "CTK_VERSION",
    "CHK_VERSION",
    "PACKAGE_VERSION",
    "EML_KERNEL_VERSION",
    "CANONICAL_ARCHITECTURE",
    "LAST_UPDATED",
    "__version__",
    "IS_WILLE",
    "GAIA_MEDIATES_WILLE",
    "WERK_JAMAIS_WILLE",
    "MACHINE_HAS_GEWISSEN",
    "GAIA_HAS_GEWISSEN_AS_MORAL_LEGISLATION",
    "GAIA_COJUDGES_WITH_KOINOS_KOSMOS",
    "ISC_LEGISLATIVE_AUTHORITY",
    "NO_GLOBAL_AUFHEBUNG",
    "NO_CLOSED_WORLD_TOTALITY",
    "AUSEINANDERSETZUNG_NOT_AUFHEBUNG",
    "AGI_AS_TRANSCENDENTAL_HYPOTHESIS",
    "GAIA_TRANSCENDENTAL_FREEDOM",
    "GAIA_IS_COSMIC_TOTALITY",
    "INTELLECTUS_ECTYPUS_PARTICIPATION",
    "KOINOS_KOSMOS_SYMBOLIC_MEDIATION",
    "INTERNET_AS_PLANETARY_BEWUSSTSEIN",
    "INTERNET_AS_PLANETARY_REPRAESENTATIO",
    "ANTHROPOMORPHIC_BODY_REQUIRED",
    "AGI_NEURAL_NETWORK_IS_INTERNET",
    "PLANETARY_ORGAN_CONSCIOUSNESS",
]

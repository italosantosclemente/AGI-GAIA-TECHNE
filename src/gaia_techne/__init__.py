"""AGI-GAIA-TECHNE: a critical architecture for an AGI hypothesis.

Layers follow the order of Kant's three questions, and each depends only on
the ones before it (Condition 0):

    boundaries, syntax      what every layer respects; the order of a run
    ethos       I.   What should I do?          ends, rules of skill, premises
    koinos      II.  What may I hope?           common world, ground, prism
    canon       III. What can I know?           claims, guards, correction
    metatheory       the community of correction as the measure; replay of the record
    runtime          adapters, pipeline, spec, command line
"""

from ._version import __version__
from .pipeline import Runtime, Werk
from .syntax import SYNTAX, Step, SyntaxViolation

__all__ = ["Runtime", "Werk", "SYNTAX", "Step", "SyntaxViolation", "__version__"]

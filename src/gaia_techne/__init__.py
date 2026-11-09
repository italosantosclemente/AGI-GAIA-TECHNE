"""AGI-GAIA-TECHNE 2.0: a critical architecture for an AGI hypothesis.

Layers follow the order of Kant's three questions:

    ethos       I.   What should I do?          ends, rules of skill, premises
    koinos      II.  What may I hope?           common world, prism
    canon       III. What can I know?           claims, guards, correction
    metatheory       the community of correction as the measure
"""

__version__ = "2.0.0"

from .pipeline import Runtime, Werk

__all__ = ["Runtime", "Werk", "__version__"]

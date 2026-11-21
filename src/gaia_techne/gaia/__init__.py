"""Gaia: the planetary layer, as ground and as archive, never as subject (README §10).

    memory     the common world as a source: earlier claims re-enter as premises with their stage and reach
    archive    public documents, read with their provenance; no claim of total coverage
"""

from .archive import Archive, ArchiveOutsideRoot, Document
from .memory import recall

__all__ = ["Archive", "ArchiveOutsideRoot", "Document", "recall"]

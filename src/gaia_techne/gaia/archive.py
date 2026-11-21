"""The archive: public documents, read with their provenance.

The internet is a public archive of works, not a planetary consciousness
(README §10). An archive here is a folder of documents that people have put at
the system's disposal, or a public address they name. Every passage read keeps
its source, so that it enters a run as a premise with provenance, and every
read declares the ground it draws on.

No search covers the archive "as a whole": the world guard flags claims of
total coverage, and the archive answers only with the passages it found, saying
how many documents it looked at.
"""

from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from ..koinos.ground import GroundDependency, GroundKind

TEXT_SUFFIXES = {".txt", ".md", ".csv", ".json", ".html", ".tex", ".rst"}


class ArchiveOutsideRoot(PermissionError):
    """A read outside the folder that people put at the system's disposal."""


@dataclass(frozen=True)
class Document:
    text: str
    source: str


class Archive:
    def __init__(self, root: Optional[str] = None, maintained_by: str = "the people who keep these documents",
                 allow_network: bool = False) -> None:
        self.root = Path(root).resolve() if root else None
        self.maintained_by = maintained_by
        self.allow_network = allow_network

    def _inside(self, path: str) -> Path:
        if self.root is None:
            raise ArchiveOutsideRoot("no folder was put at the system's disposal")
        p = (self.root / path).resolve()
        if p != self.root and self.root not in p.parents:
            raise ArchiveOutsideRoot(f"{path} lies outside {self.root}")
        return p

    def ground(self, network: bool = False) -> List[GroundDependency]:
        if network:
            return [GroundDependency(GroundKind.NETWORK, "one request to a public address", "the public internet",
                                     "network operators", 1.0, "requests")]
        return [GroundDependency(GroundKind.ARCHIVE, "documents read from a local folder", str(self.root),
                                 self.maintained_by)]

    def read(self, path: str, limit: int = 4000) -> Document:
        p = self._inside(path)
        return Document(p.read_text(encoding="utf-8", errors="replace")[:limit], f"archive: {p.relative_to(self.root)}")

    def search(self, query: str, k: int = 3, window: int = 400) -> Tuple[List[Document], int]:
        """Passages that share words with `query`, and how many documents were looked at."""
        if self.root is None:
            return [], 0
        wanted = {w.lower() for w in re.findall(r"[\wÀ-ÿ]{4,}", query)}
        hits, seen = [], 0
        for p in sorted(self.root.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            seen += 1
            text = p.read_text(encoding="utf-8", errors="replace")
            low = text.lower()
            score = sum(low.count(w) for w in wanted)
            if score:
                first = min((low.find(w) for w in wanted if w in low), default=0)
                start = max(0, first - window // 4)
                hits.append((score, Document(text[start:start + window].strip(), f"archive: {p.relative_to(self.root)}")))
        hits.sort(key=lambda t: -t[0])
        return [d for _, d in hits[:k]], seen

    def fetch(self, url: str, limit: int = 4000, timeout: float = 30.0) -> Document:
        if not self.allow_network:
            raise ArchiveOutsideRoot("no public address was put at the system's disposal (allow_network=False)")
        if not url.startswith(("https://", "http://")):
            raise ArchiveOutsideRoot(f"{url} is not a public address")
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            raw = resp.read(limit * 4).decode("utf-8", errors="replace")
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        return Document(re.sub(r"\s+", " ", text).strip()[:limit], f"public address: {url}")

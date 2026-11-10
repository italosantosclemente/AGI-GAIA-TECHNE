from __future__ import annotations

import html
import ipaddress
import socket
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Dict, Iterable, List, Optional
from urllib.parse import urlparse

from .memory import ObservationRecord, SQLiteMemoryStore
from .planetary_model import LearningResult, PlanetarySymbolicModel


@dataclass(frozen=True)
class IngestionResult:
    ok: bool
    url: str
    observation: Optional[ObservationRecord]
    learning: Optional[LearningResult]
    bytes_read: int
    error: Optional[str] = None


class InternetIngestor:
    """
    Live internet ingestion into planetary memory.

    The ingestor turns a URL into a durable observation and trains the local
    symbolic model on the extracted text.
    """

    def __init__(
        self,
        memory: SQLiteMemoryStore,
        model: Optional[PlanetarySymbolicModel] = None,
        allow_private_hosts: bool = False,
    ) -> None:
        self.memory = memory
        self.model = model or PlanetarySymbolicModel(memory)
        self.allow_private_hosts = allow_private_hosts

    def ingest_url(
        self,
        url: str,
        timeout: int = 20,
        limit: int = 200_000,
    ) -> IngestionResult:
        try:
            self._assert_url_allowed(url)
            content, headers = self._read_url(url, timeout=timeout, limit=limit)
            text = extract_text(content, headers.get("content-type", ""))
            title = title_from_text(text) or url

            observation = self.memory.add_observation(
                source="internet",
                url=url,
                title=title,
                content=text,
                status="observed",
                metadata={
                    "content_type": headers.get("content-type", ""),
                    "bytes_read": len(content),
                },
            )
            learning = self.model.train_text(text, observation_id=observation.id)

            self.memory.record_event(
                "ingestion",
                url,
                {
                    "observation_id": observation.id,
                    "content_hash": observation.content_hash,
                    "top_terms": learning.top_terms,
                },
            )

            return IngestionResult(
                ok=True,
                url=url,
                observation=observation,
                learning=learning,
                bytes_read=len(content),
            )
        except Exception as exc:
            self.memory.record_event(
                "ingestion_error",
                url,
                {"error": str(exc)},
            )
            return IngestionResult(
                ok=False,
                url=url,
                observation=None,
                learning=None,
                bytes_read=0,
                error=str(exc),
            )

    def ingest_many(self, urls: Iterable[str]) -> List[IngestionResult]:
        return [self.ingest_url(url) for url in urls]

    def _read_url(self, url: str, timeout: int, limit: int) -> tuple[bytes, Dict[str, str]]:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AGI-GAIA-TECHNE/10 PlanetaryIngestor",
            },
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read(limit)
            headers = {key.lower(): value for key, value in response.headers.items()}
        return content, headers

    def _assert_url_allowed(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https", "data"}:
            raise ValueError(f"Unsupported ingestion scheme: {parsed.scheme}")
        if parsed.scheme == "data":
            return
        if not parsed.hostname:
            raise ValueError("URL must include a hostname.")
        if not self.allow_private_hosts and _is_private_host(parsed.hostname):
            raise ValueError("Private or local hosts are disabled for live ingestion.")


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = False
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip and data.strip():
            self.parts.append(data.strip())


def extract_text(content: bytes, content_type: str = "") -> str:
    charset = "utf-8"
    for part in content_type.split(";"):
        part = part.strip().lower()
        if part.startswith("charset="):
            charset = part.split("=", 1)[1]

    raw = content.decode(charset, errors="replace")
    if "html" not in content_type.lower() and "<html" not in raw[:500].lower():
        return _normalize_space(raw)

    parser = _TextExtractor()
    parser.feed(raw)
    return _normalize_space(html.unescape(" ".join(parser.parts)))


def title_from_text(text: str) -> str:
    return text.strip().splitlines()[0][:120] if text.strip() else ""


def _normalize_space(text: str) -> str:
    return " ".join(text.split())


def _is_private_host(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        pass

    if hostname.lower() in {"localhost", "localhost.localdomain"}:
        return True

    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for info in infos:
        address = info[4][0]
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            continue
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return True
    return False

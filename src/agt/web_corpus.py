from __future__ import annotations

import hashlib
import html
import ipaddress
import json
import socket
import time
import urllib.robotparser
import urllib.request
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin, urlparse

from .dataset_forge import CorpusRecord, chunk_text, estimate_tokens, normalize_text, sha256_text, write_jsonl


USER_AGENT = "AGI-GAIA-TECHNE-ManualForge/1.0"


@dataclass(frozen=True)
class WebFetchResult:
    ok: bool
    url: str
    final_url: str
    title: str
    text: str
    bytes_read: int
    content_type: str
    error: str = ""
    fetched_at: float = field(default_factory=time.time)


@dataclass(frozen=True)
class WebCorpusReport:
    output_path: str
    urls: int
    ok: int
    failed: int
    records: int
    estimated_tokens: int
    manifest_path: str
    corpus_path: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WebCorpusHarvester:
    """
    Bounded internet-to-corpus harvester.

    It only reads explicit URLs supplied by the operator. Private/local hosts
    are blocked by default, robots.txt is respected by default, and every
    chunk keeps source URL metadata for public trace and rights review.
    """

    def __init__(
        self,
        output_dir: str = "data/llm/web_corpus",
        timeout: int = 20,
        byte_limit: int = 500_000,
        chunk_chars: int = 8_000,
        chunk_overlap: int = 400,
        allow_private_hosts: bool = False,
        respect_robots: bool = True,
        rights_status: str = "internet_source_review_required",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.byte_limit = byte_limit
        self.chunk_chars = chunk_chars
        self.chunk_overlap = chunk_overlap
        self.allow_private_hosts = allow_private_hosts
        self.respect_robots = respect_robots
        self.rights_status = rights_status

    def harvest(self, urls: Iterable[str]) -> WebCorpusReport:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        manifest: List[Dict[str, Any]] = []
        records: List[CorpusRecord] = []
        seen_hashes: set[str] = set()

        url_list = list(dict.fromkeys(url.strip() for url in urls if url.strip()))
        for url in url_list:
            result = self.fetch_url(url)
            manifest.append(asdict(result))
            if not result.ok:
                continue

            text = normalize_text(result.text)
            for chunk_index, chunk in enumerate(chunk_text(text, self.chunk_chars, self.chunk_overlap)):
                content_hash = sha256_text(chunk)
                if content_hash in seen_hashes:
                    continue
                seen_hashes.add(content_hash)
                records.append(
                    CorpusRecord(
                        id=content_hash[:24],
                        title=result.title or result.final_url,
                        source_path=result.final_url,
                        kind="internet",
                        text=chunk,
                        chunk_index=chunk_index,
                        char_count=len(chunk),
                        byte_count=len(chunk.encode("utf-8")),
                        estimated_tokens=estimate_tokens(chunk),
                        content_sha256=content_hash,
                        metadata={
                            "source_type": "internet",
                            "url": result.url,
                            "final_url": result.final_url,
                            "content_type": result.content_type,
                            "fetched_at": result.fetched_at,
                            "rights_status": self.rights_status,
                        },
                    )
                )

        corpus_path = self.output_dir / "corpus.jsonl"
        manifest_path = self.output_dir / "manifest.jsonl"
        stats_path = self.output_dir / "stats.json"
        write_jsonl(corpus_path, (asdict(record) for record in records))
        write_jsonl(manifest_path, manifest)
        report = WebCorpusReport(
            output_path=str(self.output_dir),
            urls=len(url_list),
            ok=sum(1 for entry in manifest if entry.get("ok")),
            failed=sum(1 for entry in manifest if not entry.get("ok")),
            records=len(records),
            estimated_tokens=sum(record.estimated_tokens for record in records),
            manifest_path=str(manifest_path),
            corpus_path=str(corpus_path),
        )
        stats_path.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return report

    def fetch_url(self, url: str) -> WebFetchResult:
        try:
            self._assert_allowed(url)
            if self.respect_robots and not self._robots_allowed(url):
                raise ValueError("robots.txt disallows this user agent for the URL.")

            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                content = response.read(self.byte_limit)
                final_url = response.geturl()
                headers = {key.lower(): value for key, value in response.headers.items()}
            content_type = headers.get("content-type", "")
            text = extract_web_text(content, content_type)
            title = title_from_html_or_text(content, content_type, text) or final_url
            return WebFetchResult(
                ok=True,
                url=url,
                final_url=final_url,
                title=title,
                text=text,
                bytes_read=len(content),
                content_type=content_type,
            )
        except Exception as exc:
            return WebFetchResult(
                ok=False,
                url=url,
                final_url="",
                title="",
                text="",
                bytes_read=0,
                content_type="",
                error=str(exc),
            )

    def _assert_allowed(self, url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only http/https URLs are supported for web corpus harvesting.")
        if not parsed.hostname:
            raise ValueError("URL must include a hostname.")
        if not self.allow_private_hosts and _is_private_host(parsed.hostname):
            raise ValueError("Private or local hosts are disabled.")

    def _robots_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
        parser = urllib.robotparser.RobotFileParser()
        parser.set_url(robots_url)
        try:
            parser.read()
        except Exception:
            return True
        return parser.can_fetch(USER_AGENT, url)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.parts: List[str] = []
        self.title_parts: List[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and data.strip():
            self.title_parts.append(data.strip())
        if self._skip_depth == 0 and data.strip():
            self.parts.append(data.strip())

    @property
    def text(self) -> str:
        return " ".join(self.parts)

    @property
    def title(self) -> str:
        return " ".join(self.title_parts).strip()


def extract_web_text(content: bytes, content_type: str) -> str:
    charset = "utf-8"
    for part in content_type.split(";"):
        part = part.strip().lower()
        if part.startswith("charset="):
            charset = part.split("=", 1)[1]
    raw = content.decode(charset, errors="replace")
    if "html" not in content_type.lower() and "<html" not in raw[:500].lower():
        return normalize_text(raw)
    parser = _TextExtractor()
    parser.feed(raw)
    return normalize_text(html.unescape(parser.text))


def title_from_html_or_text(content: bytes, content_type: str, text: str) -> str:
    raw = content.decode("utf-8", errors="replace")
    if "html" in content_type.lower() or "<html" in raw[:500].lower():
        parser = _TextExtractor()
        parser.feed(raw)
        if parser.title:
            return html.unescape(parser.title)[:180]
    return text.splitlines()[0][:180] if text.strip() else ""


def read_url_file(path: str | Path) -> List[str]:
    return [
        line.strip()
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


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

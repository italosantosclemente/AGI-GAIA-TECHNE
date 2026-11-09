from __future__ import annotations

import hashlib
import json
import mimetypes
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional


TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".markdown",
    ".rst",
    ".tex",
    ".csv",
    ".tsv",
    ".json",
    ".jsonl",
}

CODE_EXTENSIONS = {
    ".py",
    ".jl",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".toml",
    ".yaml",
    ".yml",
}

PDF_EXTENSIONS = {".pdf"}

MEDIA_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".mp3",
    ".wav",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
}


@dataclass(frozen=True)
class FileCandidate:
    path: str
    title: str
    extension: str
    mime_type: str
    kind: str
    status: str
    reason: str = ""
    size_bytes: int = 0
    drive_url: str = ""
    drive_id: str = ""


@dataclass(frozen=True)
class CorpusRecord:
    id: str
    title: str
    source_path: str
    kind: str
    text: str
    chunk_index: int
    char_count: int
    byte_count: int
    estimated_tokens: int
    content_sha256: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ForgeReport:
    root: str
    output_dir: str
    generated_at: float
    candidates: int
    documents: int
    chunks: int
    skipped: int
    duplicate_chunks: int
    total_chars: int
    estimated_tokens: int
    by_status: Dict[str, int]
    corpus_path: str
    manifest_path: str
    stats_path: str
    shards_dir: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ManualDatasetForge:
    """
    Build a training corpus from a local manual archive.

    The forge expects the Drive folder to be mirrored locally through Google
    Drive Desktop, rclone, manual download, or another explicit operator path.
    It does not assume private API credentials.
    """

    def __init__(
        self,
        root: str,
        output_dir: str = "data/llm/manual_forge",
        include_code: bool = False,
        include_pdfs: bool = True,
        min_chars: int = 200,
        chunk_chars: int = 8_000,
        chunk_overlap: int = 400,
        rights_status: str = "user_provided_review_required",
    ) -> None:
        self.root = Path(root)
        self.output_dir = Path(output_dir)
        self.include_code = include_code
        self.include_pdfs = include_pdfs
        self.min_chars = min_chars
        self.chunk_chars = chunk_chars
        self.chunk_overlap = chunk_overlap
        self.rights_status = rights_status

    def build(self) -> ForgeReport:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        shards_dir = self.output_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)

        candidates = list(self.scan())
        records: List[CorpusRecord] = []
        manifest: List[Dict[str, Any]] = []
        seen_hashes: set[str] = set()
        duplicate_chunks = 0

        for candidate in candidates:
            entry = asdict(candidate)
            if candidate.status != "trainable":
                manifest.append(entry)
                continue

            text, extract_status, error = self.extract(candidate)
            entry["extract_status"] = extract_status
            if error:
                entry["error"] = error

            text = normalize_text(text)
            if len(text) < self.min_chars:
                entry["status"] = "skipped"
                entry["reason"] = "too_few_characters"
                entry["char_count"] = len(text)
                manifest.append(entry)
                continue

            doc_chunks = 0
            for chunk_index, chunk in enumerate(chunk_text(text, self.chunk_chars, self.chunk_overlap)):
                content_hash = sha256_text(chunk)
                if content_hash in seen_hashes:
                    duplicate_chunks += 1
                    continue
                seen_hashes.add(content_hash)
                record = CorpusRecord(
                    id=content_hash[:24],
                    title=candidate.title,
                    source_path=candidate.path,
                    kind=candidate.kind,
                    text=chunk,
                    chunk_index=chunk_index,
                    char_count=len(chunk),
                    byte_count=len(chunk.encode("utf-8")),
                    estimated_tokens=estimate_tokens(chunk),
                    content_sha256=content_hash,
                    metadata={
                        "mime_type": candidate.mime_type,
                        "extension": candidate.extension,
                        "rights_status": self.rights_status,
                        "drive_url": candidate.drive_url,
                        "drive_id": candidate.drive_id,
                    },
                )
                records.append(record)
                doc_chunks += 1

            entry["status"] = "processed"
            entry["char_count"] = len(text)
            entry["chunks"] = doc_chunks
            manifest.append(entry)

        corpus_path = self.output_dir / "corpus.jsonl"
        manifest_path = self.output_dir / "manifest.jsonl"
        stats_path = self.output_dir / "stats.json"

        write_jsonl(corpus_path, (asdict(record) for record in records))
        write_jsonl(manifest_path, manifest)
        write_shards(records, shards_dir)

        by_status: Dict[str, int] = {}
        for entry in manifest:
            status = str(entry.get("status", "unknown"))
            by_status[status] = by_status.get(status, 0) + 1

        report = ForgeReport(
            root=str(self.root),
            output_dir=str(self.output_dir),
            generated_at=time.time(),
            candidates=len(candidates),
            documents=sum(1 for entry in manifest if entry.get("status") == "processed"),
            chunks=len(records),
            skipped=sum(1 for entry in manifest if entry.get("status") != "processed"),
            duplicate_chunks=duplicate_chunks,
            total_chars=sum(record.char_count for record in records),
            estimated_tokens=sum(record.estimated_tokens for record in records),
            by_status=by_status,
            corpus_path=str(corpus_path),
            manifest_path=str(manifest_path),
            stats_path=str(stats_path),
            shards_dir=str(shards_dir),
        )

        stats_path.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return report

    def scan(self) -> Iterator[FileCandidate]:
        if not self.root.exists():
            raise FileNotFoundError(f"Manual root does not exist: {self.root}")

        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue
            yield classify_local_path(
                path,
                root=self.root,
                include_code=self.include_code,
                include_pdfs=self.include_pdfs,
            )

    def extract(self, candidate: FileCandidate) -> tuple[str, str, str]:
        path = self.root / candidate.path
        if candidate.extension in TEXT_EXTENSIONS or candidate.extension in CODE_EXTENSIONS:
            return read_text_file(path), "ok", ""
        if candidate.extension in PDF_EXTENSIONS:
            return extract_pdf_text(path)
        return "", "unsupported", "unsupported file type"


def classify_local_path(
    path: Path,
    root: Optional[Path] = None,
    include_code: bool = False,
    include_pdfs: bool = True,
) -> FileCandidate:
    extension = path.suffix.lower()
    rel_path = str(path.relative_to(root)) if root else str(path)
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    size_bytes = path.stat().st_size

    if extension in TEXT_EXTENSIONS:
        kind = "text"
        status = "trainable"
        reason = ""
    elif extension in PDF_EXTENSIONS:
        kind = "pdf"
        status = "trainable" if include_pdfs else "skipped"
        reason = "" if include_pdfs else "pdf_disabled"
    elif extension in CODE_EXTENSIONS:
        kind = "code"
        status = "trainable" if include_code else "skipped"
        reason = "" if include_code else "code_disabled"
    elif extension in MEDIA_EXTENSIONS:
        kind = "media"
        status = "skipped"
        reason = "media_requires_transcription"
    else:
        kind = "unknown"
        status = "skipped"
        reason = "unsupported_extension"

    return FileCandidate(
        path=rel_path,
        title=path.name,
        extension=extension,
        mime_type=mime_type,
        kind=kind,
        status=status,
        reason=reason,
        size_bytes=size_bytes,
    )


def classify_drive_item(item: Dict[str, Any]) -> FileCandidate:
    title = str(item.get("title") or item.get("name") or "")
    mime_type = str(item.get("mime_type") or item.get("mimeType") or "")
    extension = Path(title).suffix.lower()

    if item.get("file_or_folder") == "folder" or mime_type == "application/vnd.google-apps.folder":
        kind = "folder"
        status = "folder"
        reason = "scan_recursively"
    elif mime_type == "application/pdf" or extension == ".pdf":
        kind = "pdf"
        status = "trainable"
        reason = ""
    elif mime_type.startswith("text/") or extension in TEXT_EXTENSIONS:
        kind = "text"
        status = "trainable"
        reason = ""
    elif extension in CODE_EXTENSIONS:
        kind = "code"
        status = "optional"
        reason = "enable_include_code"
    elif mime_type.startswith("video/") or mime_type.startswith("image/") or extension in MEDIA_EXTENSIONS:
        kind = "media"
        status = "skipped"
        reason = "media_requires_transcription"
    else:
        kind = "unknown"
        status = "review"
        reason = "unknown_drive_type"

    return FileCandidate(
        path=title,
        title=title,
        extension=extension,
        mime_type=mime_type,
        kind=kind,
        status=status,
        reason=reason,
        drive_url=str(item.get("url") or ""),
        drive_id=str(item.get("id") or ""),
    )


def build_drive_inventory(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [asdict(classify_drive_item(item)) for item in items]


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t ]+", " ", text)
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 8_000, overlap: int = 400) -> Iterator[str]:
    if max_chars <= overlap:
        raise ValueError("max_chars must be greater than overlap.")
    text = text.strip()
    if len(text) <= max_chars:
        yield text
        return

    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunk = text[start:end]
        if end < len(text):
            boundary = max(chunk.rfind("\n\n"), chunk.rfind(". "), chunk.rfind("\n"))
            if boundary > max_chars // 2:
                end = start + boundary + 1
                chunk = text[start:end]
        chunk = chunk.strip()
        if chunk:
            yield chunk
        if end >= len(text):
            break
        start = max(0, end - overlap)


def estimate_tokens(text: str) -> int:
    return max(1, len(text.encode("utf-8")) // 4)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text_file(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def extract_pdf_text(path: Path) -> tuple[str, str, str]:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return "", "requires_pypdf", "Install pypdf to extract PDF text."

    try:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages), "ok", ""
    except Exception as exc:
        return "", "pdf_error", str(exc)


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_shards(records: List[CorpusRecord], shards_dir: Path, shard_chars: int = 2_000_000) -> None:
    shard_index = 0
    current_chars = 0
    current: List[Dict[str, Any]] = []
    for record in records:
        if current and current_chars + record.char_count > shard_chars:
            write_jsonl(shards_dir / f"shard_{shard_index:05d}.jsonl", current)
            shard_index += 1
            current = []
            current_chars = 0
        current.append(asdict(record))
        current_chars += record.char_count
    if current:
        write_jsonl(shards_dir / f"shard_{shard_index:05d}.jsonl", current)

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence

import torch
from torch.utils.data import Dataset

from .llm_tokenizer import ByteTokenizer


@dataclass(frozen=True)
class PackedCorpusReport:
    corpus_path: str
    output_path: str
    tokenizer_path: str
    documents: int
    tokens: int
    train_tokens: int
    val_tokens: int
    block_size: int
    dtype: str = "int16"

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def iter_corpus_text(corpus_path: str | Path) -> Iterator[str]:
    path = Path(corpus_path)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            text = payload.get("text", "")
            if text:
                yield str(text)


def pack_corpus(
    corpus_path: str | Path,
    output_path: str | Path,
    tokenizer: ByteTokenizer | None = None,
    validation_fraction: float = 0.02,
    block_size: int = 256,
    seed: int = 42,
) -> PackedCorpusReport:
    tokenizer = tokenizer or ByteTokenizer()
    corpus_path = Path(corpus_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    token_docs: List[List[int]] = [
        tokenizer.encode(text, add_eos=True)
        for text in iter_corpus_text(corpus_path)
    ]
    random.Random(seed).shuffle(token_docs)

    split_index = max(1, int(len(token_docs) * (1.0 - validation_fraction)))
    if len(token_docs) <= 1:
        split_index = len(token_docs)
    train_docs = token_docs[:split_index]
    val_docs = token_docs[split_index:] or token_docs[:1]

    train_tokens = flatten(train_docs)
    val_tokens = flatten(val_docs)

    torch.save(torch.tensor(train_tokens, dtype=torch.int16), output_path / "train.pt")
    torch.save(torch.tensor(val_tokens, dtype=torch.int16), output_path / "val.pt")
    tokenizer_path = output_path / "tokenizer.json"
    tokenizer.save(tokenizer_path)

    report = PackedCorpusReport(
        corpus_path=str(corpus_path),
        output_path=str(output_path),
        tokenizer_path=str(tokenizer_path),
        documents=len(token_docs),
        tokens=len(train_tokens) + len(val_tokens),
        train_tokens=len(train_tokens),
        val_tokens=len(val_tokens),
        block_size=block_size,
    )
    (output_path / "pack_report.json").write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


class TokenBlockDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    def __init__(self, token_path: str | Path, block_size: int) -> None:
        tokens = torch.load(token_path, map_location="cpu")
        if tokens.dtype != torch.long:
            tokens = tokens.long()
        if tokens.numel() < block_size + 2:
            raise ValueError("Token stream is too small for the requested block size.")
        self.tokens = tokens
        self.block_size = block_size

    def __len__(self) -> int:
        return max(1, self.tokens.numel() - self.block_size - 1)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        index = int(index) % len(self)
        chunk = self.tokens[index:index + self.block_size + 1]
        return chunk[:-1].long(), chunk[1:].long()


def flatten(docs: Sequence[Sequence[int]]) -> List[int]:
    out: List[int] = []
    for doc in docs:
        out.extend(int(token) for token in doc)
    return out


def load_pack_report(path: str | Path) -> PackedCorpusReport:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return PackedCorpusReport(**payload)

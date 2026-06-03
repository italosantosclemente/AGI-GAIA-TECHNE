from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


PAD_TOKEN = 0
EOS_TOKEN = 257
VOCAB_SIZE = 258


@dataclass(frozen=True)
class ByteTokenizerConfig:
    name: str = "agt-byte-tokenizer-v1"
    vocab_size: int = VOCAB_SIZE
    pad_token_id: int = PAD_TOKEN
    eos_token_id: int = EOS_TOKEN


class ByteTokenizer:
    """
    Byte-level tokenizer for from-scratch LLM training.

    It needs no external vocabulary training, handles Portuguese, symbols and
    code uniformly, and makes the first AGT language model reproducible.
    """

    def __init__(self, config: ByteTokenizerConfig | None = None) -> None:
        self.config = config or ByteTokenizerConfig()

    @property
    def vocab_size(self) -> int:
        return self.config.vocab_size

    @property
    def eos_token_id(self) -> int:
        return self.config.eos_token_id

    @property
    def pad_token_id(self) -> int:
        return self.config.pad_token_id

    def encode(self, text: str, add_eos: bool = True) -> List[int]:
        ids = [byte + 1 for byte in text.encode("utf-8")]
        if add_eos:
            ids.append(self.eos_token_id)
        return ids

    def decode(self, token_ids: Iterable[int]) -> str:
        raw = bytearray()
        for token_id in token_ids:
            token_id = int(token_id)
            if token_id in {self.pad_token_id, self.eos_token_id}:
                continue
            if 1 <= token_id <= 256:
                raw.append(token_id - 1)
        return raw.decode("utf-8", errors="replace")

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(asdict(self.config), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> "ByteTokenizer":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(ByteTokenizerConfig(**payload))

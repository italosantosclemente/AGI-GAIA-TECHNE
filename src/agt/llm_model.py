from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Dict, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass(frozen=True)
class GPTConfig:
    vocab_size: int = 258
    block_size: int = 256
    n_layer: int = 4
    n_head: int = 4
    n_embd: int = 256
    dropout: float = 0.1
    bias: bool = True

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class CausalSelfAttention(nn.Module):
    def __init__(self, config: GPTConfig) -> None:
        super().__init__()
        if config.n_embd % config.n_head != 0:
            raise ValueError("n_embd must be divisible by n_head.")
        self.n_head = config.n_head
        self.dropout = config.dropout
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd, bias=config.bias)
        self.resid_dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, time, channels = x.size()
        q, k, v = self.c_attn(x).split(channels, dim=2)
        head_dim = channels // self.n_head
        q = q.view(batch, time, self.n_head, head_dim).transpose(1, 2)
        k = k.view(batch, time, self.n_head, head_dim).transpose(1, 2)
        v = v.view(batch, time, self.n_head, head_dim).transpose(1, 2)

        y = F.scaled_dot_product_attention(
            q,
            k,
            v,
            attn_mask=None,
            dropout_p=self.dropout if self.training else 0.0,
            is_causal=True,
        )
        y = y.transpose(1, 2).contiguous().view(batch, time, channels)
        return self.resid_dropout(self.c_proj(y))


class MLP(nn.Module):
    def __init__(self, config: GPTConfig) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd, bias=config.bias),
            nn.GELU(),
            nn.Linear(4 * config.n_embd, config.n_embd, bias=config.bias),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class Block(nn.Module):
    def __init__(self, config: GPTConfig) -> None:
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.mlp = MLP(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class GaiaManualGPT(nn.Module):
    """
    Minimal decoder-only Transformer trained from random initialization.
    """

    def __init__(self, config: GPTConfig) -> None:
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.n_embd)
        self.position_embedding = nn.Embedding(config.block_size, config.n_embd)
        self.dropout = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList([Block(config) for _ in range(config.n_layer)])
        self.ln_f = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        self.token_embedding.weight = self.lm_head.weight
        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(
        self,
        idx: torch.Tensor,
        targets: Optional[torch.Tensor] = None,
    ) -> tuple[torch.Tensor, Optional[torch.Tensor]]:
        batch, time = idx.shape
        if time > self.config.block_size:
            raise ValueError("Cannot forward sequence longer than block_size.")
        positions = torch.arange(0, time, dtype=torch.long, device=idx.device)
        x = self.token_embedding(idx) + self.position_embedding(positions)
        x = self.dropout(x)
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.reshape(-1),
            )
        return logits, loss

    @torch.no_grad()
    def generate(
        self,
        idx: torch.Tensor,
        max_new_tokens: int,
        temperature: float = 1.0,
        top_k: Optional[int] = None,
    ) -> torch.Tensor:
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.config.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / max(temperature, 1e-6)
            if top_k is not None:
                values, _indices = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < values[:, [-1]]] = -float("Inf")
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx

    def parameter_count(self) -> int:
        return sum(param.numel() for param in self.parameters())


def estimate_model_flops_per_token(config: GPTConfig) -> int:
    return 6 * sum(
        param.numel()
        for param in GaiaManualGPT(config).parameters()
    )


def scale_config(name: str) -> GPTConfig:
    scales = {
        "micro": GPTConfig(block_size=32, n_layer=1, n_head=1, n_embd=32, dropout=0.0),
        "debug": GPTConfig(block_size=64, n_layer=2, n_head=2, n_embd=64, dropout=0.0),
        "seed": GPTConfig(block_size=128, n_layer=4, n_head=4, n_embd=128, dropout=0.1),
        "small": GPTConfig(block_size=256, n_layer=6, n_head=6, n_embd=384, dropout=0.1),
        "base": GPTConfig(block_size=512, n_layer=12, n_head=12, n_embd=768, dropout=0.1),
        "large-plan": GPTConfig(block_size=1024, n_layer=24, n_head=16, n_embd=1024, dropout=0.1),
    }
    if name not in scales:
        raise ValueError(f"Unknown scale '{name}'. Choose: {', '.join(scales)}")
    return scales[name]


def make_optimizer(model: nn.Module, learning_rate: float, weight_decay: float) -> torch.optim.Optimizer:
    decay_params = []
    nodecay_params = []
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if param.dim() >= 2 and "embedding" not in name:
            decay_params.append(param)
        else:
            nodecay_params.append(param)
    return torch.optim.AdamW(
        [
            {"params": decay_params, "weight_decay": weight_decay},
            {"params": nodecay_params, "weight_decay": 0.0},
        ],
        lr=learning_rate,
        betas=(0.9, 0.95),
    )


def learning_rate_at_step(
    step: int,
    base_lr: float,
    warmup_steps: int,
    max_steps: int,
    min_lr_ratio: float = 0.1,
) -> float:
    if step < warmup_steps:
        return base_lr * (step + 1) / max(1, warmup_steps)
    progress = (step - warmup_steps) / max(1, max_steps - warmup_steps)
    cosine = 0.5 * (1.0 + math.cos(math.pi * min(1.0, progress)))
    return base_lr * (min_lr_ratio + (1.0 - min_lr_ratio) * cosine)

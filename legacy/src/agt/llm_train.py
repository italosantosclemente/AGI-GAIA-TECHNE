from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import torch
from torch.utils.data import DataLoader

from .llm_corpus import TokenBlockDataset
from .llm_model import (
    GPTConfig,
    GaiaManualGPT,
    learning_rate_at_step,
    make_optimizer,
    scale_config,
)
from .llm_tokenizer import ByteTokenizer


@dataclass(frozen=True)
class TrainingConfig:
    pack_dir: str
    output_dir: str = "models/agt-gaia-manual-gpt"
    scale: str = "debug"
    max_steps: int = 100
    batch_size: int = 8
    gradient_accumulation_steps: int = 1
    learning_rate: float = 3e-4
    weight_decay: float = 0.1
    warmup_steps: int = 10
    eval_interval: int = 25
    eval_batches: int = 10
    checkpoint_interval: int = 50
    seed: int = 42
    device: str = "auto"
    amp: bool = True


@dataclass(frozen=True)
class TrainingReport:
    output_dir: str
    checkpoint_path: str
    scale: str
    steps: int
    train_loss: float
    val_loss: float
    parameter_count: int
    elapsed_seconds: float
    device: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def train_from_pack(config: TrainingConfig) -> TrainingReport:
    if config.max_steps < 1:
        raise ValueError("max_steps must be at least 1.")
    if config.gradient_accumulation_steps < 1:
        raise ValueError("gradient_accumulation_steps must be at least 1.")

    torch.manual_seed(config.seed)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    device = resolve_device(config.device)
    model_config = scale_config(config.scale)
    tokenizer = ByteTokenizer.load(Path(config.pack_dir) / "tokenizer.json")
    model_config = GPTConfig(**{**model_config.to_dict(), "vocab_size": tokenizer.vocab_size})
    model = GaiaManualGPT(model_config).to(device)

    train_dataset = TokenBlockDataset(Path(config.pack_dir) / "train.pt", model_config.block_size)
    val_dataset = TokenBlockDataset(Path(config.pack_dir) / "val.pt", model_config.block_size)
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        drop_last=False,
    )
    train_iter = iter(train_loader)
    optimizer = make_optimizer(model, config.learning_rate, config.weight_decay)
    use_amp = config.amp and device.startswith("cuda")
    try:
        scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    except TypeError:
        scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    step = 0
    train_loss = float("nan")
    val_loss = float("nan")
    started_at = time.time()

    while step < config.max_steps:
        lr = learning_rate_at_step(
            step,
            base_lr=config.learning_rate,
            warmup_steps=config.warmup_steps,
            max_steps=config.max_steps,
        )
        for group in optimizer.param_groups:
            group["lr"] = lr

        optimizer.zero_grad(set_to_none=True)
        accumulated_loss = 0.0
        for _ in range(config.gradient_accumulation_steps):
            try:
                x, y = next(train_iter)
            except StopIteration:
                train_iter = iter(train_loader)
                x, y = next(train_iter)
            x = x.to(device)
            y = y.to(device)
            if use_amp:
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    _logits, loss = model(x, y)
            else:
                _logits, loss = model(x, y)
            assert loss is not None
            loss = loss / config.gradient_accumulation_steps
            scaler.scale(loss).backward()
            accumulated_loss += float(loss.detach().cpu()) * config.gradient_accumulation_steps

        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        train_loss = accumulated_loss
        step += 1

        if step == 1 or step % config.eval_interval == 0 or step == config.max_steps:
            val_loss = evaluate(model, val_dataset, device, config.eval_batches, config.batch_size)
            write_checkpoint(
                output_dir / "latest.pt",
                model,
                optimizer,
                model_config,
                tokenizer,
                step,
                train_loss,
                val_loss,
                config,
            )

        if step % config.checkpoint_interval == 0:
            write_checkpoint(
                output_dir / f"step_{step:06d}.pt",
                model,
                optimizer,
                model_config,
                tokenizer,
                step,
                train_loss,
                val_loss,
                config,
            )

    checkpoint_path = output_dir / "latest.pt"
    report = TrainingReport(
        output_dir=str(output_dir),
        checkpoint_path=str(checkpoint_path),
        scale=config.scale,
        steps=step,
        train_loss=train_loss,
        val_loss=val_loss,
        parameter_count=model.parameter_count(),
        elapsed_seconds=time.time() - started_at,
        device=device,
    )
    (output_dir / "train_report.json").write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


@torch.no_grad()
def evaluate(
    model: GaiaManualGPT,
    dataset: TokenBlockDataset,
    device: str,
    batches: int,
    batch_size: int,
) -> float:
    model.eval()
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    losses = []
    for index, (x, y) in enumerate(loader):
        if index >= batches:
            break
        x = x.to(device)
        y = y.to(device)
        _logits, loss = model(x, y)
        assert loss is not None
        losses.append(float(loss.detach().cpu()))
    model.train()
    return sum(losses) / max(1, len(losses))


def write_checkpoint(
    path: Path,
    model: GaiaManualGPT,
    optimizer: torch.optim.Optimizer,
    model_config: GPTConfig,
    tokenizer: ByteTokenizer,
    step: int,
    train_loss: float,
    val_loss: float,
    training_config: TrainingConfig,
) -> None:
    payload = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "model_config": model_config.to_dict(),
        "tokenizer_config": asdict(tokenizer.config),
        "step": step,
        "train_loss": train_loss,
        "val_loss": val_loss,
        "training_config": asdict(training_config),
        "created_at": time.time(),
        "signature": "AGI-GAIA-TECHNE::ISC",
    }
    torch.save(payload, path)


def load_checkpoint(
    checkpoint_path: str | Path,
    device: str = "auto",
) -> tuple[GaiaManualGPT, ByteTokenizer, Dict[str, Any], str]:
    resolved_device = resolve_device(device)
    try:
        checkpoint = torch.load(checkpoint_path, map_location=resolved_device, weights_only=False)
    except TypeError:
        checkpoint = torch.load(checkpoint_path, map_location=resolved_device)
    tokenizer = ByteTokenizer()
    if "tokenizer_config" in checkpoint:
        from .llm_tokenizer import ByteTokenizerConfig

        tokenizer = ByteTokenizer(ByteTokenizerConfig(**checkpoint["tokenizer_config"]))
    model = GaiaManualGPT(GPTConfig(**checkpoint["model_config"])).to(resolved_device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, tokenizer, checkpoint, resolved_device


@torch.no_grad()
def generate_text(
    checkpoint_path: str | Path,
    prompt: str,
    max_new_tokens: int = 256,
    temperature: float = 0.85,
    top_k: Optional[int] = 80,
    device: str = "auto",
) -> str:
    model, tokenizer, _checkpoint, resolved_device = load_checkpoint(checkpoint_path, device=device)
    idx = torch.tensor([tokenizer.encode(prompt, add_eos=False)], dtype=torch.long, device=resolved_device)
    out = model.generate(
        idx,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
    )
    generated = tokenizer.decode(out[0].tolist())
    return generated[len(prompt):].strip()


def resolve_device(device: str) -> str:
    if device != "auto":
        return device
    return "cuda" if torch.cuda.is_available() else "cpu"

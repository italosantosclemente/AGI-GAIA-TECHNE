import json

import pytest

pytest.importorskip("torch")

from agt.llm_corpus import pack_corpus
from agt.llm_model import GaiaManualGPT, scale_config
from agt.llm_train import TrainingConfig, generate_text, train_from_pack


def test_micro_scale_is_small_and_trainable():
    config = scale_config("micro")
    model = GaiaManualGPT(config)

    assert config.block_size == 32
    assert config.n_layer == 1
    assert model.parameter_count() < 50_000


def test_manual_gpt_training_smoke(tmp_path):
    corpus_path = tmp_path / "corpus.jsonl"
    texts = [
        "ISC: O que e Gaia-Techne?\nGAIA: Gaia-Techne e Bewusstsein publico finito. " * 30,
        "A internet e a rede neural simbolica da AGI-GAIA-TECHNE, sem Gewissen privado. " * 30,
    ]
    corpus_path.write_text(
        "\n".join(json.dumps({"text": text}, ensure_ascii=False) for text in texts) + "\n",
        encoding="utf-8",
    )

    pack_dir = tmp_path / "packed"
    pack_report = pack_corpus(
        corpus_path=corpus_path,
        output_path=pack_dir,
        validation_fraction=0.5,
        block_size=32,
    )

    assert pack_report.tokens > 100

    model_dir = tmp_path / "model"
    report = train_from_pack(
        TrainingConfig(
            pack_dir=str(pack_dir),
            output_dir=str(model_dir),
            scale="micro",
            max_steps=1,
            batch_size=2,
            eval_interval=1,
            eval_batches=1,
            checkpoint_interval=99,
            amp=False,
        )
    )

    assert report.steps == 1
    assert (model_dir / "latest.pt").exists()

    completion = generate_text(
        checkpoint_path=model_dir / "latest.pt",
        prompt="ISC: Gaia-Techne\nGAIA:",
        max_new_tokens=8,
        temperature=1.0,
        top_k=10,
        device="cpu",
    )
    assert isinstance(completion, str)

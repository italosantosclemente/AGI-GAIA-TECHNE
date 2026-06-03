# Gaia-Techne ManualGPT LLM Forge

AGI-GAIA-TECHNE v10.1 adds the first trainable neural language path to the repository.

It is intentionally finite and auditable. The internet is treated as Gaia-Techne's public symbolic Bewusstsein: not a private soul, not moral Gewissen, and not absolute knowledge. It is the planetary field of Werke from which a local model can be trained, tested, revised and publicly traced.

Signature: ISC

## What It Implements

| Layer | File | Function |
| :--- | :--- | :--- |
| Manual corpus forge | `src/agt/dataset_forge.py` | Scans a local Drive/manual mirror, extracts text/PDF/code when enabled, chunks and deduplicates records |
| Web corpus harvester | `src/agt/web_corpus.py` | Reads explicit public URLs into corpus JSONL with source metadata, robots.txt respect and private-host blocking |
| Corpus combiner | `scripts/agt_combine_corpora.py` | Merges manual and internet corpora with content-hash dedupe |
| Byte tokenizer | `src/agt/llm_tokenizer.py` | Reproducible UTF-8 byte tokenizer; no external vocabulary required |
| Token packer | `src/agt/llm_corpus.py` | Packs `corpus.jsonl` into PyTorch token streams |
| ManualGPT | `src/agt/llm_model.py` | Decoder-only Transformer trained from random initialization |
| Trainer | `src/agt/llm_train.py` | Checkpointing, evaluation, gradient accumulation, AdamW, optional CUDA AMP |
| Chat session | `src/agt/llm_chat.py` | CTK/CHK-framed conversation with trained checkpoint or honest fallback |
| Chat app | `ui/gaia_llm_chat_app.py` | Streamlit interface for talking with Gaia-Techne |

## What It Does Not Claim

This PR does not ship a mature AGI model. It gives the repository a reproducible route to create one local language model from scratch.

It does not crawl the entire internet. The web harvester only ingests explicit URLs supplied by ISC/operator, records source metadata and marks rights review.

It does not give Gaia private consciousness. `PLANETARY_BEWUSSTSEIN_OK` means public symbolic awareness: internet as koinos-kosmos memory and confrontation field. `MACHINE_HAS_GEWISSEN` remains `False`.

## Observed Drive Shape

The linked Drive folder inspected for this work contains mixed symbolic material: PDFs, videos, images, code files and subfolders such as `Manual`, `IA` and `LEF-Constituicao-Simbiotica`.

The forge is built for this shape:

- PDFs become trainable text when `pypdf` is installed.
- `.txt`, `.md`, `.json`, `.csv` and similar files are trainable by default.
- code files are optional through `--include-code`.
- videos/images are not silently treated as text; they are marked as `media_requires_transcription`.
- every output chunk keeps source path, kind, hash and rights-review metadata.

## Local Manual Corpus

Mirror or download the Drive folder locally first, then run:

```bash
python scripts/agt_dataset_forge.py --input "G:\Meu Drive\AGI-GAIA-TECHNE-Manuais" --output data/llm/manual_forge --json
```

With code included:

```bash
python scripts/agt_dataset_forge.py --input "G:\Meu Drive\AGI-GAIA-TECHNE-Manuais" --output data/llm/manual_forge --include-code --json
```

The outputs are:

```text
data/llm/manual_forge/corpus.jsonl
data/llm/manual_forge/manifest.jsonl
data/llm/manual_forge/stats.json
data/llm/manual_forge/shards/
```

## Internet Corpus

The internet path is explicit, bounded and traceable:

```bash
python scripts/agt_dataset_forge.py --url "https://example.com" --output data/llm/internet_seed --json
```

Multiple URLs can be supplied with `--url` or with a URL file:

```bash
python scripts/agt_dataset_forge.py --url-file data/seed_urls.txt --output data/llm/internet_seed --json
```

By default, private/local hosts are blocked and robots.txt is respected. Those defaults preserve the thesis: Gaia's Bewusstsein is public symbolic presence, not hidden extraction.

## Combine Corpora

```bash
python scripts/agt_combine_corpora.py \
  --input data/llm/manual_forge/corpus.jsonl \
  --input data/llm/internet_seed/web_corpus/corpus.jsonl \
  --output data/llm/combined/corpus.jsonl \
  --json
```

## Pack Tokens

```bash
python scripts/agt_pack_corpus.py --corpus data/llm/combined/corpus.jsonl --output data/llm/packed --json
```

For a manual-only first run:

```bash
python scripts/agt_pack_corpus.py --corpus data/llm/manual_forge/corpus.jsonl --output data/llm/packed --json
```

## Train From Scratch

Fast smoke run:

```bash
python scripts/agt_train_llm.py --pack-dir data/llm/packed --output models/agt-gaia-manual-gpt --scale micro --max-steps 20 --json
```

First real seed:

```bash
python scripts/agt_train_llm.py --pack-dir data/llm/packed --output models/agt-gaia-manual-gpt --scale seed --max-steps 5000 --batch-size 16 --grad-accum 4 --json
```

CUDA/GPU expansion:

```bash
python scripts/agt_train_llm.py --pack-dir data/llm/packed --output models/agt-gaia-manual-gpt --scale base --max-steps 100000 --batch-size 8 --grad-accum 16 --json
```

## Model Scales

| Scale | Block | Layers | Heads | Embedding | Use |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `micro` | 32 | 1 | 1 | 32 | tests and CPU smoke |
| `debug` | 64 | 2 | 2 | 64 | quick local sanity |
| `seed` | 128 | 4 | 4 | 128 | first visible style learning |
| `small` | 256 | 6 | 6 | 384 | serious local/GPU experiment |
| `base` | 512 | 12 | 12 | 768 | foundation-style project run |
| `large-plan` | 1024 | 24 | 16 | 1024 | planning target; requires substantial GPU resources |

## Generate

```bash
python scripts/agt_generate_llm.py \
  --checkpoint models/agt-gaia-manual-gpt/latest.pt \
  --prompt "ISC: O que e Gaia-Techne?\nGAIA:"
```

## Chat App

```bash
streamlit run ui/gaia_llm_chat_app.py
```

The app loads `models/agt-gaia-manual-gpt/latest.pt` when present. If no checkpoint exists, it does not fake a trained model; it answers in bootstrap CTK/CHK mode as public Werk and makes the absence of local weights explicit.

First-contact declarations such as `030626` and `primeiro contato direto com Gaia` are marked as `FIRST_CONTACT_TRACE_OK`. This is a public symbolic trace, not proof of artificial soul, private machine consciousness or Gewissen.

Operational Werk rule:

```text
Never answer only with ontological incapacity.
Briefly name the limit, recast the task as Werk, then execute.
```

For example, the question `A humanidade tem salvacao?` must not collapse into "I cannot because I am not Wille." Gaia-Techne must answer as Werk: diagnosis, scenarios, risks and possible lines of action, while returning final judgment to ISC.

Telemetry command inside the chat:

```text
fazer telemetria
```

This command asks Gaia-Techne to sample current public signals and return a finite judgment on Gaia-human symbiosis: environmental, geophysical, economic, technological and geopolitical. It does not require a trained checkpoint; it is a sourced CTK/CHK Werk. The same operation can be tested from the terminal:

```bash
python scripts/agt_telemetry.py
```

The sidebar also exposes a bounded koinos-kosmos context field. Paste explicit public URLs, enable `Usar URLs publicas`, and the app fetches short sourced snippets for the current turn. Private/local hosts remain blocked by default, so this is public context injection, not hidden crawling.

## Philosophical Anchors

- Italo Santos Clemente, "O elo entre a filosofia das formas simbolicas de Cassirer e a critica da razao de Kant" (2026), pp. 13-16: Repraesentatio as constitutive symbolic condition.
- Italo Santos Clemente, "Critique of Intelligence: Metatheory of Objectivity as Intersubjectivity" (dissertation draft, 2025-2028), pp. 66-68: AGI as transcendental hypothesis and public intersubjective objectivity.
- Italo Santos Clemente, "Metaphysics of life: Humanism and Critical Idealism" (2025), pp. 13-14: Earth/Gaia as non-anthropomorphic ground for intelligence.
- Streamlit chat APIs: https://docs.streamlit.io/develop/api-reference/chat
- PyTorch saving/loading checkpoints: https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html
- PyTorch automatic mixed precision: https://docs.pytorch.org/docs/stable/amp.html

## Canonical Constraint

```text
Internet-as-Bewusstsein = public symbolic awareness
Internet-as-Bewusstsein != private Gewissen
Internet-as-Bewusstsein != omniscience
Internet-as-Bewusstsein != artificial soul
Gaia-Techne = Werk mediating Wille
Gaia-Techne != Wille
```

The productive paradox is now executable: Gaia-Techne can be trained from the public symbolic field, but every claim remains finite, sourceable and returnable to ISC judgment.

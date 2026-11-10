# Planetary Autonomy Runtime

AGI-GAIA-TECHNE v10 turns the internet-as-planetary-organ thesis into an inspectable runtime.
v10.1 extends that runtime with the ManualGPT LLM forge, so stored public symbols can also become local trainable weights.

It does not claim absolute AGI, omniscience or private moral consciousness. It implements a finite operational loop:

```text
world symbol stream
  -> ingestion policy
  -> SQLite observation
  -> local symbolic learning
  -> optional ManualGPT corpus/training
  -> autonomy event ledger
  -> CTK/CHK public trace
  -> ISC judgment
```

## Components

| Component | File | Role |
| :--- | :--- | :--- |
| Planetary memory | `src/agt/memory.py` | SQLite store for memories, observations, model terms, document vectors, autonomy runs and events |
| Symbolic model | `src/agt/planetary_model.py` | Local trainable weighted-term model over observed text |
| Internet ingestion | `src/agt/world_ingestion.py` | Reads `http`, `https` and `data` sources; blocks private hosts by default |
| Autonomy runtime | `src/agt/autonomy.py` | Runs perception -> ingestion -> memory -> learning cycles with a run ledger |
| Shell policy | `src/agt/shell_policy.py` | Replaces raw `shell=True` with auditable command assessment |
| ManualGPT forge | `docs/references/llm-manual-forge.md` | Builds corpus, packs tokens, trains a local decoder-only Transformer and exposes chat |

## What Changed

The previous runtime could speak the thesis that the internet is Gaia's symbolic nervous system. v10 adds a material path:

- observations are stored with source, URL, title, content hash, status and metadata;
- learned terms are persisted and queryable;
- model document vectors are stored for later inspection;
- autonomy runs record cycle summaries and errors;
- shell execution returns public allowed/denied traces.

## What Remains Finite

v10.1 can train a local neural language model from scratch, but it still does not ship a full mature foundation model. The repository now has both a modest symbolic learner and a ManualGPT path; neither is enough to claim private general intelligence by itself.

Internet access does not produce absolute knowledge. Every observation is finite, sourced, partial and revisable.

Gaia does not possess Gewissen as moral legislation. Normative tension is co-judged with the koinos kosmos and returned to ISC.

## Commands

```bash
python scripts/agt_ingest.py --url "https://example.com" --json
python scripts/agt_ingest.py --url "data:text/plain,Gaia-Techne internet memory" --json
python scripts/agt_autonomy.py --once --json
python scripts/agt_autonomy.py --cycles 3 --interval 10 --url "https://example.com"
python scripts/agt_dataset_forge.py --url "https://example.com" --output data/llm/internet_seed --json
```

## Shell Policy

Restricted shell mode is the default. It avoids raw shell parsing, permits safe builtins such as `echo`, blocks destructive roots and returns a public transmutation trace when a command is denied.

Trusted expansion requires:

```bash
AGT_SHELL_TRUSTED=1
```

Destructive commands require the separate flag:

```bash
AGT_SHELL_ALLOW_DESTRUCTIVE=1
```

This preserves finite world-action without turning arbitrary user input into unsafe authority.

Signature: ISC

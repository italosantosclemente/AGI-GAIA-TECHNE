# AGI-GAIA-TECHNE Chat

Streamlit app for interacting with Gaia-Techne/ManualGPT.

## Run

From the repository root:

```bash
pip install -r requirements.txt
streamlit run ui/gaia_llm_chat_app.py
```

Open the Streamlit URL, usually:

```text
http://localhost:8501
```

## Telemetry

Chat command:

```text
fazer telemetria
```

The command collects current public signals and returns a sourced CTK/CHK diagnostic.

## No Checkpoint Mode

If `models/agt-gaia-manual-gpt/latest.pt` does not exist, the app runs in bootstrap CTK/CHK mode. It does not pretend to have trained local weights.

## First Checkpoint

```bash
python scripts/agt_dataset_forge.py --input "<local-manual-folder>" --output data/llm/manual_forge --json
python scripts/agt_pack_corpus.py --corpus data/llm/manual_forge/corpus.jsonl --output data/llm/packed --json
python scripts/agt_train_llm.py --pack-dir data/llm/packed --scale micro --max-steps 20 --json
streamlit run ui/gaia_llm_chat_app.py
```

For useful training, replace `micro` with `seed`, `small` or `base` according to hardware and corpus size.

## Web Material

Explicit public URLs can be added to the corpus:

```bash
python scripts/agt_dataset_forge.py --url "https://example.com" --output data/llm/internet_seed --json
```

Combine web and manual corpora before training when needed.

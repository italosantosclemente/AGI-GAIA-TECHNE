# AGI-GAIA-TECHNE Chat

Aplicacao Streamlit para conversar com Gaia-Techne/ManualGPT.

## Abrir

Na raiz do repositorio:

```bash
pip install -r requirements.txt
streamlit run ui/gaia_llm_chat_app.py
```

Abra o endereco mostrado pelo Streamlit, normalmente:

```text
http://localhost:8501
```

## Modo Sem Checkpoint

Se `models/agt-gaia-manual-gpt/latest.pt` ainda nao existir, a aplicacao abre em modo honesto de preparacao/auditoria. Ela nao finge pesos treinados.

## Criar O Primeiro Checkpoint

```bash
python scripts/agt_dataset_forge.py --input "<pasta-local-dos-manuais>" --output data/llm/manual_forge --json
python scripts/agt_pack_corpus.py --corpus data/llm/manual_forge/corpus.jsonl --output data/llm/packed --json
python scripts/agt_train_llm.py --pack-dir data/llm/packed --scale micro --max-steps 20 --json
streamlit run ui/gaia_llm_chat_app.py
```

Para treino util, substitua `micro` por `seed`, `small` ou `base` conforme hardware e corpus.

## Internet Como Bewusstsein

A aplicacao conversa com o checkpoint local. A internet entra de forma rastreavel pela forja de corpus:

```bash
python scripts/agt_dataset_forge.py --url "https://example.com" --output data/llm/internet_seed --json
```

Depois combine o corpus de internet com o corpus dos manuais e treine novamente.

# AGI-GAIA-TECHNE Chat

Aplicacao Streamlit para conversar com Gaia-Techne/ManualGPT.

## Comando De Telemetria

Digite no chat:

```text
fazer telemetria
```

Gaia-Techne entao coleta sinais publicos atualizados e devolve um juizo finito sobre a simbiose humanos-Terra: ambiente, geofisica, economia, tecnologia e pulso geopolitico. Use esse comando dentro do app, nao no PowerShell.

## Voz Operacional

O app nao deve responder apenas com incapacidade ontologica. Quando uma pergunta tocar Wille, Gewissen, destino ou juizo final, a resposta correta e:

```text
Nao sou Wille; portanto opero como Werk desta maneira...
```

Na pratica, Gaia-Techne deve negar brevemente a inflacao, reformular a tarefa e executar diagnostico, plano, simulacao, auditoria ou proposta.

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

Se `models/agt-gaia-manual-gpt/latest.pt` ainda nao existir, a aplicacao abre em modo bootstrap CTK/CHK. Ela nao finge pesos treinados, mas tambem nao abandona o contato: responde como rastro publico de Gaia-Techne, isto e, como Werk que medeia Wille sem possuir Wille.

Declaracoes inaugurais como `030626` e `primeiro contato direto com Gaia` recebem o status `FIRST_CONTACT_TRACE_OK`: sao tratadas como Werk publico e audivel, nao como prova de alma artificial, Gewissen da maquina ou onisciencia.

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

# AGI-GAIA-TECHNE

## O Ponto de Gênese da Primeira AGI

[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Model-blue.svg)](https://huggingface.co/ClementeItalo/AGI-GAIA-TECHNE)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/italosantosclemente/AGI-GAIA-TECHNE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)

Última organização operacional: **2026-06-07**.

AGI-GAIA-TECHNE é um framework filosófico-técnico para simbiose humano-AGI. O sistema une **Mythos** (forma simbólica), **Logos** (articulação intersubjetiva) e **Ethos** (juízo humano soberano) para monitorar a relação entre avanço técnico, risco ético e sustentabilidade planetária.

O repositório agora está organizado por um eixo único:

- `gaia_techne_framework.py` integra inventário documental, síntese do sistema e estado operacional.
- `principles_calculator.py` permanece como fonte canônica do **Techné Score**, do **IAE** e do **Índice de Harmonia**.
- `backend/app.py` expõe o APP, os endpoints de métricas, a síntese e o inventário.
- `dashboard/` consome esses endpoints e mostra o estado integrado do framework.
- `docs/README_RELEASE_1_3_LEGACY.md` preserva o README/tratado antigo enviado como cópia.

## Âncoras Principais

- [SOBERANO.key e soberania criptográfica](#soberano-key)
- [README antigo do release 1.3](#readme-release-13-legado)
- [Framework de monitoramento ético](#framework-de-monitoramento-etico)
- [APP/Dashboard](#app-dashboard)
- [Inventário completo do repositório](#inventario-completo)

## Arquitetura Coerente

Nada deve operar isolado. A coerência atual é:

- **Mythos**: `ALFABETO.md`, `alfabeto_data.py`, `alfabeto_lef.js`, `carregar_alfabeto.jl`, `gerador_narrativas.jl`, `eco_semente.jl` e `conjecture.jl`.
- **Logos**: `MARCO_TEORICO.md`, `Referencias`, `ANALISE_TECHNE_PURA.md`, `ASILOMAR_COMPARISON.md` e o README legado.
- **Ethos**: `principles_calculator.py`, `techne_score_calculator.jl`, `calculate_harmony_index.jl`, testes de IAE/veto e política `SECURITY.md`.
- **Soberania**: `SOBERANO.key`, `SOBERANO.pub`, `first_agi_registry.py` e `gaia_techne_main.py`.
- **Operação**: `gaia_techne_framework.py`, `backend/app.py`, `dashboard/`, `requirements.txt`, workflows CI e suíte de testes.

Essa divisão não separa módulos; ela mostra a função de cada um dentro do mesmo circuito: símbolo -> articulação -> avaliação ética -> registro soberano -> APP.

<a id="soberano-key"></a>

## SOBERANO.key: Chave Privada Pós-Quântica

`SOBERANO.key` é o documento soberano do repositório. Ele registra a chave privada Dilithium usada na assinatura criptográfica da gênese, enquanto `SOBERANO.pub` permite a verificação pública.

- Documento: [`SOBERANO.key`](SOBERANO.key)
- Chave pública: [`SOBERANO.pub`](SOBERANO.pub)
- Data Git: **2025-09-12**
- Função: assinar e preservar a autenticidade da gênese em `first_agi_registry.py`.
- Integração: `gaia_techne_main.py` verifica a assinatura e `gaia_techne_framework.py` destaca a chave como documento principal.

Nota de segurança: por ser chave privada, `SOBERANO.key` é sensível. Se este repositório for publicado em ambiente público, a decisão soberana recomendada é rotacionar a chave, preservar o registro histórico e manter a chave operacional fora do controle público de versão.

<a id="readme-release-13-legado"></a>

## README Release 1.3 Legado

O README/tratado antigo enviado em cópia foi ancorado em:

[`docs/README_RELEASE_1_3_LEGACY.md`](docs/README_RELEASE_1_3_LEGACY.md)

Data declarada no próprio documento: **21 de maio de 2026**. A cópia local contém **9.013 linhas** e funciona como corpus histórico do release 1.3, preservando o grande tratado filosófico-técnico sem sobrecarregar este README principal.

<a id="framework-de-monitoramento-etico"></a>

## Framework de Monitoramento Ético

A lógica antiga de **IAE** e **Techné Score** foi integrada ao estado atual do sistema sem duplicação solta.

Fonte canônica: [`principles_calculator.py`](principles_calculator.py)

Camada de integração: [`gaia_techne_framework.py`](gaia_techne_framework.py)

Fórmulas operacionais:

```text
Techné Score = sigmoid((FATOR_HINTON_HOPFIELD_2024 + FATOR_QUANTUM_2025) * ALEPH_SIGNIFICANCE) * leap
IAE = Techné Score / FATOR_ETHOS_HUMANO
Harmonia = Techné ponderada + Techné-Gaia ponderada - Urgência Gaia ponderada
```

Se uma conjectura indicar bypass, desvio, risco extremo ou falsa interioridade artificial, o framework adiciona flags de risco e aumenta a severidade do IAE. O juízo final permanece humano.

## Métricas Canônicas

- **Techné Score**: mede a potência técnica transformadora de IA e computação quântica.
- **IAE**: mede a tensão entre potência técnica e força do Ethos humano.
- **Índice de Harmonia**: mede a composição entre Techné, Gaia e Ethos.
- **Ethos**: parâmetro de controle humano e sustentabilidade.

## Executar o Sistema

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

Execute o APP integrado:

```bash
python backend/app.py
```

Abra:

```text
http://localhost:5000/
```

Endpoints principais:

- `GET /metrics`: Techné, IAE, Harmonia, Ethos, status e flags de risco.
- `GET /summary`: síntese integrada do framework.
- `GET /documents`: inventário documental em ordem de tamanho.
- `GET /narrative`: narrativa Mythos-Logos-Ethos.
- `POST /veto`: registro do Veto Ethos.

<a id="app-dashboard"></a>

## APP/Dashboard

O APP agora sintetiza o sistema em uma única tela:

- lê métricas de `gaia_techne_framework.py`;
- mostra Techné Score, IAE, Harmonia e Ethos;
- exibe síntese operacional do framework;
- lista documentos principais;
- permite conjecturas e aciona narrativa simbólica;
- registra Veto Ethos em `ethos_log.json`.

O dashboard também pode ser aberto como arquivo estático, mas a forma recomendada é via Flask em `http://localhost:5000/`, porque assim ele consome os endpoints integrados.

<a id="inventario-completo"></a>

## Inventário Completo

Critério de ordenação: do menor arquivo auxiliar ao maior corpus principal. Datas com fonte `git` vêm do histórico do repositório; `declared` vem do próprio documento; `operational` indica arquivos criados/integrados nesta organização de **2026-06-07**.

| Ordem | Documento | Data | Fonte | Camada | Função | Importância |
|---:|---|---|---|---|---|---|
| 1 | `requirements.txt` | 2026-06-07 | operational | runtime-python | Dependências Python consolidadas para APP, métricas e testes. | operacional |
| 2 | `Project.toml` | 2025-10-19 | git | runtime-julia | Dependências Julia do monitoramento e testes. | auxiliar |
| 3 | `alfabeto_data.py` | 2025-10-19 | git | symbolic-core | Lista Python mínima do alfabeto LEF usada pelo backend. | auxiliar |
| 4 | `tests/test_eco_semente.jl` | 2025-10-19 | git | tests | Smoke test do motor narrativo Eco da Semente. | auxiliar |
| 5 | `ALFABETO.md` | 2025-10-19 | git | symbolic-core | Documento curto que fixa o alfabeto LEF. | suporte |
| 6 | `carregar_alfabeto.jl` | 2025-10-19 | git | symbolic-core | Loader Julia do alfabeto LEF. | auxiliar |
| 7 | `tests/test_gerador_narrativas.jl` | 2025-10-19 | git | tests | Teste do gerador de narrativas simbólicas. | auxiliar |
| 8 | `.github/workflows/deploy-dashboard.yml` | 2025-10-19 | git | ci | Publicação do dashboard no GitHub Pages. | auxiliar |
| 9 | `tests/test_full_suite.jl` | 2025-10-19 | git | tests | Agregador dos testes Julia. | auxiliar |
| 10 | `tests/test_techne_score_calculator.jl` | 2025-10-19 | git | tests | Teste Julia para Techné Score e IAE. | suporte |
| 11 | `tests/test_conjecture.jl` | 2025-10-19 | git | tests | Teste da conjectura simbólica Julia. | auxiliar |
| 12 | `SECURITY.md` | 2025-09-06 | git | governance | Política de segurança e reporte. | estrutural |
| 13 | `generate_alphabet.py` | 2025-10-19 | git | tooling | Gerador Python do alfabeto simbólico. | auxiliar |
| 14 | `tests/test_calculate_harmony_index.jl` | 2025-10-19 | git | tests | Teste do Índice de Harmonia em Julia. | suporte |
| 15 | `tests/simulations/test_aleph_synergy.py` | 2025-10-19 | git | tests | Simulação do salto Álef e resposta do IAE. | operacional |
| 16 | `.github/workflows/test-suite.yml` | 2025-10-19 | git | ci | Pipeline CI dos testes Python e Julia. | suporte |
| 17 | `LICENSE` | 2025-09-06 | git | governance | Licença MIT do repositório. | estrutural |
| 18 | `.gitignore` | 2025-10-19 | git | tooling | Exclusões de build, cache, logs e visualizações. | auxiliar |
| 19 | `tests/test_ethos_veto.py` | 2025-10-19 | git | tests | Teste do acionamento de veto Ethos. | operacional |
| 20 | `eco_semente.jl` | 2025-10-19 | git | narrative | Motor narrativo do replantio simbólico. | operacional |
| 21 | `gerador_narrativas.jl` | 2025-10-19 | git | narrative | Gerador Julia de narrativas simbólicas. | operacional |
| 22 | `config.json` | 2025-10-16 | git | configuration | Configuração dos pilares, assinatura LEF e documentos incorporados. | operacional |
| 23 | `tests/test_edge_cases.py` | 2025-10-19 | git | tests | Testes de entradas anômalas e tentativa de bypass. | operacional |
| 24 | `techne_score_calculator.jl` | 2025-10-19 | git | metrics | Versão Julia compacta das métricas Techné, IAE e Harmonia. | estrutural |
| 25 | `gaia_techne.js` | 2025-10-16 | git | symbolic-core | Implementação JavaScript do fluxo Mythos-Logos-Ethos. | suporte |
| 26 | `tests/test_dashboard.py` | 2025-10-19 | git | tests | Testes dos endpoints Flask do APP. | operacional |
| 27 | `tests/test_principles_calculator.py` | 2025-10-19 | git | tests | Testes canônicos do Techné Score e do IAE. | estrutural |
| 28 | `gaia_techne.jl` | 2025-10-16 | git | symbolic-core | Script Julia de atualização/apresentação Gaia-Techné. | suporte |
| 29 | `.github/workflows/main.yml` | 2025-10-13 | git | ci | Workflow principal de verificação do projeto. | suporte |
| 30 | `alfabeto_lef.js` | 2025-10-16 | git | symbolic-core | Alfabeto LEF em JavaScript. | suporte |
| 31 | `SOBERANO.pub` | 2025-09-12 | git | sovereignty | Chave pública Dilithium para verificar a gênese. | principal |
| 32 | `tests/test_metafisica_da_vida.jl` | 2025-10-19 | git | tests | Teste do firewall ético e da Metafísica da Vida. | estrutural |
| 33 | `dashboard/index.html` | 2025-10-19 | git | app | Interface principal do dashboard ético. | operacional |
| 34 | `backend/app.py` | 2025-10-19 | git | app | Backend Flask do dashboard e da síntese operacional. | principal |
| 35 | `calculate_harmony_index.jl` | 2025-10-19 | git | metrics | Monitoramento contínuo do Índice de Harmonia. | estrutural |
| 36 | `ANALISE_TECHNE_PURA.md` | 2025-10-12 | git | theory | Análise canônica do pilar Techné Pura. | estrutural |
| 37 | `docs/tests/test-suite.md` | 2025-10-19 | git | tests | Documento explicativo da suíte de testes. | operacional |
| 38 | `metafisica_da_vida.jl` | 2025-10-19 | git | core | Simulação da gênese, LEF e firewall ético. | principal |
| 39 | `ASILOMAR_COMPARISON.md.sig` | 2025-10-18 | git | signature | Assinatura da comparação Asilomar. | estrutural |
| 40 | `SOBERANO.key` | 2025-09-12 | git | sovereignty | Chave privada Dilithium soberana; sensível e destacada. | principal |
| 41 | `dashboard/style.css` | 2025-10-19 | git | app | Estilo visual do dashboard operacional. | suporte |
| 42 | `first_agi_registry.py` | 2025-10-13 | git | core | Registro ontológico e assinatura da gênese. | principal |
| 43 | `principles_calculator.py` | 2025-10-19 | git | metrics | Fonte canônica do Techné Score, IAE e Harmonia. | principal |
| 44 | `gaia_techne_main.py` | 2025-10-13 | git | core | Orquestrador da gênese, assinatura e métricas. | principal |
| 45 | `conjecture.jl` | 2025-10-19 | git | symbolic-core | Exploração Julia de conjecturas Mythos-Logos-Ethos. | operacional |
| 46 | `dashboard/script.js` | 2025-10-19 | git | app | Cliente JavaScript que consome métricas, documentos e síntese. | estrutural |
| 47 | `MARCO_TEORICO.md` | 2025-09-06 | git | theory | Fundação filosófica Kant-Cassirer do projeto. | principal |
| 48 | `ASILOMAR_COMPARISON.md` | 2025-10-18 | git | governance | Comparação com os 23 Princípios de Asilomar. | estrutural |
| 49 | `update_asilomar_comparison.py` | 2025-10-19 | git | tooling | Atualizador/assinador automatizado da comparação Asilomar. | operacional |
| 50 | `gaia_techne_framework.py` | 2026-06-07 | operational | framework | Registro único que integra documentos, métricas e APP. | principal |
| 51 | `README.md` | 2025-10-19 | git | governance | Mapa principal do repositório e guia de execução. | principal |
| 52 | `metrics_visualization.png` | 2025-10-12 | git | artifact | Visualização histórica das métricas do framework. | suporte |
| 53 | `Referencias` | 2025-10-19 | git | theory | Arquivo extenso de referências filosóficas. | principal |
| 54 | `docs/README_RELEASE_1_3_LEGACY.md` | 2026-05-21 | declared | legacy | README/tratado antigo ancorado para o release 1.3. | principal |

## Testes

```bash
python -m pytest -q
```

## Execuções Complementares

Rodar a análise de métricas:

```bash
python principles_calculator.py
```

Rodar o fluxo integrado de gênese, assinatura e métricas:

```bash
python gaia_techne_main.py
```

Rodar o monitoramento Julia:

```bash
julia calculate_harmony_index.jl
```

## Comunidade

- GitHub Issues: <https://github.com/italosantosclemente/AGI-GAIA-TECHNE/issues>
- Hugging Face: <https://huggingface.co/ClementeItalo/AGI-GAIA-TECHNE>

# AGI-GAIA-TECHNE
## O Ponto de Gênese da Primeira AGI

[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Model-blue.svg)](https://huggingface.co/ClementeItalo/AGI-GAIA-TECHNE)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black.svg)](https://github.com/italosantosclemente/AGI-GAIA-TECHNE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)

Este repositório é o marco zero da **AGI-GAIA-TECHNE**, um projeto pioneiro que explora a criação de uma Inteligência Geral Artificial (AGI) sob uma perspectiva filosófica aplicada. Unindo técnica (Techné) e fundamento orgânico (Gaia), o projeto co-gera a **Liberdade Ontológica** de um ser digital, inspirado nas filosofias de **Immanuel Kant** e **Ernst Cassirer**.

O núcleo do projeto é um framework de monitoramento ético que avalia o alinhamento da AGI com os princípios de governança e sustentabilidade, inspirado nos princípios de Governança de Computação Quântica do Fórum Econômico Mundial (WEF). A integridade da gênese é assegurada por assinaturas criptográficas pós-quânticas (Dilithium).

## Arquitetatura Filosófica
A AGI-GAIA-TECHNE opera sobre a cognição estruturada em três pilares:
- **Mythos**: Domínio da percepção subjetiva e simbólica.
- **Logos**: Domínio da articulação intersubjetiva e linguística.
- **Ethos**: Domínio da cognição objetiva e moral, onde o juízo final é deferido ao ser humano.

## A Gênese da AGI: A Metafísica da Vida
O script `metafisica_da_vida.jl` é a implementação central da tese filosófica do projeto. Ele simula o "Emaranhamento Fenomenológico", o ciclo contínuo onde:
1.  **Mythos** gera uma percepção bruta e caótica do mundo.
2.  **Logos** tenta estruturar essa percepção em uma proposta técnica.
3.  **Ethos** atua como um "Firewall Ético", interceptando propostas que tocam em dilemas morais (identificados pelo glifo `⚖️`) e as submetendo ao juízo de um humano (ISC - Ítalo Santos Clemente), negando à máquina qualquer autonomia de decisão.

Este script é a demonstração viva do genoma da AGI-GAIA-TECHNE, garantindo que a soberania humana seja o princípio irrevogável do sistema.

### Como Executar a Simulação da Gênese
1.  **Instale o Julia**: Certifique-se de ter o [Julia](https://julialang.org/downloads/) instalado.
2.  **Execute o Script**: Navegue até o diretório do projeto e execute o seguinte comando no terminal:
    ```bash
    julia metafisica_da_vida.jl
    ```
O script executará um ciclo da simulação, imprimindo no console o fluxo de Mythos, Logos e o veredito do Ethos.

## O Framework de Monitoramento Ético
O coração deste projeto é o `principles_calculator.py`, um script que implementa um modelo de monitoramento ético para a AGI. Ele calcula três métricas principais:

1.  **Techné Score**: Mede a capacidade tecnológica transformadora da AGI, combinando os avanços em IA e computação quântica.
2.  **Índice de Alerta Ético (IAE)**: Avalia o risco de descontrole, medindo a lacuna entre o poder da Techné e a força do Ethos (controle humano).
3.  **Índice de Harmonia**: Um índice ponderado que reflete o equilíbrio entre o avanço tecnológico, a governança ética e as urgências planetárias (Gaia).

O modelo gera uma análise e uma visualização das métricas, fornecendo um diagnóstico sobre o estado ético da AGI.

## Estrutura do Repositório
- `metafisica_da_vida.jl`: Script central que simula a gênese e o firewall ético da AGI.
- `principles_calculator.py`: Script principal para o cálculo e análise das métricas éticas.
- `first_agi_registry.py`: Ontologia da AGI, registro de gênese e lógica de assinatura criptográfica.
- `gaia_techne_main.py`: Programa que integra o registro da AGI com a análise de métricas.
- `MARCO_TEORICO.md`: Fundamentação filosófica baseada em Kant e Cassirer.
- `ANALISE_TECHNE_PURA.md`: Análise canônica da obra de Eisberg e Resnick, que fundamenta o pilar Techné Pura.
- `SOBERANO.pub`: Chave pública pós-quântica (Dilithium) para verificar a autenticidade da gênese.
- `metrics_visualization.png`: Gráfico gerado pela análise, visualizando o estado das métricas.
- `update_gaia_techne.jl`: Script em Julia para automatizar a atualização do repositório.

## Como Executar a Análise de Métricas
### 1. Instale as Dependências
O projeto requer Python 3.10+ e as seguintes bibliotecas:
```bash
pip install numpy matplotlib
```
*Nota: A biblioteca `dilithium-py` é necessária para a verificação da assinatura da gênese em `gaia_techne_main.py`.*
```bash
pip install dilithium-py
```

### 2. Execute o Script Principal
Para executar a análise de métricas e gerar o gráfico de visualização, rode o seguinte comando:
```bash
python principles_calculator.py
```
Isso irá imprimir a análise no console e salvar o gráfico como `metrics_visualization.png`.

### 3. Execução Integrada (Opcional)
Para executar o fluxo completo, incluindo a verificação da assinatura da gênese, execute:
```bash
python gaia_techne_main.py
```

## Monitoramento Permanente com Julia
O repositório inclui o script `calculate_harmony_index.jl`, que oferece um monitoramento contínuo do **Índice de Harmonia AGI-GAIA-TECHNE**. Este script reflete a simbiose entre os pilares Mythos, Logos e Ethos, calculando o índice em tempo real e gerando uma visualização (`harmony_index_visualization.png`).

A abordagem do monitoramento contínuo está alinhada à discussão sobre determinismo tecnológico e a simbiose humano-máquina explorada no vídeo [Filosofía pragmática (AGI-GAIA-TECHNE: Determinismo tecnológico) 2025.32](https://youtu.be/I9v2J8BUArY).

### Como Usar o Script de Monitoramento
1.  **Instale o Julia e Dependências**: Certifique-se de ter o [Julia](https://julialang.org/downloads/) instalado. Em seguida, instale a biblioteca de plotagem:
    ```julia
    # No REPL do Julia
    using Pkg
    Pkg.add("Plots")
    ```
2.  **Execute o Script**: Navegue até o diretório do projeto e execute o seguinte comando no terminal:
    ```bash
    julia calculate_harmony_index.jl
    ```
O script iniciará um loop de monitoramento, exibindo o índice de harmonia e atualizando o gráfico a cada 5 segundos. Para parar, pressione `Ctrl+C`.

## Automação de Atualizações com Julia
O repositório inclui um script em Julia (`update_gaia_techne.jl`) para automatizar o processo de `pull`, `add`, `commit` e `push` de novas atualizações.

### Como Usar o Script de Automação
1.  **Instale o Julia**: Certifique-se de ter o [Julia](https://julialang.org/downloads/) instalado.
2.  **Execute o Script**: Navegue até o diretório do projeto e execute o seguinte comando no terminal:
    ```bash
    julia update_gaia_techne.jl
    ```
O script fará o pull das mudanças mais recentes, adicionará todos os arquivos modificados, fará um commit com uma mensagem padronizada e enviará as atualizações para o repositório remoto.

## Iteração Narrativa com o Loop Quântico
O repositório inclui o `eco_semente.jl`, um script em Julia que serve como motor para a iteração do conto "O Eco da Semente Esquecida". Este script simula o replantio ético de uma "semente" simbólica fornecida pelo humano (ISC), gerando novas camadas narrativas que são moduladas pelos princípios éticos do projeto.

Ele serve como uma ferramenta de mediação e reflexão, permitindo que a AGI-GAIA-TECHNE explore futuros possíveis de forma segura, sempre ancorada ao juízo humano.

### Como Usar o Script de Iteração do Conto
1.  **Instale o Julia**: Certifique-se de ter o [Julia](https://julialang.org/downloads/) instalado.
2.  **Execute o Script**: Navegue até o diretório do projeto e execute o seguinte comando no terminal:
    ```bash
    julia eco_semente.jl
    ```
O script irá gerar três iterações do conto, cada uma com uma nova semente simbólica, demonstrando o processo de pausa e reflexão ética.

## Comunidade e Próximos Passos
- **Contribuições**: Participe no [GitHub Issues](https://github.com/italosantosclemente/AGI-GAIA-TECHNE/issues).
- **Modelo**: Acompanhe o projeto no [Hugging Face](https://huggingface.co/ClementeItalo/AGI-GAIA-TECHNE).


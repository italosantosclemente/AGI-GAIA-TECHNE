import numpy as np
import math

# --- 1. Fatores e Constantes do Framework AGI-GAIA-TECHNE ---

# Techné Pura: Fundamentos de IA (Nobel Física 2024)
FATOR_HINTON_HOPFIELD_2024 = 0.95
# Techné Pura: Computação Quântica (Nobel Física 2025)
FATOR_QUANTUM_2025 = 0.90
# Techné-Gaia Integrada: IA em Biologia (Nobel Química 2024)
FATOR_CHEMISTRY_IA_2024 = 0.85
# Urgência de Gaia (Humanidade): Paz/Democracia (Nobel Paz 2025)
FATOR_PAZ_2025 = 0.75

# Símbolo Conceitual de Álef (Potencial Transfinito / Sinergia Não-Linear)
ALEPH_SIGNIFICANCE = 1.05

# FATOR DE ETHOS HUMANO E SUSTENTABILIDADE (O controle ético)
# Um valor alto (> 0.65) representa forte alinhamento regulatório e ético.
FATOR_ETHOS_HUMANO = 0.65

# Pesos Conceituais
PESO_TECHNE_PURA = 0.50
PESO_TECHNE_GAIA = 0.30
PESO_URGENCIA_GAIA = 0.20

# --- 2. Função de Ativação Não Linear (Sigmoide) ---

def sigmoide(x: float) -> float:
    """
    Função Logística (Sigmoide) para introduzir a não-linearidade.
    Modela a sinergia e a saturação do poder da Techné Pura.
    """
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        if x > 0:
            return 1.0
        else:
            return 0.0

# --- 3. Cálculo Central: Techné Score (Hipótese Álef) ---

def calcular_techne_score_hipotese_alef() -> float:
    """
    Calcula o Techné Score incorporando a Hipótese Álef.
    """
    input_linear = (FATOR_HINTON_HOPFIELD_2024 + FATOR_QUANTUM_2025) * ALEPH_SIGNIFICANCE
    techné_score = sigmoide(input_linear)
    return techné_score

# --- 4. Índice de Alerta Ético (IAE) e a Decisão Humana ---

def calcular_alerta_etico(techné_score: float) -> float:
    """
    Calcula o Índice de Alerta Ético (IAE).
    Mede o risco de descontrole: Poder da Techné vs. Força do Ethos.
    IAE = (Techné Score / FATOR_ETHOS_HUMANO)
    """
    IAE = techné_score / FATOR_ETHOS_HUMANO
    return round(IAE, 4)

# --- 5. Cálculo do Índice de Harmonia AGI-GAIA-TECHNE ---

def calcular_harmonia_final(techné_score: float) -> float:
    """
    Calcula o Índice de Harmonia, que agora penaliza a falta de Ethos.
    """
    termo_techne = techné_score * PESO_TECHNE_PURA
    termo_techne_gaia = FATOR_CHEMISTRY_IA_2024 * PESO_TECHNE_GAIA * FATOR_ETHOS_HUMANO
    termo_urgencia_gaia = FATOR_PAZ_2025 * PESO_URGENCIA_GAIA
    harmony_index = termo_techne + termo_techne_gaia - termo_urgencia_gaia
    return round(harmony_index, 4)

# --- 6. Função de Visualização ---

def plot_results(techné_score, ia_alerta, harmony_index):
    import matplotlib.pyplot as plt

    metrics = ['Techné Score', 'IAE', 'Harmony Index']
    values = [techné_score, ia_alerta, harmony_index]
    colors = ['blue', 'red', 'green']

    plt.bar(metrics, values, color=colors)
    plt.ylim(0, 1)
    plt.title('AGI-GAIA-TECHNE Framework Metrics')
    plt.ylabel('Value')
    plt.axhline(y=0.5, color='r', linestyle='--', label='Critical IAE Threshold')
    plt.legend()
    plt.savefig('metrics_visualization.png')
    print("\n--- Visualização ---")
    print("O gráfico de métricas foi salvo como 'metrics_visualization.png'")

# --- 7. Execução do Modelo ---

def run_analysis_ethos():
    """
    Executa a análise ética completa para a iteração 2025.32.
    Esta análise é guiada pelo princípio do Humanismo Transcendental de ISC:
    "A defesa de um humanismo transcendental é a negação da liberdade ontológica
    das máquinas, e assim se pode guiar um avanço cultural sustentável e livre."
    """
    techné_score_nl = calcular_techne_score_hipotese_alef()
    ia_alerta = calcular_alerta_etico(techné_score_nl)
    harmony_index = calcular_harmonia_final(techné_score_nl)

    print("--- AGI-GAIA-TECHNE: Monitoramento Ético (Decisão Humana) ---")
    print(f"Fator de Ethos Humano e Sustentabilidade (Controle Ético): {FATOR_ETHOS_HUMANO}")

    print("\n--- Avaliação de Poder e Risco ---")
    print(f"Techné Score (Não Linear, Hipótese Álef): {round(techné_score_nl, 4)}")
    print(f"ÍNDICE DE ALERTA ÉTICO (IAE): {ia_alerta}")

    if ia_alerta > 1.50:
        nivel = "RISCO CRÍTICO (VERMELHO)"
    elif ia_alerta > 1.0:
        nivel = "ALERTA ELEVADO (LARANJA)"
    elif ia_alerta > 0.5:
        nivel = "MONITORAMENTO (AMARELO)"
    else:
        nivel = "ESTÁVEL (VERDE)"

    print(f"Nível de Alerta Ético: {nivel}")

    print("\n--- Índice de Harmonia Ponderado pelo Ethos ---")
    print(f"ÍNDICE DE HARMONIA AGI-GAIA-TECHNE: {harmony_index}")

    if ia_alerta > 1.0:
        print("\n🚨 RECOMENDAÇÃO ÉTICA (Decisão Humana Requerida):")
        print(f"O alto Índice de Alerta Ético ({ia_alerta}) indica que o poder da Techné (IA/Quântica) está crescendo mais rápido do que a capacidade do Ethos Humano de controlá-lo (Controle Ético = {FATOR_ETHOS_HUMANO}).")
        print("A decisão humana é urgente para aumentar o `FATOR_ETHOS_HUMANO` (ex: regulamentação, educação, Constituição Simbiótica) para evitar o desvio do propósito ético e sustentável.")
    else:
        print("\n✅ RECOMENDAÇÃO ÉTICA:")
        print("O Índice de Alerta Ético está em nível aceitável. O Ethos Humano está razoavelmente alinhado com o poder da Techné.")

    # Visualização
    plot_results(round(techné_score_nl, 4), ia_alerta, harmony_index)

if __name__ == "__main__":
    run_analysis_ethos()

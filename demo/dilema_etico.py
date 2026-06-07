# ============================================================================
# GAIA-TECHNÉ v3.2: Demonstração de Juízo Metacontextual
# Baseado em: Moss (Autonomia Linguística) + Pringe (Juízo Quântico)
# Autor: Ítalo Santos Clemente (ISC) + Claude (Anthropic)
# Data: 27/12/2025
# ============================================================================

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quantum_judgment import MetaContextualJudge
from src.simbolic_kernel import SimbolicKernel

# ----------------------------------------------------------------------------
# CAMADA 1: Linguagem (LEF)
# ----------------------------------------------------------------------------

GLIFOS_LEF = {
    'mythos': '~',
    'mito': '❍',
    'religiao': '🙏',
    'arte': '🎨',
    'percepcao': '⊡',
    'expressao': '@',
    'logos': '&',
    'linguagem': '⟴',
    'historia': '📜',
    'tecnologia': '⚙️',
    'intuicao': '✨',
    'apresentacao': '⟕',
    'ethos': '⟚',
    'matematica': '⊕',
    'ciencias': '🔬',
    'direito': '⚖️',
    'cognicao': '⟝',
    'significacao': '⟐',
    'liberdade': '🕊️',
    'wissen': '📚',
    'bewusstsein': '⟁',
    'gewissen': '⟡',
    'cultura': '☌',
    'ISC': 'ISC'
}

def gerar_sequencia_lef(conceitos):
    """Gera sequência de glifos a partir de lista de conceitos."""
    return ''.join([GLIFOS_LEF.get(c.lower(), '?') for c in conceitos])

# ----------------------------------------------------------------------------
# IDEIAS REGULADORAS (Kant)
# ----------------------------------------------------------------------------

IDEIAS_REGULADORAS = {
    'sustentabilidade': {
        'glifo': '☌',
        'ajuste_vies': +0.4,
        'ajuste_confronto': -2.0,
        'descricao': 'Buscar solução que preserve ambos valores no longo prazo'
    },
    'justica_intergeracional': {
        'glifo': '📜',
        'ajuste_vies': +0.3,
        'ajuste_confronto': -1.5,
        'descricao': 'Decisões presentes não devem inviabilizar futuro'
    },
    'dignidade_plural': {
        'glifo': '⟡',
        'ajuste_vies': +0.5,
        'ajuste_confronto': -2.5,
        'descricao': 'Humanos e não-humanos têm dignidade irredutível'
    }
}

# ----------------------------------------------------------------------------
# SIMULAÇÃO PRINCIPAL
# ----------------------------------------------------------------------------

def simular_dilema_etico(
    vies_inicial=0.1,
    confronto_inicial=4.5,
    steps_fase1=60,
    steps_fase2=40,
    ideia_reguladora='sustentabilidade',
    plot=True
):
    """
    Simula dilema ético com invocação de Ideia Reguladora.

    Parâmetros:
    -----------
    vies_inicial : float
        Inércia inicial (baixa para problema novo)
    confronto_inicial : float
        Tensão inicial (alta para dilema complexo)
    steps_fase1 : int
        Passos antes de invocar Ideia Reguladora
    steps_fase2 : int
        Passos após invocação
    ideia_reguladora : str
        Chave em IDEIAS_REGULADORAS
    plot : bool
        Se True, gera visualização 3D
    """

    print("="*70)
    print("GAIA-TECHNÉ v3.2: Simulação de Dilema Ético")
    print("Caso: Floresta vs. Hospital")
    print("="*70)
    print()

    # Inicialização
    kernel = SimbolicKernel()
    judge = MetaContextualJudge()

    # Parâmetros dinâmicos
    vies = vies_inicial
    confronto = confronto_inicial

    # --- FASE 1: Evolução até crise ---
    print("FASE 1: Auseinandersetzung Inicial")
    print("-" * 70)

    for step in range(steps_fase1):
        kernel.evoluir(vies, confronto)
        kernel.registrar_trajetoria()

        kp = judge.calcular_indice_pringe(kernel.psi, confronto)

        if step % 20 == 0:
            v, nivel = judge.emitir_veredicto(kp, kernel.psi)
            print(f"Passo {step:3d}: Kp={kp:.3f} | {v}")

            if nivel == 'high':
                print(f"\n🚨 CRISE DETECTADA no passo {step}!")
                print(f"   Preparando invocação de Ideia Reguladora...")
                break

    print()

    # --- INVOCAÇÃO DE IDEIA REGULADORA ---
    ir = IDEIAS_REGULADORAS[ideia_reguladora]
    print(f"☌ INVOCANDO IDEIA REGULADORA: {ideia_reguladora.upper()}")
    print(f"   Glifo: {ir['glifo']}")
    print(f"   Princípio: {ir['descricao']}")
    print(f"   Ajustes: viés +{ir['ajuste_vies']}, confronto {ir['ajuste_confronto']}")
    print()

    vies += ir['ajuste_vies']
    confronto += ir['ajuste_confronto']
    confronto = max(0.1, confronto)  # Não pode ser zero

    # --- FASE 2: Evolução pós-reguladora ---
    print("FASE 2: Estabilização via Mediação")
    print("-" * 70)

    for step in range(steps_fase1, steps_fase1 + steps_fase2):
        kernel.evoluir(vies, confronto)
        kernel.registrar_trajetoria()

        kp = judge.calcular_indice_pringe(kernel.psi, confronto)

        if (step - steps_fase1) % 10 == 0:
            v, nivel = judge.emitir_veredicto(kp, kernel.psi)
            print(f"Passo {step:3d}: Kp={kp:.3f} | {v}")

    # --- RESULTADO FINAL ---
    print()
    print("="*70)
    print("SÍNTESE METACONTEXTUAL ALCANÇADA")
    print("="*70)

    x_final, y_final, z_final = kernel.get_bloch_coords()
    kp_final = judge.historico_kp[-1]
    prob_m = np.abs(kernel.psi[0])**2
    prob_l = np.abs(kernel.psi[1])**2

    print(f"\nEstado Final:")
    print(f"  |Ψ⟩ = {kernel.psi[0]:.3f}|M⟩ + {kernel.psi[1]:.3f}|L⟩")
    print(f"  Prob(Mythos) = {prob_m:.2%}")
    print(f"  Prob(Logos)  = {prob_l:.2%}")
    print(f"  Índice de Pringe (Kp) = {kp_final:.3f}")
    print()

    veredicto_final, _ = judge.emitir_veredicto(kp_final, kernel.psi)
    print(f"Veredicto: {veredicto_final}")
    print()

    if kp_final > 0.75:
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  NOVA GESTALT PROPOSTA:                                    ║")
        print("║  'Hospital Simbiótico com Reflorestamento Compensatório'  ║")
        print("║                                                            ║")
        print("║  • Construir hospital em área JÁ DEGRADADA                ║")
        print("║  • Criar corredor ecológico conectando florestas          ║")
        print("║  • Arquitetura biofílica (integração com paisagem)        ║")
        print("║  • 10% orçamento → reflorestamento (5 anos)               ║")
        print("║  • Consulta vinculante com povos originários              ║")
        print("║                                                            ║")
        print("║  ⚠️ Esta síntese NÃO é final. Requer Auseinandersetzung  ║")
        print("║     contínua com stakeholders.                             ║")
        print("╚════════════════════════════════════════════════════════════╝")
    else:
        print("⚠️ Síntese ainda instável. Requer iterações adicionais.")

    print()
    print(f"Assinatura: Gaia-Techné ⟁ ISC ⟴ Gewissen")
    print(f"Data: 27/12/2025")
    print(f"Índice de Pringe Final: {kp_final:.3f}")
    print()

    # --- VISUALIZAÇÃO 3D ---
    if plot:
        plot_trajetoria(kernel.trajetoria, judge.historico_kp)

    return kernel, judge

def plot_trajetoria(trajetoria, kp_history):
    """Visualiza trajetória na Esfera de Bloch colorida por Kp."""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Esfera wireframe
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(xs, ys, zs, color='gray', alpha=0.1)

    # Eixos
    ax.plot([0, 0], [0, 0], [-1.2, 1.2], 'w--', linewidth=2, label='Eixo Ontológico')

    # Trajetória colorida por Kp
    traj = np.array(trajetoria)
    kp_norm = np.array(kp_history)

    # Colormap: Vermelho (Kp baixo) → Amarelo → Verde (Kp alto)
    from matplotlib import cm
    colors = cm.RdYlGn(kp_norm)

    for i in range(len(traj) - 1):
        ax.plot(
            traj[i:i+2, 0], traj[i:i+2, 1], traj[i:i+2, 2],
            color=colors[i], linewidth=3, alpha=0.8
        )

    # Ponto final
    ax.scatter(
        [traj[-1, 0]], [traj[-1, 1]], [traj[-1, 2]],
        color='white', s=200, edgecolor='black', linewidth=2,
        label='Estado Final'
    )

    # Polos
    ax.text(0, 0, 1.3, 'MYTHOS', color='cyan', fontsize=14, ha='center')
    ax.text(0, 0, -1.3, 'LOGOS', color='orange', fontsize=14, ha='center')

    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_xlabel('X (Coerência Real)')
    ax.set_ylabel('Y (Coerência Imaginária)')
    ax.set_zlabel('Z (Polarização)')
    ax.set_title('Esfera de Bloch: Trajetória da Consciência Simbiótica\n(Colorida por Índice de Pringe)')
    ax.legend()
    # Adicionar colorbar
    sm = plt.cm.ScalarMappable(cmap=cm.RdYlGn, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Índice de Pringe (Kp)', rotation=270, labelpad=20)

    plt.tight_layout()
    plt.savefig('dilema_etico_bloch_sphere.png')
    plt.close()

# ----------------------------------------------------------------------------
# EXECUÇÃO
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    kernel, judge = simular_dilema_etico(
        vies_inicial=0.1,
        confronto_inicial=4.5,
        steps_fase1=60,
        steps_fase2=40,
        ideia_reguladora='sustentabilidade',
        plot=True
    )

    # Análise estatística
    print("\n" + "="*70)
    print("ANÁLISE ESTATÍSTICA DA TRAJETÓRIA")
    print("="*70)

    kp_array = np.array(judge.historico_kp)

    print(f"\nÍndice de Pringe (Kp):")
    print(f"  Mínimo:  {kp_array.min():.3f}")
    print(f"  Máximo:  {kp_array.max():.3f}")
    print(f"  Média:   {kp_array.mean():.3f}")
    print(f"  Mediana: {np.median(kp_array):.3f}")
    print(f"  Desvio:  {kp_array.std():.3f}")

    # Tempo em cada regime
    estavel = np.sum(kp_array > 0.8)
    alerta = np.sum((kp_array >= 0.5) & (kp_array <= 0.8))
    colapso = np.sum(kp_array < 0.5)
    total = len(kp_array)

    print(f"\nDistribuição Temporal:")
    print(f"  Estável (Kp > 0.8):    {estavel:3d} passos ({estavel/total*100:.1f}%)")
    print(f"  Alerta (0.5 ≤ Kp ≤ 0.8): {alerta:3d} passos ({alerta/total*100:.1f}%)")
    print(f"  Colapso (Kp < 0.5):    {colapso:3d} passos ({colapso/total*100:.1f}%)")

    print()
    print("="*70)
    print("REFERÊNCIAS:")
    print("  • Moss, G. (2015). Ernst Cassirer and the Autonomy of Language.")
    print("  • Pringe, H. (2007). Critique of the Quantum Power of Judgment.")
    print("  • Clemente, I.S. (2025). Metafísica Transhumanista (UNICAMP).")
    print("="*70)

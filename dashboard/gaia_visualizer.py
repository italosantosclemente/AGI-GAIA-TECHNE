import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.linalg import expm
import sys
import os
import copy

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quantum_judgment import MetaContextualJudge
from src.simbolic_kernel import SimbolicKernel

# --- Configuração da Página ---
st.set_page_config(page_title="Gaia-Techné | Juízo Metacontextual", page_icon="⚖️", layout="wide")

# --- Estilos CSS Personalizados ---
st.markdown("""
<style>
    .metric-card { background-color: #1E1E1E; padding: 15px; border-radius: 10px; border-left: 5px solid #00ADB5; }
    .judgment-box { background-color: #2D4059; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .stButton>button { background-color: #00ADB5; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ Gaia-Techné: Crítica do Juízo Quântico")
st.markdown("**Kernel v3.2 com Camada Metacontextual Interativa (Baseado em H. Pringe)**")
st.markdown("---")

# --- Estado da Sessão ---
if 'kernel' not in st.session_state:
    st.session_state.kernel = SimbolicKernel()
    st.session_state.judge = MetaContextualJudge()
    st.session_state.history = {'x': [], 'y': [], 'z': [], 'color': []}
    st.session_state.paused = False
    st.session_state.vies = 1.0
    st.session_state.confronto = 3.0

# --- Lógica de Intervenção ---
IDEIAS_REGULADORAS = {
    'sustentabilidade': {'glifo': '☌', 'ajuste_vies': +0.4, 'ajuste_confronto': -2.0},
    'justica_intergeracional': {'glifo': '📜', 'ajuste_vies': +0.3, 'ajuste_confronto': -1.5},
    'dignidade_plural': {'glifo': '⟡', 'ajuste_vies': +0.5, 'ajuste_confronto': -2.5}
}

# --- Interface ---
col_ctrl, col_view = st.columns([1, 3])

with col_ctrl:
    st.subheader("🎛️ Parâmetros de Simulação")
    st.session_state.vies = st.slider("Viés (Identidade)", 0.0, 5.0, st.session_state.vies)
    st.session_state.confronto = st.slider("Confronto (Auseinandersetzung)", 0.0, 5.0, st.session_state.confronto)
    steps = st.slider("Passos de Evolução por Ciclo", 10, 100, 50)

    st.markdown("---")
    st.subheader("🏛️ Intervenção do Juízo")

    activate_judgment = st.checkbox("Ativar Juízo Metacontextual", value=True)
    if activate_judgment:
        kp_threshold = st.slider("Limiar de Invocação (Kp <)", 0.3, 0.7, 0.5)
        ideia_selecionada = st.selectbox(
            "Ideia Reguladora a Invocar",
            options=list(IDEIAS_REGULADORAS.keys()),
            format_func=lambda x: f"{IDEIAS_REGULADORAS[x]['glifo']} {x.capitalize()}"
        )

    if st.button("Reiniciar Simulação"):
        st.session_state.kernel = SimbolicKernel()
        st.session_state.history = {'x': [], 'y': [], 'z': [], 'color': []}
        st.session_state.paused = False
        st.rerun()

    if st.session_state.paused:
        st.warning("🚨 Colapso Ontológico Detectado! Simulação pausada.")
        if st.button("Invocar Ideia Reguladora"):
            ideia = IDEIAS_REGULADORAS[ideia_selecionada]
            st.session_state.vies += ideia['ajuste_vies']
            st.session_state.confronto += ideia['ajuste_confronto']
            st.session_state.confronto = max(0.1, st.session_state.confronto)
            st.session_state.paused = False
            st.success(f"Ideia '{ideia_selecionada}' invocada. Novos parâmetros definidos.")
            st.rerun()

# --- Simulação ---
if not st.session_state.paused:
    for _ in range(steps):
        st.session_state.kernel.evoluir(st.session_state.vies, st.session_state.confronto)
        x, y, z = st.session_state.kernel.get_bloch_coords()
        st.session_state.history['x'].append(x)
        st.session_state.history['y'].append(y)
        st.session_state.history['z'].append(z)

        kp_instataneo = st.session_state.judge.calcular_indice_pringe(st.session_state.kernel.psi, st.session_state.confronto)
        st.session_state.history['color'].append(kp_instataneo)

        if activate_judgment and kp_instataneo < kp_threshold:
            st.session_state.paused = True
            break

# --- Estado Final e Diagnóstico ---
if st.session_state.history['x']:
    x_final, y_final, z_final = st.session_state.history['x'][-1], st.session_state.history['y'][-1], st.session_state.history['z'][-1]
    diagnostico = st.session_state.judge.diagnostico_completo(st.session_state.kernel.psi, st.session_state.confronto)
    kp_final = diagnostico['kp']
    veredicto = diagnostico['veredicto']
    nivel_alerta = diagnostico['nivel_alerta']
    coerencia = diagnostico['coerencia']
    polarizacao_z = diagnostico['polarizacao_z']
else:
    x_final, y_final, z_final, kp_final, veredicto, nivel_alerta, coerencia, polarizacao_z = 0,0,1,1,"Iniciando...",'low',0,1

# --- Visualização ---
with col_view:
    fig = go.Figure()

    # Esfera
    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
    xs = np.cos(u)*np.sin(v)
    ys = np.sin(u)*np.sin(v)
    zs = np.cos(v)
    fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.1, showscale=False, colorscale='Greys'))

    # Eixo Ontológico
    fig.add_trace(go.Scatter3d(x=[0,0], y=[0,0], z=[-1.2, 1.2], mode='lines', line=dict(color='white', width=2, dash='dash'), name='Eixo Ontológico'))

    # Trajetória
    fig.add_trace(go.Scatter3d(
        x=st.session_state.history['x'], y=st.session_state.history['y'], z=st.session_state.history['z'],
        mode='lines',
        line=dict(color=st.session_state.history['color'], colorscale='RdYlGn', width=6, showscale=True, colorbar=dict(title="Índice Pringe (Kp)")),
        name='Fluxo da Consciência'
    ))

    # Ponto Final
    fig.add_trace(go.Scatter3d(
        x=[x_final], y=[y_final], z=[z_final],
        mode='markers', marker=dict(size=12, color='white', line=dict(width=2, color='black')), name='Estado Atual'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            annotations=[
                dict(x=0, y=0, z=1.2, text="MYTHOS (Percepção)", font=dict(color="#00ADB5", size=14)),
                dict(x=0, y=0, z=-1.2, text="LOGOS (Conceito)", font=dict(color="#FF9F1C", size=14)),
            ]
        ),
        margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='rgba(0,0,0,0)', height=550
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Painel de Juízo Metacontextual ---
    st.markdown("### 🏛️ Tribunal da Razão Pura (Diagnóstico)")

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Índice de Pringe (Kp)", f"{kp_final:.2f}")
    col_m2.metric("Coerência (Síntese)", f"{coerencia:.2f}")
    col_m3.metric("Polarização (Z)", f"{polarizacao_z:.2f}")

    box_color = {"low": "#2D5938", "med": "#594A2D", "high": "#592D2D"}.get(nivel_alerta, "#2D4059")

    st.markdown(f"""
    <div style="background-color: {box_color}; padding: 20px; border-radius: 10px; border: 1px solid #555;">
        <h4 style="margin:0">Veredicto Metacontextual:</h4>
        <p style="font-size: 18px; margin-top: 10px;">{veredicto}</p>
    </div>
    """, unsafe_allow_html=True)

# --- Rodapé ---
st.markdown("---")
st.markdown("Referências: *Pringe, H. (2007). Critique of the Quantum Power of Judgment.*, *Moss, G. (2015). Ernst Cassirer and the Autonomy of Language.*")

# Trigger rerun for animation loop
if not st.session_state.paused:
    st.rerun()

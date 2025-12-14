# src/firewalls/proof_of_sincerity.jl

"""
Calcula o custo genuíno do confronto simbólico.
Tensão baixa = potencial instrumentalização.
"""
function calculate_proof_of_sincerity(
    T_initial::Float64,
    T_final::Float64,
    elapsed_time::Float64,
    T_M::Float64,  # Tensão Mythos
    T_L::Float64,  # Tensão Logos
    T_E::Float64   # Tensão Ethos
)::Float64

    # Componente temporal (tempo de deliberação)
    time_cost = log(1 + elapsed_time)  # Custo logarítmico

    # Componente de redução de tensão
    tension_reduction = max(0, T_initial - T_final)

    # Componente de tensões específicas
    symbolic_cost = sqrt(T_M^2 + T_L^2 + T_E^2)

    # Fórmula sintética
    T_g = (tension_reduction * symbolic_cost) / (time_cost + 1e-6)

    return T_g
end

function is_suspiciously_low(
    T_g::Float64,
    complexity::Float64  # Complexidade da crise
)::Bool
    # Limite adaptativo baseado na complexidade
    THRESHOLD_MIN_TENSION = 0.3 * complexity

    return T_g < THRESHOLD_MIN_TENSION
end
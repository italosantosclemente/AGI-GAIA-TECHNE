using Printf  # Para formatação de output

# Constantes base (tunáveis)
const FATOR_ETHOS_HUMANO = 0.65
const PESO_TECHNE_PURA = 0.50
const PESO_TECHNE_GAIA = 0.30
const PESO_URGENCIA_GAIA = 0.20
const FATOR_HINTON_HOPFIELD_2024 = 0.95
const FATOR_QUANTUM_2025 = 0.90
const FATOR_CHEMISTRY_IA_2024 = 0.85
const FATOR_PAZ_2025 = 0.75
const ALEPH_SIGNIFICANCE = 1.05

function sigmoide(x::Float64)
    try
        return 1.0 / (1.0 + exp(-x))
    catch e
        if isa(e, OverflowError)
            if x > 0
                return 1.0
            else
                return 0.0
            end
        else
            rethrow(e)
        end
    end
end

# Função principal: Techné Score com Aleph variável
function calcular_techne_score_hipotese_alef()
    input_linear = (FATOR_HINTON_HOPFIELD_2024 + FATOR_QUANTUM_2025) * ALEPH_SIGNIFICANCE
    techné_score = sigmoide(input_linear)
    return techné_score
end

# Derivadas
function calcular_alerta_etico(techné_score::Float64)
    IAE = techné_score / FATOR_ETHOS_HUMANO
    return round(IAE, digits=4)
end

function calcular_harmonia_final(techné_score::Float64)
    termo_techne = techné_score * PESO_TECHNE_PURA
    termo_techne_gaia = FATOR_CHEMISTRY_IA_2024 * PESO_TECHNE_GAIA * FATOR_ETHOS_HUMANO
    termo_urgencia_gaia = FATOR_PAZ_2025 * PESO_URGENCIA_GAIA
    harmony_index = termo_techne + termo_techne_gaia - termo_urgencia_gaia
    return round(harmony_index, digits=4)
end

# gerador_narrativas.jl: Automação da criação de narrativas simbólicas (v2, com 14 glifos).

include("carregar_alfabeto.jl")

# Gramática expandida com novos glifos
const AGENTES = ["☉", "◈", "🌱", "🔗"]
const ACOES = ["➤", "⨁", "☌", "✨"]
const OBJETOS = ["❍", "⟴", "⟁"]

"""
Gera uma frase simbólica com base na gramática expandida, com base em uma conjectura.
"""
function gerar_frase(conjecture::String)
    local agente
    if occursin("human", lowercase(conjecture))
        agente = "🌱"
    elseif occursin("machine", lowercase(conjecture))
        agente = "🔗"
    else
        agente = rand(AGENTES)
    end

    acao = rand(ACOES)
    objeto = rand(OBJETOS)
    return "$agente $acao $objeto"
end

"""
Gera uma narrativa com um número específico de frases, com opção de interpretação ética.
"""
function gerar_narrativa(conjecture::String, num_frases::Int = 3; etica::Bool = true)
    narrativa = []
    push!(narrativa, "--- Nova Narrativa Simbólica (Expandida) ---")
    for i in 1:num_frases
        frase = gerar_frase(conjecture)
        push!(narrativa, "Frase $i: $frase")
    end
    if etica
        push!(narrativa, "[ETHOS] Deferindo juízo ao ISC: Essa narrativa é ferramenta para liberdade ontológica?")
    end
    push!(narrativa, "--- Fim da Narrativa ---")
    return join(narrativa, "\n")
end

# Execução principal
if abspath(PROGRAM_FILE) == @__FILE__
    conjecture = length(ARGS) > 0 ? ARGS[1] : ""
    narrativa_gerada = gerar_narrativa(conjecture, etica=true)
    println(narrativa_gerada)
end

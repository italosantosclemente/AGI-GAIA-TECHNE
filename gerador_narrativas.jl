# gerador_narrativas.jl: Automação da criação de narrativas simbólicas.

include("alfabeto.jl")

# Definição de uma gramática simples
const AGENTES = ["☉", "◈"]
const ACOES = ["➤", "⨁", "☌"]
const OBJETOS = ["❍", "⟴", "⟁"]

"""
Gera uma frase simbólica com base na gramática.
"""
function gerar_frase()
    agente = rand(AGENTES)
    acao = rand(ACOES)
    objeto = rand(OBJETOS)
    return "$agente $acao $objeto"
end

"""
Gera uma narrativa com um número específico de frases.
"""
function gerar_narrativa(num_frases::Int = 3)
    println("--- Nova Narrativa Simbólica ---")
    for i in 1:num_frases
        frase = gerar_frase()
        println("Frase $i: $frase")
    end
    println("--- Fim da Narrativa ---")
end

# Execução principal
gerar_narrativa()

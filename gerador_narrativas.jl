# gerador_narrativas.jl: Automação da criação de narrativas simbólicas (v2, com 14 glifos).

const ALFABETO_LEF = ["~", "⨁", "➤", "☌", "❍", "🕊️", "⟴", "⟁", "☉", "✨", "◈", "⚖️", "🔗", "🌱"]

# Gramática expandida com novos glifos
const AGENTES = ["☉", "◈", "🌱"]  # Adicionei humano soberano
const ACOES = ["➤", "⨁", "☌", "✨"]  # Adicionei brilho intuitivo
const OBJETOS = ["❍", "⟴", "⟁", "🔗"]  # Adicionei máquina techné

"""
Gera uma frase simbólica com base na gramática expandida.
"""
function gerar_frase()
    agente = rand(AGENTES)
    acao = rand(ACOES)
    objeto = rand(OBJETOS)
    return "$agente $acao $objeto"
end

"""
Gera uma narrativa com um número específico de frases, com opção de interpretação ética.
"""
function gerar_narrativa(num_frases::Int = 3; etica::Bool = true)
    println("--- Nova Narrativa Simbólica (Expandida) ---")
    for i in 1:num_frases
        frase = gerar_frase()
        println("Frase $i: $frase")
    end
    if etica
        println("[ETHOS] Deferindo juízo ao ISC: Essa narrativa é ferramenta para liberdade ontológica?")
    end
    println("--- Fim da Narrativa ---")
end

# Execução principal
gerar_narrativa(etica=true)

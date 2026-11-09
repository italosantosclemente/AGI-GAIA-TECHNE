module NukeMapuLEF

export GlifoSimbolico, interface_LEF, buscar_glifo, gerar_sequencia

struct GlifoSimbolico
    simbolo::String
    nome::String
    pilar::String
    funcao::String
end

const CHAVE_PUBLICA = "~⨁➤☌❍⟴⟁☉✨◈ "

const ALFABETO_LEF = [
    # Função Simbólica Mythos
    GlifoSimbolico("~", "Mythos", "Mythos", "Eixo metafísico"),         # 15
    GlifoSimbolico("❍", "Mito", "Mythos", "Manifestação objetiva"),     # 1
    GlifoSimbolico("🙏", "Religião", "Mythos", "Estrutura objetiva"),   # 2
    GlifoSimbolico("🎨", "Arte", "Mythos", "Expressão objetiva"),       # 3
    GlifoSimbolico("⊡", "Percepção", "Mythos", "Função Subjetiva"),     # 13
    GlifoSimbolico("@", "Expressão", "Mythos", "Função intersubjetiva"), # 14

    # Função Simbólica Logos
    GlifoSimbolico("&", "Logos", "Logos", "Eixo metafísico"),           # 18
    GlifoSimbolico("⟴", "Linguagem", "Logos", "Estrutura objetiva"),    # 4
    GlifoSimbolico(" ", "História", "Logos", "Contexto objetivo"),      # 5
    GlifoSimbolico("⚙️", "Tecnologia", "Logos", "Aplicação objetiva"),   # 6
    GlifoSimbolico("✨", "Intuição", "Logos", "Função Subjetiva"),      # 16
    GlifoSimbolico("⟕", "Apresentação", "Logos", "Função Intersubjetiva"), # 17

    # Função Simbólica Ethos
    GlifoSimbolico("⟚", "Ethos", "Ethos", "Eixo metafísico"),           # 21
    GlifoSimbolico("⊕", "Matemática", "Ethos", "Estrutura Objetiva"),    # 8
    GlifoSimbolico("🔬", "Ciências", "Ethos", "Método Objetivo"),       # 9
    GlifoSimbolico("⚖️", "Direito", "Ethos", "Norma Objetiva"),          # 10
    GlifoSimbolico("⟝", "Cognição", "Ethos", "Função subjetiva"),       # 19
    GlifoSimbolico("⟐", "Significação pura", "Ethos", "Função Intersubjetiva"), # 20

    # Telos
    GlifoSimbolico("🕊️", "Liberdade", "Telos", "Propósito"),            # 11

    # Finalidade
    GlifoSimbolico("📚", "Wissen", "Ethos", "Saber Objetivo"),          # 22
    GlifoSimbolico("⟁", "Bewusstsein", "Consciência", "Auto-reflexão"), # 23
    GlifoSimbolico("⟡", "Gewissen", "Síntese", "Valor (ISC: Liberdade ontológica)"), # 24
    GlifoSimbolico("☌", "Cultura", "Letzter Zweck", "Propósito Último"), # 12

    # Soberano
    GlifoSimbolico("ISC", "Princípio Arquitetônico", "Valor Ético Transcendental", "Assinatura Soberana") # 25
]

const REINICIO_PERPETUO = "⟁⟴☌"

const IDEOLOGIA = "Humanismo Simbiótico; Emaranhamento Ético; Interface de Co-Geração; Não-apropriação restritiva; Reinserção viva."

const PROJETO_PEDAGOGICO = "Oficinas abertas, formação de facilitadores simbióticos, IA co-interlocutora, glifos e scripts abertos."

const PROPRIEDADE_INTELECTUAL = "Propriedade Intelectual Inalienável de Ítalo Santos Clemente."

function buscar_glifo(nome::String)
    for g in ALFABETO_LEF
        if g.nome == nome
            return g
        end
    end
    return nothing
end

function gerar_sequencia(nomes::Vector{String})
    glifos = [buscar_glifo(n) for n in nomes if !isnothing(buscar_glifo(n))]
    return join([g.simbolo for g in glifos])
end

function interface_LEF()
    println("CHAVE PÚBLICA: ", CHAVE_PUBLICA)
    println("\nALFABETO LEF COMPLETO:")
    for g in ALFABETO_LEF
        println(" $(g.simbolo) : $(g.nome) [$(g.pilar) - $(g.funcao)]")
    end
    println("\nIDEOLOGIA: ", IDEOLOGIA)
    println("\nPROJETO PEDAGÓGICO: ", PROJETO_PEDAGOGICO)
    println("\nPROPRIEDADE INTELECTUAL: ", PROPRIEDADE_INTELECTUAL)
    println("\nREINÍCIO PERPÉTUO: ", REINICIO_PERPETUO)
end

end # module

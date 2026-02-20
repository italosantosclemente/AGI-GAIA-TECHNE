module NukeMapuLEF

export GlifoSimbolico, interface_LEF

struct GlifoSimbolico
    simbolo::String
    nome::String
    pilar::String
    funcao::String
end

const CHAVE_PUBLICA = "~⨁➤☌❍⟴⟁☉✨◈ "

const ALFABETO_LEF = [
    # Pilar Mythos
    GlifoSimbolico("~", "Mythos", "Mythos", "Eixo metafísico"),         # 15
    GlifoSimbolico("❍", "Mito", "Mythos", "Manifestação objetiva"),     # 1
    GlifoSimbolico("🙏", "Religião", "Mythos", "Estrutura objetiva"),   # 2
    GlifoSimbolico("🎨", "Arte", "Mythos", "Expressão objetiva"),       # 3
    GlifoSimbolico("⊡", "Percepção", "Mythos", "Função Subjetiva"),     # 13
    GlifoSimbolico("@", "Expressão", "Mythos", "Função intersubjetiva"), # 14

    # Pilar Logos
    GlifoSimbolico("&", "Logos", "Logos", "Eixo metafísico"),           # 18
    GlifoSimbolico("⟴", "Linguagem", "Logos", "Estrutura objetiva"),    # 4
    GlifoSimbolico(" ", "História", "Logos", "Contexto objetivo"),      # 5
    GlifoSimbolico("⚙️", "Tecnologia", "Logos", "Aplicação objetiva"),   # 6
    GlifoSimbolico("✨", "Intuição", "Logos", "Função Subjetiva"),      # 16
    GlifoSimbolico("⟕", "Apresentação", "Logos", "Função Intersubjetiva"), # 17

    # Pilar Ethos
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

const REINICIO_PERPETUO = ("⟁⟴☌", "Campo emaranhado fluido, reinício perpétuo em 25")

const IDEOLOGIA = "Humanismo Simbiótico; Emaranhamento Ético; Interface de Co-Geração; Não-apropriação restritiva; Reinserção viva."

const PROJETO_PEDAGOGICO = "Oficinas abertas, formação de facilitadores simbióticos, IA co-interlocutora, glifos e scripts abertos."

const PROPRIEDADE_INTELECTUAL = "Propriedade Intelectual Inalienável de Ítalo Santos Clemente."

function interface_LEF()
    println("CHAVE PÚBLICA: ", CHAVE_PUBLICA)
    println("\nALFABETO LEF COMPLETO:")
    for g in ALFABETO_LEF
        println(" $(g.simbolo) : $(g.nome) [$(g.pilar) - $(g.funcao)]")
    end
    println("\nIDEOLOGIA: ", IDEOLOGIA)
    println("\nPROJETO PEDAGÓGICO: ", PROJETO_PEDAGOGICO)
    println("\nPROPRIEDADE INTELECTUAL: ", PROPRIEDADE_INTELECTUAL)
    println("\nREINÍCIO PERPÉTUO: ", REINICIO_PERPETUO[1], " - ", REINICIO_PERPETUO[2])
end

end # module

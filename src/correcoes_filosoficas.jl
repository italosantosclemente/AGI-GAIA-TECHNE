# src/correcoes_filosoficas.jl
module CorreçõesFilosóficas

"""
Documenta correções terminológicas v1.0 → v1.1
Baseadas na dissertação de mestrado (UNICAMP 2025)
e seminário UDP 2025 (Kant y Cassirer)
"""

const CORREÇÕES = Dict(
    "materialismo" => Dict(
        :termo_correto => "idealismo crítico-transcendental",
        :razão => "Kant/Cassirer são idealistas, não materialistas. " *
                  "Referência: KrV B:XVI (revolução copernicana)",
        :impacto => "Fundamental",
        :citação_acadêmica => "Seminário UDP 2025, p.5: 'el pomposo nombre " *
                             "de uma ontología debe ceder lugar a una mera " *
                             "analítica del entendimiento puro'",
        :arquivos => ["README.md", "src/analitica_vida_simbolica.jl"]
    ),

    "pilares" => Dict(
        :termo_correto => "funções simbólicas",
        :razão => "Pilares sugere hierarquia (Mythos < Logos < Ethos). " *
                  "Cassirer defende emaranhamento não-hierárquico.",
        :impacto => "Arquitetural",
        :citação_acadêmica => "Seminário p.17, nota 39: 'Auseinandersetzung... " *
                             "not the case that two already existing unrelated " *
                             "positions clash, but that the positions themselves " *
                             "are a product of the conflict'",
        :arquivos => ["src/analitica_vida_simbolica.jl", "README.md"]
    ),

    "metafísica" => Dict(
        :termo_correto => "analítica transcendental",
        :razão => "Metafísica = ontologia dogmática (afirma essências). " *
                  "Analítica = investigação crítica (condições de possibilidade).",
        :impacto => "Terminológico",
        :citação_acadêmica => "Kant KrV B:116-8: 'trascendental es todo conocimiento " *
                             "que se ocupa no tanto de los objetos, sino del modo " *
                             "de conocer objetos'",
        :arquivos => ["src/analitica_vida_simbolica.jl (nome do arquivo)"]
    ),

    "teleologia_biológica" => Dict(
        :termo_correto => "teleologia psicossocial",
        :razão => "Krois (2004): formas simbólicas têm teleologia social/psicológica, " *
                  "mas NÃO biológica. Distinção fundamental com Maturana.",
        :impacto => "Conceitual",
        :citação_acadêmica => "Seminário p.13: 'John Michael Krois (2004) sostiene " *
                             "que hay una teleología social y psicológica en la " *
                             "filosofía de las formas simbólicas, pero no biológica'",
        :arquivos => ["README.md", "docs/THEORY.md"]
    )
)

function exibir_correções()
    println("📋 CORREÇÕES FILOSÓFICAS v1.0 → v1.1")
    println("Baseadas em: Dissertação UNICAMP 2025 + Seminário UDP 2025")
    println("=" ^ 70)
    println()

    for (erro, dados) in CORREÇÕES
        println("❌ Erro: $erro")
        println("   ✅ Correto: $(dados[:termo_correto])")
        println("   📝 Razão: $(dados[:razão])")
        println("   📚 Citação: $(dados[:citação_acadêmica])")
        println("   📁 Arquivos: $(join(dados[:arquivos], ", "))")
        println()
    end
end

function verificar_arquivo(caminho::String)
    """Verifica se arquivo ainda contém termos incorretos"""
    if !isfile(caminho)
        return String["Arquivo não encontrado"]
    end

    conteudo = read(caminho, String)
    erros_encontrados = String[]

    termos_incorretos = [
        "ontologia materialista",
        "Pilar Mythos",
        "Pilar Logos",
        "Pilar Ethos",
        "metafisica_da_vida" # nome antigo
    ]

    for termo in termos_incorretos
        if occursin(termo, conteudo)
            push!(erros_encontrados, termo)
        end
    end

    return erros_encontrados
end

export CORREÇÕES, exibir_correções, verificar_arquivo

end # module

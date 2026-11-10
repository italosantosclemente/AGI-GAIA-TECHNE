using Test
include("../src/correcoes_filosoficas.jl")
using .CorreçõesFilosóficas

@testset "Consistência Filosófica v1.1" begin

    @testset "Terminologia Kantiana" begin
        readme = read("README.md", String)

        # Não deve conter termos incorretos
        @test !occursin("materialismo", lowercase(readme))
        @test !occursin("ontologia materialista", lowercase(readme))

        # Deve conter termos corretos
        @test occursin("idealismo", lowercase(readme))
        @test occursin("transcendental", lowercase(readme))
    end

    @testset "Funções Simbólicas (não pilares)" begin
        analitica = read("src/analitica_vida_simbolica.jl", String)

        # Arquivo deve existir com novo nome
        @test isfile("src/analitica_vida_simbolica.jl")

        # Não deve usar "pilar"
        @test !occursin("Pilar Mythos", analitica)
        @test !occursin("Pilar Logos", analitica)

        # Deve usar "função simbólica"
        @test occursin("Função Simbólica", analitica) ||
              occursin("FunçãoSimbólica", analitica)
    end

    @testset "Verificação via módulo de correções" begin
        # Verificar README
        erros_readme = CorreçõesFilosóficas.verificar_arquivo("README.md")
        @test isempty(erros_readme) ||
              println("⚠️ Erros em README: ", erros_readme)

        # Verificar arquivo principal
        erros_src = CorreçõesFilosóficas.verificar_arquivo(
            "src/analitica_vida_simbolica.jl"
        )
        @test isempty(erros_src) ||
              println("⚠️ Erros em src: ", erros_src)
    end
end

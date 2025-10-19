using Test
include("../gerador_narrativas.jl")

@testset "Testes para gerador_narrativas.jl" begin
    @testset "gerar_frase" begin
        frase = gerar_frase()
        @test typeof(frase) == String
        @test length(split(frase)) == 3
    end

    @testset "gerar_narrativa" begin
        # Teste não implementado para a saída de impressão
    end
end

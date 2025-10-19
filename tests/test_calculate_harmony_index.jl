using Test
include("../calculate_harmony_index.jl")

@testset "Testes para calculate_harmony_index.jl" begin
    @testset "Mythos" begin
        percepcao = Mythos.gerar_percepcao_inicial(ALFABETO_LEF)
        @test length(percepcao) == 3
    end

    @testset "Logos" begin
        percepcao = Mythos.gerar_percepcao_inicial(ALFABETO_LEF)
        discurso = Logos.estruturar_discurso(percepcao)
        @test typeof(discurso) == String
        tech, ethos, gaia = Logos.simular_metricas(percepcao)
        @test 0.0 <= tech <= 1.0
        @test 0.0 <= ethos <= 1.0
        @test 0.0 <= gaia <= 1.0
    end

    @testset "Ethos" begin
        indice = Ethos.calcular_indice_harmonia(0.5, 0.6, 0.7)
        @test typeof(indice) == Float64
        percepcao = Mythos.gerar_percepcao_inicial(ALFABETO_LEF)
        historico = Float64[]
        Ethos.monitorar_permanentemente(percepcao, historico)
        @test length(historico) == 1
    end
end

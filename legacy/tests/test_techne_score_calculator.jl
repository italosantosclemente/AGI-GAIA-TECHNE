using Test
include("../techne_score_calculator.jl")

@testset "Testes para techne_score_calculator.jl" begin
    @testset "Cálculos de Métricas" begin
        ts = calcular_techne_score_hipotese_alef()
        @test 0.0 <= ts <= 1.0
        iae = calcular_alerta_etico(ts)
        @test typeof(iae) == Float64
        hi = calcular_harmonia_final(ts)
        @test typeof(hi) == Float64
    end
end

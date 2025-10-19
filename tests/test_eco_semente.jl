using Test
include("../eco_semente.jl")

@testset "Testes para eco_semente.jl" begin
    @testset "Mythos" begin
        semente = Mythos.gerar_semente_humana(ALFABETO_LEF)
        @test typeof(semente) == String
    end
end

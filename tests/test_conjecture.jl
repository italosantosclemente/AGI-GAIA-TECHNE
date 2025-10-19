using Test
include("../conjecture.jl")

@testset "Testes para conjecture.jl" begin
    @testset "ConjecturaMythos" begin
        conjectura = ConjecturaMythos.gerar_conjectura()
        @test length(conjectura) == 5
    end

    @testset "ConjecturaLogos" begin
        conjectura = ConjecturaMythos.gerar_conjectura()
        discurso = ConjecturaLogos.estruturar_conjectura(conjectura)
        @test typeof(discurso) == String
    end
end

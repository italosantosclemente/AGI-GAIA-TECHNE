using Test
using LinearAlgebra

include("../src/nuke_mapu_lef.jl")
using .NukeMapuLEF

@testset "LEF: Autonomia da Linguagem (Moss)" begin
    @testset "Busca de Glifos" begin
        glifo_mythos = buscar_glifo("Mythos")
        @test glifo_mythos !== nothing
        @test glifo_mythos.simbolo == "~"
        @test glifo_mythos.pilar == "Mythos"
    end

    @testset "Geração de Sequências Simbólicas" begin
        seq = gerar_sequencia(["Mythos", "Linguagem", "Liberdade"])
        @test seq == "~⟴🕊️"
    end

    @testset "Reinício Perpétuo" begin
        @test NukeMapuLEF.REINICIO_PERPETUO == "⟁⟴☌"
    end
end

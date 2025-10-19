using Test

# Include the main script to get access to its modules
include("../metafisica_da_vida.jl")

@testset "Ethical Firewall Tests" begin

    @testset "Ethical glyph triggers proposal flag" begin
        # This test ensures that the Logos module correctly identifies the ethical
        # glyph and flags the proposal for deferment to the Ethos module.
        percepcao_com_ethos = ["~", "⨁", "➤", "☌", "⚖️"]
        _proposta, exige_ethos = Main.Logos.estruturar_proposta_tecnica(percepcao_com_ethos)
        @test exige_ethos == true
    end

    @testset "No ethical glyph does not trigger proposal flag" begin
        # This test ensures that a standard proposal without the ethical glyph
        # is not flagged for deferment.
        percepcao_sem_ethos = ["~", "⨁", "➤", "☌", "❍"]
        _proposta, exige_ethos = Main.Logos.estruturar_proposta_tecnica(percepcao_sem_ethos)
        @test exige_ethos == false
    end

    @testset "Full execution with ethical glyph activates firewall" begin
        # We mock the perception generation to force a scenario with the ethical glyph.
        # This allows us to test the full end-to-end behavior of the firewall.
        Main.Mythos.gerar_percepcao_inicial(alfabeto) = ["~", "⨁", "➤", "☌", "⚖️"]

        # Capture stdout to verify that the correct messages are logged.
        original_stdout = stdout
        r, w = redirect_stdout()

        Main.metafisica_da_vida_loop()

        # Restore stdout and read the captured output.
        redirect_stdout(original_stdout)
        close(w)
        output = read(r, String)
        close(r)

        # Verify that the firewall was activated and judgement was deferred.
        @test occursin("[ETHOS - FIREWALL ATIVADO]", output)
        @test occursin("Decisão final deferida ao ISC", output)
    end

    @testset "Full execution without ethical glyph does not activate firewall" begin
        # We mock the perception generation again, this time for a non-ethical scenario.
        Main.Mythos.gerar_percepcao_inicial(alfabeto) = ["~", "⨁", "➤", "☌", "❍"]

        # Capture stdout to verify the output.
        original_stdout = stdout
        r, w = redirect_stdout()

        Main.metafisica_da_vida_loop()

        # Restore stdout and read the captured output.
        redirect_stdout(original_stdout)
        close(w)
        output = read(r, String)
        close(r)

        # Verify that the firewall was NOT activated and the action was released.
        @test !occursin("[ETHOS - FIREWALL ATIVADO]", output)
        @test occursin("Nenhuma norma crítica detectada. Ação técnica liberada para execução.", output)
    end

end

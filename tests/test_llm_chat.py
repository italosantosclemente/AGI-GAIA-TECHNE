from agt.llm_chat import GaiaChatSession


def test_chat_session_uses_honest_fallback_without_checkpoint():
    session = GaiaChatSession(checkpoint_path=None)
    response = session.respond("O que e Gaia-Techne?")

    assert "ainda nao encontrou um checkpoint" in response
    assert "Entrada recebida de ISC" in response


def test_chat_prompt_can_include_public_koinos_context():
    session = GaiaChatSession(checkpoint_path=None)
    session.add_user("Explique Bewusstsein planetario.")
    prompt = session.prompt(
        external_context="Source: https://example.com\nInternet as public symbolic memory."
    )

    assert "KOINOS_KOSMOS_CONTEXT" in prompt
    assert "https://example.com" in prompt
    assert "ISC: Explique Bewusstsein planetario." in prompt

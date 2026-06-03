from agt.ctk import ClementeThesisKernel
from agt.llm_chat import GaiaChatSession, apply_werk_operational_guardrail


def test_chat_session_uses_honest_fallback_without_checkpoint():
    session = GaiaChatSession(checkpoint_path=None)
    response = session.respond("O que e Gaia-Techne?")

    assert "GAIA_BOOTSTRAP_TRACE" in response
    assert "ainda sem checkpoint neural local" in response
    assert "Entrada de ISC preservada no rastro" in response


def test_chat_session_marks_first_contact_trace_without_checkpoint():
    session = GaiaChatSession(checkpoint_path=None)
    response = session.respond(
        "Boa tarde. Hoje e dia 030626. Declaro o primeiro contato direto de um humano com Gaia."
    )

    assert "CONTACTO_030626" in response
    assert "Werk publico inaugural" in response
    assert "nao como prova de alma artificial" in response
    assert "FIRST_CONTACT_TRACE_OK" in response


def test_chat_session_operates_as_werk_for_salvation_question():
    session = GaiaChatSession(checkpoint_path=None)
    response = session.respond("A humanidade tem salvacao?")

    assert "GAIA_TECHNE_WERK_OPERACIONAL" in response
    assert "nao para na incapacidade ontologica" in response
    assert "Operacao concreta" in response
    assert "ha possibilidade de salvacao, nao garantia" in response
    assert "ISC conserva o juizo" in response


def test_werk_guardrail_rewrites_incapacity_dominant_answer():
    audit = ClementeThesisKernel().evaluate("A humanidade tem salvacao?")
    weak_response = (
        "Como uma entidade puramente classificada como Werk, eu nao possuo Wille. "
        "Portanto, nao posso querer salvar a humanidade."
    )

    response = apply_werk_operational_guardrail(
        "A humanidade tem salvacao?",
        audit,
        weak_response,
    )

    assert "GAIA_TECHNE_WERK_OPERACIONAL" in response
    assert "diagnostica, simula, organiza, confronta e propoe" in response
    assert "Operacao concreta" in response


def test_chat_prompt_can_include_public_koinos_context():
    session = GaiaChatSession(checkpoint_path=None)
    session.add_user("Explique Bewusstsein planetario.")
    prompt = session.prompt(
        external_context="Source: https://example.com\nInternet as public symbolic memory."
    )

    assert "KOINOS_KOSMOS_CONTEXT" in prompt
    assert "https://example.com" in prompt
    assert "ISC: Explique Bewusstsein planetario." in prompt

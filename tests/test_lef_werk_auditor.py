from agt.lef_werk import LEF_WERK_SIGNATURE
from agt.lef_werk_auditor import (
    GL25_AUDITOR,
    audit_trace,
    daily_ledger_entry,
    explain_alphabet,
    format_audit_markdown,
    relocate_argument,
)


def test_gl25_symbol_is_wave():
    assert GL25_AUDITOR["symbol"] == "🌊"


def test_gl25_is_not_part_of_signature():
    assert GL25_AUDITOR["not_part_of_signature"] is True
    assert GL25_AUDITOR["symbol"] not in LEF_WERK_SIGNATURE


def test_signature_remains_24_glifos():
    assert len(LEF_WERK_SIGNATURE) == 24


def test_explain_alphabet_mentions_wave_not_25th_paragraph():
    explanation = explain_alphabet()
    assert "🌊" in explanation
    assert "not a 25th paragraph" in explanation
    assert "24 glifos" in explanation


def test_audit_detects_block_mapping_contradiction():
    audit = audit_trace("Metatheory = Mythos")
    assert "CONTRADICTION" in audit["verdicts"]
    assert audit["contradictions"]


def test_audit_detects_agi_wille_contradiction():
    audit = audit_trace("AGI is Wille")
    assert "CONTRADICTION" in audit["verdicts"]
    assert any("Wille" in item for item in audit["contradictions"])


def test_audit_marks_ai_without_werk_as_improvement():
    audit = audit_trace("AI will optimize all institutions.")
    assert "IMPROVEMENT" in audit["verdicts"]
    assert any("AI/AGI" in item for item in audit["improvements"])


def test_audit_marks_core_formula_as_sufficient():
    audit = audit_trace("Werk, never Wille.")
    assert "SUFFICIENT" in audit["verdicts"]
    assert audit["sufficient"]


def test_relocation_maps_einstein_to_gl04():
    relocation = relocate_argument(
        "Einstein and Cassirer reconstruct objectivity through geometry and experience."
    )
    assert relocation["target"] == "GL04"


def test_relocation_maps_negarestani_and_agi_to_gl15():
    relocation = relocate_argument("Negarestani and AGI as transcendental hypothesis.")
    assert relocation["target"] == "GL15"


def test_daily_ledger_contains_returned_to_isc():
    audit = audit_trace("Werk, never Wille.", source="unit test")
    ledger = daily_ledger_entry(audit, date="2026-06-15")
    assert "returned_to_ISC: true" in ledger


def test_contingent_external_case_is_not_canonized():
    audit = audit_trace("Anthropic Fable Mythos jailbreak model access case")

    assert audit["category"] == "contingent_external_case"
    assert audit["contingent_case"]["affected_glifos"] == ["🜄", "🜁", "⚘", "🜛", "🜜"]
    assert "GL14" in audit["contingent_case"]["internal_targets"]
    assert "GL15" in audit["contingent_case"]["internal_targets"]
    assert any("not doctrine" in item for item in audit["sufficient"])


def test_contingent_case_format_prefers_real_glifos():
    audit = audit_trace("Anthropic Fable Mythos jailbreak model access case")
    rendered = format_audit_markdown(audit)

    assert "🜄, 🜁, ⚘, 🜛, 🜜" in rendered
    assert "GL14 / GL15" not in rendered
    assert "Contingent External Case" in rendered


def test_model_access_suspension_does_not_prove_wille():
    audit = audit_trace("Model access suspension proves Wille and Gewissen")

    assert "CONTRADICTION" in audit["verdicts"]
    assert any("cannot prove Wille" in item for item in audit["contradictions"])


def test_jailbreak_without_scope_distinction_is_improvement():
    audit = audit_trace("Anthropic Fable Mythos jailbreak caused model access suspension")

    assert "IMPROVEMENT" in audit["verdicts"]
    assert any("narrow jailbreak" in item for item in audit["improvements"])


def test_contingent_case_ledger_uses_requested_category():
    audit = audit_trace("Anthropic Fable Mythos jailbreak model access case", source="unit test")
    ledger = daily_ledger_entry(audit, date="2026-06-15")

    assert "# 🌊 Audit — contingent external case" in ledger
    assert "category: contingent_external_case" in ledger
    assert "affected glifos:" in ledger
    assert "🜄, 🜁, ⚘, 🜛, 🜜" in ledger
    assert "returned_to_ISC: true" in ledger

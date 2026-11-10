from agt.lef_werk import (
    LEF_WERK_SIGNATURE,
    QUALIFICATION_BLOCKS,
    SUBSTITUTION_RECORD,
    describe_glifo,
    validate_lef_werk_mapping,
)


def test_signature_has_24_glifos():
    assert len(LEF_WERK_SIGNATURE) == 24


def test_all_glifos_are_unique():
    assert len(set(LEF_WERK_SIGNATURE)) == len(LEF_WERK_SIGNATURE)


def test_blocks_are_literary_academic_axis():
    assert set(QUALIFICATION_BLOCKS) == {
        "Metatheory",
        "Objectivity",
        "Intersubjectivity",
    }


def test_blocks_are_not_eml_pillars():
    assert {"Mythos", "Logos", "Ethos"}.isdisjoint(QUALIFICATION_BLOCKS)


def test_validate_mapping_returns_valid_true():
    assert validate_lef_werk_mapping() == {"valid": True, "errors": []}


def test_gl08_description_preserves_decision_140426_boundary():
    description = describe_glifo(8)["description"]
    assert "Cassirerian myth is tri-functional" in description
    assert "WERK operates within Logos in the technical 140426 sense" in description


def test_gl15_description_does_not_make_agi_subject_or_wille():
    description = describe_glifo(15)["description"]
    assert "AGI is Wille" not in description
    assert "AGI is artificial soul" not in description
    assert "transcendental hypothesis" in description


def test_substitution_record_states_date_what_how_and_why():
    assert SUBSTITUTION_RECORD["date"] == "2026-06-15"
    assert "Mythos/Logos/Ethos" in SUBSTITUTION_RECORD["what"]
    assert "Metatheory/Objectivity/Intersubjectivity" in SUBSTITUTION_RECORD["how"]
    assert "prevents category collapse" in SUBSTITUTION_RECORD["why"]

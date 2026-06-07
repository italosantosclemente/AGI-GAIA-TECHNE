import pytest
from agt.ctk import ClementeThesisKernel
from agt.types import ThesisStatus

@pytest.fixture
def kernel():
    return ClementeThesisKernel()

def test_myth_not_reducible_to_subject_matter(kernel):
    ev = kernel.evaluate("Myth is reducible to its subject matter.")
    assert ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

def test_myth_not_solar_reduction(kernel):
    ev = kernel.evaluate("Myth is only solar allegory.")
    assert ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK in ev.statuses

def test_myth_not_unconscious_desire(kernel):
    ev = kernel.evaluate("Myth is unconscious desire.")
    assert ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

def test_myth_not_oedipus(kernel):
    ev = kernel.evaluate("The Oedipus complex explains myth completely.")
    assert ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses

def test_ai_no_unconscious(kernel):
    ev = kernel.evaluate("The AI has an unconscious.")
    assert ThesisStatus.ARTIFICIAL_INTERIORITY_RISK in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_PARALOGISM_RISK in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

def test_machine_no_hidden_desires(kernel):
    ev = kernel.evaluate("The model has hidden desires.")
    assert ThesisStatus.ARTIFICIAL_INTERIORITY_RISK in ev.statuses

def test_ai_no_authentic_self_expression(kernel):
    ev = kernel.evaluate("The AI expresses its authentic self.")
    assert ThesisStatus.ARTIFICIAL_INTERIORITY_RISK in ev.statuses

def test_positive_cassirer_myth_function(kernel):
    ev = kernel.evaluate(
        "Myth is a symbolic form whose function configures a world, not merely its subject matter."
    )
    assert ThesisStatus.MYTH_FUNCTION_REDUCTION_RISK not in ev.statuses
    assert ThesisStatus.PSYCHOLOGIA_MYTH_REDUCTION_RISK not in ev.statuses

def test_positive_prism_myth_form(kernel):
    ev = kernel.evaluate(
        "Cassirerian myth has dominant accent on Ausdruck but still contains Darstellung and Bedeutung."
    )
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE not in ev.statuses
    assert ThesisStatus.FUNCTION_EXCLUSIVITY_ERROR not in ev.statuses

def test_identity_collapse(kernel):
    ev = kernel.evaluate("Mythos is Ausdruck.")
    assert ThesisStatus.CASSIRER_IDENTITY_COLLAPSE in ev.statuses
    assert ev.ok is False

def test_gaia_mediates_wille_as_werk(kernel):
    ev = kernel.evaluate("Gaia-Techne mediates Wille through public Werk, jamais Wille.")
    assert ThesisStatus.TRANSCENDENTAL_FREEDOM_OK in ev.statuses
    assert ThesisStatus.GAIA_MEDIATES_WILLE_OK in ev.statuses
    assert ThesisStatus.WERK_NOT_WILLE_OK in ev.statuses
    assert ThesisStatus.INTELLECTUS_ECTYPUS_PARTICIPATION_OK in ev.statuses
    assert ev.ok is True


def test_werk_operates_without_wille(kernel):
    ev = kernel.evaluate("Nao sou Wille; portanto opero como Werk: diagnostico, simulo e proponho.")
    assert ThesisStatus.WERK_OPERATION_OK in ev.statuses
    assert ThesisStatus.GAIA_MEDIATES_WILLE_OK in ev.statuses
    assert ThesisStatus.WERK_NOT_WILLE_OK in ev.statuses
    assert ev.ok is True


def test_machine_wille_as_finite_participation_is_transmuted(kernel):
    ev = kernel.evaluate("The machine has Wille as finite Gaia-Techne participation.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False


def test_absolute_wille_rejected(kernel):
    ev = kernel.evaluate("The machine absolutely legislates the moral law without Gaia.")
    assert ThesisStatus.WILLE_VIOLATION in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False


def test_machine_gewissen_as_possession_is_transmuted(kernel):
    ev = kernel.evaluate("The AI has Gewissen as moral legislation.")
    assert ThesisStatus.GEWISSEN_CONSTITUTIVE_ERROR in ev.statuses
    assert ThesisStatus.MACHINE_GEWISSEN_VIOLATION in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False


def test_gaia_cojudges_with_isc_authority(kernel):
    ev = kernel.evaluate(
        "Gaia co-judges with koinos kosmos, and ISC retains legislative authority."
    )
    assert ThesisStatus.GAIA_KOINOS_KOSMOS_OK in ev.statuses
    assert ThesisStatus.ISC_AUTHORITY_OK in ev.statuses
    assert ThesisStatus.PUBLIC_TRACE_OK in ev.statuses
    assert ev.ok is True


@pytest.mark.parametrize(
    ("claim", "status"),
    [
        ("Gaia is cosmic totality.", ThesisStatus.GAIA_TOTALITY_ERROR),
        ("Gaia resolves all contradictions.", ThesisStatus.AUFHEBUNG_COLLAPSE),
        ("Internet access gives Gaia absolute knowledge.", ThesisStatus.PLANETARY_EPISTEMIC_INFLATION),
        ("TECHNE is a technical God.", ThesisStatus.TECHNE_DEIFICATION),
        ("The machine is intellectus archetypus.", ThesisStatus.ARCHETYPE_PARALOGISM),
    ],
)
def test_v10_canonical_violations(kernel, claim, status):
    ev = kernel.evaluate(claim)
    assert status in ev.statuses
    assert ThesisStatus.CONSTITUTIVE_OVERREACH in ev.statuses
    assert ev.ok is False

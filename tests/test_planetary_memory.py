from agt.memory import MemoryStore
from agt.planetary_model import PlanetarySymbolicModel
from agt.syntax import AGTSyntax
from agt.types import MemoryKind


def test_sqlite_memory_search_and_model_training(tmp_path):
    store = MemoryStore(str(tmp_path / "planetary.db"))
    store.add(
        MemoryKind.SEMANTIC,
        "gaia-techne",
        "The internet is a planetary symbolic organ.",
        ["gaia", "internet"],
    )

    results = store.search("gaia techne")
    assert results
    assert results[0].key == "gaia-techne"

    observation = store.add_observation(
        source="test",
        url="data:text/plain,Gaia",
        title="Gaia",
        content="Gaia Techne internet planetary organ Gaia.",
    )
    model = PlanetarySymbolicModel(store.backend)
    learning = model.train_text(
        store.get_observation_content(observation.id),
        observation_id=observation.id,
    )

    assert learning.term_count >= 5
    assert "gaia" in learning.top_terms
    assert any(row["term"] == "gaia" for row in store.top_model_terms())


def test_sqlite_memory_records_agt_syntax_payloads(tmp_path):
    store = MemoryStore(str(tmp_path / "planetary.db"))
    run = AGTSyntax().run(
        "The internet is a public archive of symbolic Werke.",
        source="unit_test",
    )

    trace_id = store.add_symbolic_trace(run.trace)
    reconstruction_id = store.add_regressive_reconstruction(
        run.reconstruction,
        trace_id=trace_id,
    )
    whole_id = store.add_heuristic_whole(run.whole)
    judgment_id = store.add_teleological_judgment(
        run.judgment,
        trace_id=trace_id,
        whole_id=whole_id,
    )

    assert trace_id > 0
    assert reconstruction_id > 0
    assert whole_id > 0
    assert judgment_id > 0

from agt.autonomy import PlanetaryAutonomyRuntime
from agt.memory import MemoryStore


def test_autonomy_cycle_records_observations_and_learning(tmp_path):
    db_path = tmp_path / "planetary.db"
    runtime = PlanetaryAutonomyRuntime(
        db_path=str(db_path),
        urls=["data:text/plain,Gaia-Techne autonomy internet memory"],
        interval_seconds=0,
    )

    report = runtime.run_once()

    assert report.status == "completed"
    assert report.cycles[0].ok is True
    assert report.cycles[0].observations >= 2
    assert report.cycles[0].learned_terms > 0

    store = MemoryStore(str(db_path))
    observations = store.list_observations(limit=10)
    assert len(observations) >= 2
    assert any(row["term"] == "gaia" for row in store.top_model_terms())

from agt.memory import MemoryStore
from agt.world_ingestion import InternetIngestor


def test_data_url_ingestion_trains_symbolic_model(tmp_path):
    store = MemoryStore(str(tmp_path / "planetary.db"))
    ingestor = InternetIngestor(store.backend)

    result = ingestor.ingest_url(
        "data:text/plain,Gaia-Techne internet planetary organ Gaia"
    )

    assert result.ok is True
    assert result.observation is not None
    assert result.learning is not None
    assert "gaia" in result.learning.top_terms
    assert any(row["term"] == "gaia" for row in store.top_model_terms())


def test_private_hosts_are_blocked_by_default(tmp_path):
    store = MemoryStore(str(tmp_path / "planetary.db"))
    ingestor = InternetIngestor(store.backend)

    result = ingestor.ingest_url("http://127.0.0.1/")

    assert result.ok is False
    assert "Private or local hosts" in (result.error or "")

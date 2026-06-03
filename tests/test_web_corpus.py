from __future__ import annotations

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from agt.web_corpus import WebCorpusHarvester


def test_web_corpus_harvests_explicit_local_url_when_allowed(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(
        "<html><head><title>Gaia Source</title></head>"
        "<body><main>Internet as planetary Bewusstsein and public symbolic memory.</main></body></html>",
        encoding="utf-8",
    )

    handler = partial(SimpleHTTPRequestHandler, directory=str(site))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/index.html"
        report = WebCorpusHarvester(
            output_dir=str(tmp_path / "web"),
            allow_private_hosts=True,
            respect_robots=False,
            chunk_chars=400,
            chunk_overlap=20,
        ).harvest([url])
    finally:
        server.shutdown()
        thread.join(timeout=5)

    assert report.ok == 1
    assert report.failed == 0
    assert report.records == 1
    rows = [
        json.loads(line)
        for line in (tmp_path / "web" / "corpus.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert rows[0]["title"] == "Gaia Source"
    assert rows[0]["metadata"]["rights_status"] == "internet_source_review_required"


def test_web_corpus_blocks_private_hosts_by_default(tmp_path):
    result = WebCorpusHarvester(
        output_dir=str(tmp_path / "web"),
        respect_robots=False,
    ).fetch_url("http://127.0.0.1:9/")

    assert result.ok is False
    assert "Private or local hosts are disabled" in result.error

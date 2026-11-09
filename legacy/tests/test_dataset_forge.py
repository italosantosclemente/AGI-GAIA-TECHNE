import json

from agt.dataset_forge import ManualDatasetForge, classify_drive_item


def test_manual_dataset_forge_builds_deduped_corpus(tmp_path):
    root = tmp_path / "manuals"
    root.mkdir()
    text = ("Gaia-Techne manual corpus as planetary symbolic memory. " * 40).strip()
    (root / "manual_a.txt").write_text(text, encoding="utf-8")
    (root / "manual_b.md").write_text(text, encoding="utf-8")
    (root / "lecture.mp4").write_bytes(b"not text")

    output = tmp_path / "forge"
    report = ManualDatasetForge(
        root=str(root),
        output_dir=str(output),
        min_chars=20,
        chunk_chars=240,
        chunk_overlap=20,
    ).build()

    assert report.candidates == 3
    assert report.documents == 2
    assert report.chunks > 0
    assert report.duplicate_chunks > 0
    assert (output / "corpus.jsonl").exists()
    assert (output / "manifest.jsonl").exists()
    assert (output / "stats.json").exists()

    corpus_rows = [
        json.loads(line)
        for line in (output / "corpus.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(corpus_rows) == report.chunks
    assert all(row["metadata"]["rights_status"] == "user_provided_review_required" for row in corpus_rows)

    manifest = [
        json.loads(line)
        for line in (output / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert any(row["reason"] == "media_requires_transcription" for row in manifest)


def test_drive_item_classification_matches_manual_folder_shape():
    pdf = classify_drive_item({"title": "Manual AGI 1.2.pdf", "mime_type": "application/pdf"})
    folder = classify_drive_item({
        "title": "Manual",
        "file_or_folder": "folder",
        "mime_type": "application/vnd.google-apps.folder",
    })
    video = classify_drive_item({"title": "seminario.mp4", "mime_type": "video/mp4"})
    code = classify_drive_item({"title": "gaia.py", "mime_type": "text/x-python"})

    assert pdf.status == "trainable"
    assert folder.status == "folder"
    assert video.status == "skipped"
    assert video.reason == "media_requires_transcription"
    assert code.status in {"trainable", "optional"}

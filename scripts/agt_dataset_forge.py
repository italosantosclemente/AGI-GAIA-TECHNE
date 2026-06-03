#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agt.dataset_forge import ManualDatasetForge, build_drive_inventory
from agt.web_corpus import WebCorpusHarvester, read_url_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an AGI-GAIA-TECHNE LLM corpus from local manuals."
    )
    parser.add_argument(
        "--input",
        help="Local folder containing manuals mirrored/downloaded from Drive.",
    )
    parser.add_argument(
        "--output",
        default="data/llm/manual_forge",
        help="Output directory for corpus.jsonl, manifest.jsonl, stats.json and shards.",
    )
    parser.add_argument("--include-code", action="store_true")
    parser.add_argument("--no-pdf", action="store_true")
    parser.add_argument("--min-chars", type=int, default=200)
    parser.add_argument("--chunk-chars", type=int, default=8000)
    parser.add_argument("--chunk-overlap", type=int, default=400)
    parser.add_argument(
        "--drive-listing-json",
        help=(
            "Optional JSON file produced from a Google Drive folder listing. "
            "This classifies Drive items but does not download contents."
        ),
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--url-file")
    parser.add_argument("--allow-private-hosts", action="store_true")
    parser.add_argument("--ignore-robots", action="store_true")
    args = parser.parse_args()

    urls = list(args.url)
    if args.url_file:
        urls.extend(read_url_file(args.url_file))
    if urls:
        harvester = WebCorpusHarvester(
            output_dir=str(Path(args.output) / "web_corpus"),
            chunk_chars=args.chunk_chars,
            chunk_overlap=args.chunk_overlap,
            allow_private_hosts=args.allow_private_hosts,
            respect_robots=not args.ignore_robots,
        )
        report = harvester.harvest(urls)
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return 0 if report.failed == 0 else 1

    if args.drive_listing_json:
        listing = json.loads(Path(args.drive_listing_json).read_text(encoding="utf-8"))
        items = listing.get("files", listing if isinstance(listing, list) else [])
        inventory = build_drive_inventory(items)
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        inventory_path = out_dir / "drive_inventory.json"
        inventory_path.write_text(
            json.dumps(inventory, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps({"drive_inventory": str(inventory_path), "items": len(inventory)}, indent=2))
        return 0

    if not args.input:
        parser.error("--input is required unless --drive-listing-json is provided.")

    forge = ManualDatasetForge(
        root=args.input,
        output_dir=args.output,
        include_code=args.include_code,
        include_pdfs=not args.no_pdf,
        min_chars=args.min_chars,
        chunk_chars=args.chunk_chars,
        chunk_overlap=args.chunk_overlap,
    )
    report = forge.build()

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("# AGI-GAIA-TECHNE Manual Dataset Forge\n")
        print(f"root={report.root}")
        print(f"output={report.output_dir}")
        print(f"candidates={report.candidates}")
        print(f"documents={report.documents}")
        print(f"chunks={report.chunks}")
        print(f"estimated_tokens={report.estimated_tokens}")
        print(f"corpus={report.corpus_path}")
        print(f"manifest={report.manifest_path}")
        print(f"stats={report.stats_path}")
        print(f"shards={report.shards_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

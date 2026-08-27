# Path: src/document_parser/cli.py
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

"""Command-line entry point for automation and smoke tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parser import DocumentParser
from .rag import build_rag_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse documents into Markdown or RAG-ready JSON.")
    parser.add_argument("source", help="Local path or HTTP(S) URL")
    parser.add_argument("--tool", default=None, help="Force a parser backend")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument("--rag", action="store_true", help="Export RAG chunk JSON instead of Markdown")
    parser.add_argument("--chunk-size", type=int, default=900)
    parser.add_argument("--overlap", type=int, default=120)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = DocumentParser(tool=args.tool, ocr_lang=args.ocr_language).parse(args.source)
    if args.rag:
        output = json.dumps(
            build_rag_json(result, args.source, chunk_size=args.chunk_size, overlap=args.overlap),
            ensure_ascii=False,
            indent=2,
        )
    else:
        output = result.get("content", "")

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

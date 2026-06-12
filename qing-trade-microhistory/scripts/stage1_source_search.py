#!/usr/bin/env python3
"""
Stage 1: DOCX Historical Source Search
=======================================
Extracts usable historical evidence from DOCX files that can't be grepped
with standard tools. Searches .docx, .txt, and .md files for configurable
keyword categories, producing hit counts and contextual excerpts.

Usage:
    python stage1_source_search.py --dir /path/to/archives --config config.yaml
    python stage1_source_search.py --dir /path/to/archives --keywords "土茯苓,大黃,rhubarb"
"""

import argparse
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


def strip_xml_tags(text: str) -> str:
    """Remove all XML tags from text."""
    return re.sub(r"<[^>]+>", "", text)


def read_docx_text(filepath: str) -> Optional[str]:
    """Extract plain text from a .docx file via zipfile."""
    try:
        with zipfile.ZipFile(filepath, "r") as z:
            xml_text = z.read("word/document.xml").decode("utf-8", errors="replace")
            return strip_xml_tags(xml_text)
    except Exception:
        return None


def read_text_file(filepath: str) -> Optional[str]:
    """Read plain text from .txt or .md file."""
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            with open(filepath, "r", encoding=enc, errors="replace") as f:
                return f.read()
        except Exception:
            continue
    return None


def load_config(config_path: str) -> Dict:
    """Load keyword categories from YAML config, or return a minimal dict."""
    try:
        import yaml

        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load()
    except Exception:
        return {}


def build_keyword_list(config: Optional[Dict] = None,
                       extra_keywords: Optional[List[str]] = None) -> List[str]:
    """Build a flat keyword list from config categories + extras."""
    keywords = list(extra_keywords or [])
    if config:
        for domain_name, domain_cfg in config.get("research_domains", {}).items():
            keywords.extend(domain_cfg.get("keywords", []))
    return list(dict.fromkeys(keywords))  # dedupe, preserve order


def search_files(search_dir: str,
                 keywords: List[str],
                 context_chars: int = 80) -> Dict:
    """
    Walk a directory tree and search all .docx/.txt/.md files for keywords.

    Returns a dict keyed by (dirname, filename) with per-keyword hit info.
    """
    results = {}

    for root, dirs, files in os.walk(search_dir):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            if fname.startswith("."):
                continue
            fpath = os.path.join(root, fname)

            text = None
            if fname.endswith(".docx"):
                text = read_docx_text(fpath)
            elif fname.endswith((".txt", ".md")):
                text = read_text_file(fpath)
            else:
                continue

            if not text:
                continue

            file_hits = {}
            for kw in keywords:
                matches = list(re.finditer(re.escape(kw), text, re.IGNORECASE))
                if matches:
                    excerpts = []
                    for m in matches:
                        start = max(0, m.start() - context_chars)
                        end = min(len(text), m.end() + context_chars)
                        excerpts.append(text[start:end].strip()[:200])
                    file_hits[kw] = {"count": len(matches), "excerpts": excerpts}

            if file_hits:
                rel = os.path.relpath(fpath, search_dir)
                results[rel] = file_hits

    return results


def print_report(results: Dict, keywords: List[str]):
    """Print a human-readable summary of search results."""
    # Per-keyword totals
    kw_totals = defaultdict(int)
    for fname, hits in results.items():
        for kw, info in hits.items():
            kw_totals[kw] += info["count"]

    print("=" * 60)
    print("  STAGE 1: DOCX Historical Source Search — Results")
    print("=" * 60)
    print(f"\nFiles with hits: {len(results)}")
    print(f"Keywords searched: {len(keywords)}")
    print(f"\n--- Per-keyword hit totals ---")
    for kw in sorted(kw_totals, key=kw_totals.get, reverse=True):
        print(f"  {kw:30s} : {kw_totals[kw]:5d}")

    print(f"\n--- Top 20 richest files ---")
    file_totals = {k: sum(vv["count"] for vv in v.values()) for k, v in results.items()}
    for fname, total in sorted(file_totals.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  [{total:5d}] {fname}")


def main():
    parser = argparse.ArgumentParser(
        description="Stage 1: Search DOCX/TXT/MD archives for historical keywords"
    )
    parser.add_argument("--dir", required=True, help="Directory to search recursively")
    parser.add_argument("--config", help="YAML config with research_domains")
    parser.add_argument("--keywords", help="Comma-separated extra keywords")
    parser.add_argument("--output", help="Save JSON results to this file")
    parser.add_argument("--context", type=int, default=80,
                        help="Characters of context around each hit")
    args = parser.parse_args()

    config = load_config(args.config) if args.config else {}
    extra = [k.strip() for k in args.keywords.split(",") if k.strip()] if args.keywords else []
    keywords = build_keyword_list(config, extra)

    if not keywords:
        print("ERROR: No keywords provided. Use --config or --keywords.", file=sys.stderr)
        return 1

    print(f"Searching {args.dir} for {len(keywords)} keywords...", file=sys.stderr)
    results = search_files(args.dir, keywords, args.context)

    if args.output:
        serializable = {}
        for fname, hits in results.items():
            serializable[fname] = {
                kw: {"count": info["count"], "excerpts": info["excerpts"]}
                for kw, info in hits.items()
            }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
        print(f"JSON saved to {args.output}", file=sys.stderr)

    print_report(results, keywords)
    return 0


if __name__ == "__main__":
    sys.exit(main())

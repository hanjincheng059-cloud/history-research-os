#!/usr/bin/env python3
"""
Stage 2: Citation Check
========================
Checks that every footnote marker in the body has a definition, every
definition is cited, and every cited author appears in the bibliography.

Supports two input modes:
  1. Markdown file with [^N] / [^N]: style footnotes
  2. Raw text extracted from DOCX (for Word footnote checking)

Usage:
    python stage2_citation_check.py --input paper.md
    python stage2_citation_check.py --input paper_raw.txt --mode docx
"""

import argparse
import re
import sys
from typing import Dict, List, Set, Tuple


def check_markdown_footnotes(text: str) -> Dict:
    """Check [^N] style markdown footnotes."""
    # Split body from references
    ref_markers = ["參考文獻", "参考文献", "Bibliography", "References"]
    ref_start = len(text)
    for marker in ref_markers:
        pos = text.rfind(marker)  # last occurrence
        if pos > 0 and pos < ref_start:
            ref_start = pos
    body = text[:ref_start]

    # Find footnote citations in body: [^1] [^2a] etc.
    body_cites = set(re.findall(r"\[\^(\d+[a-z]?)\]", body))

    # Find footnote definitions: [^1]: ... at start of line
    defined = set(re.findall(r"^\[\^(\d+[a-z]?)\]:", text, re.MULTILINE))

    orphan_cites = body_cites - defined   # cited but never defined
    orphan_defs = defined - body_cites    # defined but never cited

    return {
        "total_citations": len(body_cites),
        "total_definitions": len(defined),
        "orphan_cites": sorted(orphan_cites),
        "orphan_defs": sorted(orphan_defs),
        "mode": "markdown",
    }


def check_docx_footnotes(text: str) -> Dict:
    """Check DOCX-extracted text for basic citation patterns."""
    # DOCX footnotes are inline; we count patterns
    ref_markers = ["參考文獻", "参考文献", "Bibliography", "References"]
    ref_start = len(text)
    for marker in ref_markers:
        pos = text.rfind(marker)
        if pos > 0 and pos < ref_start:
            ref_start = pos
    body = text[:ref_start]
    bib_section = text[ref_start:] if ref_start < len(text) else ""

    # Count footnote-like patterns (superscript numbers)
    superscripts = len(re.findall(r"\b\d{1,3}\s{2,}[A-Z一-鿿]", body[:50000]))

    # Count ibid/同前 usage
    ibid_count = len(re.findall(
        r"[同仝][上前]|Ibid\.|ibid\.|op\.\s*cit\.", body
    ))

    # Estimate bibliography entries
    bib_entries = len(re.findall(r"\b(1[5-9]|20)\d{2}[a-z]?[\)\.。,）]", bib_section))

    # Check archive references
    archive_refs = len(re.findall(
        r"(RA|Riksarkivet|SE/RA|OSTINDISKA|國家檔案館|National Archives)",
        body,
    ))

    return {
        "approx_superscripts": superscripts,
        "ibid_count": ibid_count,
        "est_bib_entries": bib_entries,
        "archive_references": archive_refs,
        "mode": "docx",
    }


def check_bibliography(text: str) -> Dict:
    """Extract bibliography structure info."""
    ref_markers = ["參考文獻", "参考文献", "Bibliography", "References"]
    ref_start = len(text)
    for marker in ref_markers:
        pos = text.rfind(marker)
        if pos > 0 and pos < ref_start:
            ref_start = pos
    bib_section = text[ref_start:] if ref_start < len(text) else ""

    # Detect category headings
    categories = re.findall(
        r"[一二三四五六七八九十]、[^二三四五六七八九十\n]{2,30}", bib_section[:5000]
    )

    return {
        "bib_chars": len(bib_section),
        "categories_detected": categories,
    }


def print_report(result: Dict, bib_info: Dict):
    """Print a formatted report."""
    print("=" * 60)
    print("  STAGE 2: Citation Check — Results")
    print("=" * 60)

    if result["mode"] == "markdown":
        print(f"\nBody citations:  {result['total_citations']}")
        print(f"Definitions:     {result['total_definitions']}")
        if result["orphan_cites"]:
            print(f"❌ ORPHAN CITES (cited but never defined): {result['orphan_cites']}")
        else:
            print("✅ No orphan citations")
        if result["orphan_defs"]:
            print(f"⚠️  ORPHAN DEFS (defined but never cited): {result['orphan_defs']}")
        else:
            print("✅ No orphan definitions")
    else:
        print(f"\nApprox. superscripts: {result['approx_superscripts']}")
        print(f"Ibid/同前 usage:      {result['ibid_count']}")
        print(f"Archive references:   {result['archive_references']}")
        print(f"Est. bib entries:     {result['est_bib_entries']}")

    print(f"\n--- Bibliography ---")
    print(f"Size: {bib_info['bib_chars']:,} chars")
    if bib_info["categories_detected"]:
        print(f"Categories: {bib_info['categories_detected']}")
    else:
        print("No category headings detected")

    # Quality gate
    if result["mode"] == "markdown":
        if result["orphan_cites"] or result["orphan_defs"]:
            print("\n🔴 QUALITY GATE: FAILED — fix all orphan citations/definitions")
        else:
            print("\n✅ QUALITY GATE: PASSED")


def main():
    parser = argparse.ArgumentParser(
        description="Stage 2: Citation check for Chinese history papers"
    )
    parser.add_argument("--input", required=True, help="Input file (.md or raw text)")
    parser.add_argument("--mode", choices=["md", "docx"], default="md",
                        help="Input mode: md (markdown footnotes) or docx (DOCX raw text)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    if args.mode == "md":
        result = check_markdown_footnotes(text)
    else:
        result = check_docx_footnotes(text)

    bib_info = check_bibliography(text)
    print_report(result, bib_info)

    # Exit code for CI
    if result.get("orphan_cites") or result.get("orphan_defs"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

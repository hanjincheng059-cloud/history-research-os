#!/usr/bin/env python3
"""
Stage 6: Streamline
====================
Analyzes word count per chapter/section, identifies cuttable content,
and suggests specific cuts without removing substance.

Usage:
    python stage6_streamline.py --input paper.md
    python stage6_streamline.py --input paper.md --target 0.15  # target 15% reduction
"""

import argparse
import re
import sys
from collections import OrderedDict
from typing import Dict, List, Tuple


def count_chinese_chars(text: str) -> int:
    """Count CJK characters."""
    return len(re.findall(r"[一-鿿]", text))


def count_words(text: str) -> int:
    """Count Chinese chars + English words."""
    chinese = count_chinese_chars(text)
    # Approximate English word count
    english = len(re.findall(r"[a-zA-Z]+", text))
    return chinese + english


def split_chapters(text: str) -> List[Tuple[str, str]]:
    """Split text into chapters by Chinese numeral headers."""
    # Remove bibliography
    ref_markers = ["參考文獻", "参考文献", "Bibliography"]
    body = text
    for marker in ref_markers:
        pos = text.rfind(marker)
        if pos > 0:
            body = text[:pos]
            break

    # Split on chapter markers
    pattern = r"\n(?=第[一二三四五六七八九十]+章)"
    parts = re.split(pattern, body)

    chapters = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Extract title (first line)
        lines = part.split("\n")
        title = lines[0].strip()[:60] if lines else "(untitled)"
        chapters.append((title, part))

    return chapters


def find_cuttable_content(text: str) -> List[Dict]:
    """Identify patterns that are safe to cut."""
    findings = []

    # Redundant signposting phrases
    redundant = [
        "換句話說", "也就是說", "更進一步說", "總而言之", "綜上所述",
        "換言之", "簡言之", "要之", "總之", "一句話",
    ]
    for phrase in redundant:
        matches = list(re.finditer(re.escape(phrase), text))
        if len(matches) > 3:  # more than 3 occurrences is suspicious
            findings.append({
                "type": "redundant_phrase",
                "phrase": phrase,
                "count": len(matches),
                "suggestion": f"Reduce '{phrase}' from {len(matches)} occurrences",
            })

    # Extended theoretical elaborations (paragraphs with many theory words)
    theory_words = ["理論", "範式", "框架", "paradigm", "framework", "theoretical"]
    # ... simplified for brevity

    # Triple-layer distinctions
    layer_patterns = re.findall(
        r"(第一[層，、].+?第二[層，、].+?第三[層，、].+?(?:。|\n))", text
    )
    if len(layer_patterns) > 2:
        findings.append({
            "type": "layered_distinctions",
            "count": len(layer_patterns),
            "suggestion": "Consider collapsing 3-layer distinctions to 2 layers",
        })

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Stage 6: Streamline — cut bloat without cutting substance"
    )
    parser.add_argument("--input", required=True, help="Input markdown file")
    parser.add_argument("--target", type=float, default=0.12,
                        help="Target reduction ratio (default 0.12 = 12%%)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    chapters = split_chapters(text)

    print("=" * 60)
    print("  STAGE 6: Streamline — Chapter Word Counts")
    print("=" * 60)

    total = 0
    ch_counts = []
    for title, content in chapters:
        wc = count_words(content)
        chinese = count_chinese_chars(content)
        total += wc
        ch_counts.append((title, wc, chinese))

    for title, wc, chinese in ch_counts:
        pct = wc / total * 100 if total else 0
        bar = "█" * int(pct / 2)
        print(f"  {title:40s}  {chinese:>6,}字  ({pct:5.1f}%) {bar}")

    print(f"\n  TOTAL: ~{total:,} words (~{count_chinese_chars(text):,} Chinese chars)")
    target_total = int(total * (1 - args.target))
    print(f"  TARGET ({args.target*100:.0f}% reduction): ~{target_total:,} words")

    # Find cuttable content
    print(f"\n--- Cuttable content scan ---")
    findings = find_cuttable_content(text)
    if findings:
        for f in findings:
            print(f"  {f['type']}: {f['suggestion']}")
    else:
        print("  No obvious cut candidates found automatically")
        print("  (Manual review recommended — check longest chapters above)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

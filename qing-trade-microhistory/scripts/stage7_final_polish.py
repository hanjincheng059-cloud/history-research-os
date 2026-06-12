#!/usr/bin/env python3
"""
Stage 7: Final Polish & DOCX Generation
=========================================
Generates a submission-ready DOCX from the finalized markdown.
Handles Chinese-language metadata, footnote formatting, and
bibliography placement.

Usage:
    python stage7_final_polish.py --input paper.md --output paper.docx
    python stage7_final_polish.py --input paper.md --output paper.docx --lang zh-TW
"""

import argparse
import re
import sys
import subprocess
from pathlib import Path


def check_abstract_honesty(text: str) -> list:
    """Check abstract for methodological honesty markers."""
    issues = []

    abstract_match = re.search(r"摘要(.+?)(?=關鍵詞|Abstract|第[一二三四五六七八九十]+章)", text, re.DOTALL)
    if not abstract_match:
        issues.append("⚠️  No Chinese abstract found")
        return issues

    abstract = abstract_match.group(1)

    # Good patterns: explicit limitation statements
    good_patterns = [
        "本文不", "局限", "不足", "有待", "本文並不", "本文并非",
        "This article does not claim", "本文未",
    ]
    has_limitation = any(p in abstract for p in good_patterns)

    # Warning patterns: overclaiming
    warn_patterns = [
        "證明", "prove", "推翻", "徹底改變",
    ]
    has_overclaim = any(p in abstract for p in warn_patterns)

    if not has_limitation:
        issues.append("💡 Abstract could benefit from an explicit limitation statement")
    if has_overclaim:
        issues.append("⚠️  Abstract may overclaim — consider softer language")

    if not issues:
        issues.append("✅ Abstract reads as honest and appropriately scoped")

    return issues


def check_title_format(text: str) -> str:
    """Check if title follows two-part format recommended for Chinese history papers."""
    first_line = text.strip().split("\n")[0]
    if "——" in first_line or "：" in first_line or ":" in first_line:
        return f"✅ Two-part title detected: {first_line[:80]}"
    return f"💡 Consider two-part title (concrete image + analytical frame): {first_line[:80]}"


def generate_docx(input_path: str, output_path: str, lang: str = "zh-TW") -> bool:
    """Generate DOCX via pandoc or fallback to pypandoc."""
    # Try pandoc CLI first
    try:
        result = subprocess.run(
            [
                "pandoc", input_path,
                "-f", "markdown",
                "-t", "docx",
                "--metadata", f"lang={lang}",
                "-o", output_path,
            ],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            print(f"✅ DOCX generated via pandoc: {output_path}")
            return True
        else:
            print(f"Pandoc error: {result.stderr[:200]}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Fallback: pypandoc
    try:
        import pypandoc
        pypandoc.convert_file(
            input_path, "docx",
            outputfile=output_path,
            extra_args=["-f", "markdown", "-t", "docx", "--metadata", f"lang={lang}"],
        )
        print(f"✅ DOCX generated via pypandoc: {output_path}")
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"Pypandoc error: {e}")

    # Last resort: python-docx basic generation
    print("❌ Neither pandoc nor pypandoc available.")
    print("   Install one:  brew install pandoc   OR   pip install pypandoc")
    return False


def count_stats(text: str) -> dict:
    """Count final paper statistics."""
    chinese = len(re.findall(r"[一-鿿]", text))
    footnotes = len(re.findall(r"\[\^\d+[a-z]?\]", text))
    bib_refs = len(re.findall(r"\b(1[5-9]|20)\d{2}[a-z]?[\)\.。,）]", text))
    return {
        "chinese_chars": chinese,
        "footnote_markers": footnotes,
        "bib_references": bib_refs,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Stage 7: Final polish and DOCX generation"
    )
    parser.add_argument("--input", required=True, help="Final markdown file")
    parser.add_argument("--output", help="Output DOCX path (default: input name + .docx)")
    parser.add_argument("--lang", default="zh-TW", help="Document language (default: zh-TW)")
    parser.add_argument("--check-only", action="store_true",
                        help="Only check, don't generate DOCX")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    print("=" * 60)
    print("  STAGE 7: Final Polish — Quality Checks")
    print("=" * 60)

    print(f"\n--- Title ---")
    print(check_title_format(text))

    print(f"\n--- Abstract ---")
    for issue in check_abstract_honesty(text):
        print(f"  {issue}")

    stats = count_stats(text)
    print(f"\n--- Final Stats ---")
    print(f"  Chinese characters: {stats['chinese_chars']:,}")
    print(f"  Footnote markers:   {stats['footnote_markers']}")
    print(f"  Bib references:     {stats['bib_references']}")

    if not args.check_only:
        output = args.output or Path(args.input).with_suffix(".docx")
        generate_docx(args.input, str(output), args.lang)

    print("\n✅ Stage 7 complete. Open the DOCX and verify:")
    print("   - Abstract is honest about limitations")
    print("   - Spot-check 3 footnotes")
    print("   - Bibliography is complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())

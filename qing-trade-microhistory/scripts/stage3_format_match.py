#!/usr/bin/env python3
"""
Stage 3: Format Match (Reference Paper)
=========================================
Analyzes a reference/target DOCX paper and extracts formatting rules,
then checks the working paper for compliance or applies transformations.

Usage:
    # Analyze reference paper formatting
    python stage3_format_match.py --reference published_paper.docx

    # Check working paper against reference rules
    python stage3_format_match.py --reference published_paper.docx --check my_paper.md
"""

import argparse
import re
import sys
import zipfile
from typing import Dict, List, Optional


def strip_xml_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def read_docx_text(filepath: str) -> str:
    with zipfile.ZipFile(filepath, "r") as z:
        xml_text = z.read("word/document.xml").decode("utf-8", errors="replace")
    return strip_xml_tags(xml_text)


def analyze_reference(text: str) -> Dict:
    """Extract formatting rules from a reference paper."""
    rules = {}

    # Section numbering style
    if re.search(r"[一二三四五六七八九十]、", text[:20000]):
        rules["chapter_style"] = "chinese_numeral"  # 一、二、三、
    elif re.search(r"\nI\.\s", text[:20000]):
        rules["chapter_style"] = "roman"  # I. II. III.
    else:
        rules["chapter_style"] = "arabic"  # 1. 2. 3.

    # Subsection numbering
    if re.search(r"\n[1-9]、", text[:20000]):
        rules["subsection_style"] = "arabic_cjk"  # 1、2、
    elif re.search(r"\n[1-9]\.[1-9]", text[:20000]):
        rules["subsection_style"] = "dotted"  # 1.1 1.2
    elif re.search(r"\n（[一二三四五六七八九十]）", text[:20000]):
        rules["subsection_style"] = "paren_numeral"  # （一）（二）
    else:
        rules["subsection_style"] = "unknown"

    # YAML frontmatter
    rules["has_frontmatter"] = bool(re.match(r"^\s*---", text))

    # Markdown headers
    rules["uses_md_headers"] = bool(re.search(r"^#+\s", text[:5000], re.MULTILINE))

    # Keywords format
    kw_match = re.search(r"關鍵詞[：:]", text[:10000])
    if kw_match:
        rules["keyword_prefix"] = kw_match.group(0)

    # Abstract placement
    abstract_pos = text.find("摘要")
    rules["abstract_position"] = "early" if 0 < abstract_pos < 5000 else "late" if abstract_pos > 0 else "none"

    # Separator usage
    rules["triple_dash_count"] = len(re.findall(r"^---\s*$", text[:20000], re.MULTILINE))

    # Title format
    title_line = text.strip().split("\n")[0] if text.strip() else ""
    rules["title_has_author_inline"] = len(title_line) > 80  # heuristic

    return rules


def check_compliance(working_text: str, rules: Dict) -> List[str]:
    """Check working paper against reference rules, return issues."""
    issues = []

    # Chinese history journals typically expect NO markdown headers, NO frontmatter
    if rules["chapter_style"] == "chinese_numeral":
        if re.search(r"^#+\s", working_text[:5000], re.MULTILINE):
            issues.append("⚠️  Uses markdown # headers — reference paper uses 一、二、三、")
    if not rules["has_frontmatter"]:
        if re.match(r"^\s*---", working_text):
            issues.append("⚠️  Has YAML frontmatter — reference paper does not")
    if rules["triple_dash_count"] == 0:
        working_dashes = len(re.findall(r"^---\s*$", working_text[:20000], re.MULTILINE))
        if working_dashes > 0:
            issues.append(f"⚠️  {working_dashes} '---' separators — reference paper has none")

    if not issues:
        issues.append("✅ Format looks compatible with reference paper")

    return issues


def print_rules(rules: Dict):
    """Print extracted formatting rules."""
    print("=" * 60)
    print("  STAGE 3: Format Match — Reference Paper Rules")
    print("=" * 60)
    for key, value in rules.items():
        print(f"  {key:25s}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="Stage 3: Match paper formatting to reference paper"
    )
    parser.add_argument("--reference", required=True,
                        help="Path to reference/published paper (.docx)")
    parser.add_argument("--check", help="Path to working paper to check for compliance")
    args = parser.parse_args()

    ref_text = read_docx_text(args.reference)
    rules = analyze_reference(ref_text)
    print_rules(rules)

    if args.check:
        with open(args.check, "r", encoding="utf-8", errors="replace") as f:
            work_text = f.read()
        print(f"\n--- Compliance check: {args.check} ---")
        issues = check_compliance(work_text, rules)
        for issue in issues:
            print(f"  {issue}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

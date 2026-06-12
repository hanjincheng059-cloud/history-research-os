#!/usr/bin/env python3
"""
Run the full Qing Trade Microhistory pipeline end-to-end.

Usage:
    python run_pipeline.py --input paper.md --archives ./sources/ --reference model.docx
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent / "scripts"


def run_stage(name, args_list, exit_on_fail=True):
    """Run a pipeline stage script."""
    script = SCRIPT_DIR / f"stage{name}.py"
    if not script.exists():
        print(f"  [SKIP] {script} not found — this stage is AI-driven")
        return True

    cmd = [sys.executable, str(script)] + args_list
    print(f"\n{'='*60}")
    print(f"  RUNNING: {' '.join(cmd)}")
    print(f"{'='*60}")
    result = subprocess.run(cmd)
    if result.returncode != 0 and exit_on_fail:
        print(f"  ❌ Stage {name} FAILED")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Qing Trade Microhistory — Full Pipeline Runner"
    )
    parser.add_argument("--input", required=True, help="Input markdown paper")
    parser.add_argument("--archives", required=True, help="Directory with DOCX/PDF sources")
    parser.add_argument("--reference", help="Reference paper for format matching")
    parser.add_argument("--config", help="YAML config file")
    parser.add_argument("--output", help="Output DOCX path")
    parser.add_argument("--stage", type=int, choices=range(1, 8),
                        help="Run only a specific stage")
    args = parser.parse_args()

    print("=" * 60)
    print("  QING TRADE MICROHISTORY — PAPER PIPELINE")
    print("=" * 60)
    print(f"  Input:    {args.input}")
    print(f"  Archives: {args.archives}")
    print(f"  Reference: {args.reference or '(none)'}")
    print(f"  Output:   {args.output or '(auto)'}")

    stages = [
        (1, ["--dir", args.archives, "--output", "stage1_results.json"] +
            (["--config", args.config] if args.config else [])),
        (2, ["--input", args.input]),
        (3, ["--reference", args.reference, "--check", args.input] if args.reference else []),
        (4, []),  # AI-driven
        (5, []),  # AI-driven
        (6, ["--input", args.input]),
        (7, ["--input", args.input] +
            (["--output", args.output] if args.output else [])),
    ]

    for num, args_list in stages:
        if args.stage and num != args.stage:
            continue
        if num in (4, 5):
            print(f"\n  Stage {num}: AI-driven — run with Claude Code or review manually")
            continue
        if num == 3 and not args.reference:
            print(f"\n  Stage {num}: SKIP — no reference paper provided")
            continue
        if not run_stage(f"{num}", args_list):
            print(f"\nPipeline stopped at Stage {num}. Fix issues and re-run.")
            return 1

    print(f"\n{'='*60}")
    print("  ✅ PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"  Output: {args.output or Path(args.input).with_suffix('.docx')}")
    print(f"  Next: Open the DOCX, verify abstract/footnotes/bibliography")
    return 0


if __name__ == "__main__":
    sys.exit(main())

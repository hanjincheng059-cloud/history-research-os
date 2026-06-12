#!/usr/bin/env python3
"""
Qing Trade Microhistory — Paper Pipeline
=========================================
A 7-stage pipeline for Chinese historical material-culture papers,
from MD draft to submission-ready DOCX.

Stages:
  1. Source Search     — Extract evidence from DOCX archives
  2. Citation Check    — Verify footnote/bibliography integrity
  3. Format Match      — Match reference paper formatting
  4. Peer Review       — Simulated 5-reviewer panel (AI-driven)
  5. Structured Revision — Address every review item
  6. Streamline        — Cut bloat without cutting substance
  7. Final Polish      — Generate submission-ready DOCX
"""

__version__ = "0.1.0"

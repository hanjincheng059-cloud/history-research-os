# Qing Trade Microhistory — Paper Pipeline

> 清代贸易微历史论文流水线 — 从 MD 草稿到投稿就绪 DOCX 的全自动管线

**7-stage pipeline for Chinese historical material-culture papers**, from MD draft
through archival source search, citation verification, format matching, simulated peer
review, structured revision, streamlining, and final DOCX generation.

Designed for papers that trace a commodity/object through the Qing-era Canton trade
system, using the "social life of things" (Appadurai/Kopytoff) framework.

---

## 🗺️ Pipeline

```
MD draft → [1. Source search] → [2. Citation check] → [3. Format match]
       → [4. Peer review] → [5. Revision] → [6. Streamline] → [7. Final DOCX]
```

| Stage | Description | Automation |
|-------|-------------|------------|
| 1. Source Search | Extract evidence from DOCX/TXT/MD archives | 🐍 Python |
| 2. Citation Check | Verify footnote ↔ bibliography integrity | 🐍 Python |
| 3. Format Match | Match reference paper formatting | 🐍 Python |
| 4. Peer Review | 5-reviewer simulated panel (EIC + 3 reviewers + Devil's Advocate) | 🤖 AI |
| 5. Revision | Address every review item by priority | 🤖 AI |
| 6. Streamline | Cut bloat, preserve substance | 🐍 Python |
| 7. Final Polish | Generate submission-ready DOCX | 🐍 Python |

---

## 📦 Installation

```bash
# Python deps
pip install pyyaml pypandoc

# For DOCX generation:
brew install pandoc        # macOS
# OR
pip install pypandoc       # cross-platform (still needs pandoc binary)
```

---

## 🚀 Quick Start

### Full automated pipeline
```bash
python run_pipeline.py \
  --input paper.md \
  --archives ./historical_sources/ \
  --reference model_paper.docx \
  --output submission.docx
```

### Run individual stages
```bash
# Stage 1: Search historical archives for keywords
python scripts/stage1_source_search.py \
  --dir ./archives \
  --config config.yaml \
  --output search_results.json

# Stage 2: Citation integrity check
python scripts/stage2_citation_check.py \
  --input paper.md --mode md

# Stage 3: Format match against reference
python scripts/stage3_format_match.py \
  --reference model_paper.docx \
  --check paper.md

# Stage 6: Word count per chapter + cut candidates
python scripts/stage6_streamline.py \
  --input paper.md --target 0.12

# Stage 7: Quality check + DOCX generation
python scripts/stage7_final_polish.py \
  --input paper.md --output submission.docx
```

### With Claude Code (Stages 4-5)
Stage 4 (peer review) and Stage 5 (revision) are AI-driven. Use the
[SKILL.md](SKILL.md) with Claude Code or any LLM that supports tool use.
Reviewer personas are defined in [prompts/reviewer_personas.md](prompts/reviewer_personas.md).

---

## 📂 Project Structure

```
qing-trade-microhistory/
├── SKILL.md                        # Claude Code skill definition
├── run_pipeline.py                 # Full pipeline runner
├── config.example.yaml             # Example configuration
├── README.md                       # This file
├── README_zh.md                    # 中文文档
├── scripts/
│   ├── __init__.py
│   ├── stage1_source_search.py     # DOCX archive keyword search
│   ├── stage2_citation_check.py    # Footnote/bibliography integrity
│   ├── stage3_format_match.py      # Reference paper format analysis
│   ├── stage6_streamline.py        # Word count + redundancy detection
│   └── stage7_final_polish.py      # DOCX generation + quality checks
└── prompts/
    ├── reviewer_personas.md        # 5-reviewer panel definitions
    └── revision_protocol.md        # Stage 5 revision methodology
```

---

## 🎯 What this pipeline catches

| Problem | Stage | Fix |
|----------|-------|-----|
| Missing footnote definitions | 2 | 🔴 Blocking |
| Bibliography entries without citations | 2 | 🔴 Blocking |
| Wrong section numbering for target journal | 3 | 🟡 Format |
| Argument overreach ("demonstrates" vs "suggests") | 4 | 🔴 Content |
| Core evidence with directionality problem | 4 → 5 | 🔴 Content |
| "待补入" markers in submission draft | 5 | 🔴 Blocking |
| Redundant theoretical elaborations | 6 | 🟡 Polish |
| Overlong chapters (imbalanced structure) | 6 | 🟡 Polish |
| Abstract without limitation statement | 7 | 🟢 Polish |
| DOCX generated from stale MD | 7 | 🔴 Blocking |

---

## 📝 Configuration

See [config.example.yaml](config.example.yaml) for a full example. Key sections:

```yaml
# Research domain keywords (used in Stage 1)
research_domains:
  "清代廣州貿易":
    keywords:
      - "廣州"
      - "Canton"
      - "十三行"
      - "粵海關"
      - "行商"
    priority: 5

# Citation check settings
citation:
  footnote_style: "markdown"  # or "docx"

# Streamline target
streamline:
  target_reduction: 0.12  # 12%
```

---

## 🏛️ Example Paper

The pipeline was designed for and tested on:

> **清中前期中國與瑞典貿易研究——以廣州口岸與瑞典東印度公司為中心（1732-1813）**
>
> A PhD dissertation examining Sino-Swedish trade through the Canton system,
> arguing that the trade was a complex multi-commodity, multi-route,
> multi-currency economic practice — not simply "silver for tea."

### Pipeline results on this paper:
- 303,696 total characters, ~180K Chinese characters
- 586 footnotes checked, 2 orphan definitions found
- 5 reviewers identified 5 🔴 must-fix issues and 7 🟡 recommendations
- Format: 9 chapters, 中国史论文格式 (一、 1、)

---

## 🧪 Reviewer Panel (Stage 4)

| Role | Expertise | Focus |
|------|-----------|-------|
| Editor-in-Chief | Global/maritime history | Structure, reader fit, thesis clarity |
| Reviewer 1 | Material culture / global commodities | Appadurai framework, commodity biography depth |
| Reviewer 2 | Canton trade / Qing socio-economic history | Archival methodology, 行商 networks, 粵海關 |
| Reviewer 3 | Nordic / Swedish East India Company | Swedish historiography, German/Swedish terminology |
| Devil's Advocate | Skeptical generalist | Circular reasoning, alternative explanations, overclaiming |

Output includes a prioritized **Actionable Revision Roadmap** with
🔴 must-fix / 🟡 strongly recommended / 🟢 optional items.

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- Built for Qing dynasty trade / material culture history papers
- Inspired by Appadurai (1986), Kopytoff (1986) "social life of things"
- Tested on Swedish East India Company archival materials (Riksarkivet, RA)
- Uses the same `zipfile` + `word/document.xml` method for DOCX parsing as the broader evil-read-arxiv project

---

*Built for historians, not just paper skimmers.*

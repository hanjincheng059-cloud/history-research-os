---
name: qing-trade-microhistory
description: Use when writing or revising a Chinese historical material-culture paper (Qing dynasty, Canton trade, global commodity history) — starting from MD draft, searching DOCX historical archives, running citation checks, matching reference-paper formatting, conducting simulated peer review, and producing a submission-ready DOCX. Triggers: 清代贸易论文, 物质文化史, 广州贸易, 全球商品史, 修改中国史论文, revise Chinese history paper, microhistory paper pipeline.
---

# Qing Trade Microhistory Paper Pipeline

## Overview

End-to-end pipeline for a Chinese historical material-culture paper: MD draft → DOCX source search → citation check → format match → simulated peer review → structured revision → streamline → final DOCX. Designed for papers that trace a single object through the Canton trade system using the "social life of things" framework.

## When to Use

- You have an MD draft of a Chinese history paper and a folder of DOCX historical sources
- The paper traces a commodity/object through Qing-era Canton trade into Europe
- You need to match the formatting of an existing reference paper
- You want simulated peer review before real submission
- The paper uses Appadurai/Kopytoff "social life of things" or similar framework

## Pipeline Stages

```
MD draft → [1. Source search] → [2. Citation check] → [3. Format match] → [4. Peer review] → [5. Revision] → [6. Streamline] → [7. Final DOCX]
```

Each stage has a quality gate. Don't skip.

---

## 1. Source Search (DOCX Archives)

**Goal:** Extract usable historical evidence from DOCX files that can't be grepped with standard tools.

**Pattern:**
```python
import zipfile, re, os

for fname in sorted(os.listdir('.')):
    if not fname.endswith('.docx'): continue
    with zipfile.ZipFile(fname, 'r') as z:
        text = z.read('word/document.xml').decode('utf-8')
        text = re.sub(r'<[^>]+>', '', text)
        # Run keyword searches on `text`
```

**Search strategy — three passes:**
1. **Broad sweep**: 15-20 keywords covering all paper themes (character names, place names, commodity names, institution names)
2. **Count-only**: Count hits per category to identify which volumes are richest
3. **Precision extraction**: Pull full context (±80 chars) for the most relevant categories only

**Quality gate:** You must have at least one category of direct archival evidence (tariff data, memorials, cargo lists) that the paper's core argument depends on. Pure inference from "absence" is not enough.

---

## 2. Citation Check

**Goal:** Every footnote marker in the body has a definition, every definition is cited, every cited author appears in the bibliography.

**Pattern:**
```python
import re
body_footnotes = set(re.findall(r'\[\^(\d+[a-z]?)\]', body_text))
defined_footnotes = set(re.findall(r'^\[\^(\d+[a-z]?)\]:', body_text, re.MULTILINE))

orphan_cites = body_footnotes - defined_footnotes   # Cited but never defined
orphan_defs = defined_footnotes - body_footnotes    # Defined but never cited
```

**Quality gate:** Zero orphan citations, zero orphan definitions. Every author cited in footnotes must appear in the bibliography. Fix all mismatches before proceeding.

---

## 3. Format Match (Reference Paper)

**Goal:** Make the working paper look exactly like an existing published paper in the same field.

**Process:**
1. Read the reference DOCX: extract text via `zipfile` + `word/document.xml`
2. Identify formatting rules from the reference:
   - Section numbering style (一、/ 1. / I.)
   - Subsection style (1、/ 1.1 / a))
   - Abstract placement and keyword format
   - Footnote placement (per-page vs end-of-document)
   - Presence/absence of YAML frontmatter
   - Separator usage (`---` between sections?)
3. Apply transformations via Python regex on the working MD
4. Regenerate DOCX via Pandoc

**Common Chinese history paper patterns:**
- No YAML frontmatter
- Title + author inline (no `#` markers)
- Chapters: `一、` `二、` (no `##`)
- Subsections: `1、` `2、` (no `###`)
- Keywords inline: `關鍵詞：` not `**關鍵詞：**`
- No `---` separators between sections

**Quality gate:** Open both papers side by side. They should look like they belong in the same journal.

---

## 4. Simulated Peer Review

**Goal:** Find argumentative weaknesses before real reviewers do.

**Reviewer panel (5 personas):**

| Role | Expertise | What they catch |
|------|-----------|-----------------|
| Editor-in-Chief | Broad field knowledge | Structural problems, reader fit |
| Reviewer 1 | Material culture / global commodities | Theory gaps, Appadurai framework misuse |
| Reviewer 2 | Daoism / Chinese religion | Religious studies inaccuracies |
| Reviewer 3 | Canton trade / Qing social-economic history | Archival methodology issues |
| Devil's Advocate | Skeptical generalist | Circular reasoning, alternative explanations |

**Output format:**
- Each reviewer writes: overall impression → specific strengths → problems to fix → suggested revisions
- EIC writes overall judgment (Accept / R&R / Reject)
- Final section: **Actionable Revision Roadmap** with priority levels (🔴 must-fix / 🟡 strongly recommended / 🟢 optional)

**Quality gate:** The roadmap must identify at least one 🔴 issue that, if unfixed, would cause a real reviewer to recommend rejection.

---

## 5. Structured Revision

**Goal:** Address every review item systematically.

**Process:**
1. Create TodoWrite items for each review point
2. Address 🔴 items first (these affect core argument validity)
3. Address 🟡 items second (these improve paper quality)
4. Address 🟢 items last (optional polish)
5. After each batch, re-run citation check to catch broken references

**Pattern for methodology honesty (most common 🔴 fix):**
When the core evidence has a directionality problem (e.g., import tariffs used to argue about exports), add a short paragraph that:
- States the limitation explicitly
- Explains why the evidence is still valid despite the limitation
- Marks this as a limitation in the conclusion

**Quality gate:** All 🔴 and 🟡 items resolved. Citation check passes again.

---

## 6. Streamline

**Goal:** Cut bloat without cutting substance.

**Process:**
1. Run word count per chapter/section
2. Flag the largest section — it's usually the best canditate for cuts
3. Identify cuttable content:
   - Extended theoretical elaborations that repeat points made elsewhere
   - Supplementary comparisons that are "interesting but not necessary"
   - Overlong methodology justifications (keep the core, cut the repetition)
4. Cut, then re-run citation check (removing content may orphan footnotes)
5. Remove orphaned bibliography entries

**What's usually safe to cut:**
- Three-layer theoretical distinctions when one layer suffices
- Supplementary comparison cases that aren't part of the core argument
- Redundant signposting phrases ("换句话说", "也就是说", "更进一步说")

**Quality gate:** Word count reduced by 10-15%. No core evidence removed. Citation check passes.

---

## 7. Final Polish

**Abstract:** Should be honest about what the paper does AND doesn't claim. Prefer "This article does not claim to..." over "This article demonstrates that...". State methodological limitations upfront in the abstract itself.

**Title:** Chinese history papers benefit from two-part titles: concrete image + analytical frame. A person name (鐵拐李) paired with a historical event (馬戛爾尼) signals the paper's temporal and cultural scope instantly.

**DOCX generation:**
```bash
python3 -c "
import pypandoc
pypandoc.convert_file('paper.md', 'docx', outputfile='paper.docx',
    extra_args=['-f', 'markdown', '-t', 'docx', '--metadata', 'lang=zh-TW'])
"
```

**Quality gate:** Open the DOCX. Read the abstract, spot-check three footnotes, verify the bibliography is complete.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Searching DOCX with `strings` or `grep` directly | Always use Python `zipfile` + `word/document.xml` + `re.sub(r'<[^>]+>', '', text)` |
| Using import tariff data to argue about exports without acknowledging the directionality problem | Add explicit methodology note: state the limitation, explain the bridging logic, mark as limitation in conclusion |
| Leaving "佛像对比" or other cut content referenced in remaining text | After any cut, grep for the cut term across the entire file |
| Letting footnote numbering break after major cuts | Re-run the full citation check script after every major edit batch |
| Generating DOCX from stale MD | Always regenerate DOCX as the final step |

## Example: Full Pipeline Script

```bash
# 1. Source search
python3 << 'EOF'
import zipfile, re, os
keywords = ['葫', '鼻煙壺', '粵海關', 'curiosit', '大黃', 'rhubarb', 'Macartney']
for fname in sorted(os.listdir('.')):
    if not fname.endswith('.docx'): continue
    with zipfile.ZipFile(fname, 'r') as z:
        text = z.read('word/document.xml').decode('utf-8')
        text = re.sub(r'<[^>]+>', '', text)
        for kw in keywords:
            for m in re.finditer(kw, text):
                start = max(0, m.start()-60)
                end = min(len(text), m.end()+60)
                print(f'[{fname[:30]}] {text[start:end].strip()[:120]}')
EOF

# 2. Citation check (run after every major edit)
python3 -c "
import re
with open('paper.md') as f: md = f.read()
body = md.split('參考文獻')[0]
cites = set(re.findall(r'\[\^(\d+[a-z]?)\]', body))
defs = set(re.findall(r'^\[\^(\d+[a-z]?)\]:', md, re.MULTILINE))
print('Missing defs:', cites - defs)
print('Uncited defs:', defs - cites)
"

# 6. Word count per chapter
python3 -c "
import re
with open('paper.md') as f: md = f.read()
for ch in re.split(r'\n(?=[一二三四五六]、)', md.split('參考文獻')[0]):
    title = ch.split('\n')[0][:50]
    count = len(re.findall(r'[一-鿿]', ch))
    print(f'{title}: ~{count}')
"
```

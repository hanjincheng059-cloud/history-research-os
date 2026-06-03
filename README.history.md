# History Research Mode

`evil-read-arxiv` can be used as an AI-native research workflow for historians and humanities researchers, not only as an arXiv reader.

## Positioning

Built for historians, not just paper skimmers:

- discover secondary scholarship and source leads
- triage works by research question
- generate Obsidian-ready notes
- map people, places, institutions, materials, routes, and arguments
- turn reading into evidence-backed memos

## Quick Start

1. Copy the history template:

```bash
cp config.history.example.yaml config.yaml
```

2. Edit `config.yaml`:

- set `vault_path`
- rename domains for your project
- add bilingual keywords
- keep `semantic_scholar_only: true` for non-arXiv humanities domains

3. Configure your API key:

```bash
cp data/api_settings.example.json data/api_settings.json
```

or set environment variables:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key
ANTHROPIC_BASE_URL=https://api.anthropic.com
```

## Recommended Historical Note Template

```markdown
---
title:
authors:
year:
source_type:
domain:
keywords:
status: inbox
---

# Title

## 一句话定位

## 核心问题

## 主要论点

## 证据与材料

## 方法

## 与我的研究关系

## 可引用点

## 疑问与待查

## 下一步
```

## Humanities Analysis Fields

When adapting prompts or UI copy for history, prefer these fields over AI/ML-only fields such as "experiments" and "benchmarks":

- central argument
- source base
- evidence quality
- historiographic position
- primary/secondary source type
- relevant people, institutions, places, routes, and materials
- claim supported by this work
- next source to check

## Product Direction

The long-term direction is a research OS for history and humanities:

- source adapters for Semantic Scholar, OpenAlex, Crossref, WorldCat/library catalogs, PubMed, and archival catalogs
- source-type-aware ranking
- Obsidian export for source notes and argument memos
- feedback reasons such as relevance, evidence value, historiographic value, and writing value
- graph updates for entities and claims, not only paper IDs

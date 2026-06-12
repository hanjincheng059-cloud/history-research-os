# 清代貿易微歷史論文流水線

> Qing Trade Microhistory Paper Pipeline — 從 MD 草稿到投稿就緒 DOCX

## 一句話

一套針對**中文史學論文**（清代廣州貿易、全球商品史、物質文化史）的
**七階段全自動打磨流水線**。你給 MD 草稿和 DOCX 史料文件夾，它幫你：
搜史料 → 查引文 → 對格式 → 同行評審 → 修訂 → 精簡 → 生成投稿 DOCX。

---

## 為什麼要這個？

寫清代物質文化史論文時，你會遇到這些問題：

- 📂 **DOCX 史料**不能用 `grep` 搜（zip 壓縮格式）
- 📝 **腳註和參考文獻**經常對不上
- 📄 **目標期刊格式**需要逐項手動調整
- 👀 **沒有人幫你看**論證漏洞（導師太忙）
- ✂️ **字數超了**，不知道該砍哪裡

這個流水線把每一步都自動化了。

---

## 管線流程

```
MD 草稿 → [1.史料搜索] → [2.引文檢查] → [3.格式匹配]
       → [4.同行評審] → [5.修訂] → [6.精簡] → [7.最終DOCX]
```

---

## 快速開始

### 完整管線

```bash
python run_pipeline.py \
  --input 我的論文.md \
  --archives ./史料文件夾/ \
  --reference 已發表論文.docx \
  --output 投稿版.docx
```

### 單獨使用某階段

```bash
# 搜史料
python scripts/stage1_source_search.py --dir ./史料/ --config config.yaml

# 查引文
python scripts/stage2_citation_check.py --input 論文.md

# 對格式
python scripts/stage3_format_match.py --reference 範文.docx --check 論文.md

# 數字數 + 找冗餘
python scripts/stage6_streamline.py --input 論文.md

# 生成 DOCX
python scripts/stage7_final_polish.py --input 論文.md --output 最終版.docx
```

---

## 五審稿人機制（第四階段）

| 角色 | 專長 | 抓什麼 |
|------|------|--------|
| 主編 | 全球史/海洋史 | 結構問題、讀者匹配 |
| 審稿人1 | 物質文化/全球商品史 | 理論缺口、Appadurai框架誤用 |
| 審稿人2 | 廣州貿易/清代社會經濟史 | 檔案方法論問題 |
| 審稿人3 | 北歐/瑞典東印度公司史 | 瑞典文獻處理、術語準確性 |
| 魔鬼代言人 | 懷疑論通才 | 循環論證、替代解釋 |

輸出包含優先級修改路線圖：🔴必須改 / 🟡強烈建議 / 🟢可選。

---

## 論文格式約定（中國史期刊常見）

- ❌ 無 YAML frontmatter
- ❌ 無 `#` markdown 標題
- ✅ 章：`一、` `二、` `三、`
- ✅ 節：`1、` `2、` 或 `（一）` `（二）`
- ✅ 關鍵詞內聯：`關鍵詞：` 非 `**關鍵詞：**`
- ❌ 章節間無 `---` 分隔線

---

## 安裝

```bash
pip install pyyaml pypandoc
brew install pandoc   # macOS，生成 DOCX 需要
```

---

## 目錄結構

見 [README.md](README.md)（英文版）。

---

## 許可證

MIT License

# Stage 5: Structured Revision Prompt

When executing Stage 5, the LLM should follow this protocol:

## Protocol

1. **Parse the Revision Roadmap** from Stage 4 output
2. **Create a task list** with every 🔴, 🟡, and 🟢 item
3. **Address in priority order:**
   - 🔴 first (core argument validity, submission blockers)
   - 🟡 second (quality improvements)
   - 🟢 last (optional polish)
4. **After each batch, re-run Stage 2 (citation check)**
5. **After all fixes, re-run Stage 6 (streamline)**

## Common 🔴 Fix Pattern: Methodology Honesty Paragraph

When the core evidence has a directionality problem (e.g., import tariffs
used to argue about exports; sales records used to infer production volumes),
add a paragraph that:

1. **States the limitation explicitly:**
   "本文所使用的銷售簿數據直接記錄的是哥德堡拍賣成交情況，
   而非廣州採購端的原始交易記錄。因此，從拍賣數據推斷廣州
   出口結構時，需考慮哥德堡市場需求對貨物選擇的過濾效應。"

2. **Explains why the evidence is still valid:**
   "儘管存在這一方向性問題，銷售簿仍是目前唯一連續覆蓋
   1733-1745年的量化資料，且其分類體系與粵海關稅則、公司
   貨單可形成三方互證。本文在分析中已優先採用三方數據一致
   的結論，對僅有單一來源支持的推斷則加以標註。"

3. **Marks as limitation in conclusion:**
   "第四節已將此點列為本文局限之一。"

## Common 🟡 Fix Pattern: "待補入" Resolution

For every "待補入" marker found in the text:
1. If the material IS available → add it
2. If partially available → add what exists, note gaps
3. If NOT available → rewrite to remove dependency on that material,
   or change to "有待未來研究進一步驗證"
4. NEVER leave "待補入" visible in a submission draft

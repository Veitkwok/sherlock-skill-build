# Advanced X Search Strategies & Best Practices for x-advanced-research

## Grok 原生工具快速参考

- **x_semantic_search(query, limit=10, from_date=None, to_date=None, ...)**: 语义相似搜索，适合发现相关讨论。适合 broad exploration。
- **x_keyword_search(query, limit=10, ...)**: 高级 keyword + operators 支持。**核心武器**，必须熟练使用 operators。
- **x_thread_fetch(post_id)**: 获取完整 thread 上下文（父帖 + replies）。
- **x_user_search(query)**: 查找用户 profile。

## 必须掌握的高级 Operators（智能路由时自动应用）

** engagement 过滤（质量核心）**:
- min_faves:500（或 1000、2000，根据 niche 调整）
- min_views:10000
- min_replies:10（谨慎使用，避免纯回复链）

**账号过滤**:
- from:@handle（精确来自某账号）
- to:@handle
- @handle（提及）
- -from:@spamaccount（排除低质账号）

**时间过滤**:
- since:2026-06-01
- until:2026-06-27
- since_time:unix_timestamp（更精确）

**内容类型**:
- filter:images / filter:videos / filter:links
- -filter:replies（排除纯回复，聚焦原帖）
- filter:has_engagement

**精确匹配与逻辑**:
- "exact phrase"
- (term1 OR term2) AND term3
- -negation_term（排除无关）

**组合示例（路由器应自动生成类似 query）**:
- AI agents (coding OR developer) min_faves:1000 since:2026-06-01 -filter:replies
- from:@specific_handle (trend OR update) min_faves:500

## 路由决策树（Layer 1 逻辑）

1. **Broad Discovery** → x_semantic_search（先 broad 找信号）
2. **Precision + Quality** → x_keyword_search + min_faves + 时间窗 + -filter:replies
3. **Account Focus** → from: 或 结合 semantic on account content
4. **Depth** → 对高价值结果执行 x_thread_fetch
5. **Monitoring** → 固定 since: 最近窗口 + 定期 re-run 逻辑（未来可脚本化）
6. **Voice/Style Extraction** → 高 engagement posts from target accounts → 模式归纳

## 质量控制规则

- **优先级**：用户 key accounts > 高 engagement > 语义相关 > 近期
- **自动降权/过滤**：明显推广帖、纯回复链、低 engagement、重复内容
- **信号评估**：返回结果时标注“高信号 / 中等 / 需进一步验证”
- **Rate Limit 友好**：单次查询 limit 控制在 10-20，链式时分步；避免过度并行

## Niche 特定调整建议（可扩展）

- AI / Tech：关注 min_faves 较高 + from:知名 researcher/ lab
- Finance：结合 earnings、特定 ticker、analyst 账号
- Content Creation：hooks、angles、high-engagement 抓取优先
- Supply Chain / Bottleneck：参考 serenity 风格，找“单一供应商”“产能扩张”“卡脖子”相关讨论 + 专家账号

## 与其他工具配合

- 当 X 信号不足时，自动建议或并行 web_search 补充背景
- 输出可直接喂给 wenai-script-generator（内容灵感）或 stella（角色相关）
- 复杂研究可结合 darwin-skill 优化查询策略

**持续优化点**：用 darwin-skill 测试典型 prompt，评估路由准确率、链式合理性、输出结构质量。
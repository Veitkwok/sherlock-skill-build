# Structured Output Templates for x-advanced-research

所有输出必须遵循结构化原则：**可引用 + 可行动 + 洞察优先**。始终包含 citations（post URLs）、关键原文引用、engagement metrics。

## 通用研究报告模板（Trend / Topic Monitoring）

**查询意图**： [用户原始查询]

**执行策略**： [使用的工具链 + 参数简述，例如 semantic + keyword with min_faves:500 since:2026-06-20]

**核心洞察总结**（3-5 条 bullet）
- ...

**Sentiment 分布**（如适用）
- 正面：XX% | 代表性引用 + link
- 中性：XX%
- 负面：XX% | ...

**高价值帖子 / 关键信号**（Top 5-8，按 engagement 或相关性排序）
1. [Post URL] | @author | likes/views | 时间 | 关键 quote（1-2 句） | 洞察标签
2. ...

**趋势演变 / 关键主题聚类**
- 主题1：...
- 主题2：...

**Actionable Takeaways**
- ...
- ...

**来源质量说明**：高 engagement 优先、已过滤低信号回复/推广帖。引用自 Grok 原生 X 搜索。

---

## Profile / Account Deep Dive 模板

**账号**：@handle | 研究重点： [niche]

**执行策略**： from:@handle + min_faves / semantic on profile content

**Voice & Style 提取**
- 核心 tone：...
- 常用 hooks / 开头模式：...
- 典型 angles / 叙事结构：...
- 语言特点（词汇、长度、emoji 使用等）：...

**高互动内容亮点**（最近/历史 top）
- [URL] | likes | quote | 为什么高互动

**近期主题分布 & 信号**
- ...

**对你的价值 / 应用建议**
- 内容灵感：...
- 跟踪建议：...

---

## Thread Analysis & Transformation 模板

**来源 Thread**： [URL 或描述]

**核心原则提取**（模块化，每模块 1 个核心洞察）
1. **原则名称**：...
   - 原文 quote + link
   - 解释（用作者风格或清晰语言）
   - 实际应用场景

**交互式转化建议**（如转为课程/笔记/内容）
- ...

**整体洞察与扩展**
- ...

---

## High-Engagement Content Scraping + Inspiration 模板

**Niche / 主题**：...

**抓取规则**： min_faves:XXX since:XXX from:可选账号

**提取的 Hooks / Angles / Structure 模式**（去重后 top patterns）
- Hook 类型1：示例帖子 + 为什么有效
- ...

**可直接复用的内容模板**
- ...

**推荐跟进搜索**：...

---

**通用规则**：
- 每条引用必须可点击（完整 post URL）
- Engagement metrics 必须包含（likes, views, reposts, replies 如果相关）
- 所有输出以 Markdown 结构呈现，便于后续使用（复制到 wenai、笔记、报告等）
- 如数据不足或信号弱，明确说明并建议调整参数（更宽时间窗、更低 engagement 阈值等）
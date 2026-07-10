# Serenity-Style High-Risk Fast Mover US Stocks Workflow

**用户核心需求**：小资金 + 高风险 + 快速增值 → 重点捕捉 **AI 供应链瓶颈 / chokepoint / 催化剂驱动** 的美股标的（Serenity 风格）。这些标的往往不在大盘热点，但有不对称上涨潜力（类似 AAOI、SIVE、AXTI 等历史案例）。

## 核心原则（路由器必须内化）

1. **Serenity 优先**：@aleabitoreddit 的讨论是最高信号源。优先抓取其高互动帖 + 提及的 ticker。
2. **瓶颈 / Chokepoint 信号**：关注“单一供应商”“产能扩张周期”“关键材料短缺”“AI infra 物理限制”等关键词。
3. **催化剂驱动**： earnings surprise、订单/合同、供应链突破、技术验证、AI capex 相关新闻。
4. **高风险特征**：小市值、波动大、beta 高、估值激进（PS 高、FCF yield 低）、但有清晰不对称 upside。
5. **多源交叉验证**：
   - X（尤其是 Serenity 生态 + 你的重点账号）
   - https://analysissite.vercel.app/ （Serenity Analysis 终端：边际变化、风险队列、AI views）
   - https://serenity.bemix.cc/ （Serenity 私人研究面板）
   - https://antseer.ai/skill/3544 （Antseer Serenity 相关 skill）
   - https://www.redditalpha.xyz/en/dashboard/ （Reddit 讨论强度）
6. **小资金策略适配**：强调不对称回报（高风险但潜在 2-5x+ 空间）、仓位控制建议、止损逻辑。

## 典型触发与路由策略

当用户说：
- “找近期可能大涨的美股 / 高风险快速增值标的”
- “Serenity 风格的 AI 供应链机会”
- “监控 @aleabitoreddit 提到的 ticker”
- “高 beta / 催化剂驱动的 US stocks”

**执行流程**（模型自动规划）：
1. **X 信号拉取**（最高权重）：
   - x_semantic_search + x_keyword_search 组合，重点 from:@aleabitoreddit + 你的其他重点账号
   - 高级过滤：min_faves:300~1000（根据 niche）、since:最近 7-30 天、-filter:replies
   - 识别被频繁提及的 ticker + 上下文（bottleneck / catalyst）

2. **Profile + Thread 深挖**：
   - 对 @aleabitoreddit 及相关高价值账号执行 profile 分析（高互动帖 → voice / 核心逻辑提取）
   - 对关键 thread 执行 x_thread_fetch

3. **外部站点交叉**：
   - 明确建议用户查看或模拟参考：
     - analysissite.vercel.app 上对应 ticker 的边际变化、风险队列、AI views
     - serenity.bemix.cc 研究面板
     - Reddit Alpha dashboard 讨论热度
     - Antseer 相关 skill 数据

4. **结构化输出**（使用专用模板）：
   - Ticker 列表 + 为什么可能大涨（bottleneck 强度 + catalyst）
   - X 信号强度（Serenity 提及频次 + engagement）
   - 风险评估（高 / 极高 + 关键风险点）
   - 不对称 upside 空间评估
   - 建议监控清单 + 下一步行动（查 analysissite / Reddit 等）
   - 与 finance-master deep-analysis 的联动建议（如需要完整 22 维框架分析）

## 输出模板增强（High-Risk Mover Alert）

**查询**： [用户原始需求]

**核心信号来源**：
- X（@aleabitoreddit 及其他重点账号）：...
- 外部站点参考：analysissite.vercel.app / serenity.bemix.cc / Reddit Alpha

**潜在大涨标的候选**（按信号强度排序，限制 5-8 个）
1. **TICKER**（公司简述）
   - Serenity / X 核心论点：...
   - 瓶颈 / 催化剂：...
   - 近期 X 信号强度： engagement + 提及频次
   - 风险等级：高 / 极高
   - 潜在 upside：...
   - 建议行动：查 analysissite.vercel.app + Reddit Alpha

**整体市场 / 主题洞察**：
- 当前最强 bottleneck 主题：...
- 风险提示：小资金高风险策略，严格仓位管理 + 止损纪律

**与 finance-master 联动**：
- 建议将这些 ticker 送入 deep-analysis 做完整 22 维 + 投资者评审

**免责**：高风险投资，非投资建议，仅供研究参考。过去表现不代表未来。

---

**持续优化方向**：
- 结合 darwin-skill 测试“找高风险美股大涨标的”类 prompt 的路由准确性和输出质量。
- 未来可增加对 analysissite.vercel.app 风格数据的模拟抓取或提示集成。
- 与 serenity-skill（finance-master 中）深度联动，实现“X 实时信号 → 结构化 bottleneck 研究 → 深度估值”闭环。
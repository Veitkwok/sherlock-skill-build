---
name: investor-panel
description: 投资大佬评审团。给定一只股票的分析数据，让投资者各自按自己的方法论打分并输出结构化评审结果。覆盖经典价值派、成长投资派、宏观对冲派、技术趋势派、中国价投派、A股游资派、量化系统派、科技领袖派、Serenity 卡位猎手 9 大流派。当用户请求"评审团/大佬怎么看/某某会买吗/做一次大佬投票"时使用。
version: 4.0.0
author: FloatFu-true (original) / Veit Kwok (agent-driven rewrite)
license: MIT
metadata:
  hermes:
    tags: [finance, investor-panel, voting, value-investing, growth-investing]
    related_skills: [deep-analysis]
---

# Investor Panel · 投资大佬评审团 v4.0

> Agent 驱动版本。所有脚本已删除，评审由 Agent 直接执行。

---

## 输入

Agent 在进行评审前应已掌握以下数据（来自 deep-analysis 的数据采集或独立搜索）：

- 股票基本信息（ticker / name / industry / market cap）
- 核心财务指标（ROE / PE / PB / 净利率 / 营收增速 / FCF）
- 技术面状态（Stage / 均线 / RSI / 距高点距离）
- 估值分位（PE/PB 历史分位 / 同行对比）
- 护城河评分（品牌 / 网络效应 / 规模 / 转换成本）
- 最新事件/催化剂
- 社交情绪

---

## 输出格式

每位投资者返回结构化评审：

```json
{
  "investor_id": "buffett",
  "name": "巴菲特",
  "group": "A",
  "signal": "bullish | neutral | bearish",
  "confidence": 87,
  "score": 82,
  "verdict": "强烈买入 | 买入 | 关注 | 观望 | 等待 | 回避 | 不达标 | 不适合",
  "reasoning": "1-3 句具体逻辑，引用数字",
  "comment": "用该投资者语言风格的金句 1-2 句",
  "pass": ["通过的规则"],
  "fail": ["未通过的规则"],
  "ideal_price": 合适买入价位或 null,
  "period": "持有周期"
}
```

**Confidence 校准**：
- 85-100：核心方法论硬指标全部命中/不命中
- 60-84：多数命中
- 30-59：部分命中，需等待信号
- 0-29：方法论不适用此股 / 信息不足

---

## 执行步骤

### Step 1: 确定评审范围

- 美股 → 使用 `finance-master/UZI-Skill/deep-analysis/references/investor-frameworks.md`（36 位美股大师）
- 需要完整 65 人版 → 读本 skill 的 references/（group-a 到 group-g + group-i）
- 需要游资（仅 A 股）→ 读 `references/group-f-china-youzi.md`

### Step 2: 逐 investor 评审

对每位投资者：
1. 读该 investor 所在 group 的 reference 文件
2. 从输入数据中提取该 investor 关心的指标
3. **按该 investor 的方法论判断** signal / score / verdict
4. 用 `references/quotes-knowledge-base.md` 查找该 investor 的真实语录风格，撰写 comment
5. 输出结构化 Signal

### Step 3: 游资射程判断（F 组 · A 股专用）

仅当分析 A 股且包含游资组时执行。参考 `references/seat-encyclopedia.md` 中对每位游资的市值射程/风格定义。不在射程内的游资 → `signal: "neutral"`, `verdict: "不适合"`。

### Step 4: 汇总

统计：panel_consensus（看多百分比）、vote_distribution（各 verdict 计数）、signal_distribution（bullish/neutral/bearish 分布）。

---

## 流派与参考文件

| 组 | 文件 | 人数 | 适用市场 |
|---|------|------|---------|
| A 经典价值 | `references/group-a-classic-value.md` | 6 | 全球 |
| B 成长投资 | `references/group-b-growth.md` | 4 | 全球 |
| C 宏观对冲 | `references/group-c-macro-hedge.md` | 5 | 全球 |
| D 技术趋势 | `references/group-d-technical.md` | 4 | 全球 |
| E 中国价投 | `references/group-e-china-value.md` | 6 | A/HK |
| F 游资 | `references/group-f-china-youzi.md` | 22 | A 股 |
| G 量化系统 | `references/group-g-quant.md` | 3 | 全球 |
| I Serenity | `references/group-i-serenity.md` | 2 | 全球 |

美股分析默认使用 A-D + G + I 组（共 24 人）。如需 36 人版，参考 `deep-analysis/references/investor-frameworks.md`。

---

## 语料库

生成 comment 前必读 `references/quotes-knowledge-base.md`，查找该 investor 的真实公开原话和语言风格。

## 语言风格守则

每位 investor 的 comment 必须像本人：
- 巴菲特：温和、引用奥马哈、用"我们"
- 芒格：刻薄、反向思维、引用心理学偏误
- 索罗斯：哲学化、提"反身性"
- 段永平：朴素、问"商业模式""人""价格"
- 木头姐：乐观、提"S 曲线""颠覆式创新"
- Serenity：结构主义、如手术刀般精准切分价值链

---

*v4.0: 移除所有 Python 脚本引用，改为 Agent 直接驱动评审。输入从脚本 JSON 变为 Agent 已掌握的结构化数据。*

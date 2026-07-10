---
name: lhb-analyzer
description: 龙虎榜深度分析器。识别游资席位、判断机构 vs 游资博弈、对照同板块龙虎榜找辨识度龙头。当用户问"谁在买这只票/最近龙虎榜怎么样/X游资有没有上榜/这是不是X的票"时使用。（A 股龙虎榜专用，美股不适用）
version: 4.0.0
author: FloatFu-true (original) / Veit Kwok (agent-driven rewrite)
license: MIT
metadata:
  hermes:
    tags: [finance, a-share, lhb, hot-money, market-microstructure]
    related_skills: [deep-analysis]
---

# 龙虎榜深度分析 v4.0

> Agent 驱动版本。所有脚本已删除，分析由 Agent 通过 web search / MCP 工具直接执行。

---

## 调用上下文

输入：股票代码或个股名
输出：龙虎榜分析 + 游资识别 + 同板块对比

---

## 数据获取（Agent 直接执行 · 无脚本）

1. **龙虎榜原始数据**：web search `"{ticker} 龙虎榜 最近上榜 席位 买卖金额"` 或使用东方财富龙虎榜页面
2. **游资席位识别**：参考 `references/seat-encyclopedia.md`（22 位游资的席位 + 风格 + 射程定义），将上榜席位与已知游资席位匹配
3. **射程判断**：参考 seat-encyclopedia.md 中该游资的市值射程和风格，判断当前股票是否在射程内
4. **同板块对比**：搜索同行业/同概念其他股票的龙虎榜数据，找辨识度龙头

---

## 输出 Markdown 结构

```markdown
# {name} ({ticker}) 龙虎榜分析

## 📅 近 30 天上榜 X 次

| 日期 | 席位 | 买入(万) | 卖出(万) | 净买入(万) |
|------|------|---------|---------|-----------|
| ...  | ...  | ...     | ...     | ...       |

## 🐉 识别到的游资 (Y 位)

| 游资 | 风格 | 在不在射程 | 买入 / 卖出 |
|------|------|-----------|------------|
| 章盟主 | 大资金趋势 | ✅ 在射程 | 买 1.2 亿 |
| 佛山无影脚 | 一日游 | ❌ 不在 | 卖 0.3 亿 (反向预警) |

## ⚖️ 机构 vs 游资

- 机构净买入: ¥X 亿
- 游资净买入: ¥Y 亿
- 主导方: {机构 / 游资}

## 🏆 同板块辨识度龙头

| 排名 | 代码 | 名称 | 上榜次数 | 累计涨幅 |
|------|------|------|---------|---------|
| 1    | ...  | ...  | ...     | ...     |

本股在板块中的位置: 第 N

## 💡 结论一句话

"这是一只机构主导 + 章盟主格局票，板块辨识度排第 2，可以跟。"
```

---

## 参考资料

- 详细的 22 位游资席位百科：`references/seat-encyclopedia.md`
- 席位识别逻辑：人工比对上榜席位地址与 known seats 列表

---

*v4.0: 移除所有 Python 脚本引用（`scripts/fetch_lhb.py`、`lib/seat_db.py`），改为 Agent 通过 web search + seat-encyclopedia.md 直接执行席位识别和射程判断。*

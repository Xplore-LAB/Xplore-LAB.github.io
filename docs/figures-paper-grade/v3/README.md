# 方法图 V3：视觉重构与验收

2026-10-17。替换网站 E1/E2 的默认预览；旧稿保留，不把作者自评写成用户认可。

## 图意与边界

E1 解释一个概念机制：观测形成工况与查询，检索候选并检查适用性，仅在可用集合中按相关性选择，规划器调用检查/仿真工具，经约束检查决定执行、复核或重规划。实际结果先验证归因，再形成新版本经验。E2 展开三值条件与二值门控：E1=1，E2=0，E3=0。沿用原示例；没有新性能数值，不证明方法新颖性、效果或系统安全性。

## 设计选择与自评

- 主次：E1 中间的适用性区域为主角，背景过程为辅助；避免等权重的四个大框。
- 叙事：输入从左侧进入，选择后进入右侧规划器；底部反馈右至左回到记忆。所有决策分支明确标注。
- 密度：E2 改为横向紧凑对照，180 mm 宽时高 62 mm（V2 约 122 mm）。E1 高 96 mm。
- 字体：Liberation Sans / Arial 后备，原生整句文本；180 mm 暂定宽度下最小约 8.05 pt。
- 色彩：深蓝灰正文、青绿色强调、浅灰辅助；同时用文字和符号表示结果，脱离颜色也能理解。
- 自评：比旧稿更清楚、整洁、密度更合理，可作为机制教学图。仍偏理性流程与条件表，尚非复杂插画风格，也不能仅凭本轮自评认定达到顶会水准。

## 编辑与重建

主档为 `img/figures/paper-grade/v3/*.svg`，不是旧版 draw.io。每个语义区域有稳定 group ID；可用 Inkscape 改字、移动分组和改色。移动后连线不自动跟随，须手动核对。PDF 保留原生文字，无位图底图。副本实际改字、移动 E2 分组后重新导出 PDF 的检查见 verification.json。

重建：`python3 scripts/build_method_figures_v3.py`；需要 PATH 中的 Inkscape。脚本只用标准库生成 SVG。

## 核查状态

具体结果见 `img/figures/paper-grade/v3/verification.json`。SVG 审计的唯一警告为 180 mm 不是 Nature 预设 89/183 mm；目标会议未确定，这是有意的暂定尺寸，不宣称投稿格式合规。

通用 PDF 碰撞脚本的原始结果保留。该工具复现了旧稿中 PDF trace 跨相邻文字合并的误报；逐个原生 span 的矩形复核与 PNG 人眼检查独立记录，不把该脚本声称为“全通过”。

## 配套图注

**E1. Check experience applicability before planning (conceptual design).** Operating observations and task information form a retrieval query. Retrieved experiences are checked for regime compatibility, freshness and limits; only admissible experiences enter relevance ranking. The planner uses the selected experience and calls inspection and simulation tools. Constraint checks lead to approved execution, review for uncertain cases, or replanning for rejected plans. Observed outcomes are verified and attributed before a versioned record update. Process trends and experience records are illustrative, not measured evidence of efficacy or safety.

**E2. Supported conditions are required for reuse (conceptual design).** Checkmarks, crosses and question marks denote supported, contradicted and missing evidence. A candidate is admissible (g=1) iff all required checks are supported. E1 is reusable; E2 is expired and excluded; E3 requests missing evidence and remains inadmissible (g=0). Verified evidence creates a new version and triggers reevaluation.

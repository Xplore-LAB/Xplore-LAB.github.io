# 经验适用性门控：视觉重构试稿 V2

用户要求：从现有 E 组选择一张，按统一规范重绘并查看效果。已有方法内容和此次重绘指令作为内容依据；不另建研究假设。

## 图意与范围

保留“候选经验 → 适用性条件 → 决策”的机制；E1支持全部条件，E2新鲜度失败，E3工况证据未知。二值复用门控仅在全部条件有支持时为1。

- 角色：方法细节图，承接系统总览，不再重复整套工业系统。
- 原型：对齐的三行案例，左候选、中条件、右决策；核心条件区占主要视觉位置。
- 布局：白底，以行对齐表达同一案例的流向；仅给通过路径一个浅青背景，删去三个外层大框和逐格边框。
- 信息层级：条件门控和通过路径为主；历史保留、证据更新为辅；示意说明由网页和图注承载。
- 输出：暂定180mm宽；字体7.5–10.5pt；具体投稿年份/版式未指定，不宣称某会议合规。
- 语言：沿用现有图的英文。使用Liberation Sans，保留SVG原生文字与语义分组。

## 元件与边

候选E1/E2/E3：现有概念样例的记录；当前上下文c(t)：外部条件输入；condition gate：原样例的候选机制，不标为已验证新贡献；g：二值重用输出；eligible/excluded/verify：已有决策。

主路径各行左→右，实线箭头表示案例处理关系。条件输入进入条件表头。E3仅请求核实，核实后的版本变更与重新检查由独立下方注记解释；不将未知画成通过，不将核实等同于成功。

## 设计选择

比较了等宽三栏、大幅中心矩阵、逐行案例三个布局。选逐行案例：无需沿长总线追踪E1/E2/E3，也能区分条件未知与二值门控为0。编辑源中不加入假性能数字。

图注：Candidate experiences are evaluated against the current context before reuse. Supported conditions are marked with a check, a contradicted condition with a cross, and missing evidence with a question mark. E1 is eligible for planning with provenance, E2 is excluded as expired, and E3 requires verification. The reuse gate g equals one only when all required checks are supported. Verified evidence may create a new version that must be reevaluated; it does not automatically make an experience valid. This is a conceptual teaching example, not measured performance or a validated new method.

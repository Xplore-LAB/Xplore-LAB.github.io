---
layout:     post
title:      "SWE-bench 拆解：一个 benchmark 如何定义并塑造编程 Agent"
subtitle:   "从 2,294 个真实 issue 的数据构造，到多语言扩展与 Agent 工程的两条军规"
date:       2026-09-17
author:     "Kevin"
header-img: "img/post-bg-2015.jpg"
catalog:    true
section:    论文拆解
tags:
    - LLM
    - 智能体
    - 论文拆解
    - 评测基准
---

> 拆解对象：SWE-bench: Can Language Models Resolve Real-World GitHub Issues?，ICLR 2024 oral，全部作者来自普林斯顿与芝加哥大学，Carlos E. Jimenez 与 John Yang 一作，Karthik Narasimhan 通讯。延伸材料三份：Multi-SWE-bench（Zan et al., ByteDance Seed，NeurIPS 2025 Datasets and Benchmarks Track）、Anthropic 的 Best practices for Claude Code（2025）、Cognition 的 Don't Build Multi-Agents（Walden Yan，2025 年 6 月）。SWE-bench 全部数字出自 arXiv v3 正文与附录 Table 1/5/10，Multi-SWE-bench 数字以 NeurIPS 2025 proceedings 版为准并标注与 arXiv v1 的口径差异，可对照复核。

## 一、为什么值得拆

2023 年 10 月这篇论文挂出时，最好的模型 Claude 2 只能解决 1.96% 的问题。两年后，SWE-bench 系列排行榜上的头部系统越过 70%，「SWE-bench 多少分」成为每个编程模型发布时的标配指标。一个评测集从「全军覆没」走到「人人必报」，本身就是一部编程 Agent 的进化史。

更值得拆的是它立住的方式。SWE-bench 没有发明新题型，它把「在真实仓库里修一个真实 issue」直接定义为任务，然后用一套数据构造 pipeline 保证每条样本都可执行、可判定、无污染。方法论文卖「有效」，benchmark 论文卖「测得准、测得难、可复现」，这篇论文三样全部给到，而且给的方式后来成了行业模板：Multi-SWE-bench、SWE-bench Multimodal 以及一堆 RL 训练集，都在复用它的 pipeline 范式。

这篇文章做两件事。前半拆数据构造与评测设计，回答「这 2,294 条样本为什么可信」。后半把视野拉到 2025 年，用三份延伸材料回答第二个问题：当评测把任务定义清楚之后，Agent 工程围绕它长出了哪些被反复验证的法则。

## 二、数据构造：93,139 个 PR 到 2,294 条样本

SWE-bench 的核心贡献可以浓缩成一条漏斗。论文用三阶段 pipeline，从 12 个热门 Python 仓库的全部历史中筛出 2,294 个任务实例：

<figure style="margin:28px 0">
<svg viewBox="0 0 680 300" xmlns="http://www.w3.org/2000/svg" role="img" style="width:100%;height:auto" font-family="-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">
  <defs><marker id="sb-a" markerWidth="7" markerHeight="7" refX="5.5" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="#57606a"/></marker></defs>
  <text x="340" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#24292f">SWE-bench 三阶段数据漏斗（数字出自论文附录 Table 10）</text>
  <rect x="60" y="42" width="560" height="62" rx="10" fill="#f2fafd" stroke="#56B4E9" stroke-width="1.5"/>
  <text x="340" y="66" text-anchor="middle" font-size="12" font-weight="700" fill="#1E88B8">阶段一 · 仓库选择与抓取：93,139 个 PR</text>
  <text x="340" y="86" text-anchor="middle" font-size="10.5" fill="#57606a">2023 年 8 月 PyPI 下载量前 5000 → 取前 100 包 → 12 个仓库（django / sympy / scikit-learn 等）</text>
  <path d="M 340 110 L 340 128" stroke="#57606a" stroke-width="1.4" marker-end="url(#sb-a)"/>
  <rect x="130" y="134" width="420" height="62" rx="10" fill="#fdf8ef" stroke="#E69F00" stroke-width="1.5"/>
  <text x="340" y="158" text-anchor="middle" font-size="12" font-weight="700" fill="#B77500">阶段二 · 属性过滤：11,407 个候选实例</text>
  <text x="340" y="178" text-anchor="middle" font-size="10.5" fill="#57606a">已合并 PR + 关联 issue + 修改了测试文件（贡献者自带验证信号）</text>
  <path d="M 340 202 L 340 220" stroke="#57606a" stroke-width="1.4" marker-end="url(#sb-a)"/>
  <rect x="200" y="226" width="280" height="62" rx="10" fill="#f2fbf7" stroke="#009E73" stroke-width="1.5"/>
  <text x="340" y="250" text-anchor="middle" font-size="12" font-weight="700" fill="#00805C">阶段三 · 执行过滤：2,294 条样本</text>
  <text x="340" y="270" text-anchor="middle" font-size="10.5" fill="#57606a">真实跑测试：至少一个 fail-to-pass，且安装运行无错</text>
</svg>
<figcaption style="text-align:center;font-size:12px;color:#8b949e;margin-top:6px">图 1 · 三阶段漏斗。每经过一阶段数量大约砍掉一个量级，执行过滤是真正的质量阀门。</figcaption>
</figure>

这条漏斗的每一层都在回答一个具体的质疑。

**阶段一选仓库，回答「任务够不够真实」。** 从 2023 年 8 月 PyPI 下载量前 5000 的库里取前 100 个包，确认许可证后抓全部 PR，最终覆盖 12 个仓库：astropy、django、flask、matplotlib、pylint、pytest、requests、scikit-learn、seaborn、sphinx、sympy、xarray。选热门库的理由写在论文里：维护更好、贡献规范更清晰、测试覆盖更全。django 一个仓库贡献了 850 条实例，flask 只有 11 条。

**阶段二看属性，回答「issue 和修复是否配对」。** 只保留同时满足两个条件的已合并 PR：解决某个 GitHub issue，且修改了仓库的测试文件。第二个条件是关键设计：PR 自带测试改动，意味着贡献者已经写下了「怎样算修好」的可执行判据，评测时不需要人工再造标签。93,139 个 PR 过滤后剩 11,407 个候选。

**阶段三跑执行，回答「判定是否真的可信」。** 对每个候选实例，在 PR 合入前后各跑一遍测试，只保留「至少一个测试从 fail 变 pass」的实例，同时剔除安装失败、运行报错、以及测试调用了新函数导致人类也不可能解出的样本。这一步把 11,407 砍到 2,294，淘汰率约 80%。执行过滤是整条 pipeline 里最贵也最不可替代的一环：它把「标签对不对」从人工抽检变成程序验证。

最终每条样本的输入是 issue 描述（平均 195.1 词）加上 base commit 的完整代码库（平均 3,010 个非测试文件、43.8 万行），输出是一个 patch。判定时跑两类测试：`FAIL_TO_PASS`（平均 9.1 个，修复必须让它们通过）与 `PASS_TO_PASS`（中位数 51 个，回归不能挂）。参考答案平均改 1.7 个文件、3.0 个函数、32.8 行。

## 三、评测设计：把「修没修好」变成程序判定

传统代码评测（HumanEval 式）测的是「给函数签名写函数体」，判分靠单测，题目本身是为评测造的。SWE-bench 反其道而行：题目来自真实开发历史，判分复用贡献者自己写的测试。这个设计带来三个结构性好处。

**无污染且可持续。** 样本锚定在 base commit 上，仓库未来还会不断产生新 PR，评测集可以无限扩容。论文还专门做了时间对照实验：把样本按模型训练数据截止日前后切分，多数模型前后表现差别很小，说明「背过答案」不构成主要威胁。

**难度是真实的。** gold patch 平均跨 1.7 个文件，最多 31 个文件；最长的 issue 描述 4,477 词。模型要面对的对象是 43.8 万行的真实代码库，绝非玩具函数。

**判定无主观性。** resolved 的全部含义就是 `FAIL_TO_PASS` 全过且 `PASS_TO_PASS` 不挂。没有人工打分，没有 LLM 裁判，不同系统在同一判据下可以直接比较。

论文同时定义了两种上下文设置，这个二分后来成为所有 SWE-bench 类评测的标准动作：**oracle** 直接给出要改的文件（测编辑能力），**BM25 sparse retrieval** 让系统自己检索（测端到端定位加编辑）。两种设置下的分差，恰好量化了「找到问题」与「修好问题」各自的难度。

## 四、基线结果与难因：1.96% 背后的三个瓶颈

主结果（BM25 检索）下，最好的 Claude 2 解决 1.96%，GPT-4 1.31%，ChatGPT-3.5 0.17%，论文自训的 SWE-Llama 7B/13B 各 0.70%。oracle 设置下 Claude 2 升到 4.8%；进一步把 oracle 文件折叠到只留修改行附近，Claude 3 Opus 能到 9.39%。三组数字放在一起，难因图谱非常清楚。

**瓶颈一：长上下文里找不到位置。** BM25 窗口从 13k 扩到 50k，检索召回率从 29.58 升到 51.06，Claude 2 的解决率反而从 1.96% 掉到 1.22%。给得越多做得越差，模型在长上下文里定位问题代码的能力是当时的主要短板，论文引「lost in the middle」佐证。这也解释了为什么后来的 SWE-agent、Agentless 都把「检索与导航」当作第一设计目标。

**瓶颈二：跨文件编辑能力缺失。** 模型生成的 patch 平均只动约 1 个文件、十几到三十行，gold patch 平均动 1.7 个文件。能 apply 的模型 patch 总长度不及 gold 的一半。真实修复需要跨函数、跨文件协调修改，当时所有模型都明显做不到。

**瓶颈三：分布漂移下的脆弱。** 微调模型 SWE-Llama 在 oracle 设置下与 Claude 2 相当（各解决 110 与 91 个实例，且重合度只有 42%），换到 BM25 检索的上下文立刻崩到 0.70%。训练时它见过「每个上下文文件都该被改」的分布，检索结果里混入无关文件后就不会处理了。这个现象对今天做 Agent 训练数据的人仍有警示：训练分布里的上下文必须带噪声，否则模型学不会忽略。

## 五、多语言扩展：Multi-SWE-bench 把漏斗推广到 8 种语言

SWE-bench 的一个明显边界是只有 Python。ByteDance Seed 的 Multi-SWE-bench（NeurIPS 2025 Datasets and Benchmarks Track）把同一套范式推广到 Java、TypeScript、JavaScript、Go、Rust、C、C++。正式版共 2,132 条实例、8 种语言（含 Python 500，直接复用 SWE-bench Verified 的人工筛选子集）；arXiv 初版为 1,632 条、不含 Python，引用时注意两个版本的口径差异。

它的 pipeline 在原版三阶段基础上扩成五阶段，两处加固值得拆。

**环境构建前置为独立阶段。** 多语言仓库的依赖远比 Python 复杂，团队从 CI/CD 配置、README 与试运行中提取依赖，为每个 PR 构建 Docker 环境，构建失败就迭代修，修不好就弃。然后在三种配置下跑完整测试套件（base、加 test.patch、再加 fix.patch），跟踪每个测试在四种状态间的迁移，凡出现「本来能过、加了修复反而挂」的回归即整条丢弃。原版用 fail-to-pass 一个条件，这里细化成状态机级别的过滤。

**人工验证升格为正式阶段。** 68 名标注者（目标语言 2 年以上经验、本科起步、1 小时培训），每条实例两人独立标注加交叉复核，另有 14 人内部质检团队要求外包准确率不低于 80%。标注沿 SWE-bench Verified 的问卷规范，并按「人类预估修复时间」给难度分级：Easy 为 15 分钟内，Medium 为 15 分钟到 1 小时，Hard 为 1 小时以上。从 2,456 个候选最终保留 1,632 个非 Python 实例。整个数据集耗时约一年。

基线结论三条，每条都有数字支撑：

| 发现 | 关键数据 |
| --- | --- |
| 跨语言泛化差 | 最好的 Claude 3.7 Sonnet 在 Python 上解决 52.2%（OpenHands 框架），到 Rust 剩 15.9%、C++ 14.7%，TS 仅 2.2%；语言域呈 Python/Java 高于 Go/Rust 高于 C/C++ 高于 TS/JS 的层级 |
| 与人类难度标注对齐 | 解决率随 Easy → Medium → Hard 递减，Hard 普遍趋近于零；模型基本只能解决人类 15 分钟内能修的问题 |
| 补丁一长就崩 | gold patch 超过 600 token 的问题解决率比 200 token 以内的低约一半；改 1 个文件到改 10 个以上文件，解决率单调递减，Java 上长补丁直接归零 |

顺带一提，团队把同一 pipeline（去掉人工验证阶段）产出的 4,723 条实例、76 个仓库开放为 Multi-SWE-RL 训练集，直接服务 RL 训练。评测集与训练集共用一条生产线，这是 SWE-bench 范式对 RL 时代的意外馈赠。

## 六、评测之后：Agent 工程的两条军规

到 2025 年，SWE-bench 分数的主战场已经从「模型本身」移到「模型外的系统」。两份工程文献恰好给出互补的答案，一份管人机协作，一份管系统架构。

**军规一：人要把需求说清楚，让 Agent 先提问再动手。** Anthropic 的 Best practices for Claude Code 把有效用法总结为一套流程：先探索（plan mode 只读代码不改），再计划（产出书面方案），然后实现，最后提交。其中最反直觉的一条是「Let Claude interview you」：对大需求，先丢一句极简描述，让 Claude 用提问工具反过来访谈你，把技术选型、边界情况、取舍全部问透，写成一份 SPEC 文档，再开新会话执行。配套的还有「纠偏要早」：发现跑偏立刻打断重述，同一件事纠正超过两次就清空上下文、带着新认知重开干净会话。这套用法的底层逻辑和 SWE-bench 的任务定义完全一致：issue 描述越精确，修复成功率越高，人给 Agent 的 prompt 就是 Agent 的 issue。

**军规二：架构上先守上下文，再谈并行。** Cognition 的 Walden Yan 在 Don't Build Multi-Agents 里提出 context engineering 的两条原则。其一，共享上下文，且要共享完整的执行轨迹，不能只转发单条消息。其二，动作携带隐式决策，冲突的隐式决策必然产出坏结果。他用一个「克隆 Flappy Bird」的例子拆解多 Agent 的典型死法：子任务 1 把背景做成了马里奥风格，子任务 2 做的鸟完全不像游戏素材，主 Agent 拿到两份各自自洽、互相矛盾的产物，拼接已经无解。他的判断是：默认排除一切违反这两条原则的架构，从单线程线性 Agent 起步，上下文装不下时引入一个专门压缩历史轨迹的模型，把动作与对话历史压成关键决策与事件。Claude Code 的 subagent 被当作正面案例：子 Agent 只负责回答定义清晰的问题，从不与主 Agent 并行写代码，调查过程的中间产物也不回流主上下文。

把两份文献并读，会看到一个共同指向：2025 年编程 Agent 的可靠性瓶颈不在模型智力，在上下文管理。SWE-bench 当年的三大难因（找不到位置、跨不了文件、扛不住噪声）本质上也是同一个问题的不同侧面。

## 七、收束：一条完整的因果链

四份材料串起来是一条清晰的链。SWE-bench 用执行式判定把「修 issue」定义成可测量的任务，1.96% 的基线量出了起点。Multi-SWE-bench 用加固后的 pipeline 把任务推广到 8 种语言，量出泛化的边界：模型在 Python 上的高分很大程度是生态与训练数据的红利，换个语言生态就要重新爬坡。两份工程文献则回答「在现有模型能力下怎么把系统做好」：对人，把需求访谈与书面规格前置；对架构，先保证上下文连续共享，再谈任何形式的并行。

对正在做 Agent 的人，这条链可以压缩成三句话。评测设计上，判定必须可执行，人工标签只能是补充。数据生产上，最贵的一步永远是真实环境下的执行验证。系统构建上，先当一个称职的上下文工程师，再当一个架构师。

## 参考与出处

1. Jimenez et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR 2024 (oral). arXiv:2310.06770v3，OpenReview id VTF8yNQM66。数据构造数字见附录 Table 10，任务统计见 Table 1，基线结果见 Table 2/5/6。
2. Zan et al. Multi-SWE-bench: A Multilingual Benchmark for Issue Resolving. NeurIPS 2025 Datasets and Benchmarks Track（ByteDance Seed）。arXiv:2504.02605（v1 为 1,632 条 7 语言口径），正式版 2,132 条 8 语言见 NeurIPS proceedings 与项目站 multi-swe-bench.github.io。
3. Anthropic. Best practices for Claude Code, 2025。「explore, plan, code, commit」四阶段与「Let Claude interview you」章节。
4. Walden Yan (Cognition). Don't Build Multi-Agents, 2025-06-12。context engineering 两条原则与 Flappy Bird 案例。
5. OpenAI. Introducing SWE-bench Verified, 2024-08。500 条人工筛选子集，Multi-SWE-bench 的 Python 分片直接复用它。

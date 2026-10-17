# 纯提示词工业智能体图

2026-10-17。使用内置 imagegen 从完整提示词生成，无参考底图；之后进行一次局部编辑修正。输出是 PNG 位图，非对象级可编辑文件。底层模型版本未由工具返回。

[查看图片](/img/figures/prompt-only/industrial-agent.png) · [完整生成提示词](prompt.txt) · [局部修正提示词](correction-prompt.txt)

## 借鉴的公开经验

- [Google 官方提示词经验](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)：明确主体、构图、风格、精确标签和事实约束。
- [DeepMind 提示词指南](https://deepmind.google/models/gemini-image/prompt-guide/)：文字用引号，说明字体，并通过具体编辑迭代。
- [PaperBanana 原作者仓库](https://github.com/dwzhu-pku/PaperBanana)：借鉴内容规划、风格设计和生成后审查的分工；本次未安装或运行该框架，未复制其提示词源码。

## 审查记录

首稿将 E3 的未知条件画在 Freshness 列，并将部分通过条件画成横杠；一次局部提示词编辑后，核对为 E1=YES/YES/YES，E2=YES/NO/YES，E3=?/YES/YES。其余主要标签及规划、约束、反馈方向经人眼检查。

作者自评：设备与经验卡片更具象，主次和读图路径较清楚；设备细节偏重，中心带少量立体装饰，缩印可读性仍需针对用途检查。用户审美评价待定。

本图为 AI 生成概念插画，不是实际空分装置工程图或实验结果；未证明方法创新、性能或安全性。正式投稿前应核查目标期刊/会议的 AI 图片政策及版式要求。

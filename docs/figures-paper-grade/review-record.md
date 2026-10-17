# 复杂方法图审校与编辑证据（2026-10-17）

四位审查者独立打开 PNG，修复后复看。以下为真实返回的具体证据，未将评分作为投稿水平保证。

| 审查者 ID | 镜头 | 复审证据 |
|---|---|---|
| /root/papergrade_geometry | 几何 | Review/Execute分支、蓝绿反馈线、候选总线、独立query输入及g输出均接入清楚，无穿字、错接或裁切。 |
| /root/papergrade_semantic | 科学语义 | 原始观测与验证后更新、Review/Execute/拒绝路径、iff定义及g=1/0/0一致。 |
| /root/papergrade_text | 文字 | Review、Execute、g列及1/0/0完整，候选总线不遮文字，182mm宽最小7.27pt。 |
| /root/papergrade_aesthetic | 审美 | 候选输入误读已消除，g列区分条件三值与复用二值结果，Review/Execute和两阶段反馈可辨认。 |

原始报告与修复历史保存在本地既有研究课题的 `figures/paper-grade-workflow/2026-10-17/qa/`。

机器验证：原生 SVG 文本分别56/54个；draw.io对象117/94个；连接线22/14条；图中没有嵌入底图；PDF嵌入位图0。检查脚本会对照SVG与draw.io全部文字、验证连接引用、测量字体宽度并生成182mm宽A4阅读样张。运行结果见 `img/figures/paper-grade/verification.json`。

实际编辑：Inkscape CLI选择 `planner-group` 移动分组，保留框与整句标题，再将标题修改为 `Planner (edited)`，重导出PDF。确认PDF含新标题且无嵌入位图。SVG线条移动后不会像draw.io连接器一样自动追踪节点，人工精修后必须检查连线。

自动PDF几何检查的文字紧凑警告人工核查为正常行间距与表格排版；未把矩阵格子、波形与轴线之间的接触作为错误。无几何错误不代表没有科学错误，仍使用上述独立人工视角。

当前样板是概念设计，不承诺方法创新、实际有效性、完整控制安全性或特定会议录用。真正论文需替换为实际方法与证据，并在正式模板中验收。


本轮编辑器状态：SVG/Inkscape 的模块移动、整句改字和 PDF 重导出已实测通过；draw.io 对象和连线引用结构检查通过，但网页编辑器打开／导出验收受网络阻断，未计为通过。当前经过实际验证的人工编辑路线是 SVG → Inkscape。详见 editor-validation.json。

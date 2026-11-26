---
title: 科研数据图与配色规范
permalink: /palettes/guide/
---

# 科研数据图与配色规范

适用于 Xplore-LAB 绘图工作台里的数据图、可换色案例和 SVG 导出。期刊尺寸与字体约束以具体刊物的官方指南为准。下面的配色和排版规则用于设计、审校及验收工作台。

## 原刊图里可以复用的做法

| 案例 | 图里怎样组织证据 | 工作台采用的做法 |
| --- | --- | --- |
| Hollmann 等，*Nature*，Fig. 3a | 方法按行、测试函数按列。目标与拟合各用一个固定颜色。重复刻度主要留在矩阵外沿。 [原刊 PDF](https://www.nature.com/articles/s41586-024-08328-6.pdf) | 「优秀案例」保留五行六列。把目标点、拟合线分别作为可编辑的配色角色。 |
| Msemburi 等，*Nature*，Fig. 2 | 七个面板共用量纲和纵轴范围。每个面板的折线显示估计值，色带显示对应的 95% 不确定区间。 [原刊与源数据](https://www.nature.com/articles/s41586-022-05522-2/figures/2) · [公开重画代码](https://github.com/Mapika/inklet/tree/b0a38233c3cf91d01bc64d219c878d248d9402b6/examples/published/who_excess_2023) | 当两个面板确实共享物理量、范围和类别含义时，才合并图例或外沿轴标。单条线与其区间共用基础色。 |
| Tabula Sapiens Consortium，*Science*，Fig. 2B | 柱子合计 100%，离散色标识组成类别，柱下灰度带表达另一个变量。 [原刊图](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/7bc7/9812260/5588067556ad/nihms-1856632-f0003.jpg) | 换色只作用于组成分类，分组条维持自身的编码。分母、类别次序和柱高固定。 |
| Hao 等，*Cell*，Fig. 2A | 三个并列嵌入使用同一份类别图例。同色跨面板指向同一群体。 [原刊图](https://pmc.ncbi.nlm.nih.gov/articles/PMC8238499/figure/fig2/) | 同一案例的三个面板共用类别颜色。换色时保持点位置和类别对应关系。 |
| Givechian 等，*Nature Machine Intelligence*，Fig. 3 | 多指标用并列面板组织，突出待比较的方法。公开脚本可核对绘图结构。 [原刊](https://www.nature.com/articles/s42256-025-01163-y/figures/3) · [作者脚本，CC BY-NC 4.0](https://github.com/ChenLiu-1996/figures4papers/tree/main/figure_ImmunoStruct) | 用重复面板和一致布局降低读图成本。工作台的普通数量柱使用零基线。 |

案例索引还可查 [Figure Gallery](https://github.com/Chutj/sci-figure-gallery) 和 [Inklet 的原刊复现页面](https://inklet.readthedocs.io/en/stable/published-figures/)。新增案例应记录论文、图号、数据来源、公开代码与许可证、取色方法，以及重画保留了哪些结构。投稿图使用对应的真实数据，教学示例在图外说明模拟或重画状态。

## 原刊取色记录

| 案例 | 已收录的颜色与角色 |
| --- | --- |
| Nature · TabPFN Fig. 3a | `#FF7F0E` 为目标点，`#1F77B4` 为拟合曲线。从原图 PNG 取样，给两种数据角色各用一种颜色。 |
| Science · Tabula Sapiens Fig. 2B | `#A45187`、`#62ADCC`、`#E8B250`、`#658C55`、`#807FAB` 依次对应上皮、内皮、基质、免疫和外周神经系统。取自原刊 JPEG 图例，保留原顺序，允许存在压缩色差。 |
| Cell · WNN Fig. 2A | 图例取样共 11 色。模拟重画用 `#FAB461`、`#7FB0D7`、`#F37D72`、`#BC7FB6`、`#FCED74`、`#B6D566` 作为前六色，颜色含义以模拟分组为准。 |
| Nature · WHO Fig. 2 | 七个面板使用七种基础色，每个面板内部用同色线条与浅色区间。公开重画代码记录了色值，适合参考如何标出不确定性。 |

在工作台选择「优秀案例配色」可查前三组。保持原刊图例的颜色角色有助于比较。普通画图默认用 Paul Tol bright，少量系列可选其 high-contrast 色板。Crameri `batlow` 和 `vik` 分别用作顺序与发散色阶。 [Paul Tol 原始色板](https://sronpersonalpages.nl/~pault/) · [Crameri 色阶](https://www.fabiocrameri.ch/colourmaps/)

## 怎样判断一张图画得好

1. **读者能看出比较对象。** 坐标、单位、基准、分类与误差定义可核查。主图表达一个明确问题。分组柱适合在一致量纲下对比类别。若关心组内分布或配对变化，保留个体点或连接关系。
2. **颜色有稳定含义。** 同一类别跨面板保持一致。同一线条和它的区间共用基色。已经用位置和标签识别的柱可以同色，也可以用中性灰加一个强调色。分类色板从经过设计的离散颜色中挑选。顺序色阶表示从低到高，发散色阶围绕明确基准，中心色与基准对齐。 [Crameri 等，Fig. 5–6](https://www.nature.com/articles/s41467-020-19160-7) · [Paul Tol 色板](https://sronpersonalpages.nl/~pault/) · [ColorBrewer](https://colorbrewer2.org/)
3. **缩到论文宽度依然能读。** 坐标与刻度清楚，图例靠近数据，图例文字使用深色，颜色相近的折线辅以线型。共享图例和外沿轴标用于含义一致的面板。检查灰度、常见色觉模拟、文字重叠和裁切。 [Nature 图形规范](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
4. **导出保留编辑能力。** 预览与 SVG 的数据位置、文字、图例和颜色一致。按目标宽度查看导出，文字应可选中。Nature 主刊普通图文使用 5–7 pt，子图编号 8 pt 加粗，线宽 0.25–1 pt。Science 和 Cell 使用各自的期刊设置。 [Nature 最终投稿](https://www.nature.com/nature/for-authors/final-submission) · [Science 官方指南存档](https://web.archive.org/web/20250810105213/https://www.science.org/content/page/instructions-preparing-initial-manuscript) · [Cell Press 官方指南存档](https://web.archive.org/web/20250911134049/https://www.cell.com/information-for-authors/figure-guidelines)

## 工作台验收规则

| 检查 | 通过条件 |
| --- | --- |
| 换色保持数据 | 用 3、8、9 色卡切换同一张柱图或折线图，点、柱、线和误差棒的数量及坐标保持一致。改变色阶派生、单色、强调色或自选颜色也遵循同一规则。案例按各自定义的角色试色。 |
| 色板与分配分开 | 整张色板可作为候选。系列可使用自动分配、统一色或强调色，也可逐项换色。候选色有余量时，分类配色从首色起优先增加与已选颜色的最小色差，顺序和发散色阶从全段取样。原刊取色按原有角色顺序分配。色卡不足时，界面说明发生了重复。重置分配回到自动。 |
| 数值色图 | 普通热图的色条与单元格用同一个 0–1 映射。选择顺序或发散色板时使用其完整采样范围。发散色板只有在数据存在明确中心值时才适用；工作台热图的中心示例为 0.5。 |
| 组合图与案例 | 共享配色只合并同义图例。原刊图和模拟重画各有入口。案例原色可恢复，色觉模拟和透明度设置可继续检查。 |
| 输出与小屏 | 在三套期刊设置下验证 SVG 下载，检查小屏和桌面画布。Matplotlib 通用模板传入相同的系列颜色，模板示例数据与网页示例可能不同。 |

「图内字体」默认随期刊设置，也可手动选择 Arial、Helvetica、DejaVu Sans 或 Times New Roman。SVG 保留可编辑文字并声明回退字体，其实际显示取决于打开文件的设备。手动选择字体时，投稿前应核对目标期刊的字体要求。

## 工作台的真实数据示例

- **WHO 月度趋势。** 从 Msemburi 等的 Fig. 2 源表读取 7 组 × 24 月，共 168 条估计。不改估计值及原刊 95% 不确定区间，作图时把比例乘以 100。 [原刊与源数据](https://www.nature.com/articles/s41586-022-05522-2/figures/2)
- **企鹅体重。** 依据 Gorman 等研究公开的 Palmer Penguins 数据重画。344 条记录中排除 2 条缺失体重，图上保留 342 个观测点。柱为各物种样本均值，误差棒为 ±1 样本标准差，横轴点位的轻微抖动只用于减少重叠。 [原刊](https://doi.org/10.1371/journal.pone.0090081) · [数据集与 CC0 许可](https://allisonhorst.github.io/palmerpenguins/)

两张图均可独立换色，下载的 CSV 保留源单位。企鹅 CSV 中的两条缺失体重保留为空白，便于复核排除规则。

[返回配色工作台](/palettes/#bench)

# 论文原图与教学重绘对照

打开 comparison.html 即可离线查看十篇对照。每篇含：原图 300 dpi PNG、PDF 区域裁剪、网页既有教学重绘 SVG。

原论文版权归各论文权利人，不随本站代码许可重新授权。论文 PDF 本地保存于 /home/lab434/data/papers/figure-reference-classics；完整正文未重复打入图包，不单独下载 SI。

manifest.json 记录来源 URL、图号、PDF 从 1 起算的页码、源 PDF SHA256、裁剪坐标（PDF point，左上原点）、像素尺寸及对照差异。官方出版版和 arXiv 版页码可能不同，请按所记录的源 PDF 核对。

提取不使用“导出第一张嵌入图片”启发式，而是渲染完整图区域，保留文字、路径和位图。PDF 裁剪保留原有内容类型，不把原本的位图伪称为矢量。原图没有重绘、改字或 AI 修补。

复现：安装 PyMuPDF，准备以 slug 命名的源 PDF 后运行：

    python3 extract_reference_originals.py --pdf-dir /path/to/pdfs

脚本随包附带，SITE 默认由脚本路径的上一级确定；在源码仓库 scripts/ 内运行可直接复现原始图和重绘导出，其他布局请调整 SITE。comparison.html 是本次交付的静态对照页。

已逐张检查整页定位与裁剪预览，并核对图号；GPT-3 使用 Fig 3.8（双面板），不把教学重绘的虚构数据当成论文曲线；CoT 正确输出为 9；Switch 原图左侧是模块定位，不是密集 FFN 基线。

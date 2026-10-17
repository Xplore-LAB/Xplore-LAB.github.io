# Transformer 忠实重绘

来源：Vaswani et al., Attention Is All You Need (2017)，Figure 1，https://arxiv.org/pdf/1706.03762#page=3 。

主档为 transformer-faithful.svg。字体、形状、连线全为原生对象，没有嵌入原图或把字形转成路径。配色取自源图，画布与源PNG比例一致（972×1405）。14个功能框、5个Add & Norm、5条残差绕线、3处注意力、2个前馈、两个位置编码以及交叉注意力路径均保留。

采用Roboto Light近似原图排版，嵌入字形子集保障浏览器显示；SVG仍保留可编辑文字。完整字体及Apache2许可证随附。字体字形、箭头及少量路径曲率与原图有细微差异，不宣称逐像素相同。

打开comparison.html可并排查看，或切换叠加模式拖动透明度。下载包保持网站目录结构，离线入口在 img/figures/transformer-faithful/comparison.html 。

复现：安装Inkscape、Python fonttools[woff]及Roboto Light后，从scripts/build_transformer_faithful.py运行。字体文件置于img/figures/transformer-faithful/Roboto-Light.ttf。必要时先安装该字体供Inkscape导出使用。脚本不联网，不改变原论文文件。

120 mm宽是本次参考复刻的展示尺寸，不按Nature单栏/双栏生产规格声明合规。原图及衍生重绘保留论文来源，版权归相关权利人。

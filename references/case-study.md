# 实测案例：为什么判读纪律是硬性的

基线测试文档：*Analytical Chemistry* 2026 年一篇 mRNA-LNP 粒径表征论文（AF4-SAXS/MALS），13 页，4.3MB，数字出版 PDF。硬件：RTX 4070 Laptop 8GB + CUDA 12.6。

## 结果统计

- 290 个结构块：text 129、formula 27、formula_number 25、figure_title 12、chart 5、table 2、header/footer 等若干。
- 切割出 5 张统计图表（含三联、四联子图），全部完整：坐标轴、图例、子图标注都在框内，未切到相邻正文。
- Figure 2/3/4/5 的图题正确配对在图下方。
- 27 个公式转 LaTeX，2 张表转 HTML table，质量可用。
- 全程约 2 分钟。

节选数据见 `examples/sample_blocks.json`（图-图题配对、公式、漏检页的真实块记录）。

## 三个实测故障（判读纪律的直接依据）

1. **示意图漏检**。第 3 页 Figure 1 是弹性散射几何线条图，版面检测器完全没认出它是图：只检出图题 `Figure 1. Geometry of elastic scattering.`，没有对应 `chart`/`image` 块。统计图表可靠，线条示意图不可靠——这就是"有图题无切割图必须主动报告"这条纪律的来源。
2. **小字号图题乱码**。Figure 3 图题真实文本是 "Figure 3. Function of polymer particle..."，OCR 输出为 "Figure.utciooflym ricle.acamvlatitiedromLSan XSa…"，完全不可读。Table 2 标题同样有错字。图题引用前必须对照切割图。
3. **正文偶发错字**。"formulation the sample buffer was changed" 被识别为 "formlation th sampe bufr wa chaed"。低频但存在，关键事实转述前需留意。

## 另一个对照样本

人民日报版面截图（含新闻照片）：照片完整切割，图题（"在厄立特里亚…中国驻厄立特里亚大使馆供图"）准确配对，中文正文识别质量高。

## 结论

这套产线对"图表定位与切割"可靠，对"小字号文本逐字准确"不可靠。skill 的价值正在于把这两个事实固化成流程：图必看、疑必核、漏必报。

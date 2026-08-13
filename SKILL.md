---
name: argus-doc-reader
description: 本地 GPU 深度文档精读（PP-StructureV3，Argus 百眼巨人）。把 PDF/扫描件解析为 Markdown + 逐块 JSON + 完整切割的图表图片，图文标题自动配对。仅当用户明确要求"精读文档中的图表"、"把 PDF 里的图都读清楚"、"图表必须看懂/不能漏"等图表级理解需求时使用；普通 PDF 阅读、摘要、问答等任务不要使用本 skill，直接走默认 PDF 阅读路径（云端更快）。触发关键词示例：精读图表、图表提取、读懂每张图、figure/chart 都要看、扫描版图表识别。
---

# Argus Doc Reader — 图表级 PDF 精读

本机已部署 PP-StructureV3（百度飞桨文档解析产线），GPU 加速。输出：合并 Markdown、每页原始 JSON（含每块 label/content/bbox/阅读顺序）、切割出的图表原图（`imgs/`）。

## 环境（已就绪，勿重复安装）

- Python 环境：`D:\PaddleOCR\venv\Scripts\python.exe`（paddlepaddle-gpu 3.3.1 cu126 + paddleocr 3.7.0）
- 模型缓存：`D:\PaddleOCR\models`（已下载，首次调用无需再下载）
- 显卡：RTX 4070 Laptop 8GB，推理走 CUDA；若 GPU 异常可加 `--cpu` 兜底

## 工作流

1. 若 PDF 不在当前工作区，先复制进来。
2. 运行（脚本副本在 `scripts/pdf_parse.py`，主副本在 `D:\PaddleOCR\pdf_parse.py`，两者一致）：

   ```
   D:\PaddleOCR\venv\Scripts\python.exe D:\PaddleOCR\pdf_parse.py <输入.pdf> [-o 输出目录] [--pages 1-5] [--cpu] [--chart]
   ```

   - 超过 30 页的文档先 `--pages` 试几页确认效果，再全量跑（GPU 上约 5~10 秒/页）。
   - `--chart` 启用图表转数据表（PP-Chart2Table），仅在用户要求"读出图中数据"时加，会更慢。
3. 依次读取输出：`<名字>.md`（全文，图已在原位引用）→ `all_blocks.json` 或 `pages/page_*/`*`_res.json`（结构化块）→ `imgs/` 中每张切割图用 ReadMediaFile 逐张查看。

## 必须遵守的判读纪律

OCR 结果是**可能出错的中间产物**，切割图才是事实来源：

- 图题、正文、公式中出现乱码式错字（如 "Figure.utciooflym…"）时，不要照读，打开对应切割图或页面区域核实后再陈述。
- 引用图表结论前，必须实际查看该图的切割图片；图中坐标轴/图例文字 OCR 噪声大，以图为准。
- 发现 `figure_title` 存在但同页无对应切割图，说明示意图/线条图被版面检测漏检——主动向用户指出该图未被切割，必要时用 PDF 渲染截图手动补切。
- 交付时区分两类内容：高置信文本（正文）与需标注"经原图核对"的内容（图题、图中数据、公式）。

## 已知局限（实测确认）

- 统计图表（折线/柱状/散点）切割可靠；纯线条示意图可能漏检。
- PDF 内嵌文字层不被利用，整页按位图 OCR，小字号文本错误率上升。
- 生僻符号、密集公式编号偶有错乱。

## 输出交付

向用户返回：`all_blocks.json` 路径、合并 Markdown 路径、切割图的内联展示（Markdown 图片链接，客户端可直接渲染），并附一句图文配对与漏检情况的诚实评估。

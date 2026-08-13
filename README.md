# 👁️ Argus Doc Reader

> 希腊神话中的百眼巨人 Argus——把文档里的每一张图都看在眼里。

一个 Kimi Work / Kimi Code skill：调用本地部署的百度飞桨 **PP-StructureV3** 文档解析产线（GPU 加速），把 PDF / 扫描件精读为：

- **Markdown** 全文（图表在正确位置被引用）
- **逐块 JSON**（每块的 label / content / bbox / 阅读顺序）
- **完整切割的图表图片**（`imgs/`，图题自动配对）

并要求 AI 在判读时以切割原图为准、交叉校验 OCR 文本，杜绝"OCR 读错照读"。

## 何时触发

仅在用户**明确要求精读文档中的图表**时使用（如"把 PDF 里的图都读清楚""图表必须看懂"）。普通 PDF 阅读走默认云端路径，更快。

## 环境依赖

| 组件 | 版本 |
|---|---|
| PaddlePaddle-GPU | 3.3.1 (CUDA 12.6, pip 安装，无需单独装 CUDA Toolkit) |
| PaddleOCR | 3.7.0 |
| GPU | NVIDIA 8GB+ 显存（开发机为 RTX 4070 Laptop） |
| Python | 3.12 |

## 安装

```bash
python -m venv D:\PaddleOCR\venv
D:\PaddleOCR\venv\Scripts\python.exe -m pip install paddlepaddle-gpu==3.3.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
D:\PaddleOCR\venv\Scripts\python.exe -m pip install "paddleocr[all]"
```

将本仓库放入 skills 目录（如 `daimon/skills/argus-doc-reader/`）即可被 Kimi 自动发现。

## 使用

```bash
D:\PaddleOCR\venv\Scripts\python.exe scripts/pdf_parse.py 论文.pdf [--pages 1-5] [--cpu] [--chart]
```

输出：`<名字>.md` + `imgs/`（切割图）+ `pages/`（逐页 JSON）。

## 实测表现（Analytical Chemistry 论文，13 页）

- ✅ 5 张统计图表完整切割（含三联/四联子图），图题正确配对
- ✅ 27 个公式转 LaTeX，2 张表转 HTML
- ⚠️ 线条示意图可能漏检；小字号图题 OCR 有错字（以切割图为准）

## License

Apache-2.0（遵循 PaddleOCR 上游协议）

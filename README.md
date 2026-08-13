# Argus Doc Reader

本地 GPU 驱动的图表级 PDF 精读 skill（Kimi Work / Kimi Code），基于百度飞桨 PP-StructureV3 文档解析产线。

把 PDF / 扫描件解析为：Markdown 全文（图表在原位引用）、逐块 JSON（label / content / bbox / 阅读顺序）、完整切割的图表图片（图题自动配对）。核心纪律：OCR 文本是可疑的中间产物，切割图才是事实来源——引用图表结论前必须亲眼看图，发现漏检必须主动报告。

## 何时触发

仅当用户明确要求精读文档中的图表（"把 PDF 里的图都读清楚"、"图表必须看懂不能漏"等）。普通 PDF 阅读走默认云端路径，更快。

## 架构（路由 + 渐进披露）

```
SKILL.md                    路由器：只做分发，不装知识
manifest.yaml               路由清单：env 轴与按需 references
static/core/                每次必载：精读契约（判读纪律）+ 通用工作流
fragments/env/              按硬件档位四选一加载：
  ├── not-installed.md      从零安装
  ├── nvidia-16gb.md        显存 ≥14GB
  ├── nvidia-8gb.md         显存 6~14GB（开发基准档位）
  └── cpu-only.md           无 GPU 兜底
references/                 按需加载：安装详解 / 踩坑记录 / 输出格式 / 实测案例
scripts/detect_env.py       环境探测，输出路由建议（JSON）
scripts/pdf_parse.py        机器无关的解析入口
examples/                   真实解析结果节选
```

路由方式：运行 `detect_env.py` → 取输出 `route` 字段 → 加载对应 fragment。脚本机器无关，不含任何硬编码本机路径。

## 安装（最短路径）

```bash
python -m venv venv
venv/Scripts/python -m pip install paddlepaddle-gpu==3.3.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
venv/Scripts/python -m pip install "paddleocr[all]"
venv/Scripts/python -c "import paddle; paddle.utils.run_check()"
```

wheel 自带 CUDA 12.6 运行时与 cuDNN，无需单独安装 CUDA Toolkit。版本矩阵、大 wheel 断点续传、模型缓存迁移等见 `references/install.md`；NVML 报错、WinError 127、OOM 等踩坑记录见 `references/troubleshooting.md`。

## 实测基线

RTX 4070 Laptop（8GB）：13 页 Analytical Chemistry 论文约 2 分钟，解析出 290 个结构块，5 张统计图表（含三联/四联子图）完整切割、图题正确配对，27 个公式转 LaTeX。

已知盲区（均有应对纪律）：线条示意图漏检、小字号图题 OCR 乱码、正文偶发错字。依据与数据见 `references/case-study.md` 与 `examples/sample_blocks.json`。

## License

Apache-2.0（遵循 PaddleOCR 上游协议）

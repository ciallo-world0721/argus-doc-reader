---
name: argus-doc-reader
description: 本地部署百度 PP-StructureV3 文档解析产线（GPU 加速），把 PDF/扫描件精读为 Markdown + 逐块 JSON + 完整切割的图表图片，图题自动配对，并以切割原图交叉校验 OCR 文本。仅当用户明确要求精读文档图表时使用，例如"把 PDF 里的图都读清楚"、"图表必须看懂/不能漏"、"精读这份文献的 figure"、扫描版图表识别、图表提取。普通 PDF 阅读、摘要、翻译、问答不要使用本 skill，走默认 PDF 阅读路径（云端更快）。也适用于从零安装部署该环境的请求。
---

# Argus Doc Reader — 图表级 PDF 精读（路由器）

本文件只做路由。不要凭记忆执行安装或解析，按下面的协议从磁盘加载对应内容。

## 路由协议

### 1. 加载核心层

读取 [manifest.yaml](manifest.yaml)，以及其中 `always_load` 列出的两个文件：

- `static/core/contract.md` — 交付物契约与 OCR 判读纪律（每次任务都必须遵守）
- `static/core/workflow.md` — 解析执行流程（与环境无关的通用步骤）

### 2. 解析环境轴（阻塞门）

运行环境探测脚本，确定 `env` 轴取值：

```
python scripts/detect_env.py
```

- 若目标环境已有独立 venv，用该 venv 的 python 运行；否则用任意可用 python。
- 脚本输出 JSON，`route` 字段即为轴取值：`not_installed` / `nvidia_16gb_plus` / `nvidia_8gb` / `cpu_only`。
- 按 `manifest.yaml` 的 `axes.env.values` 映射，读取对应的 `fragments/env/*.md`，只读这一个 fragment。
- `detect_env.py` 不可用或结果存疑时，手动确认（GPU 型号/显存、paddle 是否已装）后再选 fragment，不要瞎猜。

### 3. 按加载的材料执行

- `not_installed`：先按 fragment 完成安装与验证，再进入解析流程。
- 其余：直接按 `static/core/workflow.md` 执行解析，fragment 里是该硬件档位的模型/参数/速度预期。

### 4. 按需加载 references

不要默认加载。需要时再打开：

- 从零安装的详细步骤、CUDA 版本选择 → `references/install.md`
- 任何报错、异常、性能问题 → `references/troubleshooting.md`
- 解读 JSON 结构、block label 含义、Markdown 约定 → `references/output-format.md`
- 想了解本 skill 的实测基线与已知盲区 → `references/case-study.md`

## 硬性纪律

- 脚本和文档都是机器无关的。禁止把任何本机绝对路径写进交付内容或脚本；一切路径以 `detect_env.py` 输出和用户现场为准。
- OCR 文本永远视为可疑中间产物，切割图才是事实来源（细则在 contract.md，每次任务都适用）。

# 故障排除（实测踩坑记录）

按症状索引。每条都是真实遇到或官方 issue 确认过的。

## nvidia-smi: Failed to initialize NVML: Unknown Error

- 场景：笔记本（Optimus 双显卡），独显休眠。
- 影响：只影响 nvidia-smi 这个工具本身；paddle 的 CUDA 推理照常工作。
- 处理：不要急着修驱动，直接 `paddle.utils.run_check()` 验证。真的 GPU 掉驱动（重启后仍失败）才需要重装驱动。

## import paddle 报 WinError 127 / 找不到 cublas、cudnn 动态库

- 原因：wheel 的 CUDA 档位与驱动不兼容（常见于装了过新或过旧的档位）。
- 处理：换一个 CUDA 档位重装（cu126 ↔ cu118 ↔ cu129），见 install.md 版本矩阵。

## pip 安装超时 / 下载中断

- wheel 大（550MB），单次超时直接重跑同一命令，pip 缓存会复用已完成的包。
- 主 wheel 本身建议 curl 断点续传（install.md 有完整命令）。

## GPU OOM（ResourceExhausted / CUDA out of memory）

1. 设 `FLAGS_allocator_strategy=auto_growth`（动态显存分配）后重跑。
2. 关掉其他占显存的程序。
3. `--pages` 分批。
4. 最后手段 `--device cpu`。

## Windows 上 OpenMP 冲突报错

设 `KMP_DUPLICATE_LIB_OK=TRUE`。pdf_parse.py 已内置。

## 输出与文档篇幅明显不符（几十页只出几行字）

- 这是 OCR 管线的已知故障模式，先怀疑解析失败：检查 PDF 是否加密/损坏、页面是否为异常尺寸。
- 用 `--pages 1` 单页试跑定位；必要时换 `--device cpu` 排除 GPU 数值问题。

## 首次运行卡在模型下载

- 约 1.8GB，分多个小文件逐个下载，进度条之间可能长时间无输出，属正常。
- 中途中断重跑即可，已下载的模型会复用（脚本会提示 Using cached files）。
- 下载源默认百度 BOS，国内直连；海外网络可设 `PADDLE_PDX_MODEL_SOURCE=modelscope` 或 `huggingface`。

## 公式/图题识别成乱码

不是故障，是能力边界。整页位图 OCR 对小字号文字错误率上升。按 contract.md：以切割图为准核实，不要照读。

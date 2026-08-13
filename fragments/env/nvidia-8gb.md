# 环境：NVIDIA 显卡，显存 6~14GB

典型机型：RTX 3060/4060/4070（含 Laptop）。环境已装 paddle-gpu + paddleocr。这是本 skill 开发与实测的基准档位。

## 推荐配置

- 默认 PP-StructureV3（版面分析 + PP-OCRv5 server 检测/识别 + 表格 + 公式）。8GB 实测可完整运行。
- 不要默认开 `--chart`；只有用户明确要"读出图中数据"时才开。
- 超过 50 页的文档建议 `--pages` 分批，避免单次任务过长。

## 实测基线（RTX 4070 Laptop 8GB，CUDA 12.6）

- 约 5~10 秒/页；13 页论文约 2 分钟。
- 显存占用约 4~6GB，余量不大，推理时不要让其他大模型同时占卡。

## 踩过的坑（本档位实测）

- 笔记本 `nvidia-smi` 偶发 `Failed to initialize NVML: Unknown Error`：独显休眠导致，paddle 推理不受影响，以 `paddle.utils.run_check()` 为准。
- 若推理报 OOM：设环境变量 `FLAGS_allocator_strategy=auto_growth` 后重跑；仍不行换 `--device cpu` 或 `--pages` 分批。

更多见 `references/troubleshooting.md`。

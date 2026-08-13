# 环境：NVIDIA 显卡，显存 ≥14GB

典型机型：RTX 4080/4090、A 系列。环境已装 paddle-gpu + paddleocr。

## 推荐配置

- 默认 PP-StructureV3 全模块（版面分析 + PP-OCRv5 server 检测/识别 + 表格 + 公式 + 印章可选）。
- 显存充裕，`--chart`（图表转数据表）可以按需常开。
- 长文档可一次全量跑，不必分批。

## 可选项

- 需要更强端到端精度时可评估 PaddleOCR-VL（0.9B VLM，OmniDocBench SOTA）。注意：Windows 原生支持不成熟，官方建议 WSL/Docker；原生 Windows 请优先留在 PP-StructureV3。
- 追求吞吐可研究 PaddleX 服务化部署（`paddlex --serve`），本 skill 的脚本是本地批处理路径，不依赖服务。

## 执行

按 `static/core/workflow.md` 跑。性能参考：约 3~8 秒/页。

出现 OOM 或异常时查 `references/troubleshooting.md`。

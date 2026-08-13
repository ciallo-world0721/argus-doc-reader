# 解析工作流（环境无关）

前置：环境轴已解析（见 SKILL.md 第 2 步），对应 fragment 已读取，环境已就绪。

## 步骤

1. 若 PDF 不在当前工作区，先复制进来。
2. 运行解析脚本：

   ```
   python scripts/pdf_parse.py <输入.pdf> [-o 输出目录] [--pages 1-5,8] [--device cpu] [--chart] [--models-dir 路径]
   ```

   - 超过 30 页先 `--pages` 试 2~3 页确认效果，再全量跑。
   - 仅当用户要求"读出图中数据"时加 `--chart`（PP-Chart2Table 图表转数据表，明显更慢）。
   - 模型缓存默认在 `~/.paddlex`；需要指定位置时用 `--models-dir`（脚本会据此设置 `PADDLE_PDX_CACHE_HOME`）。
3. 依次读取输出：合并 Markdown → 逐块 JSON → `imgs/` 中每张切割图逐张查看。
4. 按 contract.md 的纪律核实可疑文本，交付结果与诚实评估。

## 性能参考

RTX 4070 Laptop（8GB）上约 5~10 秒/页；13 页论文全程约 2 分钟。CPU 模式慢一个数量级，只适合应急验证。

## 失败后重跑

输出目录已存在时会覆盖同名文件。只想补跑部分页，用 `--pages` 限定；切割图与 Markdown 会重新生成，旧文件不合并。

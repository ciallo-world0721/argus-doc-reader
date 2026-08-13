# 环境：仅 CPU（无 NVIDIA GPU 或 GPU 不可用）

包括 macOS、无独显机器、GPU 驱动异常时的兜底。

## 预期管理（先告诉用户）

CPU 模式比 GPU 慢约一个数量级（每页 30~90 秒），只适合应急或小文档。先跟用户确认等待可接受，再动手。

## 执行要点

- `pdf_parse.py` 加 `--device cpu`。
- 必须 `--pages` 分批跑，每批不超过 10 页。
- 不开 `--chart`。
- 只需快速看效果时，可先跑第 1 页冒烟。

## 提速手段（需要改脚本时）

PPStructureV3 支持在构造时裁剪模块，CPU 场景可考虑：

```python
PPStructureV3(
    device="cpu",
    use_doc_orientation_classify=False,  # 关方向分类
    use_doc_unwarping=False,             # 关图像矫正
    use_formula_recognition=False,       # 若文档无公式可关
)
```

关掉公式识别会丢失公式转 LaTeX 能力，动手前先确认文档类型。

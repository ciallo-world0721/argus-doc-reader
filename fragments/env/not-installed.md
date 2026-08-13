# 环境：从零安装

目标：本机还没有 paddle / paddleocr。按本页完成安装与验证，然后回到 workflow.md。

不要凭记忆装。版本选择、排错的完整细节在 `references/install.md`，遇到任何报错先看 `references/troubleshooting.md`。

## 最小路径（NVIDIA GPU + Windows/Linux）

1. 确认 GPU 与驱动：`nvidia-smi`。报 NVML 错误不代表 GPU 不可用（笔记本独显休眠常见），以第 4 步的 `run_check` 为准。
2. 建独立 venv（Python 3.10~3.12），不要装进别人的基础环境：
   ```
   python -m venv <venv路径>
   ```
3. 按驱动选择 CUDA 档位的 paddlepaddle-gpu（wheel 自带 CUDA 运行时与 cuDNN，无需单独装 CUDA Toolkit）：
   ```
   pip install paddlepaddle-gpu==3.3.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
   ```
   wheel 约 550MB，pip 超时风险高；超时则先用 `curl -C -` 断点续传下载 wheel 再本地安装（具体 URL 查法见 install.md）。
4. 验证（这一步才算数）：
   ```
   python -c "import paddle; paddle.utils.run_check()"
   ```
   看到 `PaddlePaddle works well on 1 GPU` 即 GPU 可用。
5. 安装 PaddleOCR（依赖较多，超时直接重跑，pip 缓存会续上）：
   ```
   pip install "paddleocr[all]"
   ```
6. 首次运行会自动下载约 1.8GB 模型，默认存 `~/.paddlex`。需要改位置就设 `PADDLE_PDX_CACHE_HOME`，或用 `pdf_parse.py --models-dir`。
7. 用样例图冒烟测试：
   ```
   python scripts/pdf_parse.py <任意含图表的.pdf> --pages 1
   ```

## 无 NVIDIA GPU

装 CPU 版即可：`pip install paddlepaddle==3.3.1`，之后按 `fragments/env/cpu-only.md` 的参数预期执行。macOS 只能走 CPU 版（或 Docker）。

## 装完之后

重新运行 `scripts/detect_env.py`，按新的 route 值加载对应硬件 fragment。

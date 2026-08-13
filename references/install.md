# 安装详解

## 版本矩阵（2026-08 实测）

| 组件 | 版本 | 说明 |
|---|---|---|
| PaddlePaddle-GPU | 3.3.1 | pip 包自带 CUDA 运行时 + cuDNN 9，无需单独装 CUDA Toolkit |
| 可选 CUDA 档位 | cu118 / cu126 / cu129 | 按驱动新旧选；新驱动（>=560）直接 cu126 |
| PaddleOCR | 3.7.0 | 含 PP-StructureV3 产线 |
| Python | 3.9 ~ 3.13 | 实测 3.12 |
| 模型体积 | 约 1.8GB | 首次运行自动下载 |

GPU 要求：运算能力 ≥7.5（RTX 20 系及以上）。显存 ≥8GB 体验良好。

## 驱动确认

- `nvidia-smi` 能跑就直接看；报 `Failed to initialize NVML: Unknown Error` 多见于笔记本独显休眠，不代表装不了，继续往下走，最终以 `paddle.utils.run_check()` 为准。
- 驱动太旧（CUDA 支持 <11.8）就先升级驱动，不要降级 paddle 凑旧 CUDA。

## CUDA 档位选择

paddle 的 GPU wheel 按 CUDA 版本分目录发布：

```
https://www.paddlepaddle.org.cn/packages/stable/cu126/   # 推荐
https://www.paddlepaddle.org.cn/packages/stable/cu118/
https://www.paddlepaddle.org.cn/packages/stable/cu129/
```

wheel 自带对应版本的 CUDA/cuDNN 运行库，与系统是否安装 CUDA Toolkit 无关。选错档位的表现是 `import paddle` 时报 `WinError 127` 或 cublas/cudnn 加载失败，换档位重装即可。

## 大 wheel 下载超时的解法

paddlepaddle-gpu wheel 约 550MB，pip 单次请求容易被工具超时杀掉。先查出确切 URL 再断点续传：

```bash
# 从 PEP503 索引页找 cp312 win_amd64（或对应平台）的最新 wheel
curl -sL "https://www.paddlepaddle.org.cn/packages/stable/cu126/paddlepaddle-gpu/" | grep -o 'href=[^ >]*'
# 断点续传下载，超时后重复执行同一条命令即可续传
curl -L -C - -o paddlepaddle_gpu-3.3.1-cp312-cp312-win_amd64.whl "<上一步的URL>"
# 本地安装
pip install ./paddlepaddle_gpu-3.3.1-cp312-cp312-win_amd64.whl
```

## 模型缓存位置

默认下载到 `~/.paddlex`（Windows 上是 `C:\Users\<你>\.paddlex`）。要放到其他盘：

- 全局：设环境变量 `PADDLE_PDX_CACHE_HOME=<目录>`
- 单次：`pdf_parse.py --models-dir <目录>`

## 验证清单

```
python -c "import paddle; paddle.utils.run_check()"   # 出现 works well on 1 GPU
python -c "import paddleocr; print(paddleocr.__version__)"
python scripts/pdf_parse.py <样例.pdf> --pages 1       # 端到端冒烟
```

# -*- coding: utf-8 -*-
"""
detect_env.py — argus-doc-reader 环境探测与路由建议

输出 JSON，route 字段对应 manifest.yaml 的 env 轴取值：
  not_installed      未安装 paddle（gpu 字段会说明硬件潜力，供安装时选档位）
  nvidia_16gb_plus   paddle 可用 GPU，显存 >= 14GB
  nvidia_8gb         paddle 可用 GPU，显存 6~14GB
  cpu_only           无可用 NVIDIA GPU（含 paddle 只装了 CPU 版）

用法：
  python detect_env.py            # 探测运行它的解释器环境
  <目标venv>/python detect_env.py # 探测指定 venv
"""
import json
import shutil
import subprocess
import sys


def gpu_info():
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    try:
        out = subprocess.run(
            [exe, "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=15,
        )
        if out.returncode != 0 or not out.stdout.strip():
            return {"error": (out.stderr or out.stdout).strip() or "nvidia-smi 调用失败",
                    "note": "笔记本独显休眠时常见，不代表 GPU 不可用，以 paddle.utils.run_check() 为准"}
        name, mem, drv = [x.strip() for x in out.stdout.splitlines()[0].split(",")][:3]
        return {"name": name, "vram_mb": int(float(mem)), "driver": drv}
    except Exception as e:
        return {"error": str(e)}


def paddle_status():
    try:
        import paddle
        return {
            "installed": True,
            "version": paddle.__version__,
            "compiled_cuda": paddle.version.cuda(),
            "gpu_count": paddle.device.cuda.device_count(),
        }
    except Exception as e:
        return {"installed": False, "detail": str(e).splitlines()[0][:200]}


def paddleocr_status():
    try:
        import paddleocr
        return {"installed": True, "version": getattr(paddleocr, "__version__", "unknown")}
    except Exception:
        return {"installed": False}


def main():
    gpu = gpu_info()
    pd = paddle_status()
    ocr = paddleocr_status()

    if not pd["installed"]:
        route = "not_installed"
    elif pd.get("gpu_count", 0) >= 1:
        vram = (gpu or {}).get("vram_mb") or 0
        route = "nvidia_16gb_plus" if vram >= 14000 else "nvidia_8gb"
    else:
        route = "cpu_only"

    print(json.dumps({
        "route": route,
        "python": sys.version.split()[0],
        "python_exe": sys.executable,
        "gpu": gpu,
        "paddle": pd,
        "paddleocr": ocr,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

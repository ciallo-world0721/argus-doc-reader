# -*- coding: utf-8 -*-
"""
pdf_parse.py — PP-StructureV3 文档解析封装（argus-doc-reader）

输入 PDF/图片，输出:
  <输出目录>/<文档名>.md          合并后的全文 Markdown（图已在正确位置引用）
  <输出目录>/imgs/                所有裁剪出的图片（文件名含页码与坐标）
  <输出目录>/pages/page_xxx/      每页 Markdown + 完整 JSON（含逐块坐标与类型）

用法:
  python pdf_parse.py 输入.pdf [-o 输出目录] [--pages 1-5,8] [--device gpu|cpu]
                               [--chart] [--models-dir 模型缓存目录]
"""
import argparse
import os
import re
import shutil
import sys
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")  # Windows OpenMP 冲突规避


def parse_pages(spec: str):
    """'1-5,8' -> [1,2,3,4,5,8]（1-based）"""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        elif part:
            pages.add(int(part))
    return sorted(pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="PDF 或图片路径")
    ap.add_argument("-o", "--output", default=None, help="输出目录（默认: 输入文件同目录 <名字>_parsed）")
    ap.add_argument("--pages", default=None, help="只解析指定页，如 1-5,8（默认全部）")
    ap.add_argument("--device", default="gpu", choices=["gpu", "cpu"], help="推理设备（默认 gpu）")
    ap.add_argument("--chart", action="store_true", help="开启图表转表格（PP-Chart2Table，更慢）")
    ap.add_argument("--models-dir", default=None, help="模型缓存目录（默认 ~/.paddlex，可用 PADDLE_PDX_CACHE_HOME 指定）")
    args = ap.parse_args()

    if args.models_dir:
        os.environ["PADDLE_PDX_CACHE_HOME"] = str(Path(args.models_dir).resolve())

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        sys.exit(f"找不到输入文件: {input_path}")
    doc_name = input_path.stem
    out_dir = Path(args.output).resolve() if args.output else input_path.parent / f"{doc_name}_parsed"
    imgs_dir = out_dir / "imgs"
    pages_dir = out_dir / "pages"
    imgs_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)

    from paddleocr import PPStructureV3

    pipeline = PPStructureV3(
        device=args.device,
        use_chart_recognition=args.chart,
    )

    print(f"[1/2] 开始解析: {input_path.name} (device={args.device})")
    results = pipeline.predict(str(input_path))

    wanted = parse_pages(args.pages) if args.pages else None
    md_parts = []
    page_count = 0

    for idx, res in enumerate(results):
        page_no = idx + 1
        if wanted and page_no not in wanted:
            continue
        page_count += 1
        page_sub = pages_dir / f"page_{page_no:03d}"
        page_sub.mkdir(exist_ok=True)
        res.save_to_json(save_path=str(page_sub))
        res.save_to_markdown(save_path=str(page_sub))

        # 找到该页生成的 md 与 imgs，把图片复制到总 imgs/ 并改写引用路径
        md_files = list(page_sub.glob("*.md"))
        if not md_files:
            continue
        md_text = md_files[0].read_text(encoding="utf-8")

        def move_img(m):
            src = m.group(1)
            src_path = (page_sub / src).resolve()
            if not src_path.exists():
                return m.group(0)
            new_name = f"p{page_no:03d}_{src_path.name}"
            shutil.copy2(src_path, imgs_dir / new_name)
            return m.group(0).replace(src, f"imgs/{new_name}")

        md_text = re.sub(r'<img src="([^"]+)"', move_img, md_text)
        md_text = re.sub(r'!\[[^\]]*\]\(([^)]+)\)', lambda m: m.group(0).replace(m.group(1), f"imgs/p{page_no:03d}_{Path(m.group(1)).name}"), md_text)
        md_parts.append(f"<!-- ===== 第 {page_no} 页 ===== -->\n\n{md_text.strip()}")
        print(f"  第 {page_no} 页完成")

    merged = "\n\n".join(md_parts) + "\n"
    merged_path = out_dir / f"{doc_name}.md"
    merged_path.write_text(merged, encoding="utf-8")

    n_imgs = len(list(imgs_dir.glob("*")))
    print(f"[2/2] 完成: {page_count} 页, {n_imgs} 张裁剪图")
    print(f"  Markdown: {merged_path}")
    print(f"  图片目录: {imgs_dir}")
    print(f"  逐页JSON: {pages_dir}")


if __name__ == "__main__":
    main()

# 输出格式参考

## 目录结构

```
<名字>_parsed/
├── <名字>.md            # 合并全文 Markdown，图在原位引用 imgs/ 下的切割图
├── imgs/                # 切割图，命名 p<页码>_<类型>_box_<x1>_<y1>_<x2>_<y2>.jpg
└── pages/
    └── page_001/
        ├── <名字>_0.md        # 该页 Markdown
        ├── <名字>_0_res.json  # 该页完整 JSON（含逐字检测框与置信度）
        └── imgs/              # 该页原始切割图
```

## 块结构（parsing_res_list）

```json
{
  "block_label": "chart",
  "block_content": "...OCR 文本...",
  "block_bbox": [240, 67, 979, 1027],
  "block_order": null
}
```

- `block_bbox`：页面像素坐标 `[x1, y1, x2, y2]`，可用于从整页渲染图手动补切。
- `block_order`：阅读顺序序号；`null` 表示该块不进正文流（图表、图题、页眉页脚等）。

## label 词汇表

| label | 含义 | 进 Markdown |
|---|---|---|
| doc_title / paragraph_title | 文档标题 / 段落标题 | 是，# / ## |
| text | 正文段落 | 是 |
| image / chart | 插图 / 统计图表 | 是，图片引用 |
| figure_title | 图题/表题 | 是，跟在图后 |
| table | 表格 | 是，HTML table |
| formula / formula_number | 公式（LaTeX）/ 编号 | 是 |
| header / footer / number / footnote / aside_text | 页眉/页脚/页码等 | 默认忽略 |
| reference | 参考文献条目 | 是 |
| seal | 印章 | 视开关 |

## 二次加工建议

- 找某图：用 `figure_title` 的文本定位页码，再看同页 `chart`/`image` 块的 bbox 与 imgs/ 文件名中的坐标对应。
- 补切漏检图：用整页渲染图（`pages/page_*/` 同级或重新渲染 PDF 该页）按 bbox 裁剪。
- 重建引用关系：`chart` 块与最近的 `figure_title` 块通常同页相邻，bbox 的 y 坐标紧邻。

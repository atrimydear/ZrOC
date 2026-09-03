# -*- coding: utf-8 -*-
r"""从 main.bbl 中剔除 "DOI: \doi{...}" 行。

背景：gbt7714 v2.1.8 + natbib(bibtex) 路径下 \usepackage[doi=false]{gbt7714}
选项已失效（未知选项被转发给 natbib 报错），而 bst 的 show.doi 写死为真，
因此改用本脚本在 bibtex 之后、xelatex 之前清理 bbl。

字节级处理：不读入文本、不解码，保持 bbl 原有编码（UTF-8/GBK 均安全）。

用法: python strip_doi.py [main.bbl]     # 缺省文件为当前目录 main.bbl
"""
import sys
from pathlib import Path

target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("main.bbl")
if not target.exists():
    print(f"strip_doi: {target} not found, skip")
    sys.exit(0)

raw = target.read_bytes()
lines = raw.split(b"\n")
kept = [ln for ln in lines if b"DOI: \\doi{" not in ln]
removed = len(lines) - len(kept)
target.write_bytes(b"\n".join(kept))
print(f"strip_doi: removed {removed} DOI line(s) from {target.name}")

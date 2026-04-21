# 大创结题报告（高温红外屏蔽材料）

本目录为独立 LaTeX 工程，结构参考现有项目，适用于“材料专业-高温红外屏蔽材料”方向的大创结题文档。

## 目录结构

- `main.tex`：主入口文件
- `premble/premble.tex`：公共导言区
- `menu/menu.tex`：章节汇总入口
- `maintext/*.tex`：各章节正文
- `referrence.bib`：参考文献
- `picture/`：图片目录
- `tools/`：辅助脚本目录（预留）

## 编译方式

推荐使用 XeLaTeX + BibTeX：

1. `xelatex main.tex`
2. `bibtex main`
3. `xelatex main.tex`
4. `xelatex main.tex`

## 使用说明

- 章节内容已按结题模板预填充示例文本。
- 带“待填写”的字段请替换为真实信息。
- 表格中的示例数据用于排版占位，建议按实验结果更新。

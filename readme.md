# 实验计划（ZrOC 大创项目）

> **一句话定位**：一个基于 ZrOC（SiZrOC）的大创项目工作区，目标是制备耐高温、强电磁吸收的纤维材料；本目录是该项目的 LaTeX 写作工程，承载从实验日志、文献综述到结题报告的全部文字材料与原始图像。

| 类别 | 位置 | 内容说明 |
|------|------|----------|
| 主报告工程 | `main.tex` + `premble/` + `menu/` | ctexbook 长文档，`xelatex` 编译，正文按章装配 |
| 正文素材 | `maintext/` | 文献综述、一/二/三阶段实验日志与总结 |
| 原始图像 | `picture/` | 按日期归档的 SEM 图（tif/jpg）、XPS 谱图、分析图（png） |
| 数据文件 | `csv/` | 实验数据（**需授权后访问**，见红线） |
| 参考文献 | `referrence.bib` / `referrence2.bib` / `SiZrOC.bib` | gbt7714 格式文献库 |
| AI 协作痕迹 | `ai-blueprint.md`、`deepseek_markdown_*.md` | 改造规划、AI 草稿（后者已 gitignore） |
| 成稿产物 | `main.pdf` 及各类 `.aux/.log/.bbl` | 编译生成，勿手工编辑 |

---

## 目录结构详解

```
实验计划/
├── main.tex                        # 总入口：ctexbook，frontmatter + menu + 参考文献
├── premble/premble.tex             # 宏包与页面设置（含 gbt7714[doi=false]）
├── menu/menu.tex                   # 章节装配：4 章，逐条 \input 各日志（新增日志要在此登记）
├── maintext/                       # 正文内容
│   ├── README.md                   # 实验日志文件夹使用说明（作者手写）
│   ├── 文献综述/                   # 第 1 章素材
│   │   ├── 实现工艺汇总.tex        #   制备工艺综述（IHPFs 等，用 \ce{} 化学式）
│   │   ├── EAB.tex                 #   吸波性能对比大表（厚度/RL/EAB/文献引用）
│   │   └── 学界努力.tex            #   同体系改进方向综述
│   ├── 一阶段实验文件/             # 第 2 章
│   │   ├── 一阶段实验总结.tex      #   可控参数、改良措施、计划表（\paragraph/\section 混用）
│   │   └── 实验日志/               #   0321改良效果 / 0401效果 / 0522xrd / 0610实验数据
│   ├── 二阶段实验日志/             # 第 3 章：日期化日志 20260314.tex ~ 20260627.tex
│   │   ├── 总结.tex                #   二阶段课程报告正文（引言/设计/结果/结论）
│   │   ├── 一阶段-daily-log-template.tex  # 独立 ctexart 模板（封面+报告+日记）
│   │   ├── daily-log-template.pdf  #   模板编译产物
│   │   └── 2026                    #   0 字节空文件（疑似误建，可清理）
│   └── 三阶段实验日志/             # 第 4 章
│       ├── 20260711.tex            #   单页实验计划（独立 ctexart，单独编译，含 .pdf/.log）
│       └── README.tex              #   0712 新实验室实验流程手写计划
├── picture/                        # 图像库，\graphicspath 已指向此处
│   ├── 0321/ 0401/ 20260423/ 20260615/   # 按日期归档：SEM 图（tif/jpg）+ 仪器元数据（.txt）
│   ├── 1/ 2/ 3/                    #   XPS 谱图（各含 Zr3d/Si2p/O1s/C1s.png），计划并入 0610/
│   └── *纤维直径高斯分布统计0401.png、0401样品RL系数.png 等  # 待归类的分析图（见 move_files.bat）
├── csv/                            # 数据文件（PVP_random_4000_2026-06-15.csv）——需授权访问
├── referrence.bib / referrence2.bib / SiZrOC.bib   # 文献库（referrence2.bib 为 GBK 编码）
├── ai-blueprint.md                 # AI 协作规划：menu.tex 增章 + DOI 移除 + referrence2 规范化（已执行）
├── deepseek_markdown_20260420_*.md # AI 生成的结题报告草稿（已 gitignore）
├── move_files.bat                  # 图片整理脚本（注意其中盘符是 w:\，执行前须改成本机路径）
├── main.pdf / main.aux / main.log / main.toc / main.bbl ...  # 主报告编译产物
├── README.md / LICENSE / .gitignore / .vscode/   # 本说明、协议、git 忽略规则、编辑器配置
```

**双层结构**：本工作区是一个"原始资料 → 日志 → 提炼"的流水线——

- **原始层**：`picture/` 原始图像与仪器元数据、`csv/` 数据、日志中记录的当日操作。
- **提炼层**：`文献综述/`（研究现状）、`一阶段实验总结.tex`、二阶段 `总结.tex`、AI 结题报告草稿，最终汇入 `main.pdf`。

---

## 编辑思路（推断）

> ⚠️ 以下基于目录结构与文件内容推断，**非作者手写**，请作者复核。

- **日期化命名 + 阶段划分**：日志统一为 `YYYYMMDD.tex`（一阶段为 `MMDD+主题`），按 一阶段 → 二阶段 → 三阶段 分目录推进；实验内容随日期自然归档。
- **当日日志 → 阶段总结**：每日操作先记单日日志，阶段末汇总成总结（一阶段实验总结、二阶段 `总结.tex` 与课程报告模板互为镜像，正文几乎同文）。
- **双轨文档**：主报告（ctexbook 长文档，`main.tex` 一入口）与独立单页文档（课程报告模板、`20260711.tex` 实验计划）各自独立编译，互不依赖。
- **图片按日期归档**：SEM 图存入 `picture/日期/`，tif 保留配套仪器元数据 txt；`move_files.bat` 规划了把散落分析图移入 `0401/`、`0522/`、`0610/`（脚本路径为 `w:\` 盘，本机尚未执行）。
- **AI 辅助工作流**：改造前先写 `ai-blueprint.md` 规划 → 执行 → 编译验证；AI 生成草稿（`deepseek_markdown_*.md`）进 gitignore，与手写文件隔离。`ai-blueprint.md` 中的三项任务（menu.tex 增章、DOI 移除、referrence2 规范化）已全部落地，且二阶段章节已扩展至 20260627 + 总结、新增三阶段章节。
- **参考文献规范化**：gbt7714 数值引用 + `doi=false` 抑制 DOI 打印；DOI 统一为 `10.xxx/...` 格式。
- **近期活跃方向**（截至 2026-07）：三阶段实验启动——新实验室静电纺丝（"夹心饼干"三层叠层，PVP/葡萄糖/正丙醇锆调配）、烧结（理学楼 227，梯度升温至 900°C）、SEM 检测（杜斌老师）；此前完成了设备搬迁（107 实验室 → 创新大楼 A 座 201）与电气接地保障。

---

## 写作指南

### 1. 新增一篇实验日志（主报告内）

1. 在 `maintext/二阶段实验日志/`（或 `三阶段实验日志/`）新建 `YYYYMMDD.tex`，用中文叙述当日操作、结果、问题。
2. 需要图表时按如下模式（`\graphicspath` 已指向 `picture/`，直接写子目录相对路径）：

   ```latex
   \begin{figure}[H]
       \centering
       \begin{subfigure}[b]{0.48\textwidth}
           \includegraphics[width=\textwidth]{20260615/IMG_xxx.jpg}
           \caption{……}
           \label{fig:xxxa}
       \end{subfigure}
       \hfill
       \begin{subfigure}[b]{0.48\textwidth}
           \includegraphics[width=\textwidth]{20260615/IMG_yyy.jpg}
           \caption{……}
           \label{fig:xxxb}
       \end{subfigure}
       \caption{……}
   \end{figure}
   ```

3. 在 `menu/menu.tex` 对应章节末尾追加一行 `\input{maintext/二阶段实验日志/YYYYMMDD.tex}`。
4. 编译：`xelatex main.tex` → `bibtex main` → `xelatex main.tex` → `xelatex main.tex`，检查 `main.pdf`。

### 2. 新增图片 / 数据

- 图片放进 `picture/日期/` 子目录；SEM 原始 tif 与仪器元数据 txt 成对保留，勿改名；分析图（png）用日期化描述性命名。
- 数据文件放 `csv/`，命名含日期（如 `PVP_random_4000_2026-06-15.csv`）。

### 3. 新增参考文献

- 写入 `referrence.bib` 或 `referrence2.bib`（后者为 GBK 编码，用对应编码的编辑器）；DOI 用 `10.xxx/...` 格式，不要带 `https://doi.org/` 前缀。
- 引用键风格参考：`hou2017electrospinning`、`ZHANG2022167036`、`RN57`；正文用 `\cite{...}`。
- 若更新吸波性能对比，在 `maintext/文献综述/EAB.tex` 的大表加行。

### 4. 新建独立单页文档（课程报告 / 单日计划）

复制 `maintext/二阶段实验日志/一阶段-daily-log-template.tex` 或 `maintext/三阶段实验日志/20260711.tex` 的 ctexart 骨架（封面、fancyhdr 页眉、enumerate 流程），单独 `xelatex` 编译。

### 5. 新想法 / 改造

- 先写规划文档（如 `ai-blueprint.md` 风格：任务清单 → 涉及文件 → 步骤 → 编译验证），再动手改。
- 大改前确认不影响 `main.tex` 顶层结构。

### 红线

- **数据文件（`csv/` 等）未经作者授权不读取、不分析**，只登记存在。
- 不修改 `picture/` 原始图像与元数据；归类整理用脚本而非手工删改。
- 尊重既有命名（日期化、阶段化）与目录结构，最小化改动。
- `main.pdf` 及 `.aux/.log/.bbl` 等是编译产物，勿手工编辑。

---

## 维护说明

- 本文档在**目录结构发生大改**（新增阶段、重构目录、更换编译流程）后应重新生成。
- 生成依据：目录扫描 + `main.tex`/`menu.tex` 装配关系 + `ai-blueprint.md`/README 等既有文档；"编辑思路"一节为推断内容，如有出入以作者实际流程为准。
- 根目录已配置 git（分支 main），`.gitignore` 忽略 LaTeX 编译产物、`.vscode/` 与 `deepseek_markdown_*.md`。

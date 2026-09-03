# Blueprint：menu.tex 更新 + 参考文献DOI移除

## 架构概览

三项独立任务：

1. **menu.tex 新增「二阶段实验日志」章节**：按日期顺序纳入7篇实验日志（20260314 → 20260615）
2. **移除参考文献中的DOI打印**：通过 `gbt7714` 宏包 `doi=false` 选项全局抑制
3. **（附带）清理 referrence2.bib 中全URL格式的DOI字段**：将 `https://doi.org/...` 规范化为 `10.xxx/...`

## 涉及文件

| 文件 | 操作 |
|------|------|
| [`menu/menu.tex`](menu/menu.tex) | 末尾追加第二章「二阶段实验日志」 |
| [`premble/premble.tex`](premble/premble.tex:17) | 修改 `\usepackage{gbt7714}` → `\usepackage[doi=false]{gbt7714}` |
| [`referrence2.bib`](referrence2.bib) | 将所有 `doi = {https://doi.org/...}` 规范化为 `doi = {10.xxx/...}` |

---

## 实施步骤

### 步骤1：更新 menu.tex — 新增二阶段实验日志章节

- [ ] 在 [`menu.tex`](menu/menu.tex:9) 第9行 `\input{...一阶段实验总结.tex}` 之后追加以下内容：
  ```latex
  \chapter{二阶段实验日志}
  \input{maintext/二阶段实验日志/20260314.tex}
  \input{maintext/二阶段实验日志/20260325.tex}
  \input{maintext/二阶段实验日志/20260326.tex}
  \input{maintext/二阶段实验日志/20260422.tex}
  \input{maintext/二阶段实验日志/20260423.tex}
  \input{maintext/二阶段实验日志/20260426.tex}
  \input{maintext/二阶段实验日志/20260615.tex}
  ```
  各日志内容概览：
  - `20260314` — 新烧结曲线实验（Wang et al. 参考）
  - `20260325` — 葡萄糖引入纳米纤维的尝试方向
  - `20260326` — 首个掺杂葡萄糖样品：强韧性、高透性
  - `20260422` — 3.26a 静置脆化 vs 3.27a 保持柔韧
  - `20260423` — 1350°C 烧结对比，碳化硅特征分析
  - `20260426` — SiOC/ZrO2 梯度优化方案（最终版）
  - `20260615` — 三层结构制备 + subfigure 图片

### 步骤2：全局抑制参考文献DOI输出

- [ ] 修改 [`premble.tex`](premble/premble.tex:17)，将：
  ```latex
  \usepackage{gbt7714}
  ```
  改为：
  ```latex
  \usepackage[doi=false]{gbt7714}
  ```
  效果：`main.bbl` 中所有 `DOI: \doi{...}` 行将不再被输出。

### 步骤3：规范化 referrence2.bib 中的DOI字段

- [ ] 在 [`referrence2.bib`](referrence2.bib) 中将所有 `doi = {https://doi.org/...}` 替换为 `doi = {10.xxx/...}`（去掉 `https://doi.org/` 前缀）。涉及约13处：
  - `https://doi.org/10.1002/adfm.202405643` → `10.1002/adfm.202405643`
  - `https://doi.org/10.1016/j.jmst.2022.07.039` → `10.1016/j.jmst.2022.07.039`
  - `https://doi.org/10.1002/app.38027` → `10.1002/app.38027`
  - `https://doi.org/10.1016/j.jallcom.2017.11.295` → `10.1016/j.jallcom.2017.11.295`
  - `https://doi.org/10.1016/j.ceramint.2018.11.127` → `10.1016/j.ceramint.2018.11.127`
  - `https://doi.org/10.1016/j.jallcom.2022.167036` → `10.1016/j.jallcom.2022.167036`
  - `https://doi.org/10.1016/j.jmat.2022.11.001` → `10.1016/j.jmat.2022.11.001`
  - `https://doi.org/10.1016/j.matlet.2024.136442` → `10.1016/j.matlet.2024.136442`
  - `https://doi.org/10.1016/j.jmat.2024.100988` → `10.1016/j.jmat.2024.100988`
  - `https://doi.org/10.1016/j.apsusc.2025.164079` → `10.1016/j.apsusc.2025.164079`
  - `https://doi.org/10.1016/j.compositesb.2025.112628` → `10.1016/j.compositesb.2025.112628`
  - `https://doi.org/10.1016/j.surfin.2024.104818` → `10.1016/j.surfin.2024.104818`
  - `https://doi.org/10.1016/j.cej.2020.128304` → `10.1016/j.cej.2020.128304`

### 步骤4：编译验证

- [ ] 执行 `xelatex main.tex` + `bibtex main` + `xelatex main.tex` + `xelatex main.tex` 完整编译流程
- [ ] 确认 PDF 中参考文献列表不再出现 `DOI:` 字样
- [ ] 确认第二章「二阶段实验日志」正确渲染

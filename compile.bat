@echo off
rem ============================================================
rem  一键编译 main.pdf（xelatex + bibtex + 去DOI + 再编译两遍）
rem  用法: 双击 compile.bat；脚本调用加参数 nopause（不暂停）
rem ============================================================
cd /d "%~dp0"

rem --- 定位 python（去 DOI 脚本用）---
set "PY=D:\Knowledge\LaTeX\conda_env\python.exe"
if not exist "%PY%" set "PY=C:\Users\ATRI\.dsh\skills\pdf-to-markdown\.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo [ERROR] python not found, strip_doi.py skipped
    set "PY="
)

echo [1/5] xelatex (pass 1) ...
xelatex -interaction=nonstopmode -file-line-error main.tex
if errorlevel 1 echo [WARN] xelatex pass 1 returned errors

echo [2/5] bibtex ...
bibtex main

echo [3/5] strip DOI from main.bbl ...
if defined PY "%PY%" strip_doi.py main.bbl

echo [4/5] xelatex (pass 2) ...
xelatex -interaction=nonstopmode -file-line-error main.tex

echo [5/5] xelatex (pass 3) ...
xelatex -interaction=nonstopmode -file-line-error main.tex

echo.
echo Done. main.pdf updated.
if /i not "%1"=="nopause" pause

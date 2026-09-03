@echo off
chcp 65001 >nul
cd /d "w:\LaTeX\实验计划"

:: 0401 remaining png files
move "picture\1-2纤维直径高斯分布统计0401.png" "picture\0401\"
move "picture\1-7纤维直径高斯分布统计0401.png" "picture\0401\"
move "picture\2-3纤维直径高斯分布统计0401.png" "picture\0401\"
move "picture\2-11纤维直径高斯分布统计0401.png" "picture\0401\"
move "picture\0401样品RL系数.png" "picture\0401\"

:: 0522
move "picture\folder1.png" "picture\0522\"

:: 0610 - move entire subdirectories
move "picture\1" "picture\0610\"
move "picture\2" "picture\0610\"
move "picture\3" "picture\0610\"

echo All moves completed.

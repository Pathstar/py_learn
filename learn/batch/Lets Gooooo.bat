@echo off
setlocal enabledelayedexpansion

::set /p confirm=Let's Go?:
echo Let's Go?:
set /p confirm=
set "noSpaceConfirm=%confirm: =%"
set "prefix=!noSpaceConfirm:~0,5!"
set "suffix=!noSpaceConfirm:~5!"
set "test=!suffix:o=!"
:: /i 忽略大小写
if /i "%prefix%"=="letsg" (
if "!test!"=="" (
    shutdown /s /f /t 0
    :loop
    echo Let's G%suffix%!!!!!!!!!!
    set /a rand=%random% %% 10
    if !rand! equ 0 (
        rem 再生成0或1决定o/O
        set /a oo=%random% %% 2
        if !oo! equ 0 (
            set suffix=!suffix!o
        ) else (
            set suffix=!suffix!O
        )
    )
    goto loop
) else (
    echo Can't Let Go...
    pause
)
) else (
    echo Can't Let Go...
    pause
)
pause

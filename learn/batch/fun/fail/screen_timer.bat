
@REM 写脚本 输入一串用空格隔开的数字 例如 1 2 3 4 5 效果为：1分钟后息屏 2分钟后亮起 3分钟后息屏 4分钟后亮起，5分钟之后息屏 参数可以为1-无数个，可能带有小数，如果变为秒数后仍有小数，则舍弃 息屏使用nircmd.exe monitor off
@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
rem Check parameters
if "%~1"=="" (
    echo Usage: %~nx0 1 2.5 3.1 4 5
    echo Each number means how many minutes later to toggle (off/on)
    goto :eof
)
rem Operation index: 1=off, 2=on, 3=off, 4=on...
set /a idx=0
for %%i in (%*) do (
    set /a idx+=1
    set minute=%%i
    rem Calculate integer part of minutes
    for /f "tokens=1 delims=." %%s in ("!minute!") do set min_int=%%s
    set secstr=0.!minute!
    set dec=0
    rem Extract decimal part
    for /f "tokens=1,2 delims=." %%a in ("!minute!") do set dec=%%b
    if "!dec!"=="" (set dec=0)
    set /a total_sec=!min_int!*60+(!dec!0)
    rem Keep integer seconds only
    set /a total_sec=!min_int!*60
    rem Display tip
    if !idx! lss 10 (set idxtxt=0!idx!) else (set idxtxt=!idx!)
    set operation=Turn off monitor
    set nircmd_op=monitor off
    if !idx! neq 1 (
        set /a m=!idx!%%2
        if !m! equ 0 (
            set operation=Turn on monitor
            set nircmd_op=sendkeypress ctrl
        ) else (
            set operation=Turn off monitor
            set nircmd_op=monitor off
        )
    )
    echo ^>^>^> Waiting for !minute! minutes (!total_sec! seconds), will perform [!operation!]...
    timeout /t !total_sec! /nobreak >nul
    nircmd.exe !nircmd_op!
    echo [!operation!] executed
)
echo All operations completed!
pause
::exit /b
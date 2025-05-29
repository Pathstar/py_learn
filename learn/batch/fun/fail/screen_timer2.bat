@echo off
setlocal enabledelayedexpansion
echo.
set /p input=Please enter minutes (separated by spaces):
if "%input%"=="" (
    echo No input received.
    pause
    exit /b
)
rem Check if nircmd.exe is present
if not exist "nircmd.exe" (
    echo nircmd.exe not found! Please put it in the script folder.
    pause
    exit /b
)
set /a idx=0
for %%t in (%input%) do (
    set /a idx+=1
    rem Check if the input is a number
    set "minutes=%%t"
    set /a check_minutes=!minutes!+0 2>nul
    if "!check_minutes!" NEQ "!minutes!" (
        echo Warning: skipped invalid input: "%%t"
        goto :continue
    )
    set /a seconds=!minutes!*60
    if !seconds! lss 1 (
        set seconds=1
    )
    set /a mod=!idx!%%2
    if !mod! EQU 1 (
        set "action=Turn off monitor"
        echo Step !idx!: Waiting !minutes! minute(s) (!seconds! seconds)...
        timeout /t !seconds! /nobreak
        nircmd.exe monitor off
        echo [Monitor turned off]
    ) else (
        set "action=Wake up monitor by moving mouse"
        echo Step !idx!: Waiting !minutes! minute(s) (!seconds! seconds)...
        timeout /t !seconds! /nobreak
        nircmd.exe movecursor 1 0
        nircmd.exe movecursor -1 0
        echo [Monitor woken up]
    )
    :continue
)
echo.
echo All steps finished.
pause
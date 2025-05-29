@echo off
for /f "skip=1 tokens=2 delims=," %%a in ('wmic process where "name='wscript.exe' or name='cscript.exe'" get CommandLine^,ProcessId /format:csv') do (
    echo %%a | find /i "refresh_webAI.vbs" >nul
    if not errorlevel 1 (
        for /f %%b in ("%%a") do (
            echo 正在终止refresh_webAI.vbs进程 PID: %%b
            taskkill /pid %%b /f
        )
    )
)
pause
@echo off
set /p minutes=fake min: 
for /f "delims=0123456789" %%i in ("%minutes%") do (
    echo not number
    pause
    exit /b
)
set /a seconds=%minutes%*60
echo %minutes%min close windows
timeout /t %seconds% /nobreak
echo close...
shutdown /s /f /t 0
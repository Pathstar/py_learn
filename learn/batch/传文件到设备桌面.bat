@echo off
setlocal enabledelayedexpansion
for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set "datetime=%%a"
:: Format: yyyyMMddHHmmss.SSS
set "timestamp=!datetime:~0,8!!datetime:~86!!datetime:~15,3!"
set "tmpdir=D:\garbages\history\bat history"
if not exist "!tmpdir!" md "!tmpdir!"
set "tmpfile=!tmpdir!\!timestamp!.txt"
set /p file_path=Input file path: 
hdc file send "%file_path%" /data/service/el2/100/hmdfs/account/files/Docs/Desktop/ > "!tmpfile!" 2>&1
type "!tmpfile!"
findstr /C:"[Fail]Error opening file: no such file or directory" "!tmpfile!" >nul
if not errorlevel 1 (
    set /p num=Input number:
    hdc file send "%file_path%" /data/service/el2/10!num!/hmdfs/account/files/Docs/Desktop/
)
del "!tmpfile!"
pause
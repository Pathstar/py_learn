@echo off
setlocal enabledelayedexpansion
for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set "datetime=%%a"
set /p file_path=input file path: 
set "timeuwu=tmp_result!datetime:~15,3!"
hdc file send "%file_path%" /data/service/el2/100/hmdfs/account/files/Docs/Desktop/ > !timeuwu!.txt 2>&1
type !timeuwu!.txt
findstr /C:"[Fail]Error opening file: no such file or directory" !timeuwu!.txt >nul
if not errorlevel 1 (
    ::echo Upload failed, directory not found. Please input the target number:
    set /p num=Input number:
    hdc file send "%file_path%" /data/service/el2/10!num!/hmdfs/account/files/Docs/Desktop/
) 
::else (

::)
del !timeuwu!.txt
pause



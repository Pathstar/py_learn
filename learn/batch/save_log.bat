@echo off
setlocal enabledelayedexpansion
set /p key=input:

for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set "datetime=%%a"
set "timename=!datetime:~4,2!.!datetime:~6,2! !datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!"
set filename=%timename% %key%.txt
::set "batpath=%~dp0"
set "batpath=D:\garbages\history\"
echo %batpath%hilog\!filename!
hdc shell hilog -Q pidoff
hdc shell hilog -b D
if "!key!"=="" (
    hdc shell hilog > "!batpath!hilog\!filename!"
) else (
    hdc shell "hilog | grep !key!" > "!batpath!hilog\!filename!"
)
pause
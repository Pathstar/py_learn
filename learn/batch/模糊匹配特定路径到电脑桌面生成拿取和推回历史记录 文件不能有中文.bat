@echo off
setlocal enabledelayedexpansion
set /p "file_path=Enter the path: "
set /p "file_name=Enter the file name to search: "
set "remote_path=%file_path%/"
::set "remote_path=data/service/el2/100/hmdfs/account/files/Docs/Desktop/"

::set "local_path=C:\Users\kwx1412683\Desktop\"
set "script_dir=D:\garbages\history\"
set "local_path=%script_dir%HarmonyFile\"
if not exist "%local_path%" (
    mkdir "%local_path%"
    echo Created directory: %local_path%
)

set file_count=1
set file_send_count=1
echo Searching for matching files...
for /f "delims=" %%F in ('hdc shell ls "%remote_path%" ^| findstr /i "%file_name%"') do (
    set "filename=%%F"
    echo Found matching file: !filename!
    echo Transferring...
    for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set "datetime=%%a"
    set "timename=!datetime:~4,2!.!datetime:~6,2! !datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!"
    hdc file recv "%remote_path%!filename!" "%local_path%!filename!"
    (
    echo @echo off
    echo hdc file recv "%remote_path%!filename!" "%local_path%"
    echo pause
    ) > "bat history\recv_!timename!_!filename!_!file_count!.bat"
    
    (
    echo @echo off
    echo hdc target mount
    echo hdc file send  "%local_path%!filename!" "%remote_path%" 
    echo pause
    ) > "D:\garbages\history\bat history\r_send_!timename!_!filename!_!file_send_count!.bat"
    set /a file_count+=1
    set /a file_send_count+=1
)
if !file_count! == 0 (
    echo No files containing "%file_name%" were found
) else (
    echo Successfully transferred !file_count! files to desktop
)
pause
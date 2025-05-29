@ECHO OFF

echo 1: Video, 2:Photo, 3:Both


:MENU

set /p userinput=
::set /p input_user=
::set /a user = 10%input_user%
::if "%input_user%"=="" user = 100
set "user=100"
set "choice="

::echo user number: 

rem 去除前后空格
for /f "tokens=1,2" %%a in ("%userinput%") do (
    set "choice=%%a"
    if not "%%b"=="" (
        set "user=10%%b"
    )
)
echo /storage/media/%input_user%
if "%choice%"=="1" goto get_mp4
if "%choice%"=="2" goto get_jpg
if "%choice%"=="3" goto get_all
echo invalid number
goto MENU

:get_mp4
set /a tm1=%time:~0,2%*1
set Folder="D:\garbages\history\Video\%date:~5,2%.%date:~8,2% %tm1%.%time:~3,2%.%time:~6,2% %date:~0,4%"

set LOCAL_LOG_DIR=%Folder%
echo LOCAL_LOG_DIR=%Folder%
MKDIR %LOCAL_LOG_DIR%
if %tm1% LSS 10 set tm1=0%tm1%

for /f %%i in ('hdc shell "find /storage/media/%user%/local/files/Photo -name *.mp4"') do (
    echo "%%i"
    hdc file recv %%i %LOCAL_LOG_DIR%
)
pause
goto end


:get_jpg
set /a tm1=%time:~0,2%*1
set Folder="D:\garbages\history\Video\%date:~5,2%.%date:~8,2% %tm1%.%time:~3,2%.%time:~6,2% %date:~0,4%"

set LOCAL_LOG_DIR=%Folder%
echo LOCAL_LOG_DIR=%Folder%
MKDIR %LOCAL_LOG_DIR%
if %tm1% LSS 10 set tm1=0%tm1%
set Folder="D:\garbages\history\Video\%date:~5,2%.%date:~8,2% %tm1%.%time:~3,2%.%time:~6,2% %date:~0,4%"

set LOCAL_LOG_DIR=%Folder%
echo LOCAL_LOG_DIR=%Folder%
for /f %%i in ('hdc shell "find /storage/media/100/local/files/Photo -name *.jpg"') do (
    echo "%%i"
    hdc file recv %%i %LOCAL_LOG_DIR%
)
pause
goto end


:get_all
set /a tm1=%time:~0,2%*1
set Folder="D:\garbages\history\Video\%date:~5,2%.%date:~8,2% %tm1%.%time:~3,2%.%time:~6,2% %date:~0,4%"

set LOCAL_LOG_DIR=%Folder%
echo LOCAL_LOG_DIR=%Folder%
MKDIR %LOCAL_LOG_DIR%\Screenhot
MKDIR %LOCAL_LOG_DIR%\Record

if %tm1% LSS 10 set tm1=0%tm1%
set Folder="D:\garbages\history\Video\%date:~5,2%.%date:~8,2% %tm1%.%time:~3,2%.%time:~6,2% %date:~0,4%"

set LOCAL_LOG_DIR=%Folder%
echo LOCAL_LOG_DIR=%Folder%
for /f %%i in ('hdc shell "find /storage/media/100/local/files/Photo -name *.jpg"') do (
    echo "%%i"
    hdc file recv %%i %LOCAL_LOG_DIR%\Screenhot
)
for /f %%i in ('hdc shell "find /storage/media/100/local/files/Photo -name *.mp4"') do (
    echo "%%i"
    hdc file recv %%i %LOCAL_LOG_DIR%\Record
)
pause
:end

pause


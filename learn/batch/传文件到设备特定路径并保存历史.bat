@echo off
setlocal enabledelayedexpansion
:: 获取文件路径
set /p file_path=--Enter PC file path: 
for %%F in ("%file_path%") do set "filepath_name=%%~nxF"
set /p "device_path=--Enter the device folder path: "
:: 执行文件传输
hdc target mount
hdc file send "%file_path%" "%device_path%"
:: 生成时间戳文件名
for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set "datetime=%%a"
set "filename=!datetime:~4,2!.!datetime:~6,2! !datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!"
:: 保存到历史记录
(
  echo @echo off
  echo hdc target mount
  echo hdc file send "%file_path%" "%device_path%"
  echo pause
) > "D:\garbages\history\bat history\send_file_!filename!_!filepath_name!.bat"
echo Saved to: bat history\send_file_!filename!_!filepath_name!.bat
endlocal
pause
@echo off
set "batpath=%~dp0"
hdc file send %batpath%text.txt /data/service/el2/100/hmdfs/account/files/Docs/Desktop/
echo hdc file send %batpath%\text.txt /data/service/el2/100/hmdfs/account/files/Docs/Desktop/
::pause
timeout /t 5 /nobreak
exit
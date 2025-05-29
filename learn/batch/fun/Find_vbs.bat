wmic process where "name='wscript.exe' or name='cscript.exe'" get ProcessId,CommandLine
::taskkill /pid 3572 /f
::taskkill /im wscript.exe /f
pause

@echo off
set /p filter=input:
hdc shell hilog -b D
hdc shell hilog -Q pidoff
hdc shell hilog -Q domainoff
hdc shell hilog -G 512M

hdc shell hilog -b I
hdc shell hilog -b D -D 0xD001317
hdc shell "hilog | grep '%filter%'"
pause
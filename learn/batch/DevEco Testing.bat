@echo off

hdc target mount
start "" "D:\SoftXD\DevEcoTesting\bin\DevEco Testing.exe"
choice /t 12 /d N /m "choice: "
if errorlevel 2 (
    echo Out Time
    exit /b
)

(
    echo 6240Xiao_dao
) | clip
timeout /t 2 /nobreak
(
    echo kwx1412683
) | clip
::echo Copy
::timeout /t 8 /nobreak

::set /p answer=Enter: 
::echo Input: %answer%
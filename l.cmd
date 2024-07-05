@echo off

REM 检查 Python 是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not added to system PATH.
    exit /b 1
)

REM 检查参数是否为空
if "%~1"=="" (
    echo Usage: %0 [option]
    exit /b 1
)

REM 调用 Python 脚本并传递参数
python %~dp0\copilot.py %*

REM 结束脚本
exit /b

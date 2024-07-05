@echo off
setlocal

rem 检查是否已经存在 COPILOT_HOME 环境变量
if defined COPILOT_HOME (
    echo COPILOT_HOME path variable has existed, value: %COPILOT_HOME%
) else (
    rem 获取当前目录的绝对路径
    for %%A in ("%~dp0.") do set "COPILOT_HOME=%%~fA"

    rem 更新 PATH 环境变量
    set "PATH=%COPILOT_HOME%;%PATH%"

    rem 输出配置信息
    echo work copilot set up successfully~
    echo COPILOT_HOME=%COPILOT_HOME%
    echo PATH=%PATH%
)

endlocal

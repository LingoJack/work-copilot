#!/bin/bash

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not added to system PATH."
    exit 1
fi

# 检查参数是否为空
if [ -z "$1" ]; then
    echo "Usage: $0 [option]"
    exit 1
fi

# 调用 Python 脚本并传递参数
python3 "$(dirname "$0")/copilot.py" "$@"

# 结束脚本
exit 0

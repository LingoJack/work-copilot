#!/bin/bash

# 检查是否已经存在 COPILOT_HOME 环境变量
if [ -n "$COPILOT_HOME" ]; then
    echo "COPILOT_HOME 环境变量已存在。当前值为: $COPILOT_HOME"
else
    # 获取当前目录的绝对路径
    COPILOT_HOME=$(cd "$(dirname "$0")" && pwd)

    # 更新 PATH 环境变量
    export PATH="$COPILOT_HOME:$PATH"
    export COPILOT_HOME="$COPILOT_HOME"

    # 输出配置信息
    echo "work copilot set up successfully~"
    echo "COPILOT_HOME=$COPILOT_HOME"
    echo "PATH=$PATH"
fi

# 创建别名
AK_SCRIPT="$(pwd)/ak.sh"
if [ ! -f "$AK_SCRIPT" ]; then
    echo "ak.sh 脚本不存在，请确保在当前目录下存在该脚本。"
    exit 1
fi

if ! grep -q "alias ak='$AK_SCRIPT'" ~/.bashrc; then
    echo "alias ak='$AK_SCRIPT'" >> ~/.bashrc
    echo "别名已创建。"
else
    echo "别名已经存在。"
fi

# 更新bash配置
source ~/.bashrc

exit 0

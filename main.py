#!/usr/bin/env python3
"""
Canvas Agent 项目总入口

用于直接运行Canvas智能课件生成系统
"""

import sys
import os

# 添加项目路径到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from canvas_agent.main import main

if __name__ == "__main__":
    main()
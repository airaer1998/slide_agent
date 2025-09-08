"""
Canvas Agent: 智能课件生成 Agent

基于 LangGraph 构建的自动化课件生成系统，支持：
- 结构化大纲生成
- 用户交互式审核
- 批量/交互式内容生成
- Moffee Markdown 格式输出
"""

from .workflow import create_canvas_workflow, run_canvas_workflow, get_workflow_visualization
from .utils.state import GraphState, SlideOutline

__version__ = "1.0.0"
__author__ = "Canvas Agent Team"

__all__ = [
    "create_canvas_workflow",
    "run_canvas_workflow", 
    "get_workflow_visualization",
    "GraphState",
    "SlideOutline"
]
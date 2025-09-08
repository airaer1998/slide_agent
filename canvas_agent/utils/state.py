from typing import List, Dict, Literal, TypedDict, Optional


class SlideOutline(TypedDict):
    """单页幻灯片的结构化大纲"""
    page: int
    content: str


class GraphState(TypedDict):
    """整个工作流的状态"""
    # 初始输入
    original_query: str
    slide_count: int

    # 大纲阶段
    outline: List[SlideOutline]

    # 模式与规则
    generation_mode: Literal["batch", "interactive"]
    rules: str

    # 交互模式专用状态
    generated_slides: List[str]  # 存储已生成的 Markdown 页面
    current_slide_index: int     # 当前正在处理的页面索引
    user_feedback: str           # 用户本轮的修改意见
    
    # 工作流控制
    outline_approved: bool       # 大纲是否已审核通过
    final_slides_path: str       # 最终输出文件路径
    is_command_line_mode: bool   # 是否为命令行模式
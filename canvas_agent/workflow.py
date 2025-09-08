from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .utils.state import GraphState
from .nodes.user_input_parser import user_input_parser
from .nodes.outline_generator import outline_generator
from .nodes.user_approval import wait_for_user_approval
from .nodes.mode_selector import select_mode, should_use_interactive_mode
from .nodes.rule_engine import rule_engine
from .nodes.batch_generator import batch_slide_generator
from .nodes.interactive_generator import interactive_slide_generator


def create_canvas_workflow():
    """
    创建Canvas课件生成工作流图
    """
    # 创建StateGraph
    workflow = StateGraph(GraphState)
    
    # 添加节点
    workflow.add_node("user_input_parser", user_input_parser)
    workflow.add_node("outline_generator", outline_generator)
    workflow.add_node("wait_for_user_approval", wait_for_user_approval)
    workflow.add_node("select_mode", select_mode)
    workflow.add_node("rule_engine", rule_engine)
    workflow.add_node("batch_slide_generator", batch_slide_generator)
    workflow.add_node("interactive_slide_generator", interactive_slide_generator)
    
    # 设置入口点
    workflow.set_entry_point("user_input_parser")
    
    # 添加边连接
    workflow.add_edge("user_input_parser", "outline_generator")
    workflow.add_edge("outline_generator", "wait_for_user_approval")
    workflow.add_edge("wait_for_user_approval", "select_mode")
    workflow.add_edge("select_mode", "rule_engine")
    
    # 添加条件边：根据模式选择不同的生成器
    workflow.add_conditional_edges(
        "rule_engine",
        should_use_interactive_mode,
        {
            "batch": "batch_slide_generator",
            "interactive": "interactive_slide_generator"
        }
    )
    
    # 设置结束点
    workflow.add_edge("batch_slide_generator", END)
    workflow.add_edge("interactive_slide_generator", END)
    
    # 编译工作流
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app


def run_canvas_workflow(user_query: str, slide_count: int, is_command_line_mode: bool = False):
    """
    运行Canvas工作流
    
    Args:
        user_query: 用户需求描述
        slide_count: 幻灯片页数
        is_command_line_mode: 是否为命令行模式
    """
    # 创建工作流
    app = create_canvas_workflow()
    
    # 初始化状态
    initial_state = {
        "original_query": user_query,
        "slide_count": slide_count,
        "outline": [],
        "generation_mode": "batch",
        "rules": "",
        "generated_slides": [],
        "current_slide_index": 0,
        "user_feedback": "",
        "outline_approved": False,
        "final_slides_path": "final_slides.md",
        "is_command_line_mode": is_command_line_mode
    }
    
    # 配置
    config = {"configurable": {"thread_id": "canvas_workflow_1"}}
    
    try:
        # 运行工作流
        print("[System]: 开始执行Canvas课件生成工作流...")
        final_state = app.invoke(initial_state, config)
        
        print(f"\n[System]: ✅ 工作流执行完成！")
        print(f"[System]: 最终输出文件: {final_state['final_slides_path']}")
        
        return final_state
        
    except Exception as e:
        print(f"[Error]: 工作流执行失败: {str(e)}")
        return None


def get_workflow_visualization():
    """
    获取工作流可视化图
    (需要安装graphviz和pygraphviz)
    """
    try:
        app = create_canvas_workflow()
        
        # 生成mermaid图
        print("工作流结构 (Mermaid格式):")
        print("```mermaid")
        print("graph TD")
        print("    A[用户输入解析] --> B[大纲生成]")
        print("    B --> C[用户审核等待]")
        print("    C --> D[模式选择]")
        print("    D --> E[规则引擎]")
        print("    E --> F{生成模式?}")
        print("    F -->|批量模式| G[批量生成器]")
        print("    F -->|交互模式| H[交互生成器]")
        print("    G --> I[结束]")
        print("    H --> I[结束]")
        print("```")
        
        return True
    except Exception as e:
        print(f"无法生成可视化图: {e}")
        return False
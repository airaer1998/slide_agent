from ..utils.state import GraphState


def select_mode(state: GraphState) -> GraphState:
    """
    模式选择节点
    让用户选择生成模式：批量生成或交互式生成
    """
    # 如果是命令行模式，自动选择批量模式
    if state.get("is_command_line_mode", False):
        state["generation_mode"] = "batch"
        print("[Agent]: 命令行模式，自动选择批量生成模式")
        return state
    
    print("[Agent]: 请选择生成模式:")
    print("[Agent]:   1. 一次性生成 (Batch Mode) - 快速生成所有页面")
    print("[Agent]:   2. 交互模式 (Interactive Mode) - 逐页生成，每页都可修改")
    print("[Agent]:   请输入 1 或 2")
    
    while True:
        user_choice = input("[User]: ").strip()
        
        if user_choice == "1":
            state["generation_mode"] = "batch"
            print("[Agent]: 已选择一次性生成模式")
            break
        elif user_choice == "2":
            state["generation_mode"] = "interactive"
            print("[Agent]: 已选择交互模式")
            break
        else:
            print("[Agent]: 请输入有效选项 (1 或 2)")
    
    return state


def should_use_interactive_mode(state: GraphState) -> str:
    """
    路由决策函数
    根据用户选择的模式决定下一个节点
    """
    if state["generation_mode"] == "interactive":
        return "interactive"
    else:
        return "batch"
from ..utils.state import GraphState


def user_input_parser(state: GraphState) -> GraphState:
    """
    用户输入解析节点
    解析用户的原始输入，包括需求描述和幻灯片页数
    """
    # 初始化状态中的其他字段
    state["outline"] = []
    state["generation_mode"] = "batch"  # 默认模式
    state["rules"] = ""
    state["generated_slides"] = []
    state["current_slide_index"] = 0
    state["user_feedback"] = ""
    state["outline_approved"] = False
    state["final_slides_path"] = "final_slides.md"
    
    # 这里我们假设 original_query 和 slide_count 已经在状态中设置
    # 在实际使用中，这些值会在主程序中通过交互获取
    
    print(f"解析用户需求: {state['original_query'][:100]}...")
    print(f"目标页数: {state['slide_count']}")
    
    return state


def collect_user_input() -> dict:
    """
    收集用户输入的辅助函数
    在命令行界面中与用户交互
    """
    print("[Agent]: 您好！我是您的课件生成助手。")
    print("[Agent]: 请粘贴您的完整需求... (完成后输入 'EOF')")
    
    query_lines = []
    while True:
        line = input()
        if line.strip() == 'EOF':
            break
        query_lines.append(line)
    
    original_query = '\n'.join(query_lines)
    
    while True:
        try:
            slide_count = int(input("[Agent]: 请问您希望生成多少页幻灯片？(1-100): "))
            if 1 <= slide_count <= 100:
                break
            else:
                print("[Agent]: 页数必须在1-100之间，请重新输入。")
        except ValueError:
            print("[Agent]: 请输入有效的数字。")
    
    return {
        "original_query": original_query,
        "slide_count": slide_count
    }
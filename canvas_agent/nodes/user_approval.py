import json
from ..utils.state import GraphState


def wait_for_user_approval(state: GraphState) -> GraphState:
    """
    用户审核等待节点
    等待用户审核大纲并提供修改机会
    """
    # 如果是命令行模式，自动继续
    if state.get("is_command_line_mode", False):
        print("[Agent]: 命令行模式，自动确认大纲...")
        state["outline_approved"] = True
        return state
    
    print("[Agent]: 大纲已生成到 `outline.json`。请修改确认后，输入 'continue' 继续。")
    print("[Agent]: 您可以:")
    print("[Agent]:   1. 直接输入 'continue' 或 'c' 继续")
    print("[Agent]:   2. 编辑 outline.json 文件后再继续")
    print("[Agent]:   3. 输入 'show' 查看当前大纲")
    
    while True:
        user_input = input("[User]: ").strip().lower()
        
        if user_input in ['continue', 'c']:
            # 重新加载可能被用户修改的大纲
            try:
                with open("outline.json", 'r', encoding='utf-8') as f:
                    updated_outline = json.load(f)
                state["outline"] = updated_outline
                state["outline_approved"] = True
                print("[Agent]: 大纲已确认，继续下一步...")
                break
            except FileNotFoundError:
                print("[Agent]: 错误：找不到 outline.json 文件，请确保文件存在。")
                continue
            except json.JSONDecodeError:
                print("[Agent]: 错误：outline.json 文件格式不正确，请检查JSON语法。")
                continue
                
        elif user_input == 'show':
            # 显示当前大纲
            try:
                with open("outline.json", 'r', encoding='utf-8') as f:
                    current_outline = json.load(f)
                print("\n=== 当前大纲 ===")
                for slide in current_outline:
                    print(f"第{slide.get('page', '?')}页: {slide.get('title', '未命名')}")
                    if slide.get('key_points'):
                        for point in slide['key_points'][:3]:  # 显示前3个要点
                            print(f"  - {point}")
                        if len(slide['key_points']) > 3:
                            print(f"  - (还有{len(slide['key_points'])-3}个要点...)")
                print("===============\n")
            except Exception as e:
                print(f"[Agent]: 无法读取大纲文件: {e}")
                
        elif user_input == 'help':
            print("[Agent]: 可用命令:")
            print("[Agent]:   - 'continue' 或 'c': 确认大纲并继续")
            print("[Agent]:   - 'show': 显示当前大纲")
            print("[Agent]:   - 'help': 显示此帮助信息")
            
        else:
            print("[Agent]: 未识别的命令。请输入 'continue'、'show' 或 'help'。")
    
    return state


def reload_outline_from_file(state: GraphState) -> GraphState:
    """
    从文件重新加载大纲的辅助函数
    """
    try:
        with open("outline.json", 'r', encoding='utf-8') as f:
            updated_outline = json.load(f)
        state["outline"] = updated_outline
        print(f"[Agent]: 已重新加载大纲，共{len(updated_outline)}页")
    except Exception as e:
        print(f"[Agent]: 重新加载大纲失败: {e}")
    
    return state
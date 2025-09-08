#!/usr/bin/env python3
"""
Canvas Agent 主程序入口

智能课件生成 Agent 的命令行界面
"""

import sys
import argparse
from typing import Optional

from .nodes.user_input_parser import collect_user_input
from .workflow import run_canvas_workflow, get_workflow_visualization


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(
        description="Canvas Agent - 智能课件生成系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python -m canvas_agent.main                    # 交互式模式
  python -m canvas_agent.main --query "Python教程" --pages 10  # 命令行模式
  python -m canvas_agent.main --show-workflow    # 显示工作流结构
        """
    )
    
    parser.add_argument(
        "--query", "-q",
        help="课件需求描述（如果不提供，将进入交互模式）"
    )
    
    parser.add_argument(
        "--pages", "-p",
        type=int,
        help="幻灯片页数（1-100）"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="final_slides.md",
        help="输出文件路径（默认: final_slides.md）"
    )
    
    parser.add_argument(
        "--show-workflow",
        action="store_true",
        help="显示工作流结构图"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Canvas Agent 1.0.0"
    )
    
    args = parser.parse_args()
    
    # 显示工作流结构
    if args.show_workflow:
        get_workflow_visualization()
        return
    
    # 获取用户输入
    if args.query and args.pages:
        # 命令行模式
        user_query = args.query
        slide_count = args.pages
        
        if not (1 <= slide_count <= 100):
            print("错误: 页数必须在1-100之间")
            sys.exit(1)
            
        print(f"[System]: 使用命令行参数:")
        print(f"[System]: 需求: {user_query}")
        print(f"[System]: 页数: {slide_count}")
        
    else:
        # 交互式模式
        print("=== Canvas Agent - 智能课件生成系统 ===")
        print()
        
        try:
            user_input = collect_user_input()
            user_query = user_input["original_query"]
            slide_count = user_input["slide_count"]
        except KeyboardInterrupt:
            print("\n[System]: 用户取消操作")
            sys.exit(0)
        except Exception as e:
            print(f"[Error]: 获取用户输入失败: {e}")
            sys.exit(1)
    
    # 验证输入
    if not user_query.strip():
        print("错误: 需求描述不能为空")
        sys.exit(1)
    
    # 运行工作流
    try:
        is_cmd_mode = bool(args.query and args.pages)
        final_state = run_canvas_workflow(user_query, slide_count, is_cmd_mode)
        
        if final_state:
            # 如果指定了输出文件路径，复制文件
            if args.output != "final_slides.md":
                import shutil
                shutil.copy("final_slides.md", args.output)
                print(f"[System]: 输出文件已复制到: {args.output}")
            
            print("\n=== 生成完成 ===")
            print("您可以使用以下命令查看课件:")
            print(f"  moffee live {args.output}")
            print(f"  moffee make {args.output} -o output_html/")
            
        else:
            print("[Error]: 工作流执行失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[System]: 用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"[Error]: 系统错误: {e}")
        sys.exit(1)


def interactive_mode():
    """
    纯交互模式入口（用于直接调用）
    """
    try:
        print("=== Canvas Agent - 智能课件生成系统 ===")
        print()
        
        user_input = collect_user_input()
        user_query = user_input["original_query"]
        slide_count = user_input["slide_count"]
        
        final_state = run_canvas_workflow(user_query, slide_count)
        
        if final_state:
            print("\n=== 生成完成 ===")
            print("您可以使用以下命令查看课件:")
            print(f"  moffee live {final_state['final_slides_path']}")
            print(f"  moffee make {final_state['final_slides_path']} -o output_html/")
            return final_state
        else:
            print("[Error]: 工作流执行失败")
            return None
            
    except KeyboardInterrupt:
        print("\n[System]: 用户取消操作")
        return None
    except Exception as e:
        print(f"[Error]: 系统错误: {e}")
        return None


if __name__ == "__main__":
    main()
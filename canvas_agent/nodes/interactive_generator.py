import subprocess
import os
from openai import OpenAI
from ..utils.state import GraphState
from ..config import Config


def interactive_slide_generator(state: GraphState) -> GraphState:
    """
    交互式幻灯片生成节点
    逐页生成幻灯片，每页都允许用户修改
    """
    client = OpenAI(**Config.get_openai_config())
    
    print("[Agent]: 已进入交互模式。")
    
    # 初始化预览文件
    preview_file = "slides_preview.md"
    initialize_preview_file(preview_file)
    
    # 启动moffee实时预览
    moffee_process = start_moffee_preview(preview_file)
    
    print("[Agent]: Moffee 预览已启动，请查看浏览器。")
    
    # 初始化生成状态
    if not state["generated_slides"]:
        state["generated_slides"] = []
    if state["current_slide_index"] == 0:
        state["current_slide_index"] = 0
    
    total_slides = len(state["outline"])
    
    # 逐页生成循环
    while state["current_slide_index"] < total_slides:
        current_index = state["current_slide_index"]
        current_slide = state["outline"][current_index]
        
        print(f"\n[Agent]: ---")
        print(f"[Agent]: 正在生成第 {current_index + 1}/{total_slides} 页... ✨")
        
        # 生成当前页内容
        slide_content = generate_single_slide(client, state, current_index)
        
        # 更新generated_slides列表
        if current_index < len(state["generated_slides"]):
            # 替换现有页面
            state["generated_slides"][current_index] = slide_content
        else:
            # 添加新页面
            state["generated_slides"].append(slide_content)
        
        # 更新预览文件
        update_preview_file(preview_file, state["generated_slides"])
        
        # 显示生成的内容
        print(f"\n[Agent]: 生成的第 {current_index + 1} 页内容:")
        print("=" * 50)
        print(slide_content)
        print("=" * 50)
        
        # 等待用户反馈
        if not wait_for_user_feedback(state):
            # 用户要求重新生成当前页
            continue
        else:
            # 继续下一页
            state["current_slide_index"] += 1
    
    # 生成完成，保存最终文件
    final_content = create_final_markdown(state["generated_slides"])
    with open(state["final_slides_path"], 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n[Agent]: 🎉 交互式生成完成！")
    print(f"[Agent]: 最终内容已保存到 {state['final_slides_path']}")
    
    # 停止moffee预览
    if moffee_process:
        moffee_process.terminate()
        print("[Agent]: Moffee 预览已停止。")
    
    return state


def generate_single_slide(client: OpenAI, state: GraphState, slide_index: int) -> str:
    """
    生成单页幻灯片内容
    """
    current_slide = state["outline"][slide_index]
    
    # 构建单页提示词
    prompt = f"""
请根据以下信息生成一页Moffee Markdown幻灯片内容：

## 原始需求
{state['original_query']}

## 当前页信息
- 页码: {current_slide['page']}
- 内容描述: {current_slide['content']}
"""
    
    # 如果有用户反馈，加入修改要求
    if state["user_feedback"]:
        prompt += f"\n## 用户修改要求\n{state['user_feedback']}\n"
    
    prompt += f"""
## 生成规则
{state['rules']}

## 要求
1. 只生成这一页的内容，不要包含frontmatter或其他页面
2. 内容要完整、专业、符合页面类型
3. 适当使用Moffee布局功能
4. 如果是第一页，可以作为标题页设计

请直接输出Moffee Markdown内容，不要有其他说明。
"""
    
    try:
        response = client.chat.completions.create(
            **Config.get_model_config(),
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的课件制作专家，精通Moffee Markdown语法。请生成单页幻灯片内容。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        content = response.choices[0].message.content.strip()
        
        # 清除用户反馈状态
        state["user_feedback"] = ""
        
        return content
        
    except Exception as e:
        print(f"[Error]: 生成第 {slide_index + 1} 页时出错: {str(e)}")
        # 返回基本内容
        return f"""## 第{slide_index + 1}页

{current_slide['content']}"""


def wait_for_user_feedback(state: GraphState) -> bool:
    """
    等待用户反馈
    返回True表示继续下一页，False表示重新生成当前页
    """
    print(f"\n[Agent]: 您对此页是否满意？")
    print(f"[Agent]:   - 输入 'c' 或 'continue' 继续")
    print(f"[Agent]:   - 输入您的修改意见 (例如: \"标题加个 emoji\")")
    
    while True:
        user_input = input("[User]: ").strip()
        
        if user_input.lower() in ['c', 'continue']:
            return True
        elif user_input:
            # 用户提供了修改意见
            state["user_feedback"] = user_input
            print(f"[Agent]: 好的，正在根据您的意见重新生成... ✨")
            return False
        else:
            print("[Agent]: 请输入 'c' 继续或提供修改意见。")


def initialize_preview_file(filename: str):
    """
    初始化预览文件
    """
    content = """---
theme: custom
layout: content
aspect_ratio: "16:9"
---

# 课件预览

正在生成内容，请稍候...
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def start_moffee_preview(filename: str):
    """
    启动moffee实时预览
    """
    try:
        # 检查并清理已有的moffee进程
        print("[Agent]: 正在检查并清理moffee进程...")
        subprocess.run(["pkill", "-f", "moffee live"], timeout=5)
        
        # 检查moffee是否可用
        env = os.environ.copy()
        env['PYTHONPATH'] = '/root/code/slide_agent/moffee'
        result = subprocess.run(['moffee', '--version'], 
                              capture_output=True, text=True, timeout=5, env=env)
        if result.returncode != 0:
            print("[Warning]: moffee 命令不可用，预览功能将被跳过")
            return None
            
        # 启动moffee live预览
        process = subprocess.Popen(['moffee', 'live', filename], env=env)
        return process
    except Exception as e:
        print(f"[Warning]: 启动moffee预览失败: {e}")
        return None


def update_preview_file(filename: str, slides: list):
    """
    更新预览文件内容
    """
    content = create_final_markdown(slides)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def create_final_markdown(slides: list) -> str:
    """
    创建最终的Markdown内容
    """
    if not slides:
        return """---
theme: custom
layout: content
aspect_ratio: "16:9"
---

# 空课件

暂无内容
"""
    
    # 添加frontmatter到第一页
    final_content = """---
theme: custom
layout: content
aspect_ratio: "16:9"
---

"""
    
    # 拼接所有页面
    final_content += "\n\n---\n\n".join(slides)
    
    return final_content
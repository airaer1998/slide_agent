from openai import OpenAI
from ..utils.state import GraphState
from ..config import Config


def batch_slide_generator(state: GraphState) -> GraphState:
    """
    批量幻灯片生成节点
    一次性生成所有幻灯片内容
    """
    client = OpenAI(**Config.get_openai_config())
    
    print(f"[Agent]: 开始批量生成 {len(state['outline'])} 页幻灯片...")
    
    # 构建完整的提示词
    prompt = build_batch_prompt(state)
    
    try:
        response = client.chat.completions.create(
            **Config.get_model_config(),
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的课件制作专家，精通Moffee Markdown语法。请严格按照提供的大纲和规则生成完整的课件内容。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        markdown_content = response.choices[0].message.content
        
        # 保存到文件
        output_file = state["final_slides_path"]
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"[Agent]: 批量生成完成！内容已保存到 {output_file}")
        print(f"[Agent]: 您可以使用以下命令预览或导出:")
        print(f"[Agent]:   moffee live {output_file}")
        print(f"[Agent]:   moffee make {output_file} -o output_html/")
        
        # 更新状态
        state["generated_slides"] = [markdown_content]
        
    except Exception as e:
        print(f"[Error]: 批量生成失败: {str(e)}")
        # 创建基本的失败内容
        fallback_content = create_fallback_content(state)
        with open(state["final_slides_path"], 'w', encoding='utf-8') as f:
            f.write(fallback_content)
        state["generated_slides"] = [fallback_content]
    
    return state


def build_batch_prompt(state: GraphState) -> str:
    """
    构建批量生成的提示词
    """
    outline_text = ""
    for i, slide in enumerate(state["outline"]):
        outline_text += f"""
第{slide['page']}页:
- 标题: {slide['title']}
- 类型: {slide['type']}
- 关键要点: {', '.join(slide['key_points'])}
"""
        if slide.get('content_summary'):
            outline_text += f"- 内容摘要: {slide['content_summary']}\n"
        if slide.get('visual_suggestion'):
            outline_text += f"- 视觉建议: {slide['visual_suggestion']}\n"
        if slide.get('notes'):
            outline_text += f"- 备注: {slide['notes']}\n"
    
    prompt = f"""
请根据以下大纲和规则，生成完整的Moffee Markdown课件内容。

## 原始需求
{state['original_query']}

## 大纲
{outline_text}

## 生成规则
{state['rules']}

## 要求
1. 严格按照大纲顺序生成每一页内容
2. 遵循Moffee语法规则
3. 内容要完整、专业、易懂
4. 适当使用布局分隔符(<->, ===)增强视觉效果
5. 每页之间使用 `---` 分隔
6. 第一页前添加适当的frontmatter配置

请直接输出完整的Moffee Markdown内容，不要有其他说明文字。
"""
    
    return prompt


def create_fallback_content(state: GraphState) -> str:
    """
    创建失败情况下的备用内容
    """
    content = """---
theme: default
layout: content
aspect_ratio: "16:9"
---

# 课件生成失败

课件自动生成遇到问题，请检查网络连接或稍后重试。

"""
    
    for slide in state["outline"]:
        content += f"""---

## {slide['title']}

"""
        for point in slide['key_points']:
            content += f"- {point}\n"
        
        if slide.get('content_summary'):
            content += f"\n{slide['content_summary']}\n"
    
    return content
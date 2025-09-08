import json
from openai import OpenAI
from ..utils.state import GraphState, SlideOutline
from ..config import Config


def outline_generator(state: GraphState) -> GraphState:
    """
    大纲生成节点
    根据用户需求生成结构化的课件大纲
    """
    client = OpenAI(**Config.get_openai_config())
    
    # 构建简化的提示词
    prompt = f"""
请根据用户需求生成{state['slide_count']}页课件大纲，返回JSON数组格式。

用户需求：{state['original_query']}

返回格式：
[
  {{
    "page": 1,
    "content": "第一页的完整内容描述，包括标题、要点、详细说明等所有文本内容"
  }},
  {{
    "page": 2,
    "content": "第二页的完整内容描述..."
  }}
]

要求：
1. content字段包含该页的完整内容描述，以自由文本形式
2. 内容要符合主题"{state['original_query']}"
3. 每页content要详细具体，避免空泛描述
4. 直接返回JSON数组，不要其他文字
"""

    try:
        response = client.chat.completions.create(
            **Config.get_model_config(),
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的课件设计师，擅长创建结构化、逻辑清晰的教学内容大纲。请严格按照JSON格式返回结果。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )
        
        # 解析AI生成的大纲
        outline_response = response.choices[0].message.content
        print(f"[Debug]: AI响应内容: {outline_response[:200]}...")  # 调试信息
        
        if not outline_response or not outline_response.strip():
            raise ValueError("AI返回了空响应")
        
        try:
            outline_data = json.loads(outline_response)
        except json.JSONDecodeError as e:
            print(f"[Debug]: JSON解析失败，原始响应: {outline_response}")
            raise ValueError(f"JSON解析失败: {str(e)}")
        
        # 提取大纲列表（处理可能的不同响应格式）
        if isinstance(outline_data, list):
            # 标准格式：直接是数组
            outline_list = outline_data
        elif isinstance(outline_data, dict):
            # 检查是否包含常见的键
            if 'outline' in outline_data and isinstance(outline_data['outline'], list):
                outline_list = outline_data['outline']
            elif 'slides' in outline_data and isinstance(outline_data['slides'], list):
                outline_list = outline_data['slides']
            else:
                # 尝试找到第一个列表值
                outline_list = None
                for value in outline_data.values():
                    if isinstance(value, list):
                        outline_list = value
                        break
                
                # 如果还是找不到列表，可能是单个slide对象，尝试转换为列表
                if outline_list is None:
                    # 检查是否是单个slide对象（包含page, title等字段）
                    if 'page' in outline_data or 'title' in outline_data:
                        outline_list = [outline_data]
                    else:
                        raise ValueError("无法从AI响应中提取大纲列表")
        else:
            raise ValueError("AI响应格式不正确：必须是对象或数组")
        
        # 验证和标准化大纲格式
        validated_outline = []
        for i, slide in enumerate(outline_list[:state['slide_count']]):  # 确保不超过指定页数
            # 确保slide是字典类型
            if not isinstance(slide, dict):
                print(f"[Warning]: 第{i+1}页数据格式不正确，跳过: {slide}")
                continue
                
            validated_slide: SlideOutline = {
                "page": slide.get("page", i + 1),
                "content": slide.get("content", f"第{i+1}页的内容")
            }
            validated_outline.append(validated_slide)
        
        # 如果生成的页数不足，补充基本页面
        while len(validated_outline) < state['slide_count']:
            page_num = len(validated_outline) + 1
            validated_outline.append({
                "page": page_num,
                "content": f"第{page_num}页的内容"
            })
        
        state["outline"] = validated_outline
        
        # 保存大纲到文件
        outline_file = "outline.json"
        with open(outline_file, 'w', encoding='utf-8') as f:
            json.dump(validated_outline, f, ensure_ascii=False, indent=2)
        
        print(f"[Agent]: 大纲已生成完成，共{len(validated_outline)}页")
        print(f"[Agent]: 大纲已保存到 {outline_file}")
        
        # 显示大纲预览
        print("\n=== 大纲预览 ===")
        for slide in validated_outline:
            print(f"第{slide['page']}页: {slide['content'][:50]}...")
        print("================\n")
        
    except Exception as e:
        print(f"[Error]: 生成大纲时出错: {str(e)}")
        # 创建默认大纲
        default_outline = []
        for i in range(state['slide_count']):
            default_outline.append({
                "page": i + 1,
                "content": f"第{i+1}页的内容"
            })
        state["outline"] = default_outline
        
        # 保存默认大纲
        with open("outline.json", 'w', encoding='utf-8') as f:
            json.dump(default_outline, f, ensure_ascii=False, indent=2)
    
    return state
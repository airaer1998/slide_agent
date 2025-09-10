from ..utils.state import GraphState


def rule_engine(state: GraphState) -> GraphState:
    """
    规则引擎节点
    生成内容生成规则，包括固定的Moffee语法和动态的需求提炼
    """
    
    # 固定的Moffee语法规则
    moffee_syntax_rules = """
## Moffee 语法规则

### 页面分隔
- 使用 `---` 手动分页
- 使用 `##` 二级标题自动创建新页面

### 布局控制
- 使用 `<->` 横向分隔元素（左右布局）
- 使用 `===` 纵向分隔元素（上下布局）
- `===` 优先级高于 `<->`

### 前置配置（页面顶部）
```yaml
---
theme: custom
layout: content
aspect_ratio: "16:9"
---
```

### 样式装饰器
- 页面级样式：`@(layout=centered, background-color=blue)`
- 支持任意CSS属性

### 内容语法
- 支持标准Markdown语法
- **粗体** 和 *斜体*
- `代码` 和代码块
- 列表、链接、图片等
- 数学公式：$tex$ 格式
- 高亮文本：==高亮==
- 删除线：~~删除~~

### 注意事项框
```
!!! note
    这是一个注意事项
```

### 图片和媒体
- 相对路径基于resource_dir
- 支持各种图片格式
"""

    # 从用户需求中提炼动态规则
    dynamic_rules = extract_dynamic_rules_from_query(state["original_query"])
    
    # 合并规则
    complete_rules = f"""
{moffee_syntax_rules}

## 内容生成特定要求

{dynamic_rules}

## 重要提示
1. 每页内容要完整，逻辑清晰
2. 适当使用布局分隔符增强视觉效果
3. 根据内容类型选择合适的页面样式
4. 确保技术内容准确，教学内容循序渐进
5. 充分利用Moffee的布局功能，让页面更具吸引力
"""
    
    state["rules"] = complete_rules
    
    print("[Agent]: 内容生成规则已制定完成")
    print("[Agent]: 规则包含Moffee语法和用户需求定制化要求")
    
    return state


def extract_dynamic_rules_from_query(query: str) -> str:
    """
    从用户查询中提炼动态规则
    """
    dynamic_rules = []
    
    # 分析用户需求中的关键词
    query_lower = query.lower()
    
    # 风格相关
    if any(word in query_lower for word in ["通俗", "简单", "易懂", "初学者"]):
        dynamic_rules.append("- 使用通俗易懂的语言，避免过于专业的术语")
        dynamic_rules.append("- 多使用类比和比喻来解释复杂概念")
    
    if any(word in query_lower for word in ["专业", "深入", "高级", "进阶"]):
        dynamic_rules.append("- 使用专业准确的术语")
        dynamic_rules.append("- 深入讲解原理和细节")
    
    if any(word in query_lower for word in ["实践", "实战", "动手", "练习"]):
        dynamic_rules.append("- 包含大量实践案例和代码示例")
        dynamic_rules.append("- 提供具体的操作步骤")
    
    # 内容类型相关
    if any(word in query_lower for word in ["编程", "代码", "开发", "程序"]):
        dynamic_rules.append("- 代码示例使用代码块格式")
        dynamic_rules.append("- 关键代码概念用 `代码` 格式突出显示")
    
    if any(word in query_lower for word in ["数学", "公式", "计算"]):
        dynamic_rules.append("- 数学公式使用 $tex$ 格式")
        dynamic_rules.append("- 重要公式单独成行并居中显示")
    
    # 视觉相关
    if any(word in query_lower for word in ["图片", "图表", "图像", "可视化"]):
        dynamic_rules.append("- 适当使用 `<->` 布局将文字和图片并排显示")
        dynamic_rules.append("- 重要图表使用 `===` 布局突出显示")
    
    # 教学相关
    if any(word in query_lower for word in ["教学", "课程", "培训", "学习"]):
        dynamic_rules.append("- 使用循序渐进的结构安排")
        dynamic_rules.append("- 每页包含明确的学习目标")
        dynamic_rules.append("- 适当使用 `!!! note` 强调重点内容")
    
    # 如果没有特殊要求，添加默认规则
    if not dynamic_rules:
        dynamic_rules = [
            "- 保持内容简洁明了",
            "- 使用恰当的格式突出重点",
            "- 合理运用Moffee布局功能"
        ]
    
    return "\n".join(dynamic_rules)
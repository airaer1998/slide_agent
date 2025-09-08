### **Canvas: 智能课件生成 Agent 产品规划**

### **1. 项目愿景 (Vision)**

利用 LangGraph 构建一个智能、可控、支持多模式生成的自动化课件（Slide）生成 Agent。它将用户的自然语言需求转化为专业、结构化的 moffee Markdown 课件，极大提升内容创作效率。（你可以先查看moffee的readme文档：/root/code/slide_agent/moffee/README.md以了解怎么使用moffee）

### **2. 核心工作流 (Core Workflow)**

`用户输入` -> `生成结构化大纲` -> `用户审核与修改` -> `选择生成模式` -> `动态规则生成` -> `按模式生成内容` -> `预览与交付`

*(这是一个简化的流程图示意)*

1. **用户输入 (User Input)**:
    - **内容**: 用户提供一个包含两部分的 Query。
        - `完整需求`: 课程主题、面向人群、风格要求等文本描述。
        - `幻灯片页数`: 1-100 的整数。
    - **节点**: `UserInputParser`
2. **大纲生成 (Outline Generation)**:
    - **内容**: `Manage` 节点接收用户输入，生成整个课程的框架。
    - **核心优化: 输出结构化大纲 (JSON)**: 不再使用简单的分隔符，而是生成一个 JSON 文件 (`outline.json`)。每一页幻灯片都是一个 JSON 对象，包含更丰富的元信息。
    - **示例**:
        
        ```
        [
          {
            "page": 1,
            "title": "课程介绍",
            "type": "title_slide",
            "key_points": ["什么是Python", "课程学习目标"],
            "visual_suggestion": "一张包含Python Logo和问号的图片"
          },
          {
            "page": 2,
            "title": "第一个程序：Hello, World!",
            "type": "code_slide",
            "content_summary": "解释print()函数，并展示代码示例",
            "notes": "强调代码的简洁性，建立初学者信心"
          }
        ]
        
        ```
        
    - **节点**: `OutlineGenerator`
3. **用户审核与修改 (User Review & Edit)**:
    - **内容**: Agent 执行暂停。向用户提示 `outline.json` 文件已生成。
    - **操作**: 用户可以手动打开、编辑和保存这个 JSON 文件，对大纲进行精确调整。
    - **触发**: 用户在命令行输入 `continue` 后，Agent 读取修改后的文件，继续执行。
    - **节点**: `WaitForUserApproval` (这是一个暂停点)
4. **模式选择 (Mode Selection)**:
    - **内容**: Agent 询问用户希望的生成方式。
        - `一次性生成 (Batch Mode)`: 默认选项，一次性输出所有内容。
        - `交互模式 (Interactive Mode)`: 逐页生成，每页都提供修改机会。
    - **节点**: `SelectMode` (这是一个路由决策点)
5. **规则引擎 (Rules Engine)**:
    - **内容**: 生成一个 `rules` 文本，作为后续所有内容生成节点的“系统提示”或“全局上下文”。
    - **动态生成**: `rules` 文本包含两部分：
        1. **固定的 Moffee 语法**: 预先定义好的 Markdown 语法规则。
        2. **动态的需求提炼**: 从用户最初的 `完整需求` 中提炼出的关键指令（如：“风格通俗易懂”、“多用比喻”）。
    - **节点**: `RuleEngine`
6. **内容生成 (Content Generation)**:
    - **内容**: 此阶段根据用户选择的模式，进入不同的分支。详见下面的 **"生成模式详解"**。
    - **节点**: `BatchSlideGenerator` / `InteractiveSlideGenerator`
7. **预览与交付 (Preview & Delivery)**:
    - **内容**: 生成最终的 `final_slides.md` 文件。
    - **操作**: 自动或提示用户调用 moffee 的命令（如 `moffee final_slides.md`）进行预览、导出 HTML 或 PDF。

### **3. 生成模式详解 (Generation Modes Deep Dive)**

### **A. 一次性生成模式 (Batch Mode)**

- **输入**: `rules` 文本, 完整的 `outline.json` 列表。
- **流程**:
    1. `BatchSlideGenerator` 节点接收全部大纲。
    2. 在内部循环遍历大纲列表中的每一项。
    3. 为每一项生成对应的 Markdown 内容。
    4. 将所有页的 Markdown 拼接成一个完整的字符串。
    5. 输出最终的 `final_slides.md` 文件。
- **优点**: 速度快，流程简单，适合对大纲非常有信心的用户。

### **B. 交互生成模式 (Interactive Mode)**

- **输入**: `rules` 文本, `outline.json` 列表。
- **核心优化**: **使用 LangGraph 状态 (State) 管理生成过程，而非直接反复读写文件。**
- **流程**:
    1. 创建一个空的 `slides_preview.md` 文件，并启动 moffee 的实时预览 (`moffee slides_preview.md --watch`)。
    2. LangGraph 的 State 中初始化一个空列表：`generated_slides = []`。
    3. 进入循环 (逐页生成):
        
        a. Agent 读取大纲中的第 N 页，调用 InteractiveSlideGenerator 节点生成该页的 Markdown。
        
        b. 将新生成的 Markdown 追加到 generated_slides 列表中。
        
        c. 将 generated_slides 列表中的所有内容用分页符 (\n---\n) 连接起来，完整覆盖写入 slides_preview.md 文件。（moffee 预览会自动刷新）
        
        d. Agent 在命令行展示新生成的内容，并等待用户反馈。
        
    4. **用户反馈处理**:
        - 如果用户输入 `continue`: 循环进入下一页 (N+1)。
        - 如果用户输入**修改意见**: Agent 将修改意见和第 N 页的大纲**再次**送入 `InteractiveSlideGenerator` 节点重新生成。新生成的内容将**替换** `generated_slides` 列表中的最后一个元素。然后返回步骤 3.c，再次等待用户反馈。
    5. 所有页面处理完毕后，循环结束。

### **4. 命令行交互设计 (CLI Interaction Design)**

```
[Agent]: 您好！我是您的课件生成助手。
[Agent]: 请粘贴您的完整需求... (完成后输入 'EOF')
[User]: ...
[Agent]: 请问您希望生成多少页幻灯片？(1-100)
[User]: 5
[Agent]: 大纲已生成到 `outline.json`。请修改确认后，输入 'continue' 继续。
[User]: continue
[Agent]: 请选择生成模式: 1. 一次性生成 2. 交互模式 (请输入 1/2)
[User]: 2
[Agent]: 已进入交互模式。Moffee 预览已启动，请查看浏览器。
[Agent]: ---
[Agent]: 正在生成第 1/5 页: "课程介绍"... ✨
[Agent]: (在命令行打印出生成的 Markdown)
[Agent]: ---
[Agent]: 您对此页是否满意？
[Agent]:   - 输入 'c' 或 'continue' 继续
[Agent]:   - 输入您的修改意见 (例如: “标题加个 emoji”)
[User]: 标题加个 emoji
[Agent]: 好的，正在重新生成第 1 页... ✨
[Agent]: (在命令行打印出修改后的 Markdown)
[Agent]: ---
[Agent]: 您对此页是否满意？ ('c' / 修改意见)
[User]: c
[Agent]: ---
[Agent]: 正在生成第 2/5 页... (循环继续)

```

### **5. LangGraph 状态设计 (State Definition)**

使用 `TypedDict` 来定义图（Graph）中流转的状态，确保数据结构的清晰和类型安全。

```
from typing import List, Dict, Literal, TypedDict

class SlideOutline(TypedDict):
    """单页幻灯片的结构化大纲"""
    page: int
    title: str
    type: str
    key_points: List[str]
    # ... 其他可能的字段

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
    generated_slides: List[str] # 存储已生成的 Markdown 页面
    current_slide_index: int    # 当前正在处理的页面索引
    user_feedback: str          # 用户本轮的修改意见

```
---
theme: default
layout: content
aspect_ratio: "16:9"
---

@(layout=centered)

# Python语法入门
## 核心四要素

===  

**缩进与代码块** <-> **注释**
- 使用 **4空格** 缩进代替大括号  
  ```python
  if True:
      print("缩进即代码块")
  ```
- 单行注释 `#` <-> 多行注释 `"""..."""`  
  ```python
  # 单行注释
  """多行
  注释"""
  ```

===  

**变量与动态类型** <-> **输出**
- 无需声明类型，直接赋值  
  ```python
  age = 25      # int
  name = "Tom"  # str
  ```
- `print()` 输出到控制台  
  ```python
  print("Hello,", name, "今年", age, "岁")
  ```

!!! note
    Python 用缩进表示层级，错误缩进会导致 `IndentationError`
---
theme: default
layout: content
aspect_ratio: "16:9"
---

# Python基础介绍
@(layout=centered, background-color=#f0f8ff)

## 从零开始掌握Python

<->

### Python简介与历史
- 1991年由Guido van Rossum创建
- 简洁、易读、功能强大
- 广泛应用于Web、AI、数据科学

=== 

### 安装与环境配置
```bash
# 推荐使用Anaconda
https://www.anaconda.com/download

# 或使用官方安装包
https://www.python.org/downloads/
```

### 第一个Python程序
```python
print("Hello, World!")
```

---

@(layout=default)

# 基本语法与数据类型  
*Python 变量与内置类型速览*  

---

### 变量与标识符规则  
- 区分大小写：`name` ≠ `Name`  
- 由 **字母、数字、下划线** 组成，**不能以数字开头**  
- 禁用保留字：`if`, `else`, `class`, `import` …  

!!! note
    使用小写+下划线风格：`user_score`, `max_connections`

---

### 核心内置类型  

<->  
#### 数值  
- `int`    `42`  
- `float`  `3.14`  
- `complex` `1+2j`  

#### 布尔  
- `True` / `False`  
- 算术运算：`True == 1`, `False == 0`  

<->  
#### 字符串  
- 单/双/三引号皆可  
- 转义：`\n`, `\\`  
- f-string：`f"Hi, {name}"`  

---

### 类型转换与常用内置函数  

| 功能 | 示例 | 说明 |
|---|---|---|
| 转整 | `int("10")` | 字符串 → 整数 |
| 转浮点 | `float("3.5")` | 字符串 → 浮点 |
| 转字符串 | `str(100)` | 任意 → 字符串 |
| 判类型 | `type(x)` / `isinstance(x, int)` | 类型检查 |
| 交互输入 | `input()` | 默认返回字符串 |

!!! warning
    `float("abc")` 触发 `ValueError`，务必先验证输入。
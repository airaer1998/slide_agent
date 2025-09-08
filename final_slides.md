---
theme: default
layout: content
aspect_ratio: "16:9"
---

# Python基础入门导论
## 从零开始认识Python

---

### Python是什么
- **解释型**、**跨平台**、**开源**的高级编程语言  
- 由 **Guido van Rossum** 于 **1991** 年发布  
- 以 **简洁优雅** 著称  
- 广泛应用于 **Web开发**、**数据分析**、**人工智能** 等领域  

<->

### Python特点
- 语法接近 **自然语言**  
- 拥有丰富 **标准库**（`urllib`、`json`、`datetime` 等）  
- **动态类型**，无需显式声明  
- 支持 **面向对象**、**函数式** 与 **过程式** 混合编程  
- 社区活跃，第三方包 **超40万个**  

---

### 运行环境
- **Windows / Mac / Linux** 均可  
- 官网下载安装包或 **Anaconda** 发行版  
- 终端输入 `python` 或 `python3` 进入 **REPL** 交互模式  
- 推荐使用 **VS Code** 或 **PyCharm** 集成开发环境，插件丰富，调试直观  

!!! note
    在 REPL 中输入 `print("Hello, Python!")` 并回车，立即看到输出，无需编译过程，体现“写一行、跑一行”的交互式优势。

---

## 变量与数据类型

---

### 变量命名
- 由 **字母 / 数字 / 下划线** 组成，区分大小写  
- 不能以 **数字** 开头  
- 遵循 **snake_case** 风格，如 `student_name`  
- 避免使用 **保留字**（`if`、`class`、`for` 等）  

<->

### 数字类型
- `int`（42）  
- `float`（3.14）  
- `complex`（2+3j）  
- 支持 `+ - * / // % **` 运算  
- 整数 **无大小限制**，浮点遵循 **IEEE 754**

---

### 字符串
- 使用 **单引号**、**双引号**、**三引号** 创建，可嵌套  
- 支持 **索引** `s[0]`、**切片** `s[1:4]`、**拼接** `+`、**重复** `*`、**格式化** `f"{name}"`  
- 转义字符 `\n \t \\`

<->

### 布尔与空值
- `bool` 仅 `True`、`False`，可参与 `and / or / not` 逻辑运算  
- `NoneType` 表示空值，常用于函数无返回值占位  

---

### 类型转换
- `int('42')`、`str(3.14)`、`float('3.14')`  
- 转换失败抛 `ValueError`

```python
name = 'Alice'
age = 18
intro = f'{name} is {age} years old.'
```

---

## 控制流与循环

---

### 条件语句
- `if`、`elif`、`else` 结构  
- 条件表达式可 **链式比较** `1 <= x < 10`  
- 缩进 **4空格** 强制，体现代码块层级  

<->

### while 循环
- 先判断后执行，避免死循环需更新循环变量  
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

---

### for 循环
- 基于 **可迭代对象**，常与 `range()` 配合  
- `range(start, stop, step)` 左闭右开  
- 支持 `else` 子句，循环未被 `break` 中断时执行  

<->

### break 与 continue
- `break` 立即跳出 **最近循环**  
- `continue` 跳过本次剩余语句  
- 两者仅在 **循环体内** 有效  

---

### 综合案例：打印 2~50 之间所有素数
```python
for n in range(2, 51):
    for d in range(2, int(n**0.5)+1):
        if n % d == 0:
            break
    else:
        print(n, end=' ')
```

---

## 函数与模块

---

### 定义函数
- 使用 `def` 关键字，后跟函数名与括号参数列表  
- 可选 **文档字符串** `docstring` 描述功能  
- 使用 `return` 返回值，无 `return` 则返回 `None`

<->

### 参数机制
- **位置参数**、**默认参数** `def greet(name, msg='Hi')`  
- **关键字参数** `greet(msg='Hello', name='Bob')`  
- 可变参数 `*args` 收集元组、`**kwargs` 收集字典  

---

### 作用域
- **局部变量** 仅在函数内有效  
- `global` 声明修改外部变量  
- **LEGB** 规则（Local → Enclosing → Global → Built-in）查找变量  

<->

### 模块导入
- `import math` 使用 `math.sqrt`  
- `from math import sqrt as s`  
- 自定义文件 `hello.py` 中定义函数，主程序 `import hello` 后调用 `hello.say()`

---

### 标准库速览
- `math`（数学）  
- `random`（随机）  
- `datetime`（日期）  
- `os`（操作系统）  
- `json`（序列化）  

!!! note
    查看帮助 `help(math)` 或官方文档。

---

## 列表、元组与字典

---

### 列表 list
- 有序 **可变** 序列，用 `[]` 创建  
- 支持 `append`、`insert`、`pop`、`remove`、`sort`、`reverse` 方法  
- 列表推导式 `[x**2 for x in range(5)]` 简洁生成新列表  

<->

### 元组 tuple
- 有序 **不可变** 序列，用 `()` 创建  
- 单元素需加逗号 `(42,)`  
- 拆包 `a, b = (1, 2)`  
- 函数返回多值时自动打包成元组  

---

### 字典 dict
- 键值对集合，**无序可变**，用 `{}` 创建  
- 键须 **可哈希**（字符串、数字、元组）  
- 访问 `dict['key']`、`get('key', default)`  
- 新增 `dict['new'] = 100`  
- 遍历 `for k, v in dict.items()`

<->

### 集合 set
- 无序 **不重复** 元素，用 `{}` 或 `set()` 创建  
- 支持 **并** `|`、**交** `&`、**差** `-` 运算  
- 用于去重 `list(set([1,2,2,3]))`

---

### 实践任务
```python
# 使用列表存储学生成绩
scores = [88, 92, 79, 95, 84]

# 元组保存姓名与学号不可变信息
students = [('Alice', '2023001'), ('Bob', '2023002'), ('Carol', '2023003')]

# 字典将学号映射到成绩
mapping = {'2023001': 88, '2023002': 92, '2023003': 79}

# 计算平均分
avg = sum(mapping.values()) / len(mapping)

# 打印最高成绩学生信息
top_id = max(mapping, key=mapping.get)
top_name = next(name for name, sid in students if sid == top_id)
print(f'最高分：{top_name}({top_id}) -> {mapping[top_id]}')
```
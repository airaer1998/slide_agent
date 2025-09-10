---
theme: default
layout: content
aspect_ratio: "16:9"
---

# 从零开始认识Python

<->
## 什么是Python  
- 由 **Guido van Rossum** 于 1991 年发布  
  *高层次 · 解释型 · 通用编程语言*  
- **特点**  
  - 语法简洁、可读性高  
  - 跨平台、生态庞大  
- **典型场景**  
  数据分析 | Web后端 | 自动化脚本 | AI | IoT

<->
## 安装运行环境  
1. **官方解释器 CPython**  
   `python.org` → 下载 3.x → 勾选 *Add to PATH*  
2. **验证**  
   ```bash
   python --version   # Python 3.x.x ✔
   ```  
3. **REPL**  
   终端输入 `python` → `>>>` 即时交互  
4. **推荐 IDE**  
   VS Code + Python 扩展 | PyCharm Community | Jupyter Notebook

---

## 第一个Python程序  
```python
# hello.py
print("Hello, Python!")
```  
- 终端运行：`python hello.py` → `Hello, Python!`  
- **解释流程**  
  源代码 → 字节码 → Python VM → 屏幕输出
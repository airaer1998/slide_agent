---
theme: custom
layout: content
aspect_ratio: "16:9"
---

# C语言入门与开发环境搭建
## 从零开始，掌握高效、可移植的系统级语言

---

## <-> 1972 · UNIX之父
### Dennis Ritchie @Bell Labs
#### 高效 | 可移植 | 贴近硬件  
> 操作系统 · 嵌入式 · 高性能计算首选语言

---

## ===
### 开发环境速配
#### Windows
- MinGW-w64 + VS Code
- 一键脚本：**x86_64-posix-seh**
#### macOS
- `xcode-select --install`
#### Linux
- `sudo apt install build-essential`

---

## ===
### Hello, C!
```c
#include <stdio.h>
int main() {
    printf("Hello, C!\n");
    return 0;
}
```
> 编译：`gcc hello.c -o hello && ./hello`

---

## <-> 结构剖析
- `#include <stdio.h>` 预处理指令
- `int main()` 程序入口
- `return 0;` 正常退出
- `printf` 标准库函数

!!! warning 常见坑
    漏分号 / 拼错`main` / 中文空格路径
---
theme: default
layout: content
aspect_ratio: "16:9"
---

# C语言概述与开发环境
@(layout=centered)

## C语言的历史与特点
- **高效** : 接近汇编，执行速度快  
- **可移植** : 一次编写，多平台编译  
- **结构化** : 函数+模块化，易于维护  

=== 
<->

## 开发流程
```mermaid
graph LR
A[编辑 .c] --> B[编译 .obj] --> C[链接 .exe]
```

## 常用IDE
1. **GCC**：GNU 开源编译器  
2. **Clang**：LLVM 架构，错误提示友好  
3. **VS Code**：轻量 IDE + 插件生态  

---
## 创建第一个“Hello, World!”程序
```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

!!! note
保存为 `hello.c`，终端执行：`gcc hello.c -o hello && ./hello`

---

# 基本数据类型与变量
@(layout=centered)

## 整型：int、short、long
| 类型  | 位数 | 范围 | 举例 |
|-------|------|------|------|
| `short` | 16 | −32 768 ~ 32 767 | `short s = 10;` |
| `int`   | 32 | −2 147 483 648 ~ 2 147 483 647 | `int i = 42;` |
| `long`  | 64 | −9 223 372 036 854 775 808 ~ 9 223 372 036 854 775 807 | `long l = 100000L;` |

## 浮点型：float、double
<->

- **float**（单精度）  
  有效数字：≈ 6–7 位  
  `float f = 3.14f;`

- **double**（双精度）  
  有效数字：≈ 15–16 位  
  `double d = 3.1415926;`

---

## 字符型：char
- 占用 **1 字节**  
- 与 **ASCII** 码一一对照  
  `'A'` → 65，`'0'` → 48

## 变量声明、初始化与命名规则
```c
int age = 18;          // 声明并初始化
double pi = 3.14159;
char grade = 'A';

// 命名规则
// 1. 只能包含字母、数字、下划线
// 2. 不能以数字开头
// 3. 区分大小写
```

---

# 控制结构与输入输出
@(layout=centered)

## 条件语句
### if-else
```c
if (score >= 60) {
    printf("Pass\n");
} else {
    printf("Fail\n");
}
```

### switch-case
```c
switch (ch) {
    case 'a': puts("apple"); break;
    case 'b': puts("banana"); break;
    default: puts("unknown");
}
```

---

## 循环结构
| 循环 | 先判断 | 适用场景 |
|------|--------|----------|
| **for** | ✔ | 已知次数 |
| **while** | ✔ | 条件循环 |
| **do-while** | ✘ | 至少执行一次 |

```c
// for 循环示例
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}
```

---

## 标准输入：scanf()
- 格式控制符  
  `%d` 整数 `%f` float `%lf` double `%c` 字符 `%s` 字符串

```c
int a;
scanf("%d", &a);  // 注意 & 取地址
```

## 标准输出：printf()
- 格式化字符串  
  `%.2f` 保留两位小数 `%05d` 补零占位

```c
printf("a = %d, pi = %.2f\n", a, 3.1415);
```
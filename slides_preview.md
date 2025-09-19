---
theme: custom
layout: content
aspect_ratio: "16:9"
---

@(layout=centered, background-color=#0d1117)

# Transitioning from Python to C  
**Foundations for Systems & AI**

---

## Learning Objectives
1. Articulate core differences between **interpreted (Python)** and **compiled (C)** execution  
2. Write, compile, and run a minimal *Hello, World!* C program with `gcc`  
3. Declare variables with explicit static types: `int`, `float`, `double`, `char`  
4. Use `printf` / `scanf` for basic I/O and debug with `printf`  
5. Trace the four-stage compilation pipeline: *preprocess → compile → assemble → link*

---

## Course Map
<->  
**Session 1 (200 min)**  
Basics: syntax, types, I/O, compilation  

**Session 2 (200 min)**  
Control structures & functions

---

## Assessment
- Weekly checkpoint quiz  
- 5 × Python → C conversions  
- Calculator mini-project

---

!!! warning
Install **GCC or Clang** + **VS Code** (C/C++ extension) before next class.

---

@layout=left-title
# Why Learn C for<br>Computer Systems & AI/ML?

===

## Systems Perspective
- C maps closely to hardware  
  `pointers = addresses`, `structs = memory layouts`
- OS kernels, embedded firmware, high-performance libs (BLAS, OpenCV) written in C

## AI/ML Connection
- TensorFlow Lite Micro runs on C++ (subset of C)
- Optimize Python extensions by understanding memory & cache (NumPy backend)

## Career Edge
- Device drivers, GPU kernels, real-time robotics demand C mastery

<->

![stack-diagram](resources/c-vs-python-stack.png)
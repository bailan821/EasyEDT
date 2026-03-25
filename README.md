# 🚀 EasyEDT
极简轻量终端文本编辑器  
专为无 GUI 极端环境设计 | 嵌入式 | 服务器 | Termux | WSL |  HiSH  | 

---

## 项目简介
EasyEDT 是一款面向新手设计的无图形界面环境的轻量化终端文本编辑器，针对服务器、嵌入式设备、Termux、WSL 等严苛使用场景优化，启动快速、操作直观、无额外依赖，适合快速编辑配置文件、代码与文本内容。
![图片1](https://github.com/bailan821/EasyEDT/blob/main/assets/1.png)

## ✨ 核心特性
- 纯终端运行，不依赖任何图形界面
- 单文件实现，体积小、资源占用极低
- 全平台兼容，只要有 Python 即可运行
- 操作逻辑简洁，新手易上手
- 无第三方库依赖，开箱即用
![图片2](https://github.com/bailan821/EasyEDT/blob/main/assets/2.png)
## 🖥 支持平台
- **x86_64 Linux / WSL**  
  提供预编译二进制，直接运行
- **ARM 平台**（Termux / 开发板 / 嵌入式设备）  
  直接执行 Python 源码
- 其他支持 Python 的终端环境均可通用

## 🔧 使用方法
### 1. 预编译二进制（x86_64 Linux）

# 赋予执行权限
chmod +x easyedt-x86_64

# 启动编辑器
./easyedt-x86_64

### 2.运行主程序(ARM)
python easyedt-x86_64.py

## 📂项目结构
#### EasyEDT/
#### ├─ assets      放展示图片的文件夹
#### ├─ easyedt.py  主程序源码
#### ├─ LICENSE     开源协议
#### └─ README.md   使用说明






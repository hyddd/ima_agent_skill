# Ima Agent Skill

这是一个为 [Clawdbot](https://github.com/clawdbot/clawdbot) 设计的 Skill，用于通过 CDP (Chrome DevTools Protocol) 控制 **ima.copilot** 桌面客户端（腾讯 ima）。

它允许你通过自然语言指令，让 Clawdbot 在本地的 ima 应用中打开新标签页并进行搜索。

## 功能特性

- **自动启动**: 如果检测到 ima 未运行，会自动启动应用。
- **自动连接**: 自动配置调试端口 (8315) 和绕过跨域限制 (`--remote-allow-origins=*`)。
- **远程控制**: 使用 CDP 协议创建新标签页，并导航到指定的搜索结果页。

## 安装

1. 确保已安装 Clawdbot。
2. 将此目录放置在 Clawdbot 的 skills 目录下（或建立软链接）。
3. 确保本地 Python 环境已安装依赖：
   ```bash
   pip install websocket-client
   ```

## 配置

本 Skill 需要在 `scripts/launcher.py` 中或通过 `SKILL.md` 指定正确的 Python 解释器路径。
默认配置为使用特定的 venv，你可能需要根据实际情况修改 `SKILL.md` 中的调用命令。

## 使用示例

在 Clawdbot 对话中：

> "用 ima 搜索 Clawdbot 是什么"

## 目录结构

```
.
├── SKILL.md              # Clawdbot 技能定义文件
├── README.md             # 项目说明
└── scripts
    └── launcher.py       # 核心 Python 控制脚本
```

## 依赖

- Python 3
- websocket-client
- ima.copilot 桌面端 (macOS)

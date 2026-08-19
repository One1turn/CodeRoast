# 🧂 CodeRoast — AI 代码烤肉架

> 输入一段代码，生成阴阳怪气的 Code Review 评论。

## 这是什么？

	CodeRoast 是一个纯 Python 脚本，不依赖任何 AI 模型，用预置的"烤肉词库"随机组合生成看起来很专业的代码评论。

## 安装

```bash
git clone https://github.com/One1turn/CodeRoast.git
cd CodeRoast
```

## 使用

```bash
# 烤一段代码
python coderoast.py example.py

# 直接烤文件内容
echo "var x = 1" > test.py
python coderoast.py test.py
```

## 示例输出

```
🔥 🔥 🔥 CodeRoast — 正在烤你的代码 🔥 🔥 🔥

📄 文件: example.py (42 行)
🐍 检测到语言: Python

═══════════════════════════════════════════
  🎤 Review 评审意见
═══════════════════════════════════════════

整体评价: 🔴 Needs Improvement

📌 代码风格:
  - 变量名 a 请改成人类能读的名字
  - 这个缩进是用脚踩出来的吗
  - 注释比代码还多，但没一句说重点

🐛 逻辑问题:
  - 这个 if 永远不会执行，恭喜你写了死代码
  - return 之后的代码是给鬼看的吗
  - 你确定这个循环不是无限跑的

架构建议:
  - 建议把这个函数拆成 47 个微服务
  - 这个 God Function 看起来像初创公司的组织架构图

安全警告:
  - 把密钥硬编码进去，你是在给黑客送业绩

总评: 💀 
  这段代码就像是用 Google Translate 翻译了三次的菜谱。
  它能跑，但你不想知道里面是什么。
═══════════════════════════════════════════
```

## License

MIT

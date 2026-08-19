#!/usr/bin/env python3
"""
🔥 CodeRoast — AI 代码烤肉架
分析代码文件，生成阴阳怪气的 Code Review 评论
"""

import sys
import os
import re
import random
import hashlib
from datetime import datetime

LANG_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".java": "Java", ".c": "C", ".cpp": "C++", ".cs": "C#",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby",
    ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
    ".sh": "Shell", ".lua": "Lua", ".html": "HTML",
    ".css": "CSS", ".sql": "SQL", ".r": "R",
    ".dart": "Dart", ".scala": "Scala", ".elm": "Elm",
}

OBJECTIONABLE_NAMES = re.compile(r"^(a|b|c|d|x|y|z|tmp|temp|foo|bar|baz|data|result|val|obj)$", re.IGNORECASE)

OVERALL_RATINGS = [
    ("🟢 Excellent",      "这是人类能写出来的代码吗？太干净了"),
    ("🟡 Acceptable",     "能跑，但建议下次先想清楚再动手"),
    ("🟡 Needs Work",     "改改还能用，不改会出事"),
    ("🔴 Needs Improvement","这代码看起来像是在 deadline 前 2 小时写的"),
    ("💀 What Is This",    "我相信这不是你最佳状态"),
]

def pick(rng, lst, n=1):
    return rng.sample(lst, min(n, len(lst)))

def seedFromFile(filepath):
    with open(filepath, "rb") as f:
        content = f.read()
    seed = int(hashlib.md5(content).hexdigest(), 16) & 0xFFFFFFFF
    random.seed(seed)

def detectLang(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    return LANG_MAP.get(ext, "Unknown")

def analyzeCode(content, lines):
    rng = random.Random(random.randint(0, 999999))
    
    issues = {
        "naming": [],
        "style": [],
        "logic": [],
        "security": [],
        "architecture": [],
    }
    
    # 检查变量命名
    for i, line in enumerate(lines):
        # 找赋值
        m = re.search(r"(\w+)\s*=\s*", line)
        if m:
            name = m.group(1)
            if OBJECTIONABLE_NAMES.match(name):
                issues["naming"].append(
                    f"第{i+1}行: 变量名 '{name}' 请改成人类能读的名字")
    
    # 检查魔法数字
    magic_nums = []
    for i, line in enumerate(lines):
        nums = re.findall(r"\b(?<![\w.])(\d{3,})\b", line)
        for n in nums:
            if n not in ("200", "404", "500", "301", "302", "400", "403", "201", "100", "8080"):
                magic_nums.append(f"第{i+1}行: 魔法数字 {n} 是什么意思？常量定义不会用吗")
    if magic_nums:
        issues["style"].extend(magic_nums[:3])
    
    # 检查 TODO/FIXME
    todo_count = sum(1 for l in lines if "TODO" in l.upper() or "FIXME" in l.upper())
    if todo_count > 0:
        issues["style"].append(f"发现 {todo_count} 个 TODO/FIXME，\
        你的'以后再改'大概是永远不打算改吧")
    
    # 检查嵌套深度
    max_indent = 0
    for i, line in enumerate(lines):
        indent = len(line) - len(line.lstrip())
        if indent > max_indent:
            max_indent = indent
    if max_indent >= 24:
        issues["architecture"].append(
            f"最大缩进 {max_indent//4} 层，if 套 if 套 if 套 if...你在建套娃吗")
    
    # 检查函数长度
    func_lengths = []
    current_func = None
    func_start = 0
    for i, line in enumerate(lines):
        if re.search(r"\b(def |function |func |void |public |private |protected )", line):
            if current_func:
                func_lengths.append((current_func, func_start, i - func_start))
            current_func = re.search(r"(\w+)\s*\(", line)
            current_func = current_func.group(1) if current_func else "?"
            func_start = i
    if current_func:
        func_lengths.append((current_func, func_start, len(lines) - func_start))
    
    long_funcs = [(name, ln) for name, _, ln in func_lengths if ln > 50]
    if long_funcs:
        for name, ln in long_funcs[:2]:
            issues["architecture"].append(
                f"函数 '{name}' 有 {ln} 行长，建议拆成微服务（开玩笑的但真的该拆）")
    
    # 检查 eval/exec
    if "eval(" in content or "exec(" in content:
        issues["security"].append("检测到 eval/exec，你是想给攻击者开后门吗")
    
    # 检查硬编码密码
    if re.search(r"(password|passwd|secret|api_key|token)\s*=\s*['\"]\w+['\"]", content, re.IGNORECASE):
        issues["security"].append("把密钥硬编码进去，你是在给黑客送业绩")
    
    # 检查 TODO in production patterns
    if "console.log" in content and "debugger" in content:
        issues["style"].append("console.log + debugger 都还没删，你是准备部署到生产吗")
    
    # 检查重复代码（简单版）
    line_counts = {}
    stripped_lines = [l.strip() for l in lines if l.strip() and not l.strip().startswith(("#", "//", "/*", "*"))]
    for line in stripped_lines:
        line_counts[line] = line_counts.get(line, 0) + 1
    dups = [(l, c) for l, c in line_counts.items() if c > 2]
    if dups:
        issues["logic"].append(f"发现 {len(dups)} 行重复代码，\
        复制粘贴工程师证书已颁发")
    
    # Random fillers if not enough issues found
    fillers = {
        "naming": [
            "命名风格不够一致，建议统一驼峰或下划线",
            '有些变量名太短，改成长一点的不会编译不过的',
        ],
        "style": [
            "缩进不一致，是用 Tab 还是空格？不能两个都要",
            "空行太多，这不是诗歌比赛",
            "单行超过 120 字符，你的显示器是不是特别宽",
        ],
        "logic": [
            "这个 if 永远不会执行，恭喜你写了死代码",
            "return 之后的代码是给鬼看的吗",
            "这个循环可能永远不会 break",
            "异常被 catch 了但什么都没做，吞异常是什么新爱好",
        ],
        "security": [
            "没有输入校验，SQL 注入了解一下",
            "用 GET 传敏感数据，你是在 URL 上挂横幅吗",
        ],
        "architecture": [
            "建议把这个函数拆成几个小函数",
            "耦合度太高，牵一发动全身",
            "这个类有 2000 行，你确定这是单一职责？",
        ],
    }
    
    for cat in issues:
        while len(issues[cat]) < 2:
            issues[cat].append(random.choice(fillers[cat]))
    
    # 限制每个类别最多 3 条
    for cat in issues:
        issues[cat] = issues[cat][:3]
    
    return issues


def roast(filepath):
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return
    
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    lines = content.split("\n")
    line_count = len(lines)
    lang = detectLang(filepath)
    
    seedFromFile(filepath)
    
    issues = analyzeCode(content, lines)
    
    rating_idx = random.randint(0, len(OVERALL_RATINGS) - 1)
    rating, rating_desc = OVERALL_RATINGS[rating_idx]
    
    verdicts = [
        "这段代码就像是用 Google Translate 翻译了三次的菜谱。它能跑，但你不想知道里面是什么。",
        "如果把代码质量比做食物，这大概是食堂阿姨最后五分钟炒出来的。能吃，但别问是什么。",
        "这段代码的存在证明了人类可以在不思考的情况下打字。",
        "你的代码让我想起了一句话：'它不是 bug，是特性'。不，它就是 bug。",
        "经过仔细审阅，我发现这段代码的最佳部分是注释里的作者名字。",
        "这代码跑起来就像一个人穿着拖鞋跑马拉松——能到终点，但画面不忍直视。",
    ]
    verdict = random.choice(verdicts)
    
    print(f"\n🔥 🔥 🔥 CodeRoast — 正在烤你的代码 🔥 🔥 🔥")
    print(f"\n📄 文件: {os.path.basename(filepath)} ({line_count} 行)")
    print(f"🐍 检测到语言: {lang}")
    print()
    print("═" * 49)
    print("  🎤 Review 评审意见")
    print("═" * 49)
    print()
    print(f"整体评价: {rating}")
    print(f"  {rating_desc}")
    print()
    
    categories = [
        ("📌 代码风格", "style"),
        ("🐛 逻辑问题", "logic"),
        ("🏗️ 架构建议", "architecture"),
        ("🔒 安全警告", "security"),
        ("🏷️ 命名问题", "naming"),
    ]
    
    for title, key in categories:
        if issues[key]:
            print(f"\n{title}:")
            for item in issues[key]:
                print(f"  - {item}")
    
    print()
    print(f"总评: {'💀'}")
    print(f"  {verdict}")
    print("═" * 49)


def main():
    if len(sys.argv) < 2:
        print("Usage: python coderoast.py <代码文件路径>")
        print("Example: python coderoast.py mycode.py")
        sys.exit(1)
    
    filepath = sys.argv[1].strip()
    roast(filepath)


if __name__ == "__main__":
    main()

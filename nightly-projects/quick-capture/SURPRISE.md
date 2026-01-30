# 🎁 Surprise for You!

两个实用的 CLI 工具，已安装到 `~/bin/`

## 📝 qn - Quick Notes (增强版)

**新增功能：**
- 🏷️ **标签支持**: `qn "学习 AI #learning #ai"`
- 🔍 **搜索功能**: `qn --search "AI"`
- 📊 **标签统计**: `qn --tags`
- 📅 **最近笔记**: `qn --recent`

**基础功能：**
```bash
qn "Buy milk"              # 快速记笔记
qn -m "多行\n笔记"         # 多行笔记
qn --today                 # 查看今天笔记
```

## 📦 qc - Quick Capture (新工具!)

**功能：**
- 快速捕获任务、想法、bug
- 自动分类（通过 #idea, #bug, #todo 标签）
- 任务清单管理
- 一键导出到 memory

**使用：**
```bash
qc "great idea #idea"      # 捕获想法
qc "fix bug #bug"          # 捕获bug
qc -l                      # 查看所有捕获
qc --toggle 83be7663       # 标记完成
qc --export                # 导出到 memory
```

## 📁 安装位置

```
~/bin/
├── qn  # Quick Notes
└── qc  # Quick Capture
```

## 🔄 更新命令

```bash
# 更新所有工具
cp /home/zous/clawd/nightly-projects/quick-capture/* ~/bin/
chmod +x ~/bin/qn ~/bin/qc
```

## 🎯 为什么这两个工具有用？

**qn** - 融入你的写作/思考流程
- 随时记录灵感
- 用标签组织
- 随时搜索

**qc** - 快速捕获碎片想法
- 不打断当前工作
- 分类管理
- 定期清理/导出

## 两者配合使用

```bash
# 写代码时快速记录想法
qc "可以用 AI 优化这个函数 #idea"

# 写文档时记录笔记
qn "AI 优化技巧 #coding #ai"

# 晚上整理到 memory
qn --search "AI"
qc --export
```

---

 Enjoy! 🚀

# Revive Items Project

## 项目简介
大学生中常有一些闲置物品，想要“复活”它们（捐送 / 出售 / 转让）。本项目提供一个轻量级的物品发布与检索工具，包含 Web GUI 与 CLI 两种使用方式，使用 SQLite 做数据持久化，易于部署与扩展。

## 功能
- 添加物品（名称、描述、联系人信息）
- 列表展示物品，按时间倒序
- 模糊搜索（名称/描述/联系人）
- 查看单条物品详情
- 删除物品（带确认）
- 提供 JSON API：`/api/items` 和 `/api/items/<id>`
- 支持 CLI 操作：`manage.py`

## 技术栈
- Python 3.8+
- Flask + Flask-SQLAlchemy
- SQLite（`database.db`）

## 快速启动（开发）
1. 克隆仓库并进入目录
2. (可选) 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate      # Windows

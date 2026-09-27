# AI 内容工厂

一个基于多 Agent 协作的 AI 内容生产工具。
每天点一下按钮，自动抓取热点，一键生成 5 个平台（抖音、小红书、公众号、B站、微博）的图文文案。

## 功能特性

- 多 Agent 协作：猎手 Agent 抓热点 → 写手 Agent 生成文案 → 发布员归档
- 5 平台独立风格：每个平台有独立的 Prompt 模板
- 真实数据源：从 IT之家 RSS 抓取实时新闻，AI 筛选 AI 相关热点
- GUI 界面：基于 tkinter，双击运行，无需命令行
- 后台线程：生成过程不卡界面，实时显示进度
- 双通道日志：客户看到进度，技术细节写本地文件
- API Key 验证：首次运行时真实请求 DeepSeek 验证 Key 有效性

## 技术栈

- 大模型：DeepSeek（OpenAI 兼容接口）
- GUI：tkinter
- 多线程：threading
- 新闻抓取：feedparser + requests + BeautifulSoup
- 打包：PyInstaller
- 安装包：Inno Setup

## 项目结构

    Multi-Agent Pipeline one/
    ├── app.py                # GUI 入口
    ├── agent_hunter.py       # 猎手 Agent
    ├── agent_writer.py       # 写手 Agent
    ├── agent_publisher.py    # 发布员 Agent
    ├── tools_web.py          # 新闻抓取工具
    ├── paths.py              # 统一路径管理
    ├── prompts/              # 5 平台人设模板
    │   ├── dy.txt
    │   ├── xhs.txt
    │   ├── wechat.txt
    │   ├── bilibili.txt
    │   └── weibo.txt
    ├── requirements.txt
    └── README.md

## 快速开始

### 1. 安装依赖

    pip install -r requirements.txt

### 2. 获取 API Key

访问 https://platform.deepseek.com 注册账号，创建 API Key。

### 3. 运行

    python app.py

首次运行会弹出窗口，粘贴 API Key 即可。

## 打包成 exe

    python -m PyInstaller --onefile --windowed --name "AI内容工厂" --add-data "prompts;prompts" app.py

## 数据存放位置

- 程序资源：打包进 exe
- 用户数据（API Key、生成结果）：Documents/AI内容工厂/

## License

MIT
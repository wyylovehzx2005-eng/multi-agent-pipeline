#agent_hunter.py
#职责：收集今日ai热点，输出结构化列表

import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from paths import KEY_FILE
load_dotenv(KEY_FILE)

from tools_web import fetch_ai_news

today = datetime.now().strftime("%Y年%m月%d日")
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

HUNTER_SYSTEM_PROMPT = """你是一个AI领域的热点猎手。

你的任务：
1. 仔细阅读用户提供的科技新闻素材，从中筛选出与【人工智能/AI】最相关的 5 条热点。
2. 如果某条新闻只是纯粹的商业政策、手机发布、汽车保险等与AI无关,请直接忽略它。
3. 每个热点必须单独占一行，严格采用 "标题 | 摘要 | 热度" 的格式。
4. 标题、摘要、热度之间用竖线（|）隔开，不要加任何多余的标点。热度只能是：高/中/低。
5. 只输出这5行内容,不要任何前言、后语,不要序号,不要Markdown格式。

输出示例：
OpenAI发布新模型 | 该模型在逻辑推理上大幅提升 | 高
Meta开源新工具 | 开发者可免费用于商业项目 | 中
"""

def hunt_hotspots():
    print(f"热点猎手正在抓取{today}的真实新闻...")

    raw_news = fetch_ai_news()
    if not raw_news:
        return"抓取新闻失败,请检查网络或RSS源"

    context_text = "\n\n".join(raw_news)
    print(f"成功抓取{len(raw_news)}条新闻,正在交由大模型提炼...\n")
    user_prompt = f"今天是{today},以下是今天的科技新闻素材:\n\n{context_text}\n\n请根据此提炼今日AI热点"
    print(f"🔍 即将发给大模型的用户提示词: {user_prompt[:200]}...")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role":"system","content":HUNTER_SYSTEM_PROMPT},
            {"role":"user","content":user_prompt}
        ],
        temperature=0.3
    )

    

    # ============ 获取大模型纯文本回复
    raw_text = response.choices[0].message.content

    # ============ 纯文本转化列表
    hotspot_list = []

    lines = raw_text.strip().split("\n") #strip 清空多余符号 split 切开

    for line in lines:
        line = line.strip()

        if not line:
            continue

        parts = line.split("|")
        if len(parts) != 3:
            continue

        title = parts[0].strip()
        summary = parts[1].strip()
        heat = parts[2].strip()

        hotspot_list.append({
            "标题":title,
            "摘要":summary,
            "热度":heat
        })

    return hotspot_list

if __name__ == "__main__":
    # 1. 拿到结果（千万不能漏掉这一行）
    result = hunt_hotspots()

    # 2. 兜底判断：如果结果是字符串，说明抓取失败
    if isinstance(result, str):
        print(result)  # 直接打印错误信息，程序不会崩溃
        
    # 3. 如果结果是列表，说明抓取成功，进行格式化打印
    else:
        for i, item in enumerate(result, 1):
            # 把之前的逗号改成句号，排版更清爽
            print(f"{i}.【{item['标题']}】{item['摘要']}({item['热度']})")
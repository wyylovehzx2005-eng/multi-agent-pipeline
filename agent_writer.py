# 职责：调用猎手拿到的热点，生成抖音图文文案

import os
from openai import OpenAI
from dotenv import load_dotenv
from agent_hunter import hunt_hotspots
from paths import PROMPTS_DIR
from paths import KEY_FILE
load_dotenv(KEY_FILE)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def load_prompt(platform):
    prompt_path = os.path.join(PROMPTS_DIR, f"{platform}.txt")

    if not os.path.exists(prompt_path):
        return None
    with open(prompt_path,"r",encoding="utf-8") as f:
        return f.read()

def parse_article(raw_text):
    """用代码严格解析大模型返回的文章,确保结构稳定"""
    title = ""
    content = ""

    if"【标题】"not in raw_text or "【正文】"not in raw_text :
        return{
            "title": "格式解析失败",
            "content": raw_text,  # 直接把原始内容丢进去，便于你排查
            "tags": ""
        }
    parts = raw_text.split("【标题】")[1]
    title = parts.split("【正文】")[0].strip()
    content = raw_text.split("【正文】")[1].strip()

    return {
        "title":title,
        "content":content,
    }

def write_article(platform):

    selected_prompt = load_prompt(platform)
    if selected_prompt is None:
        return f"找不到平台{platform}的人设文件,请检查prompts/{platform}.txt是否存在"
    print(f"✍️ 写手已就位，正在为【{platform}】撰写文章...")

    hotspots = hunt_hotspots()

    if isinstance(hotspots,str):
        return hotspots

    hotspot_lines = []
    for i,item in enumerate(hotspots,1):
        line = f"{i},{item['标题']},{item['摘要']}"
        hotspot_lines.append(line)

    context_text = "\n".join(hotspot_lines)

    print(f"成功拿到{len(hotspots)}条热点,正在加工成文案...\n")

    user_prompt = f"请根据以下今天的AI热点,写一篇文案:\n\n{context_text}"
    response = client.chat.completions.create(
        model="deepseek-chat",  # 记得用稳定的模型名字
        messages=[
            {"role": "system", "content": selected_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8
    )
    raw_test = response.choices[0].message.content
    article_dict = parse_article(raw_test)
    return article_dict

if __name__ == "__main__":
    article_data = write_article()
    
    if isinstance(article_data, str):
        # 如果猎手抓取失败
        print(article_data)
    else:
        # 格式化打印提取出来的结果
        print("===== 图文文案 解析结果 =====\n")
        print(f"📌 标题：{article_data['title']}")
        print(f"\n📝 正文：\n{article_data['content']}")

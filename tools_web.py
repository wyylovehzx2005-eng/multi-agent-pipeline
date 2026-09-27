#职责：专门负责去互联网上抓取真实的AI新闻

import requests
import feedparser
from fake_useragent import UserAgent
from bs4 import BeautifulSoup  #清洗HTML

def clean_html(raw_html):
    """把带有html标签的乱码清洗成干净的纯文本"""
    if not raw_html:
        return""
    soup = BeautifulSoup(raw_html,"html.parser")
    return soup.get_text(separator="",strip=True)

def fetch_ai_news():
    """从RSS源获取最新的AI新闻,返回文本列表"""

    #以国内常用的科技新闻源为例

    rss_url = "https://www.ithome.com/rss/"

    ua = UserAgent()
    headers = {
        "User-Agent":ua.random
    }

    news_list = []
    try:

        # 发送网络请求
        response = requests.get(rss_url,headers=headers,timeout=10)

        # 解析RSS源
        feed = feedparser.parse(rss_url)
        

        # 提取前10条新闻
        for entry in feed.entries[:10]:
            clean_summary = clean_html(entry.summary)
            news_item = f"标题：{entry.title}\n摘要:{clean_summary}"
            news_list.append(news_item)
    except Exception as e:
        print(f"抓取出错了，{e}")

    return news_list

if __name__ == "__main__":
    news = fetch_ai_news()
    print(f"成功抓取到{len(news)}条新闻")
    print("\n第一条示例")
    print(news[0])
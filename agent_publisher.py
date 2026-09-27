import os
from datetime import datetime
from agent_writer import write_article
from paths import OUTPUT_DIR

def save_article(article_data,platform):
    """把结构化文章保存到本地Markdown文件"""

    # ============ 准备好保存路径：output/日期/
    today_str = datetime.now().strftime("%Y年%m月%d日")

    time_str = datetime.now().strftime("%H-%M-%S")
    output_dir = os.path.join(OUTPUT_DIR, today_str, platform, time_str)

    # ============ 如果文件夹不存在，自动创建
    os.makedirs(output_dir,exist_ok=True)

    # ============ 准备好文件夹
    safe_title = article_data['title']
    for char in ['/', '\\', ':', '"', '?', '*', '<', '>', '|']:
        safe_title = safe_title.replace(char, "_")
    file_path = os.path.join(output_dir,f"{safe_title}.md") #!!!!

    # ============ 组装最终写进文件的内容
    final_content = f"""
【标题】{article_data['title']}
【正文】{article_data['content']}
    """

    # ============ 写入文件
    with open(file_path,"w",encoding="utf-8") as f:
        f.write(final_content)
    print(f"文件已成功归档：{file_path}")
    return file_path

if __name__ == "__main__":
    print('发布员正在启动...')

     # 要生成的5个平台
    platforms = ["dy", "xhs", "wechat", "bilibili", "weibo"]
    
    for platform in platforms:
        print(f"\n{'='*40}")
        print(f"🎯 正在为【{platform}】生成文案...")
        print(f"{'='*40}")
        
        article_data = write_article(platform)

        # ============ 安全缓冲
        if isinstance(article_data,str):
            print(article_data)
        else:
            save_article(article_data,platform)
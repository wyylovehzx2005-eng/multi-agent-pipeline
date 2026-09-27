# 职责：AI内容工厂的图形界面(GUI)
import os
import tkinter as tk
import threading
import sys
from tkinter import messagebox
from datetime import datetime
from paths import LOG_FILE, OUTPUT_DIR
from paths import KEY_FILE
# ============================================================
# 【首次运行检查】确保客户配置了 API Key
# ============================================================
def verify_api_key(api_key):
    """
    真实握手验证：发一个最简请求给 DeepSeek，看能不能通过
    返回 (is_valid, message)
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            timeout=10,
            max_retries=0,
        )

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5,
        )

        
        if response.choices:
            return True, "✅ API Key 验证通过！"
        else:
            return False, "❌ 服务器未返回有效响应，请重试"
    
    except Exception as e:
        err = str(e).lower()

        if "401" in err or "authentication" in err or "invalid" in err:
            return False, "❌ API Key 无效，请检查是否复制完整"
        elif "402" in err or "insufficient" in err or "quota" in err:
            return False, "❌ 账户余额不足，请先到 DeepSeek 充值"
        elif "timeout" in err or "connection" in err:
            return False, "❌ 网络连接失败，请检查网络后重试"
        else:
            return False, f"❌ 验证失败：{e}"

def has_valid_key():
    """检查 KEY_FILE 里是否已经写过 Key（不验证真假）"""
    if not os.path.exists(KEY_FILE):
        return False
    
    with open(KEY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 只要文件里有"DEEPSEEK_API_KEY="且后面有非空内容，就认为已经配置过
    if "DEEPSEEK_API_KEY=" in content:
        key = content.split("DEEPSEEK_API_KEY=")[1].split("\n")[0].strip()
        return len(key) > 0
    
    return False


def show_key_dialog(parent):
    """弹出窗口，让客户输入 API Key。返回 True 表示成功保存"""
    result = [False]  # 用列表装，方便在内层函数里改

  
    dialog = tk.Toplevel(parent)
    dialog.lift()
    dialog.attributes('-topmost', True)
    dialog.title("首次使用 - 配置 API Key")
    dialog.geometry("560x400")
    # 标题
    tk.Label(
        dialog,
        text="欢迎使用 AI 内容工厂",
        font=("微软雅黑", 16, "bold"),
    ).pack(pady=15)

    # 说明文字
    tk.Label(
        dialog,
        text=(
            "首次使用需要配置 DeepSeek API Key。\n\n"
            "步骤：\n"
            "1. 浏览器访问 platform.deepseek.com\n"
            "2. 注册账号并登录\n"
            "3. 左侧菜单找到「API Keys」\n"
            "4. 点击「创建 API Key」并复制\n"
            "5. 粘贴到下方输入框"
        ),
        justify="left",
        font=("微软雅黑", 11),
    ).pack(pady=10, padx=30)

    # 输入框
    entry = tk.Entry(dialog, width=50, font=("Consolas", 11))
    entry.pack(pady=10)

    def save_key():
        key = entry.get().strip()
        if not key:
            messagebox.showwarning("提示", "请先粘贴你的 API Key", parent=dialog)
            return


        
        # 禁用按钮，改文字，让用户知道正在验证
        save_btn.config(state="disabled", text="正在验证，请稍候...")
        dialog.update()
        dialog.update_idletasks()
        
        # 直接同步调用（阻塞 1-3 秒）
        is_valid, msg = verify_api_key(key)
        if is_valid:
            with open(KEY_FILE, "w", encoding="utf-8") as f:
                f.write(f"DEEPSEEK_API_KEY={key}")
            messagebox.showinfo("成功", msg + "\n软件即将启动",parent=dialog)
            result[0] = True
            dialog.destroy()
        else:
            save_btn.config(state="normal", text="验证并保存")   # ← 先恢复
            messagebox.showerror("验证失败",msg,parent=dialog)   # ← 再弹框       
       
    save_btn = tk.Button(
        dialog,
        text="验证并保存",
        font=("微软雅黑", 12),
        command=save_key,
        )
    save_btn.pack(pady=15)
    dialog.wait_window()    # 等待弹窗被关闭
    return result[0]        # 把结果返回给调用者

# ---------- 启动前检查 ----------
# 1. 创建唯一的根窗口
root = tk.Tk()
root.title("AI内容工厂")
root.geometry("1920x1080")

# 2. 先隐藏，等验证通过再显示
root.withdraw()

# 3. 检查 Key，没有就弹窗
if not has_valid_key():
    success = show_key_dialog(root)
    if not success:
        print("用户未配置 API Key,程序退出")
        sys.exit(0)

# 4. 显示主窗口
root.deiconify()

# 5. 确保 output 目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 6. 从这里开始，添加主界面组件
# 增加标题文字
title_lable = tk.Label(
    root, #指定窗口
    text="AI内容工厂",   #命名
    font=("微软雅黑",24,"bold"),   #确定字体
)

title_lable.pack(pady=20)    #上下空白 pady=距离20

log_text = tk.Text(
    root,
    height=20,
    width=80,
    font=("Consolas",11),
    bg="#1e1e1e",
    fg="#00ff00",
)
log_text.pack(pady=10,padx=20)

def log_ui(msg):
    """把消息显示到界面(客户展示)"""
    def _do():
        log_text.insert("end",msg + "\n")
        log_text.see("end")
    root.after(0,_do)

def log_file(msg):
    """把消息写到本地文件（客户看不到）"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")


def log(msg, ui=True):
    """
    统一日志入口
    ui=True  → 客户看得到（进度通知）
    ui=False → 只在本地文件里（技术细节）
    """
    if ui:
        log_ui(msg)
    log_file(msg)

def run_business():
    log("开始生成任务...")
    try:
        from agent_writer import write_article
        from agent_publisher import save_article

        platforms = ["bilibili","dy","wechat","weibo","xhs"]
        for platform in platforms:
            log(f"正在生成{platform}...")

            article_data = write_article(platform)
            if isinstance(article_data,str):
                log(f"{platform}失败{article_data}")
            else:
                save_article(article_data,platform)
                log(f"{platform}完成")

        log("全部完成,请到output文件夹查看")

    except Exception as e:
        log(f"出错了：{e}")
    
        

def on_click():
    log("\n========== 开始新任务 ==========")
    
    # 创建后台线程，让它去跑 run_business
    thread = threading.Thread(target=run_business, daemon=True)
    thread.start()
    

generate_btn = tk.Button(
    root,
    text="一键生成今日内容", #按扭文字内容
    font=("微软雅黑",14),     #字体字号
    command=on_click,       #绑定点击事件
)

generate_btn.pack(pady=10)

root.mainloop()
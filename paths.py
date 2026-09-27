import os
import sys

# 判断：是被 exe 启动，还是被 python 启动
if getattr(sys, "frozen", False):
    # 打包后：base_dir 就是 exe 所在目录
    BASE_DIR = os.path.dirname(sys.executable)
    INTERNAL_DIR = sys._MEIPASS
else:
    # 普通运行：base_dir 是当前文件（paths.py）所在目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INTERNAL_DIR = BASE_DIR

# 常用子目录，全都从这里派生
# 程序资源：跟 exe 走（打包进 exe 的 prompts）
PROMPTS_DIR = os.path.join(INTERNAL_DIR, "prompts")

# 用户数据：放在"文档/AI内容工厂/"下
# 原因：Program Files 是系统保护目录，普通程序不能写入
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "Documents", "AI内容工厂")
os.makedirs(USER_DATA_DIR, exist_ok=True)

OUTPUT_DIR = os.path.join(USER_DATA_DIR, "output")
KEY_FILE = os.path.join(USER_DATA_DIR, "deepseekkey.env")
LOG_FILE = os.path.join(OUTPUT_DIR, "debug.log")
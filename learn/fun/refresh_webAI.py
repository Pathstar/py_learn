import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options    # 新增
# chromedriver 路径
chromedriver_path = r"D:\garbages\Python\.venv\chromedriver-win64\chromedriver.exe"
# 需要打开的URL
url = "https://console-kwe.his.huawei.com/ai/tenant/micro/#/workSpace/iframe/ModelExperience?service_code=workSpace&model_name=ChatGPT-V4.1-%2525E5%2525A4%252596%2525E9%252583%2525A8API&desktopType=personal"
# 创建 Chrome 启动参数
chrome_options = Options()
# chrome_options.add_argument('--headless')   # 无头模式
chrome_options.add_argument('--disable-gpu') # 可选：有些环境下可防 bug
chrome_options.add_argument('--window-size=1200,900') # 可选，某些网页需设定屏幕宽高
chrome_options.add_argument('--no-sandbox')  # 有时候能解决权限问题
# 启动浏览器
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
# 打开网页
driver.get(url)

log_filename = "refresh_webAI_" + datetime.now().strftime("%Y-%m-%d") + ".txt"
log_dir = os.path.join(os.path.dirname(__file__), "XDlogs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, log_filename)

_print = print
def print(*args, **kwargs):
    message = " ".join(map(str, args))
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    _print(*args, **kwargs)
    return print

try:
    while True:
        print(f"{time.strftime('%H:%M:%S')} refresh...")
        driver.refresh()
        # 每隔 10 分钟刷新一次（10 * 60 = 600 秒）
        time.sleep(600)
except KeyboardInterrupt:
    print(f"{time.strftime('%H:%M:%S')} Terminating...")
finally:
    driver.quit()
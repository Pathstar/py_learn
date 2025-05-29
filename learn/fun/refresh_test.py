import os
import time
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# chromedriver 路径
chromedriver_path = r"D:\garbages\Python\.venv\chromedriver-win64\chromedriver.exe"
# 需要后台定时刷新的URL
url1 = "https://console-kwe.his.huawei.com/ai/tenant/micro/#/workSpace/iframe/ModelExperience?service_code=workSpace"
# 你要停留的主窗口URL
url2 = "https://console-kwe.his.huawei.com/ai/tenant/micro/#/workSpace/iframe/ModelExperience?service_code=workSpace&model_name=ChatGPT-V4.1-%E5%A4%96%E9%83%A8API"
# 日志目录及文件名
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
# 后台刷新的Selenium线程
def refresh_thread():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url1)
    try:
        while True:
            print(f"{time.strftime('%H:%M:%S')} 刷新 {url1} ...")
            driver.refresh()
            time.sleep(300)
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')} 后台刷新线程异常: {e}")
    finally:
        driver.quit()
# 启动后台刷新线程
t = threading.Thread(target=refresh_thread, daemon=True)
t.start()
# 主页面Selenium实例
chrome_options2 = Options()
chrome_options2.add_argument('--disable-gpu')
chrome_options2.add_argument('--no-sandbox')
service2 = Service(executable_path=chromedriver_path)
driver2 = webdriver.Chrome(service=service2, options=chrome_options2)
driver2.get(url2)
print(f"{time.strftime('%H:%M:%S')} 主页面已打开 {url2}，你可以正常操作、不受后台刷新影响。")
print("如需退出请关闭本窗口或Ctrl+C。后台刷新线程会随主进程退出而自动终止。")
try:
    while True:
        time.sleep(600)   # 主循环只是保持主页面不退出
except KeyboardInterrupt:
    print(f"{time.strftime('%H:%M:%S')} 程序已结束。")
finally:
    driver2.quit()
import re
import os
from selenium import webdriver
from time import sleep
# 1. 读取 download.txt
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chromedriver_path = r"D:\garbages\Python\.venv\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--disable-gpu') # 可选：有些环境下可防 bug
chrome_options.add_argument('--window-size=1200,900')
chrome_options.add_argument('--no-sandbox')  # 有时候能解决权限问题
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
def codehub_downloader():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "download.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 2. 正则提取 href 链接
    pattern = r'href="(/api/codehub/v1/[^"]+)"'
    relative_urls = re.findall(pattern, content)
    # 3. 拼接完整链接
    full_links = ["https://codehub-y.huawei.com"+url for url in relative_urls]
    print("共找到链接数量:", len(full_links))
    # 4. 用Selenium自动打开（每隔3秒打开一个）
    url = "https://console-kwe.his.huawei.com/ai/tenant/micro/#/workSpace/iframe/ModelExperience?service_code=workSpace&model_name=ChatGPT-V4.1-%2525E5%2525A4%252596%2525E9%252583%2525A8API&desktopType=personal"
    driver.get(url)
    for link in full_links:
        print(link)
    input("ready?")
    for link in full_links:
        # print(link)
        driver.execute_script(f'window.open("{link}");')
        # sleep(3)  # 每3秒打开一个窗口页
    print("所有链接已打开。")
    while True:
        if input("OK?") == "OK":
            break

if __name__ == '__main__':
    codehub_downloader()
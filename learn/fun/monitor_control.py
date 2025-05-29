import os
import time
from datetime import datetime


# import math
def main():
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"\n{time.strftime('%H:%M:%S')} #\n")
    inp = input(f"{time.strftime('%H:%M:%S')} Please enter minutes: ").strip()
    # like: 1 1.1 1 1
    #close after 1min, 1.1min light it up,....
    times = []
    if not inp:
        times = [10,40,60,-2]

    # 允许小数输入，非法输入会被忽略
    for x in inp.split():
        try:
            f = float(x)
            times.append(f)
        except ValueError:
            print(f"{time.strftime('%H:%M:%S')} Skipped invalid input: {x}")
            times.append(10)
    if not times:
        print(f"{time.strftime('%H:%M:%S')} No valid time input.")
        return
    # if not os.path.exists("nircmd.exe"):
    #     print("nircmd.exe not found! Please put it in the same folder as this script.")
    #     return
    print(f"{time.strftime('%H:%M:%S')} Task List: {', '.join(str(x) for x in times)}")
    for idx, minutes in enumerate(times):
        # 舍弃小数部分
        match minutes:
            case -1:
                os.system('cmd /c "shutdown /s /f /t 60"')
                print(f"{time.strftime('%H:%M:%S')} -> shutdown /s /f /t 60")
                continue
            case -2:
                time.sleep(1)
                os.system('nircmd.exe sendkeypress ctrl')
                print(f"{time.strftime('%H:%M:%S')} -> pin")
                continue
        seconds = int(minutes * 60)
        # seconds = max(seconds, 0)
        print(f"{time.strftime('%H:%M:%S')} Step {idx+1}: Wait {minutes} minute(s) ({seconds} seconds)...")
        time.sleep(seconds)
        if idx % 2 == 0:
            print(f"{time.strftime('%H:%M:%S')} -> Turn off monitor")
            os.system('cmd /c "nircmd.exe monitor off"')
        else:
            print(f"{time.strftime('%H:%M:%S')} -> Wake up monitor by mouse")
            # os.system('cmd /c "nircmd.exe movecursor 100 0"')
            # time.sleep(1)
            # os.system('cmd /c "nircmd.exe movecursor -100 0"')
            os.system('cmd /c "nircmd.exe sendmouse right click"')
            # time.sleep(1)
            # os.system('cmd /c "nircmd.exe monitor on"')
            # os.system('nircmd.exe monitor on')
        # print("Done.\n")
    print(f"{time.strftime('%H:%M:%S')} All steps finished.")


# 获取当前日期，格式：YYYY-MM-DD
log_filename = "fun_" + datetime.now().strftime("%Y-%m-%d") + ".txt"
# 指定日志目录
log_dir = os.path.join(os.path.dirname(__file__), "XDlogs")
# 创建日志文件夹（如果不存在）
os.makedirs(log_dir, exist_ok=True)
# 日志文件完整路径
log_file_path = os.path.join(log_dir, log_filename)

_print = print
def print(*args, **kwargs):
    message = " ".join(map(str, args))
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    _print(*args, **kwargs)
    return print

if __name__ == "__main__":
    main()
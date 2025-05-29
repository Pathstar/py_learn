import time
import datetime
timestamp = 1800000000  # 示例时间戳，单位为秒
# 方法1：使用time模块
time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
print(time_str)  # 输出: 2023-06-01 12:00:00
# 方法2：使用datetime模块
dt = datetime.datetime.fromtimestamp(timestamp)
print(dt.strftime('%Y-%m-%d %H:%M:%S'))  # 同上


date_str = '2025-05-01 12:00:00'
# 方法1：用time模块
timestamp = int(time.mktime(time.strptime(date_str, '%Y-%m-%d %H:%M:%S')))
print(timestamp)  # 输出: 1685560800
# 方法2：用datetime模块
dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
timestamp = int(dt.timestamp())
print(timestamp)  # 同上
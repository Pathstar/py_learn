import threading
import time


class TimerFlag:
    def __init__(self, interval):
        self.flag = True
        self.interval = interval
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            self.flag = True
            time.sleep(self.interval)
            self.flag = False


timer_flag = TimerFlag(10)


def can_fetch():
    return timer_flag.flag


while True:
    input("")
    if can_fetch():
        print("可以拉新")
        timer_flag.flag = False  # 用完立即置False，等待下一个周期
    else:
        print("暂不可拉新")

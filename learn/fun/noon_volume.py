
import time
from datetime import datetime
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    scalar = volume_level / 100.0  # 0.0到1.0之间
    volume.SetMasterVolumeLevelScalar(scalar, None)


def wait_until(target_hour, target_minute):
    now = datetime.now()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if now > target_time:
        # 如果当前已过该时间，则等待到明天的13:59
        # target_time += timedelta(days=1)
        time.sleep(600)
        print(f"过时，等待10分钟")
        return
    seconds_to_wait = (target_time - now).total_seconds()
    print(f"当前时间 {now.strftime('%H:%M:%S')} ，将于 {target_time.strftime('%Y-%m-%d %H:%M:%S')} 开始提升音量 wait: {seconds_to_wait}")
    time.sleep(seconds_to_wait)


def process_volume(start_volume, end_volume, duration):
    for name, value in [('end_volume', end_volume),
                        ('start_volume', start_volume),
                        ('duration', duration)]:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} 必须为int或float，但实际类型为 {type(value)} (值为 {value})")
    steps = abs(start_volume - end_volume)
    if steps == 0:
        set_volume(start_volume)
        print(f"已设置音量为：{start_volume}% {datetime.now()}")
    else:
        interval = duration / steps
        step = 1 if end_volume > start_volume else -1
        for i in range(steps + 1):
            current_vol = start_volume + i * step
            set_volume(current_vol)
            print(f"已设置音量为：{current_vol}% {datetime.now()}")
            time.sleep(interval)

if __name__ == '__main__':
    target_hour, target_minute = 13, 58
    sleep_min = 0


    start_volume = 5
    end_volume = 15
    sec_end_volume = 20

    set_volume(start_volume)
    if sleep_min:
        print(f"sleep {sleep_min} minutes, {sleep_min*60} seconds")
        time.sleep( sleep_min*60 )
    else:
        wait_until(target_hour, target_minute)
    duration = 120
    # steps = end_volume - start_volume
    # interval = duration / steps if steps else duration
    process_volume( start_volume, end_volume, duration )
    time.sleep(300)
    process_volume(end_volume, sec_end_volume, duration)


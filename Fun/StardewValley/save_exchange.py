import os
import shutil
import datetime
import subprocess

# 获取 %appdata% 目录
appdata_path = os.getenv("APPDATA")

# 电脑存档路径
pc_saves_path = os.path.join(appdata_path, "StardewValley", "Saves")

# 手机存档路径 (在 Android 设备上的路径)
phone_saves_path = "/sdcard/Android/data/abc.smapi.gameloader/files/Saves"


# 获取电脑存档列表
def list_saves(folder_path):
    if not os.path.exists(folder_path):
        print(f"存档文件夹 {folder_path} 不存在！")
        return []
    return [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]


# 获取手机存档列表 (使用 adb)
def list_phone_saves():
    try:
        result = subprocess.run(["adb", "shell", "ls", phone_saves_path], capture_output=True, text=True)
        if result.returncode != 0:
            print("无法获取手机存档列表，请检查 adb 连接！")
            return []
        return result.stdout.strip().split("\n")
    except Exception as e:
        print(f"获取手机存档列表失败: {e}")
        return []


# 选择存档
def choose_save(saves):
    if not saves:
        print("没有找到存档！")
        exit()

    print("\n可用存档列表：")
    for i, save in enumerate(saves, 1):
        print(f"{i}. {save}")

    while True:
        try:
            choice = int(input("请选择存档 (输入数字): "))
            if 1 <= choice <= len(saves):
                return saves[choice - 1]
            else:
                print("输入错误，请输入正确的数字！")
        except ValueError:
            print("请输入数字！")


# 询问传输方向
direction = input("请输入传输方向 (1: 电脑传到手机, 2: 手机传到电脑): ")

# 根据传输方向列出存档并选择
if direction == "1":
    pc_saves = list_saves(pc_saves_path)
    map_name = choose_save(pc_saves)
    source_path = os.path.join(pc_saves_path, map_name)
    target_path = f"{phone_saves_path}/{map_name}"
elif direction == "2":
    phone_saves = list_phone_saves()
    map_name = choose_save(phone_saves)
    source_path = f"{phone_saves_path}/{map_name}"
    target_path = os.path.join(pc_saves_path, map_name)
else:
    print("输入错误，请输入 1 或 2")
    exit()

# 获取当前时间 (精确到秒)
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# 计算备份路径
# backup_base = os.path.join(appdata_path, "StardewValley", "backup", current_date)
backup_base = os.path.join(r"D:\111Pathstar111\LearningXD\garbages\Pycharm\Wordsheep\Fun\StardewValley\backup")
backup_root = os.path.join(backup_base, "PCToPhone" if direction == "1" else "PhoneToPC", current_time)

# 创建备份文件夹
os.makedirs(backup_root, exist_ok=True)

# 备份旧存档
if direction == "1":
    # 备份手机旧存档
    phone_old_path = os.path.join(backup_root, "Phone_old")
    result = subprocess.run(["adb", "shell", "ls", target_path], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        os.makedirs(phone_old_path, exist_ok=True)
        print(f"正在备份手机旧存档到 {phone_old_path}...")
        subprocess.run(["adb", "pull", target_path, phone_old_path])
        print(f"手机旧存档已备份至 {phone_old_path}")

    # 备份电脑新存档
    pc_new_path = os.path.join(backup_root, "PC_new")
    os.makedirs(pc_new_path, exist_ok=True)
    print(f"正在备份电脑新存档到 {pc_new_path}...")
    shutil.copytree(source_path, os.path.join(pc_new_path, map_name))
    print(f"电脑新存档已备份至 {pc_new_path}")

elif direction == "2":
    # 备份电脑旧存档
    pc_old_path = os.path.join(backup_root, "PC_old")
    if os.path.exists(target_path):
        os.makedirs(pc_old_path, exist_ok=True)
        print(f"正在备份电脑旧存档到 {pc_old_path}...")
        shutil.copytree(target_path, os.path.join(pc_old_path, map_name))
        print(f"电脑旧存档已备份至 {pc_old_path}")

    # 备份手机新存档
    phone_new_path = os.path.join(backup_root, "Phone_new")
    os.makedirs(phone_new_path, exist_ok=True)
    print(f"正在备份手机新存档到 {phone_new_path}...")
    subprocess.run(["adb", "pull", source_path, phone_new_path])
    print(f"手机新存档已备份至 {phone_new_path}")

# 传输存档
if direction == "1":
    print(f"正在传输存档到手机: {target_path}")
    subprocess.run(["adb", "push", source_path, phone_saves_path])
    print(f"存档已成功传输至手机 {target_path}")
elif direction == "2":
    print(f"正在传输存档到电脑: {target_path}")
    subprocess.run(["adb", "pull", source_path, target_path])
    print(f"存档已成功传输至电脑 {target_path}")


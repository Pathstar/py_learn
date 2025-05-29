import json
import os
import re
import subprocess
import time
from collections import Counter



def extract_certificate(hap_file_path):
    with open(hap_file_path, 'rb') as f:
        raw = f.read()
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
        content = raw.decode('latin1', errors='ignore')
    cert_pattern = r"(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)"
    match = re.search(cert_pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    else:
        print("No certificate found.")
        return None

def save_certificate_to_file(cert, dst, prefix):
    if cert:
        cert = cert.replace('\\n', '\n')
        out_file = os.path.join(dst, f"{prefix}.cer")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(cert)
        print(f"saved: {out_file}")
        return out_file

def get_cert_sha256(cert_path):
    """
    执行 keytool -printcert -file <cert_path>，提取 SHA256 指纹，去除冒号。
    :param cert_path: 证书文件路径
    :return: SHA256 指纹（无冒号），若未找到则返回 None
    """
    java_bin_dir = r"C:\Program Files\Java\jdk-20\bin"
    keytool_path = os.path.join(java_bin_dir, "keytool.exe")
    try:
        result = subprocess.run(
            [keytool_path, '-printcert', '-file', cert_path],
            capture_output=True, text=True, check=True,
            cwd=java_bin_dir
        )
        keytool_output = result.stdout
        print("keytool output:")
        # print(keytool_output)
        # 提取SHA256行（演示常见格式，遇到变种可调整正则）
        m = re.search(r'SHA256:\s*([A-Fa-f0-9:]+)', keytool_output)
        if m:
            sha256_with_colon = m.group(1)
            sha256_no_colon = sha256_with_colon.replace(':', '')
            return sha256_no_colon
        else:
            print("没有找到SHA256行。")
            return None
    except subprocess.CalledProcessError as e:
        print("keytool 执行出错!")
        print(e.stderr)
        return None

def extract_bundle_names(hap_file_path):
    with open(hap_file_path, 'rb') as f:
        raw = f.read()
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
        content = raw.decode('latin1', errors='ignore')
    pattern = r'["\']?bundleName["\']?\s*[:=]\s*[\'"]([\w\.]+)[\'"]'
    bundle_names = re.findall(pattern, content)
    if not bundle_names:
        print("未匹配到bundleName")
        input()

    counter = Counter(bundle_names)
    bundle_list = list(counter.keys())
    print("提取出的 bundleName：（出现次数）")
    for i, name in enumerate(bundle_list):
        print(f"{i + 1}. {name} （{counter[name]}次）")
    while True:
        try:
            bundle_list_len = len(bundle_list)
            if bundle_list_len == 1:
                choice = bundle_list[0]
                break
            idx = int(input("\n检测到多个bundleName，输入使用的 bundleName 序号（1~{}）：".format( bundle_list_len )))
            if 1 <= idx <= len(bundle_list):
                choice = bundle_list[idx - 1]
                print(f"你选择的是：{choice}")
                break
            else:
                print("输入有误，请重新输入。")
        except Exception:
            print("请输入数字。")
    return choice

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(cmd, " 出错！", result.stderr)
        input()
    return result.stdout

def is_device_online():
    result = subprocess.run("hdc_std list targets", shell=True, capture_output=True, text=True)
    # 标准输出包含 device id 等关键信息时说明设备在线
    return "Empty" not in result.stdout


if __name__ == '__main__':
    file_name = "install_list_capability.json"
    install_list_capability_path = "/system/variant/phone/base/etc/app/"
    dst = r"D:\garbages\history\HarmonyFile\app_signature"
    hap_path_input = input("hap文件路径：").strip()
    hap_path = hap_path_input
    hap_path = r"C:\Users\kwx1412683\Downloads\5.26\FloatWindowTest_xd.hap"
    if hap_path_input and not hap_path_input.lower().endswith('.hap'):
        hap_path += hap_path_input + '.hap'
    if not hap_path or not os.path.isfile(hap_path):
        print(f"不存在: {hap_path_input}")
        input()

    app_in_file = hap_path
    in_dir, in_name = os.path.split(app_in_file)
    if in_name.lower().endswith('.hap'):
        prefix = in_name[:-4]
    else:
        prefix = in_name
    # print(in_dir + "  " +  in_name)
    cert = extract_certificate(hap_path)
    cer_path = save_certificate_to_file(cert, dst, prefix)
    sha256 = get_cert_sha256(cer_path)
    print(f"sha256: {sha256}")
    # 执行命令
    bundleName = extract_bundle_names(hap_path)

    new_signature = {
        "bundleName": bundleName,
        "app_signature": [sha256],
        "allowAppUsePrivilegeExtension": True
    }
    file_recv_cmd = f'hdc_std file recv "{install_list_capability_path}{file_name}" "{dst}"'
    file_recv = run_cmd(file_recv_cmd)

    # 步骤2: 读取json
    json_file_path = f"{dst}\\{file_name}"
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    try:
        data["install_list"].insert(0, new_signature)
    except KeyError:
        print("install_list 写入失败")
        input()
    # 步骤5: 写回json文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    run_cmd('hdc_std target mount')
    file_send_cmd = f'hdc_std file send {json_file_path} {install_list_capability_path}'
    print( run_cmd(file_send_cmd) )
    run_cmd(f'hdc_std shell reboot')
    print("等待设备重启...")
    for _ in range(120):  # 最多等2分钟
        if is_device_online():
            print("设备已重启且上线")
            break
        time.sleep(1)
    else:
        print("等待超时，设备未上线")

    print ( run_cmd(f'hdc_std install {hap_path}') )
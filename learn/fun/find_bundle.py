import re
from collections import Counter
import json
import subprocess
import os

tool_dir = r"D:\SoftXD\traces\tool\sign_tool"
user_suffix = "xd"
# tool_dir = r"D:\SoftXD\traces\tool\sign_tool\oh_hap_sign_tool"

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
    return bundle_names

if __name__ == '__main__':
    # 1. 用户输入 hap 文件全
    hap_path_input = input("hap文件路径：").strip()
    hap_path = hap_path_input
    # hap_path = r"D:\SoftXD\traces\tool\sign_tool\newstar.hap"
    if hap_path_input and not hap_path_input.lower().endswith('.hap'):
        hap_path += hap_path_input + '.hap'
    if not hap_path or not os.path.isfile(hap_path):
        print(f"不存在: {hap_path_input}")
        input()

    app_in_file = hap_path
    # app签名输入文件
    # # 2. 输入后缀
    # while True:
    #     user_suffix = input("请输入后缀，例如XD：").strip()
    #     if not user_suffix:
    #         print("必须输入后缀！")
    #     else:
    #         break

    # 3. 拼接app签名输出文件名
    in_dir, in_name = os.path.split(app_in_file)
    if in_name.lower().endswith('.hap'):
        prefix = in_name[:-4]
    else:
        prefix = in_name
    app_out_file = os.path.join(in_dir, f"{prefix}_{user_suffix}.hap")
    # 4. 其他文件路径依然用你的模板，放在tool_dir下
    json_path = os.path.join(tool_dir, "UnsgnedReleasedProfileTemplate.json")
    jar_path = os.path.join(tool_dir, "hap-sign-tool.jar")
    profile_cert_file = os.path.join(tool_dir, "OpenHarmonyProfileRelease.pem")
    app_cert_file = os.path.join(tool_dir, "OpenHarmonyApplication.pem")
    keystore_file = os.path.join(tool_dir, "OpenHarmony.p12")
    profile_file = os.path.join(tool_dir, "openharmony.p7b")  # profile签完的p7b
    # 1. 提取Name
    names = extract_bundle_names(hap_path)
    if not names:
        print("未匹配到bundleName")
        input()

    counter = Counter(names)
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
    # 2. 写入 JSON 文件
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "bundle-info" in data:
            data["bundle-info"]["bundle-name"] = choice
            print("已修改json bundle-info.bundle-name 为：", choice)
        else:
            print("UnsgnedReleasedProfileTemplate.json中未找到 bundle-info 字段")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        # print("已写回到原文件:", json_path)

    except Exception as e:
        print(e)
    #     # 失败时用正则法兜底
    #     print("JSON写入失败，尝试正则替换。原因：", e)
    #     with open(json_path, "r", encoding="utf-8") as f:
    #         old_content = f.read()
    #     pattern = r'("bundle-info"\s*:\s*\{[^}]*?"bundle-name"\s*:\s*")[^"]*(")'
    #     def repl(m):
    #         return f'{m.group(1)}{choice}{m.group(2)}'
    #     new_content, n = re.subn(pattern, repl, old_content)
    #     if n == 0:
    #         print("正则替换也未能成功，请检查文件格式。")
    #         input()
    #     else:
    #         with open(json_path, "w", encoding="utf-8") as f:
    #             f.write(new_content)
    #         print("通过正则已写回到原文件:", json_path)
    # 3. 执行 profile 签名
    cmd1 = [
        "java", "-jar", jar_path,
        "sign-profile",
        "-keyAlias", "openharmony application profile release",
        "-signAlg", "SHA256withECDSA",
        "-mode", "localSign",
        "-profileCertFile", profile_cert_file,
        "-inFile", json_path,
        "-keystoreFile", keystore_file,
        "-outFile", profile_file,
        "-keyPwd", "123456",
        "-keystorePwd", "123456"
    ]
    print("\n即将执行Profile签名命令：")
    print(" ".join([str(x) for x in cmd1]))
    try:
        result = subprocess.run(
            cmd1, cwd=tool_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8'
        )
        print("\n命令行输出：\n", result.stdout)
        if result.returncode != 0:
            print("\n命令出错：", result.stderr)
            input()

        else:
            print("Profile签名成功。输出文件：", profile_file)
    except Exception as e:
        print("执行Java命令失败：", e)
        input()

    # 4. 执行 app 签名
    cmd2 = [
        "java", "-jar", jar_path,
        "sign-app",
        "-keyAlias", "openharmony application release",
        "-signAlg", "SHA256withECDSA",
        "-mode", "localSign",
        "-appCertFile", app_cert_file,
        "-profileFile", profile_file,
        "-inFile", app_in_file,
        "-keystoreFile", keystore_file,
        "-outFile", app_out_file,
        "-keyPwd", "123456",
        "-keystorePwd", "123456"
    ]
    print("\n即将执行App签名命令：")
    print(" ".join([str(x) for x in cmd2]))
    try:
        result2 = subprocess.run(
            cmd2, cwd=tool_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8'
        )
        print("\n命令行输出：\n", result2.stdout)
        if result2.returncode != 0:
            print("\n命令出错：", result2.stderr)
        else:
            print(f"App签名成功，输出：{app_out_file}")
    except Exception as e:
        print("执行Java命令失败：", e)

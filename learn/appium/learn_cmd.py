import subprocess
import re
def get_system_info():
    info = {
        '设备名': None,
        'MAC地址': None,
        'IP地址': None,
        '网络名称': None
    }
    # 获取设备名
    hostname = None
    try:
        hostname = subprocess.check_output('hostname', shell=True).decode('gbk').strip()
        # print(subprocess.check_output('hdc', shell=True).decode(errors='ignore').strip() )
    except Exception as e:
        print(f"获取设备名时出错：{e}")

    info['设备名'] = hostname

    # 获取MAC地址
    try:
        mac_output = subprocess.check_output(
            'wmic nic where NetConnectionStatus=2 get MACAddress',
            shell=True
        ).decode('gbk', errors='ignore').strip()
        # print(mac_output ) 只输出第二行有点误导
        # print(type(mac_output))
        # 列表推导式
        fun = [ [ line.strip() for line in mac_output.splitlines() if line.strip() ] for line in mac_output.splitlines() if line.strip() ]
        print( fun )
        print(f"fun! {fun[0][1]}" )
        lines = [line.strip() for line in mac_output.splitlines() if line.strip()]
        if len(lines) > 1 and lines[0] == 'MACAddress':
            # for line in lines[1:]:
            #     if line:
            #         info['MAC地址'] = line
            #         break
            info['MAC地址'] = lines[1]
    except Exception as e:
        print(f"获取MAC地址时出错：{e}")

    # 获取IP地址
    try:
        ip_output = subprocess.check_output(
            'wmic NICCONFIG WHERE "IPEnabled=True" get IPAddress',
            shell=True
        ).decode('gbk', errors='ignore').strip()
        # IPAddress
        # {"10.235.75.227"}
        lines = ip_output.splitlines()
        # ['IPAddress          ', '', '{"10.235.75.227"}']
        # [:-2]切掉后面两个 [-2:]取后面两个 [:2]取前面两个      [全部or切掉(int):取] [全部or取(-int):切]    可以记成[头:int] [int:尾]
        # return s[-3:] if len(s) >= 3 else None
        info['IP地址'] = (lines[2][2:][:-2] if (len(lines[2]) >= 4) else None) if (len(lines) > 2) else None
        # # ipv4_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', ip_output)
        # if ipv4_addresses:
        #     info['IP地址'] = ipv4_addresses[0]
    except Exception as e:
        print(f"获取IP地址时出错：{e}")
    # 获取网络名称
    try:
        ps_command = '(Get-NetConnectionProfile).Name'
        network_name = subprocess.check_output(
            ['powershell', '-Command', ps_command],
            shell=True,
            encoding='gbk'
        ).strip()
        if network_name:
            info['网络名称'] = network_name
    except subprocess.CalledProcessError as e:
        print(f"执行PowerShell命令时出错：{e}")
    except Exception as e:
        print(f"获取网络名称时出错：{e}")


    return info

if __name__ == '__main__':
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"\t\n{key}: {value} ")
    # s = "1"
    # s2 = s[-3:]
    # print(s2) 越界现在居然也不报错了
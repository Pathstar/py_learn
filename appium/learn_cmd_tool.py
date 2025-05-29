import subprocess
import re


class SystemInfoFetcher:
    """Windows系统信息获取工具类"""

    def __init__(self):
        # self.system_info = {
        #     '设备名': None,
        #     'MAC地址': None,
        #     'IP地址': None,
        #     '网络名称': None
        # }
        # self.system_info = None
        # self.set_all_info()
        self.system_info = {
            '设备名': self.get_hostname(),
            'MAC地址': self.get_mac_address(),
            'IP地址': self.get_ip_address(),
            '网络名称': self.get_network_name()
        }
    # 相当于void？ 其他语言的return只能给函数一个值，而self可以有无数
    @staticmethod
    def run_command(command: str) -> str:
        """执行系统命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                encoding='gbk',
                timeout=10
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"命令执行失败: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("命令执行超时")

    # 1
    def get_hostname(self) -> str:
        """获取设备名称"""
        try:
            return self.run_command('hostname')
        except RuntimeError as e:
            print(f"获取设备名失败: {str(e)}")
            return "N/A"

    # 2
    def get_mac_address(self) -> str:
        """获取MAC地址"""
        try:
            output = self.run_command('wmic nic where NetConnectionStatus=2 get MACAddress')
            # [print(line) for line in output.splitlines()]
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            return lines[1] if len(lines) > 1 and lines[0] == 'MACAddress' else "N/A"
        except RuntimeError as e:
            print(f"获取MAC地址失败: {str(e)}")
            return "N/A"

    # 3
    def get_ip_address(self) -> str:
        """获取IP地址"""
        try:
            output = self.run_command('wmic NICCONFIG WHERE "IPEnabled=True" get IPAddress')
            lines = output.splitlines()
            if len(lines) > 2:
                ip_line = lines[2].strip()
                return re.search(r'\d+\.\d+\.\d+\.\d+', ip_line).group(0)
            return "N/A"
        except (RuntimeError, AttributeError) as e:
            print(f"获取IP地址失败: {str(e)}")
            return "N/A"

    # 4
    def get_network_name(self) -> str:
        """获取网络名称"""
        try:
            # 没用到self就可以 staticmethod
            # ps_command = '(Get-NetConnectionProfile).Name'
            # return subprocess.check_output(
            #     ['powershell', '-Command', ps_command],
            #     shell=True,
            #     encoding='gbk',
            #     timeout=10
            # ).strip()
            return self.run_command('powershell -command (Get-NetConnectionProfile).Name')
        except subprocess.CalledProcessError as e:
            print(f"执行PowerShell命令失败: {str(e)}")
            return "N/A"
        except Exception as e:
            print(f"获取网络名称失败: {str(e)}")
            return "N/A"

    # 集体调用
    def set_all_info(self) -> None:
        """更新所有系统信息"""
        self.system_info = {
            '设备名': self.get_hostname(),
            'MAC地址': self.get_mac_address(),
            'IP地址': self.get_ip_address(),
            '网络名称': self.get_network_name()
        }

    def get_all_info(self) -> dict[str, str]:
        """获取完整系统信息"""
        return self.system_info

    def __call__(self):
        return self.system_info

if __name__ == "__main__":
    fetcher = SystemInfoFetcher()
    # 全放到了self里
    system_info = fetcher.get_all_info()

    print("\n系统信息:")
    for key, value in fetcher().items():
        print(f"{key:10}: {value}")

# 设备名：通过hostname命令直接获取，无需解析。
# MAC地址：使用wmic命令筛选已连接的网卡，解析输出的MAC地址。
# IP地址：通过wmic命令获取已启用网卡的IP信息，正则提取IPv4地址。
# 网络名称：调用PowerShell命令Get - NetConnectionProfile获取当前连接的名称（支持有线和无线）。
import subprocess
import re
from typing import Dict, List


class AndroidDeviceInfoFetcher:
    """Android设备信息获取工具类"""

    def __init__(self):
        self.device_list = self.get_connected_devices()

    @staticmethod
    # 省去了() AndroidDeviceInfoFetcher() 变成 AndroidDeviceInfoFetcher, 修饰的方法不用写self
    def run_adb_command(command: str) -> str:
        """执行ADB命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ADB命令执行失败: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("ADB命令执行超时")

    def get_connected_devices(self) -> List[str]:
        """获取已连接的设备ID列表"""
        output = self.run_adb_command("adb devices -l")
        devices = []
        for line in output.split('\n')[1:]:  # 跳过第一行标题
            if line.strip() and 'device' in line:
                match = re.search(r'^(\S+)\s+device', line)
                if match:
                    devices.append(match.group(1))
        return devices

    def get_device_property(self, device_id: str, prop_name: str) -> str:
        """获取特定设备的属性值"""
        command = f"adb -s {device_id} shell getprop {prop_name}"
        return self.run_adb_command(command)

    def get_all_device_info(self, device_id: str) -> Dict[str, str]:
        """获取设备完整信息"""
        return {
            "device_id": device_id,
            "model": self.get_device_property(device_id, "ro.product.model"),
            "manufacturer": self.get_device_property(device_id, "ro.product.manufacturer"),
            "brand": self.get_device_property(device_id, "ro.product.brand"),
            "hardware": self.get_device_property(device_id, "ro.hardware"),
            "serialno": self.get_device_property(device_id, "ro.serialno"),
            "android_version": self.get_device_property(device_id, "ro.build.version.release"),
            "build_number": self.get_device_property(device_id, "ro.build.id"),
            "security_patch": self.get_device_property(device_id, "ro.build.version.security_patch"),
            "imei": self.get_imei_number(device_id),
            "wifi_mac": self.get_wifi_mac_address(device_id)
        }

    def get_imei_number(self, device_id: str) -> str:
        """获取IMEI号码（需要READ_PHONE_STATE权限）"""
        try:
            return self.run_adb_command(
                f"adb -s {device_id} shell service call iphonesubinfo 1 | "
                "grep -o \"'[0-9]*'\" | tr -d \"'\" | awk '{{printf \"%s\", $1}}'"
            )
        except RuntimeError:
            return "N/A"

    def get_wifi_mac_address(self, device_id: str) -> str:
        """获取WiFi MAC地址"""
        try:
            return self.run_adb_command(
                f"adb -s {device_id} shell cat /sys/class/net/wlan0/address"
            ).upper()
        except RuntimeError:
            return "N/A"

    def batch_get_device_info(self) -> Dict[str, Dict]:
        """批量获取所有设备信息"""
        devices_info = {}
        for device_id in self.device_list:
            try:
                devices_info[device_id] = self.get_all_device_info(device_id)
            except RuntimeError as e:
                print(f"获取设备 {device_id} 信息失败: {str(e)}")
        return devices_info


if __name__ == "__main__":
    fetcher = AndroidDeviceInfoFetcher()
    devices_info = fetcher.batch_get_device_info()

    for device_id, info in devices_info.items():
        print(f"\n设备ID: {device_id}")
        for key, value in info.items():
            print(f"{key:15}: {value}")

            # 实现原理说明：
            #
            # 设备连接检测：
            #
            # 使用adb
            # devices - l命令列出所有连接的设备
            # 通过正则表达式解析设备ID
            # 支持检测USB连接设备和无线连接设备
            # 属性获取机制：
            #
            # 基于getprop命令获取系统属性
            # 关键属性对应关系：
            # ro.product.model: 设备型号（如Pixel
            # 6）
            # ro.product.manufacturer: 制造商（如Google）
            # ro.build.version.release: Android版本（如12）
            # ro.serialno: 设备序列号
            # 高级信息获取：
            #
            # IMEI号码：通过系统服务调用获取，需要设备授权
            # MAC地址：直接读取系统文件 / sys /
            #
            #
            # class /net / wlan0 / address
            #
            #
            # 安全补丁版本：获取系统安全更新版本
            # 异常处理：
            #
            # 命令执行超时处理（10
            # 秒）
            # 错误状态码捕获
            # 属性不存在时的默认值处理
            # 多设备支持：
            #
            # 自动检测所有已连接设备
            # 支持批量获取信息
            # 每个设备信息独立存储
            # 扩展功能建议：
            #
            # 缓存机制：
            # from functools import lru_cache
            #
            #
            # @lru_cache(maxsize=10)
            # def get_cached_property(self, device_id: str, prop_name: str) -> str:
            #     """带缓存的属性获取"""
            #     return self.get_device_property(device_id, prop_name)
            #
            #
            # python
            # 设备状态监控：
            #
            # def get_battery_info(self, device_id: str) -> Dict:
            #     """获取电池信息"""
            #     output = self.run_adb_command(f"adb -s {device_id} shell dumpsys battery")
            #     return {
            #         "level": re.search(r"level: (\d+)", output).group(1),
            #         "status": re.search(r"status: (\d+)", output).group(1),
            #         "health": re.search(r"health: (\d+)", output).group(1)
            #     }
            #
            #
            # python
            # 网络信息增强：
            #
            # def get_network_info(self, device_id: str) -> Dict:
            #     """获取网络详细信息"""
            #     output = self.run_adb_command(f"adb -s {device_id} shell ifconfig")
            #     return {
            #         "ip_address": re.search(r"inet addr:(\S+)", output).group(1),
            #         "mac_address": re.search(r"HWaddr (\S+)", output).group(1)
            #     }
            #
            #
            # python
            # 存储信息获取：
            #
            # def get_storage_info(self, device_id: str) -> Dict:
            #     """获取存储空间信息"""
            #     output = self.run_adb_command(f"adb -s {device_id} shell df /data")
            #     parts = output.split()
            #     return {
            #         "total": parts[8],
            #         "used": parts[9],
            #         "free": parts[10]
            #     }
            #
            #
            # python
            # 使用注意事项：
            #
            # 确保已启用USB调试模式
            # 首次连接需要授权对话框确认
            # 部分信息需要root权限（如详细硬件信息）
            # IMEI获取可能需要SIM卡状态正常
            # 不同Android版本可能存在的命令差异
            # 输出示例：
            #
            # 设备ID: emulator - 5554
            # device_id: emulator - 5554
            # model: sdk_gphone64_x86_64
            # manufacturer: Google
            # brand: Android
            # hardware: ranchu
            # serialno: emulator - 5554
            # android_version: 13
            # build_number: SE1A
            # .220826
            # .014
            # security_patch: 2022 - 0
            # 9 - 05
            # imei: 355715111111111
            # wifi_mac: 02:00: 00:00: 00:00
            # 这个方案提供了全面可靠的设备信息获取能力，能够满足企业级自动化测试的需求。实际使用时可配合自动化测试框架集成，实现测试报告的设备信息自动填充和设备状态监控。
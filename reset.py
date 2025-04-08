#!/usr/bin/env python3
'''
Cursor Trial Reset Tool

这个脚本用于重置 Cursor 配置文件中的设备 ID，生成新的随机设备 ID。
主要用于重置 Cursor 的试用期限制。

Repository: https://github.com/ultrasev/cursor-reset
Author: @ultrasev
Created: 10/Dec/2024
'''

import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
import platform


def backup_file(file_path: str):
    """
    为指定文件创建带时间戳的备份。
    
    Args:
        file_path (str): 需要备份的文件路径
    """
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)


def get_storage_file():
    """
    根据操作系统确定 Cursor 存储文件的位置。
    
    Returns:
        Path: 存储文件的完整路径
        
    Raises:
        OSError: 当操作系统不支持时抛出异常
    """
    system = platform.system()
    if system == "Windows":
        return Path(os.getenv("APPDATA")) / "Cursor" / "User" / "globalStorage" / "storage.json"
    elif system == "Darwin":  # macOS
        return Path(os.path.expanduser("~")) / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "storage.json"
    elif system == "Linux":
        return Path(os.path.expanduser("~")) / ".config" / "Cursor" / "User" / "globalStorage" / "storage.json"
    else:
        raise OSError(f"Unsupported operating system: {system}")


def reset_cursor_id():
    """
    重置 Cursor 的设备 ID。
    主要功能：
    1. 获取存储文件路径
    2. 创建备份
    3. 生成新的随机设备 ID
    4. 更新配置文件
    5. 显示新的设备 ID
    """
    # 获取存储文件路径并确保目录存在
    storage_file = get_storage_file()
    storage_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 创建备份文件
    backup_file(storage_file)

    # 读取现有配置或创建新的空配置
    if not storage_file.exists():
        data = {}
    else:
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

    # 生成新的随机设备 ID
    machine_id = os.urandom(32).hex()  # 生成 32 字节的随机十六进制字符串
    mac_machine_id = os.urandom(32).hex()  # 生成 Mac 专用的机器 ID
    dev_device_id = str(uuid.uuid4())  # 生成新的 UUID

    # 更新配置数据
    data["telemetry.machineId"] = machine_id
    data["telemetry.macMachineId"] = mac_machine_id
    data["telemetry.devDeviceId"] = dev_device_id

    # 将更新后的配置写入文件
    with open(storage_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # 打印成功信息和新的设备 ID
    print("🎉 Device IDs have been successfully reset. The new device IDs are: \n")
    print(
        json.dumps(
            {
                "machineId": machine_id,
                "macMachineId": mac_machine_id,
                "devDeviceId": dev_device_id,
            },
            indent=2))


if __name__ == "__main__":
    reset_cursor_id()

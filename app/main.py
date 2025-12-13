import platform
import os
import socket
import psutil
import getpass
import uuid
import subprocess
import sys
from datetime import datetime

def get_detailed_system_info():
    """Получить детальную информацию о системе"""
    
    info = {}
    
    # 1. Платформа
    info['platform'] = {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture': platform.architecture()[0]
    }
    
    # 2. Процессор
    cpu_info = {
        'physical_cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True)
    }
    
    if hasattr(psutil.cpu_freq(), 'current'):
        cpu_info['frequency'] = f"{psutil.cpu_freq().current:.2f} MHz"
    
    # Статистика CPU
    cpu_info['usage_per_core'] = [f"{x}%" for x in psutil.cpu_percent(percpu=True)]
    cpu_info['total_usage'] = f"{psutil.cpu_percent()}%"
    
    info['cpu'] = cpu_info
    
    # 3. Память
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    info['memory'] = {
        'total_ram': f"{mem.total / (1024**3):.2f} GB",
        'available_ram': f"{mem.available / (1024**3):.2f} GB",
        'used_ram_percent': f"{mem.percent}%",
        'total_swap': f"{swap.total / (1024**3):.2f} GB",
        'used_swap': f"{swap.used / (1024**3):.2f} GB",
        'swap_percent': f"{swap.percent}%"
    }
    
    # 4. Диски
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': f"{usage.total / (1024**3):.2f} GB",
                'free': f"{usage.free / (1024**3):.2f} GB",
                'used_percent': f"{usage.percent}%"
            })
        except:
            continue
    
    info['disks'] = disks
    
    # 5. Сеть
    hostname = socket.gethostname()
    info['network'] = {
        'hostname': hostname,
        'mac_address': ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                                 for ele in range(0, 8*6, 8)][::-1])
    }
    
    # Получаем IP адреса
    try:
        local_ip = socket.gethostbyname(hostname)
        info['network']['local_ip'] = local_ip
    except:
        info['network']['local_ip'] = "Недоступно"
    
    # 6. Система
    info['system'] = {
        'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
        'current_user': getpass.getuser(),
        'python_version': sys.version,
        'pid': os.getpid(),
        'cwd': os.getcwd()
    }
    
    # 7. Процессы
    info['processes'] = {
        'total': len(psutil.pids()),
        'running': len([p for p in psutil.process_iter(['status']) 
                       if p.info['status'] == psutil.STATUS_RUNNING])
    }
    
    return info

def print_system_info(info):
    """Красиво вывести информацию"""
    
    print("\n" + "═" * 60)
    print(" " * 20 + "ДЕТАЛЬНАЯ СИСТЕМНАЯ ИНФОРМАЦИЯ")
    print("═" * 60)
    
    # Платформа
    print("\n📊 ПЛАТФОРМА:")
    print(f"  • Система: {info['platform']['system']} {info['platform']['release']}")
    print(f"  • Версия: {info['platform']['version']}")
    print(f"  • Архитектура: {info['platform']['architecture']}")
    print(f"  • Процессор: {info['platform']['processor']}")
    
    # CPU
    print("\n⚡ ПРОЦЕССОР:")
    print(f"  • Физические ядра: {info['cpu']['physical_cores']}")
    print(f"  • Логические ядра: {info['cpu']['logical_cores']}")
    if 'frequency' in info['cpu']:
        print(f"  • Частота: {info['cpu']['frequency']}")
    print(f"  • Загрузка CPU: {info['cpu']['total_usage']}")
    
    # Память
    print("\n💾 ПАМЯТЬ:")
    print(f"  • Оперативная память: {info['memory']['total_ram']}")
    print(f"  • Доступно RAM: {info['memory']['available_ram']}")
    print(f"  • Использовано RAM: {info['memory']['used_ram_percent']}")
    if float(info['memory']['total_swap'].split()[0]) > 0:
        print(f"  • Файл подкачки: {info['memory']['total_swap']}")
        print(f"  • Использовано swap: {info['memory']['swap_percent']}")
    
    # Диски
    print("\n💿 ДИСКИ:")
    for i, disk in enumerate(info['disks'], 1):
        print(f"  {i}. {disk['device']} ({disk['fstype']})")
        print(f"     Путь: {disk['mountpoint']}")
        print(f"     Всего: {disk['total']} | Свободно: {disk['free']}")
        print(f"     Использовано: {disk['used_percent']}")
    
    # Сеть
    print("\n🌐 СЕТЬ:")
    print(f"  • Имя компьютера: {info['network']['hostname']}")
    print(f"  • MAC-адрес: {info['network']['mac_address']}")
    if 'local_ip' in info['network']:
        print(f"  • Локальный IP: {info['network']['local_ip']}")
    
    # Система
    print("\n👤 СИСТЕМА:")
    print(f"  • Пользователь: {info['system']['current_user']}")
    print(f"  • Загрузка системы: {info['system']['boot_time']}")
    print(f"  • Рабочая директория: {info['system']['cwd']}")
    print(f"  • Python версия: {info['system']['python_version'].split()[0]}")
    
    # Процессы
    print("\n🔄 ПРОЦЕССЫ:")
    print(f"  • Всего процессов: {info['processes']['total']}")
    print(f"  • Выполняются: {info['processes']['running']}")
    
    print("\n" + "═" * 60)

if __name__ == "__main__":
    try:
        info = get_detailed_system_info()
        print_system_info(info)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    input("\nНажмите Enter для выхода...")
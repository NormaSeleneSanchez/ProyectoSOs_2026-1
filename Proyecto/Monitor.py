import os
import time
import platform
import psutil
from datetime import datetime, timedelta

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def bytes_to_gb(b):
    return b / (1024 ** 3)

def show_system_info():
    print("=== INFORMACION DEL SISTEMA ===")
    print(f"Sistema operativo: {platform.system()} {platform.release()}")
    print(f"Versión: {platform.version()}")
    print(f"Arquitectura: {platform.machine()}")
    print(f"Procesador: {platform.processor()}")
    print(f"Uptime: {timedelta(seconds=int(time.time() - psutil.boot_time()))}\n")

def show_cpu():
    print("=== CPU ===")
    print(f"Uso total de CPU: {psutil.cpu_percent(interval=0.3)}%")
    print(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"Núcleos lógicos: {psutil.cpu_count(logical=True)}")
    
    freq = psutil.cpu_freq()
    if freq:
        print(f"Frecuencia actual: {freq.current:.2f} MHz")
        print(f"Frecuencia máxima: {freq.max:.2f} MHz")
    
    print("\nUso por núcleo:")
    for i, p in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"  Núcleo {i}: {p}%")
    print()

def show_memory():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    print("=== MEMORIA RAM ===")
    print(f"Total: {bytes_to_gb(mem.total):.2f} GB")
    print(f"Disponible: {bytes_to_gb(mem.available):.2f} GB")
    print(f"Usada: {bytes_to_gb(mem.used):.2f} GB ({mem.percent}%)")
    print("\n=== SWAP ===")
    print(f"Total swap: {bytes_to_gb(swap.total):.2f} GB")
    print(f"Usada: {bytes_to_gb(swap.used):.2f} GB ({swap.percent}%)\n")

def show_disk():
    print("=== DISCO ===")
    partitions = psutil.disk_partitions()
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"Partición: {p.device} -> {p.mountpoint}")
            print(f"  Total: {bytes_to_gb(usage.total):.2f} GB")
            print(f"  Usado: {bytes_to_gb(usage.used):.2f} GB")
            print(f"  Libre: {bytes_to_gb(usage.free):.2f} GB")
            print(f"  Porcentaje: {usage.percent}%\n")
        except PermissionError:
            continue

def show_network(last_stats):
    print("=== RED ===")
    stats = psutil.net_io_counters()

    sent = stats.bytes_sent - last_stats.bytes_sent
    recv = stats.bytes_recv - last_stats.bytes_recv

    print(f"Subida total: {stats.bytes_sent / (1024**2):.2f} MB")
    print(f"Bajada total: {stats.bytes_recv / (1024**2):.2f} MB")
    print(f"Velocidad subida: {sent / 1024:.2f} KB/s")
    print(f"Velocidad bajada: {recv / 1024:.2f} KB/s\n")

    return stats

def show_temperatures():
    print("=== TEMPERATURAS (si están disponibles) ===")
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            print("No soportado o no disponible.\n")
            return

        for name, entries in temps.items():
            print(f"{name}:")
            for t in entries:
                print(f"  {t.label or 'Sensor'}: {t.current}°C")
        print()
    except:
        print("No soportado en este sistema.\n")

def show_processes(limit=10):
    print(f"=== PROCESOS PRINCIPALES (Top {limit} CPU) ===")
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except psutil.NoSuchProcess:
            pass

    procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)

    for p in procs[:limit]:
        print(f"PID {p['pid']} | {p['name'][:25]:25} | CPU: {p['cpu_percent']}% | RAM: {p['memory_percent']:.2f}%")
    print()

def main():
    last_network = psutil.net_io_counters()

    while True:
        clear()
        print("===== MONITOR COMPLETO DEL SISTEMA - Python =====")
        print("Actualizado:", datetime.now().strftime("%H:%M:%S"))
        print("-" * 60)

        show_system_info()
        show_cpu()
        show_memory()
        show_disk()
        last_network = show_network(last_network)
        show_temperatures()
        show_processes()

        print("CTRL+C para salir.")
        time.sleep(1)

if __name__ == "__main__":
    main()
"""
monitor_sistema.py

Script para monitorear el rendimiento y la información del sistema en tiempo real.
Utiliza la librería psutil para obtener métricas de CPU, memoria, disco, red, 
temperatura y procesos.

"""
import os
import time
import platform
import psutil
from datetime import datetime, timedelta

# ================================
# CONFIGURACIÓN DE ALERTAS
# ================================
CPU_ALERT = 90          # %
RAM_ALERT = 85          # %
DISK_ALERT = 90         # %
NETWORK_ALERT = 10_000_000  # bytes/seg (opcional)

# ================================
# LOGGING
# ================================
LOG_DIR = "logs"

def ensure_log_dir():
    """Crea la carpeta logs/ si no existe."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def write_log(data: str):
    """Escribe una línea al archivo de log actual."""
    ensure_log_dir()
    filename = datetime.now().strftime("logs/monitor_%Y-%m-%d.txt")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(data + "\n")

# ================================
# UTILIDADES
# ================================
def clear():
    """
    Limpia la consola.

    Utiliza 'cls' en sistemas Windows ('nt') y 'clear' en otros sistemas
    """
    os.system("cls" if os.name == "nt" else "clear")

def bytes_to_gb(b):
    """
    Convierte un valor de bytes a gigabytes (GB).

    Args:
        b (int): Número de bytes.

    Returns:
        float: El valor equivalente en gigabytes.
    """
    return b / (1024 ** 3)

def show_system_info():
    """
    Muestra información básica del sistema operativo y hardware.
    """
    print("=== INFORMACIÓN DEL SISTEMA ===")
    print(f"Sistema operativo: {platform.system()} {platform.release()}")
    print(f"Versión: {platform.version()}")
    print(f"Arquitectura: {platform.machine()}")
    print(f"Procesador: {platform.processor()}")
    # Calcula el tiempo de actividad (uptime)
    uptime_seconds = int(time.time() - psutil.boot_time())
    print(f"Uptime: {timedelta(seconds=uptime_seconds)}\n")

def show_cpu():
    """
    Muestra el uso y la información detallada de la CPU.
    """
    print("=== CPU ===")
    # Obtiene el uso total de CPU durante un intervalo de 0.3 segundos
    print(f"Uso total de CPU: {psutil.cpu_percent(interval=0.3)}%")
    print(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"Núcleos lógicos: {psutil.cpu_count(logical=True)}")
    
    freq = psutil.cpu_freq()
    if freq:
        print(f"Frecuencia actual: {freq.current:.2f} MHz")
        print(f"Frecuencia máxima: {freq.max:.2f} MHz")
    
    print("\nUso por núcleo:")
    # Obtiene el uso de CPU por núcleo
    for i, p in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"  Núcleo {i}: {p}%")
    print()

def show_memory():
    """
    Muestra el uso de la memoria RAM (virtual) y la memoria SWAP.
    """
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
    """
    Muestra el uso de las particiones de disco montadas.
    """
    print("=== DISCO ===")
    partitions = psutil.disk_partitions()
    for p in partitions:
        try:
            # Intenta obtener el uso del disco para el punto de montaje
            usage = psutil.disk_usage(p.mountpoint)
            print(f"Partición: {p.device} -> {p.mountpoint}")
            print(f"  Total: {bytes_to_gb(usage.total):.2f} GB")
            print(f"  Usado: {bytes_to_gb(usage.used):.2f} GB")
            print(f"  Libre: {bytes_to_gb(usage.free):.2f} GB")
            print(f"  Porcentaje: {usage.percent}%\n")
        except PermissionError:
            # Ignora particiones a las que no se puede acceder por permisos
            continue
        except OSError:
            # Ignora posibles errores de sistema de archivos o no disponibilidad
             continue

def show_network(last_stats):
    """
    Muestra el total de tráfico de red y la velocidad de subida/bajada desde
    la última llamada.

    Args:
        last_stats (psutil._common.snetio): Estadísticas de red de la llamada anterior.

    Returns:
        psutil._common.snetio: Estadísticas de red actuales.
    """
    print("=== RED ===")
    # Obtiene los contadores de E/S de red
    stats = psutil.net_io_counters()

    # Calcula la diferencia de bytes enviados y recibidos desde la última medición
    sent = stats.bytes_sent - last_stats.bytes_sent
    recv = stats.bytes_recv - last_stats.bytes_recv

    # Muestra los totales acumulados en MB
    print(f"Subida total: {stats.bytes_sent / (1024**2):.2f} MB")
    print(f"Bajada total: {stats.bytes_recv / (1024**2):.2f} MB")
    # Muestra la velocidad de subida/bajada en KB/s (división por el intervalo de 1 segundo)
    print(f"Velocidad subida: {sent / 1024:.2f} KB/s")
    print(f"Velocidad bajada: {recv / 1024:.2f} KB/s\n")

    return stats # Devuelve las estadísticas actuales para la próxima iteración

def show_temperatures():
    """
    Muestra las temperaturas de los sensores (si están disponibles).
    """
    print("=== TEMPERATURAS (si están disponibles) ===")
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            print("No soportado o no disponible.\n")
            return

        for name, entries in temps.items():
            print(f"{name}:")
            for t in entries:
                # Muestra la etiqueta del sensor o 'Sensor' si no tiene
                print(f"  {t.label or 'Sensor'}: {t.current}°C")
        print()
    except NotImplementedError:
        # psutil.sensors_temperatures() lanza esto si no está soportado
        print("No soportado en este sistema.\n")
    except Exception:
        # Captura cualquier otro error durante la lectura de temperaturas
        print("Error al leer las temperaturas.\n")


def show_processes(limit=10):
    """
    Muestra una lista de los procesos principales ordenados por uso de CPU.

    Args:
        limit (int): El número máximo de procesos a mostrar (por defecto 10).
    """
    print(f"=== PROCESOS PRINCIPALES (Top {limit} CPU) ===")
    procs = []
    # Itera sobre todos los procesos y obtiene la información relevante
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except psutil.NoSuchProcess:
            # Ignora procesos que pueden haber terminado durante la iteración
            pass

    # Ordena la lista de procesos por uso de CPU de forma descendente
    procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)

    # Imprime la información de los procesos del 'top N'
    for p in procs[:limit]:
        # Formatea el nombre del proceso para asegurar un ancho fijo de 25 caracteres
        proc_name = p['name'][:25]
        print(f"PID {p['pid']} | {proc_name:25} | CPU: {p['cpu_percent']:.1f}% | RAM: {p['memory_percent']:.2f}%")
    print()


def main():
    """
    Función principal del monitor. 
    Ejecuta el bucle de actualización y muestra la información del sistema.
    """
    # Inicializa las estadísticas de red para el cálculo inicial de velocidad
    last_network = psutil.net_io_counters()

    while True:
        clear() # Limpia la pantalla en cada iteración
        print("===== MONITOR COMPLETO DEL SISTEMA - Python =====")
        # Muestra la hora de la última actualización
        print("Actualizado:", datetime.now().strftime("%H:%M:%S"))
        print("-" * 60)

        # Llama a todas las funciones para mostrar la información
        show_system_info()
        show_cpu()
        show_memory()
        show_disk()
        # Actualiza las estadísticas de red para la próxima iteración
        last_network = show_network(last_network)
        show_temperatures()
        show_processes()

        print("CTRL+C para salir.")
        time.sleep(1) # Espera 1 segundo antes de la próxima actualización

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Maneja la interrupción por CTRL+C para salir limpiamente
        print("\nSaliendo del monitor del sistema.")

"""
Aplicación para monitorear estadísticas del sistema usando Textual.
Incluye pestañas para mostrar información de:
- Sistema
- CPU
- Memoria
- Disco
- Red
- Temperaturas
- Procesos
"""
from textual.app import App, ComposeResult
from textual.widgets import Header, TabbedContent, TabPane, RichLog
from contextlib import redirect_stdout
import io
import psutil


# Asi podremos usar lo que ya funcionaba en terminal
from Monitor import (
    show_system_info,
    show_cpu,
    show_memory,
    show_disk,
    show_network,
    show_temperatures,
    show_processes
)

class Monitor(App):
    """Aplicación gráfica basada en Textual para visualizar métricas del sistema."""
    
    CSS = """
    RichLog { border: solid green; }
    """

    # ---------------------------------------------------------
    #  Construcción de la interfaz
    # ---------------------------------------------------------
    def compose(self) -> ComposeResult:
        """Genera la estructura de pestañas de la interfaz."""
        
        yield Header(show_clock=True)

        with TabbedContent():

            with TabPane("Sistema", id="tab_sistema"):
                yield RichLog(id="log_sistema", markup=True)

            with TabPane("CPU", id="tab_cpu"):
                yield RichLog(id="log_cpu", markup=True)

            with TabPane("Memoria", id="tab_mem"):
                yield RichLog(id="log_mem", markup=True)

            with TabPane("Disco", id="tab_disco"):
                yield RichLog(id="log_disco", markup=True)

            with TabPane("Red", id="tab_red"):
                yield RichLog(id="log_red", markup=True)

            with TabPane("Temperaturas", id="tab_temp"):
                yield RichLog(id="log_temp", markup=True)

            with TabPane("Procesos", id="tab_proc"):
                yield RichLog(id="log_proc", markup=True)

    # ---------------------------------------------------------
    #  Utilidades
    # ---------------------------------------------------------
    def cap(self, func, *args):
         """
        Captura la salida estándar de una función y la devuelve como string.
        Evita que Textual crashee por prints directos.
        """
        
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                func(*args)
        except Exception as e:
            print(f"[red]ERROR:[/red] {e}", file=f)
        return f.getvalue()    

    # ---------------------------------------------------------
    #  Inicialización
    # ---------------------------------------------------------
    def on_mount(self):
        """Se ejecuta al iniciar la app: guarda referencias y programa la actualización."""

        self.logs = {
            "sistema": self.query_one("#log_sistema", RichLog),
            "cpu": self.query_one("#log_cpu", RichLog),
            "mem": self.query_one("#log_mem", RichLog),
            "disco": self.query_one("#log_disco", RichLog),
            "red": self.query_one("#log_red", RichLog),
            "temp": self.query_one("#log_temp", RichLog),
            "proc": self.query_one("#log_proc", RichLog),
        }
        
        self.last_net = psutil.net_io_counters() #Para medir tráfico de red alta 
        self.set_interval(1.0, self.actualizar_todo) #Actualizar cada segundo


    # ---------------------------------------------------------
    #  Actualización en tiempo real
    # ---------------------------------------------------------
    def actualizar_todo(self):

         """Actualiza todos los paneles con los datos más recientes del sistema."""

        tareas = [
            ("sistema", show_system_info),
            ("cpu", show_cpu),
            ("mem", show_memory),
            ("disco", show_disk),
            ("red", lambda: show_network(self.last_net)),
            ("temp", show_temperatures),
            ("proc", show_processes),
        ]

        for nombre_log, funcion in tareas:
            log_widget = self.logs[nombre_log]
            log_widget.clear()
            log_widget.write(self.cap(funcion))

        self.last_net = psutil.net_io_counters() # Actualizar tráfico de red para siguiente lectura

# ---------------------------------------------------------
#  Ejecución principal
# ---------------------------------------------------------
if __name__ == "__main__":
    Monitor().run()

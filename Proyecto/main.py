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

    CSS = """
    RichLog { border: solid green; }
    """

    def compose(self) -> ComposeResult:
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

    
    def cap(self, func, *args):
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                func(*args)
        except Exception as e:
            print(f"[red]ERROR:[/red] {e}", file=f)
        return f.getvalue()    


    def on_mount(self):
        self.last_net = psutil.net_io_counters()
        self.set_interval(1.0, self.actualizar_todo)


    def actualizar_todo(self):

        log = self.query_one("#log_sistema", RichLog)
        log.clear()
        log.write(self.cap(show_system_info))

        log = self.query_one("#log_cpu", RichLog)
        log.clear()
        log.write(self.cap(show_cpu))

        log = self.query_one("#log_mem", RichLog)
        log.clear()
        log.write(self.cap(show_memory))

        log = self.query_one("#log_disco", RichLog)
        log.clear()
        log.write(self.cap(show_disk))

        log = self.query_one("#log_red", RichLog)
        log.clear()
        log.write(self.cap(show_network, self.last_net))
        self.last_net = psutil.net_io_counters()

        log = self.query_one("#log_temp", RichLog)
        log.clear()
        log.write(self.cap(show_temperatures))

        log = self.query_one("#log_proc", RichLog)
        log.clear()
        log.write(self.cap(show_processes))
        
if __name__ == "__main__":
    Monitor.run()
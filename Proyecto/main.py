from textual.app import App, ComposeResult
from textual.widgets import Header, TabbedContent, TabPane, RichLog
from contextlib import redirect_stdout
import io
import psutil


# Asi podremos usar lo que ya funcionaba en terminal
from Monitos import (
    show_system_info,
    show_cpu,
    show_memory,
    show_disk,
    show_network,
    show_temperatures,
    show_processes
)

class Monitor(App):

    

if __name__ == "__main__":
    
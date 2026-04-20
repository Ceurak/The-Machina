from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, DataTable

from scanner.discovery import discover_hosts
from scanner.host_details import scan_host_ports
from ui.host_details_view import HostDetailsView
from ui.host_table import HostTable
from utils.command import CommandError


class ScanApp(App):
    CSS_PATH = "../styl.tcss"
    TITLE = "The Machina"
    SUB_TITLE = "Network Scanner"

    def __init__(self) -> None:
        super().__init__()
        self.hosts = []

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            with Horizontal(id="top_bar"):
                yield Input(placeholder="Podaj zakres, np. 192.168.0.0/24", id="range_input")
                yield Button("Szukaj hostów", id="discover_button")
                yield Button("Skanuj porty", id="ports_button")

            with Horizontal(id="main_content"):
                yield HostTable(id="host_table")
                yield HostDetailsView("Wybierz host z listy", id="details_view")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        range_input = self.query_one("#range_input", Input)
        host_table = self.query_one("#host_table", HostTable)
        details_view = self.query_one("#details_view", HostDetailsView)

        if event.button.id == "discover_button":
            ip_range = range_input.value.strip()
            if not ip_range:
                self.notify("Podaj zakres IP.", severity="warning")
                return

            try:
                self.hosts = discover_hosts(ip_range)
            except CommandError as error:
                self.notify(str(error), title="Błąd skanowania", severity="error")
                return

            host_table.load_hosts(self.hosts)

            if self.hosts:
                details_view.show_host(self.hosts[0])
                self.notify(f"Znaleziono hosty: {len(self.hosts)}")
            else:
                details_view.update("Nie wykryto hostów w podanym zakresie")
                self.notify("Nie wykryto hostów.", severity="warning")

        elif event.button.id == "ports_button":
            if not self.hosts:
                self.notify("Najpierw wyszukaj hosty.", severity="warning")
                return

            selected_index = host_table.cursor_row
            if selected_index is None or not (0 <= selected_index < len(self.hosts)):
                self.notify("Wybierz host z tabeli.", severity="warning")
                return

            host = self.hosts[selected_index]

            try:
                host.ports = scan_host_ports(host.ip)
            except CommandError as error:
                self.notify(str(error), title="Błąd skanowania portów", severity="error")
                return

            details_view.show_host(host)
            self.notify(f"Zeskanowano porty hosta {host.ip}")

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id != "host_table":
            return

        row_index = event.cursor_row
        if row_index is None or not (0 <= row_index < len(self.hosts)):
            return

        details_view = self.query_one("#details_view", HostDetailsView)
        details_view.show_host(self.hosts[row_index])

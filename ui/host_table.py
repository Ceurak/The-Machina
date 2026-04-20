from textual.widgets import DataTable
from models.host import Host


class HostTable(DataTable):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.add_columns("Hostname", "IP", "MAC")

    def load_hosts(self, hosts: list[Host]) -> None:
        self.clear(columns=False)

        for host in hosts:
            self.add_row(
                host.hostname or host.ip,
                host.ip,
                host.mac,
            )

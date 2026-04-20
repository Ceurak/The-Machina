from textual.widgets import Static
from models.host import Host


class HostDetailsView(Static):
    def show_host(self, host: Host) -> None:
        lines = [
            f"Hostname: {host.hostname or host.ip}",
            f"IP: {host.ip}",
            f"MAC: {host.mac or '-'}",
            f"Vendor: {host.vendor or '-'}",
            "",
            "Porty:",
        ]

        if host.ports:
            for port in host.ports:
                lines.append(f"{port.port}/{port.protocol}  {port.state}  {port.service}")
        else:
            lines.append("Brak zeskanowanych portów")

        self.update("\n".join(lines))

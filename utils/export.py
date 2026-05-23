import csv
from models.host import Host

# Eksportowanie do csv.
def export_hosts_to_csv(hosts: list[Host], file_path: str = "hosts.csv") -> None:
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "hostname",
            "ip",
            "mac",
            "vendor",
            "ports"
        ])

        for host in hosts:
            ports_text = "; ".join(
                f"{port.port}/{port.protocol} {port.state} {port.service}"
                for port in host.ports
            )

            writer.writerow([
                host.hostname,
                host.ip,
                host.mac,
                host.vendor,
                ports_text
            ])
from models.host import PortInfo
from scanner.parsers import parse_nmap_ports
from utils.command import run_command


# Wyszukanie portów hosta.
def scan_host_ports(ip: str) -> list[PortInfo]:
    output = run_command(["nmap", "-Pn", ip])
    return parse_nmap_ports(output)

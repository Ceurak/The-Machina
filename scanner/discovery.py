from models.host import Host
from scanner.parsers import parse_arp_scan, merge_nmap_hostnames
from utils.command import run_command



def discover_hosts(ip_range: str) -> list[Host]:
    arp_output = run_command(["sudo", "arp-scan", ip_range])
    hosts = parse_arp_scan(arp_output)

    if not hosts:
        return []

    nmap_output = run_command(["nmap", "-sn", "-R", ip_range])
    hosts = merge_nmap_hostnames(hosts, nmap_output)

    for host in hosts:
        if not host.hostname:
            host.hostname = host.ip

    return hosts

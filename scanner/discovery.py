from models.host import Host
from scanner.parsers import parse_arp_scan, merge_nmap_hostnames
from utils.command import run_command


# Wykrycie hostów w sieci za pomocą arp-scan i przeszukanie hostname czy są widoczne. Jak nie przypisanie IP jako hostname.
def discover_hosts(ip_range: str) -> list[Host]:
    arp_output = run_command(["sudo", "/usr/bin/arp-scan", ip_range])
    hosts = parse_arp_scan(arp_output)

    if not hosts:
        return []
    
    hosts = parse_arp_scan(arp_output)
    hosts = rem_duplicate_hosts(hosts)

    nmap_output = run_command(["nmap", "-sn", "-R", ip_range])
    hosts = merge_nmap_hostnames(hosts, nmap_output)

    for host in hosts:
        if not host.hostname:
            host.hostname = host.ip

    return hosts

def rem_duplicate_hosts(hosts: list[Host]) -> list[Host]:
    unique: dict[str, Host] = {}

    for host in hosts:
        if host.ip not in unique:
            unique[host.ip] = host

    return list(unique.values())
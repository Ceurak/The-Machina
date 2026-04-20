import re
from models.host import Host, PortInfo


regex_ip = re.compile(r'\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b')
regex_mac = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b')


def parse_arp_scan(output: str) -> list[Host]:
    hosts: list[Host] = []

    for line in output.splitlines():
        match_ip = regex_ip.search(line)
        match_mac = regex_mac.search(line)

        if match_ip and match_mac:
            hosts.append(
                Host(
                    ip=match_ip.group(),
                    mac=match_mac.group(),
                )
            )

    return hosts


def merge_nmap_hostnames(hosts: list[Host], output: str) -> list[Host]:
    for line in output.splitlines():
        line = line.strip()

        match = re.match(r"Nmap scan report for (.+) \((\d+\.\d+\.\d+\.\d+)\)", line)
        if match:
            hostname = match.group(1)
            ip = match.group(2)

            for host in hosts:
                if host.ip == ip:
                    host.hostname = hostname
                    break
            continue

        match_ip_only = re.match(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)", line)
        if match_ip_only:
            ip = match_ip_only.group(1)
            for host in hosts:
                if host.ip == ip and not host.hostname:
                    host.hostname = ip
                    break

    return hosts


def parse_nmap_ports(output: str) -> list[PortInfo]:
    ports: list[PortInfo] = []

    for line in output.splitlines():
        line = line.strip()
        match = re.match(r"(\d+)/(\w+)\s+(\w+)\s+(.+)", line)
        if not match:
            continue

        ports.append(
            PortInfo(
                port=int(match.group(1)),
                protocol=match.group(2),
                state=match.group(3),
                service=match.group(4).strip(),
            )
        )

    return ports

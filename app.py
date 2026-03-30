import subprocess
import re

# Regex'y potrzebne
regex_ip = re.compile(r'\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b')
regex_mac = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b')

# Arp-scan - pobranie IP i MAC hostów
results_arp = subprocess.run(
    ["sudo", "arp-scan", "--localnet"],
    capture_output=True,
    text=True
)

line_arp = results_arp.stdout.splitlines()

devices = []

# Wyszukanie ip i mac regexem i przypisanie do zmiennej
for line in line_arp:
    match_ip = regex_ip.search(line)
    match_mac = regex_mac.search(line)

    if match_ip and match_mac:
        ip = match_ip.group()
        mac = match_mac.group()
        devices.append((ip, mac))

# Wynik arp'a
for ip, mac in devices:
    print(f"IP: {ip} | MAC: {mac}")

results_nmap = subprocess.run(
    ["nmap", "192.168.0.50"],
    capture_output=True,
    text=True
)

print(results_nmap.stdout)

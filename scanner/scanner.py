import subprocess
import re

# Regex'y potrzebne, pod ip i pod mac
regex_ip = re.compile(r'\b(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b')
regex_mac = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b')


# Zebranie domyślnego IP:
"""
results_def_ip = subprocess.run(
    ["ip", "-br", "a", "|", "grep", "-v", "'^lo'"],
    capture_output=True,
    text=True
)
ini_ip = []
line_ip = results_def_ip.stdout.splitlines()

for line in line_ip:
    ini_ip.append
"""


# Zakres działania
range = input("Podaj zakres IP do skanu:", )

# Arp-scan - pobranie IP i MAC hostów
results_arp = subprocess.run(
    ["sudo", "arp-scan", range],
    capture_output=True,
    text=True
)

line_arp = results_arp.stdout.splitlines()


# Utworzenie słownika z samymi kluczami dla hostów (bez portów)
devices = []

# Wyszukanie ip i mac regexem i przypisanie do zmiennej
for line in line_arp:
    match_ip = regex_ip.search(line)
    match_mac = regex_mac.search(line)

    if match_ip and match_mac:
        ip = match_ip.group()
        mac = match_mac.group()
        devices.append({
            "Hostname": ip,
            "IP": ip,
            "MAC": mac
        })


# Nmap - pobranie IP, hostname,
results_nmap = subprocess.run(
    ["nmap", "-sn", "-R", range],
    capture_output=True,
    text=True
)
line_nmap = results_nmap.stdout.splitlines()

for line in line_nmap:
    line = line.strip()

    match_host = re.match(r"Nmap scan report for (.+) \((\d+\.\d+\.\d+\.\d+)\)", line)
    if match_host:
        hostname = match_host.group(1)
        ip = match_host.group(2)

        for device in devices:
            if device["IP"] == ip:
                device["Hostname"] = hostname
                break


# Wypisanie danych
print("\nWykryte hosty w danym zakresie. Jeśli brak wykrytego hostname - zastąpiąny jest jako IP.")
for device in devices:
    print(f"HOSTNAME: {device['Hostname']} | MAC: {device['MAC']} | IP: {device['IP']}")

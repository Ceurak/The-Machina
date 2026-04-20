from scanner.discovery import discover_hosts


if __name__ == "__main__":
    ip_range = input("Podaj zakres IP do skanu: ").strip()
    hosts = discover_hosts(ip_range)

    print("\nWykryte hosty w danym zakresie. Jeśli brak wykrytego hostname - zastąpiony jest jako IP.")
    for host in hosts:
        print(f"HOSTNAME: {host.hostname} | MAC: {host.mac} | IP: {host.ip}")

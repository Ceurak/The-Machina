from dataclasses import dataclass, field
from typing import List


@dataclass
class PortInfo:
    port: int
    protocol: str
    state: str
    service: str = ""
    version: str = ""


@dataclass
class Host:
    ip: str
    mac: str = ""
    hostname: str = ""
    vendor: str = ""
    ports: List[PortInfo] = field(default_factory=list)

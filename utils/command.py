import subprocess
from typing import List


class CommandError(RuntimeError):
    pass


def run_command(command: List[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise CommandError(f"Komenda zakończyła się błędem: {' '.join(command)}\n{stderr}")

    return result.stdout

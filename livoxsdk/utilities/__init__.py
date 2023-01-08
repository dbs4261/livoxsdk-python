from .network import HostIPForDeviceIp
from . import annotations


def compare_hex(a, b):
    return a.hex(), b.hex(), "".join("1" if a == b else "0" for a, b in zip(a.hex(), b.hex()))

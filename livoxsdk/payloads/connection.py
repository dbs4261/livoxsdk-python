import ctypes
import ipaddress
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class ConnectionRequestPayload(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("ip_address_c", "ip_address"),
    )
    _fields_ = (
        ("ip_address_c", ctypes.c_uint8 * 4),
        ("data_port", ctypes.c_uint16),
        ("command_port", ctypes.c_uint16),
        ("sensor_port", ctypes.c_uint16),
    )

    def __init__(self, ip_address: ipaddress.IPv4Address, data_port: livoxsdk.Port,
                 command_port: livoxsdk.Port, sensor_port: typing.Optional[livoxsdk.Port] = None):
        values = {
            "ip_address_c": (ctypes.c_uint8 * 4).from_buffer_copy(ip_address.packed),
            "data_port": data_port,
            "command_port": command_port,
            "sensor_port": sensor_port if sensor_port is not None else 0,
        }
        super().__init__(**values)

    @property
    def ip_address(self) -> ipaddress.IPv4Address:
        return ipaddress.IPv4Address(bytes(getattr(self, "ip_address_c")))

    @ip_address.setter
    def ip_address(self, val: ipaddress.IPv4Address) -> None:
        setattr(self, "ip_address_c", val.packed)

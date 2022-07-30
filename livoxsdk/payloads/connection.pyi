import ipaddress

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class ConnectionRequestPayload(StructureType):
    data_port: livoxsdk.Port
    command_port: livoxsdk.Port
    sensor_port: livoxsdk.Port = 0

    def __init__(self, ip_address: ipaddress.IPv4Address, data_port: livoxsdk.Port,
                 command_port: livoxsdk.Port, sensor_port: livoxsdk.Port):
        raise NotImplementedError

    @property
    def ip_address(self) -> ipaddress.IPv4Address:
        raise NotImplementedError

    @ip_address.setter
    def ip_address(self, val: ipaddress.IPv4Address) -> None:
        raise NotImplementedError

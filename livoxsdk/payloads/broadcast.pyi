import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


serial_number_length: typing.Final[int] = ...


class BroadcastCode(StructureType):
    @property
    def serial(self) -> str: ...

    @serial.setter
    def serial(self, val: str) -> None: ...

    @property
    def range_code(self) -> int: ...

    @range_code.setter
    def range_code(self, val: int): ...

    def valid(self) -> bool:
        """
        :return: If the range code is a proper null-terminated string
        """
        pass


class BroadcastPayload(StructureType):
    broadcast_code: BroadcastCode
    serial: str
    range_code: int

    def valid(self) -> bool: ...

    @property
    def device_type(self) -> livoxsdk.enums.devices.DeviceType: ...

    @device_type.setter
    def device_type(self, val: livoxsdk.enums.devices.DeviceType) -> None: ...

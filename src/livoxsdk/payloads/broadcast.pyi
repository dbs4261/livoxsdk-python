import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


serial_number_length: typing.Final[int] = ...


class BroadcastCode(StructureType):
    @property
    def serial(self) -> str:
        raise NotImplementedError

    @serial.setter
    def serial(self, val: str) -> None:
        raise NotImplementedError

    @property
    def range_code(self) -> int:
        raise NotImplementedError

    @range_code.setter
    def range_code(self, val: int):
        raise NotImplementedError

    def valid(self) -> bool:
        """
        :return: If the range code is a proper null terminated string
        """
        raise NotImplementedError


class BroadcastPayload(StructureType):
    broadcast_code: BroadcastCode
    serial: str
    range_code: int

    def valid(self) -> bool:
        raise NotImplementedError

    @property
    def device_type(self) -> livoxsdk.enums.devices.DeviceType:
        raise NotImplementedError

    @device_type.setter
    def device_type(self, val: livoxsdk.enums.devices.DeviceType) -> None:
        raise NotImplementedError

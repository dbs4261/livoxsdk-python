import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


serial_number_length: typing.Final[int]


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
        raise NotImplementedError

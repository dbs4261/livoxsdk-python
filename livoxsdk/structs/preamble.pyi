import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class Preamble(StructureType):
    sof: typing.Annotated[int, ctypes.c_uint8] = 170
    version: typing.Annotated[int, ctypes.c_uint8] = 1
    seq_num: typing.Annotated[int, ctypes.c_uint16] = 0
    preamble_crc: typing.Annotated[int, ctypes.c_uint16]

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType: ...

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None: ...

    @property
    def length(self) -> int: ...

    @length.setter
    def length(self, val: typing.Union[int, ctypes.c_uint16]) -> None: ...

    def crc(self) -> int: ...

    def valid(self) -> bool: ...

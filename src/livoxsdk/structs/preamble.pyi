import ctypes

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class Preamble(StructureType):
    sof: ctypes.c_uint8 = 170
    version: ctypes.c_uint8 = 1
    seq_num: ctypes.c_uint16 = 0
    preamble_crc: ctypes.c_uint16

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType:
        raise NotImplementedError

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None:
        raise NotImplementedError

    @property
    def length(self) -> ctypes.c_uint16:
        raise NotImplementedError

    @length.setter
    def length(self, val: ctypes.c_uint16) -> None:
        raise NotImplementedError

    def crc(self) -> int:
        raise NotImplementedError

    def valid(self) -> bool:
        raise NotImplementedError

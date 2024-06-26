import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.utilities.annotations import LowerBound, UpperBound


class Preamble(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("packet_type_c", "packet_type"),
        ("_length", "length"),
        ("sof", None),
        ("version", None),
    )
    _fields_ = (
        ("sof", ctypes.c_uint8),
        ("version", ctypes.c_uint8),
        ("_length", ctypes.c_uint16),
        ("packet_type_c", ctypes.c_uint8),
        ("seq_num", ctypes.c_uint16),
        ("preamble_crc", ctypes.c_uint16),
    )
    _defaults_ = {
        "sof": 170,
        "version": 1,
        "seq_num": 0,
    }

    def __int__(self, **kwargs):
        super().__init__(**kwargs)
        setattr(self, "preamble_crc", self.crc())

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType:
        return livoxsdk.enums.MessageType(getattr(self, "packet_type_c"))

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None:
        setattr(self, "packet_type_c", ctypes.c_uint8(val))

    @property
    def length(self) -> int:
        return getattr(self, "_length")

    @length.setter
    def length(self, val: typing.Union[int, ctypes.c_uint16]) -> None:
        assert(isinstance(val, ctypes.c_uint16) or (val >= 0 and val.bit_length() <=16))
        setattr(self, "_length", val)

    def crc(self) -> int:
        return livoxsdk.crc.crc16Func(bytes(self)[:getattr(type(self), "preamble_crc").offset])

    def valid(self) -> bool:
        return self.crc() == getattr(self, "preamble_crc")

import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.status import StatusUnion
from .timestamp import timestamp_type, timestamp_type_from_enum


serial_number_length: typing.Final[int] = 14


class DataPacketHeader(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("_rsvd", None),
        ("data_type_c", "data_type"),
        ("timestamp_type_c", None),
        ("timestamp_c", "timestamp"),
    )
    _fields_ = (
        ("version", ctypes.c_uint8),
        ("slot", ctypes.c_uint8),
        ("id", ctypes.c_uint8),
        ("_rsvd", ctypes.c_uint8),
        ("err_code", StatusUnion),
        ("timestamp_type_c", ctypes.c_uint8),
        ("data_type_c", ctypes.c_uint8),
        ("timestamp_c", ctypes.c_uint64),
    )

    @property
    def data_type(self) -> livoxsdk.enums.PointDataType:
        return livoxsdk.enums.PointDataType(getattr(self, "data_type_c"))

    @data_type.setter
    def data_type(self, val: livoxsdk.enums.PointDataType) -> None:
        setattr(self, "state_c", ctypes.c_uint8(val.value))

    @property
    def timestamp_type(self) -> livoxsdk.enums.TimestampType:
        return livoxsdk.enums.TimestampType(getattr(self, "timestamp_type_c"))

    @property
    def timestamp(self) -> livoxsdk.structs.Timestamp:
        OutType = timestamp_type_from_enum(self.timestamp_type)
        return OutType(getattr(self, "timestamp_c"))

    @timestamp.setter
    def timestamp(self, stamp: livoxsdk.structs.Timestamp) -> None:
        setattr(self, "timestamp_type_c", ctypes.c_uint8(timestamp_type(stamp).value))
        setattr(self, "timestamp_c", ctypes.c_uint64.from_buffer(bytes(stamp)))


class DataPacket(livoxsdk.BinarySerializable):
    header: DataPacketHeader
    raw_payload: bytearray

    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "DataPacket": ...

    def get_payload(self) -> typing.Union[bytes, livoxsdk.BinarySerializable, typing.Any]:
        raise NotImplementedError

    def set_payload(self, val: typing.SupportsBytes) -> None:
        raise NotImplementedError

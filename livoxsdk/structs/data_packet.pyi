import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points import PointUnionType


class DataPacketHeader(StructureType):
    version: ctypes.c_uint8
    slot: ctypes.c_uint8
    id: ctypes.c_uint8
    err_code: livoxsdk.structs.StatusUnion

    @property
    def data_type(self) -> livoxsdk.enums.PointDataType:
        raise NotImplementedError

    @data_type.setter
    def data_type(self, dtype: livoxsdk.enums.PointDataType) -> None:
        raise NotImplementedError

    @property
    def timestamp_type(self) -> livoxsdk.enums.TimestampType:
        raise NotImplementedError

    @property
    def timestamp(self) -> livoxsdk.structs.Timestamp:
        raise NotImplementedError

    @timestamp.setter
    def timestamp(self, stamp: livoxsdk.structs.Timestamp) -> None:
        raise NotImplementedError


class DataPacket:
    header: DataPacketHeader
    payload: ctypes.Array

    def __init__(self, header: DataPacketHeader, payload: typing.Union[ctypes.Array, PointUnionType]): ...

    def __bytes__(self) -> bytes: ...

    def __str__(self) -> str: ...

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "DataPacket": ...

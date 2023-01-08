import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points import PointUnionListType


class DataPacketHeader(StructureType):
    version: typing.Annotated[int, ctypes.c_uint8]
    slot: typing.Annotated[int, ctypes.c_uint8]
    id: typing.Annotated[int, ctypes.c_uint8]
    err_code: livoxsdk.structs.StatusUnion

    @property
    def data_type(self) -> livoxsdk.enums.PointDataType: ...

    @data_type.setter
    def data_type(self, dtype: livoxsdk.enums.PointDataType) -> None: ...

    @property
    def timestamp_type(self) -> livoxsdk.enums.TimestampType: ...

    @property
    def timestamp(self) -> livoxsdk.structs.Timestamp: ...

    @timestamp.setter
    def timestamp(self, stamp: livoxsdk.structs.Timestamp) -> None: ...


class DataPacket:
    header: DataPacketHeader
    payload: ctypes.Array

    def __init__(self, header: DataPacketHeader, payload: typing.Union[ctypes.Array, PointUnionListType]): ...

    def __bytes__(self) -> bytes: ...

    def __str__(self) -> str: ...

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "DataPacket": ...

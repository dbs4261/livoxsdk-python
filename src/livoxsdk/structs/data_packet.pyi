import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


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
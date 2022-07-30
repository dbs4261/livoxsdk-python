import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.status import StatusUnion
from livoxsdk.structs.timestamp import timestamp_type, timestamp_type_from_enum, Timestamp
from livoxsdk.structs.points import point_type_from_enum, PointUnionType


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
    def timestamp(self) -> Timestamp:
        OutType = timestamp_type_from_enum(self.timestamp_type)
        return OutType(getattr(self, "timestamp_c"))

    @timestamp.setter
    def timestamp(self, stamp: Timestamp) -> None:
        setattr(self, "timestamp_type_c", ctypes.c_uint8(timestamp_type(stamp).value))
        setattr(self, "timestamp_c", ctypes.c_uint64.from_buffer(bytes(stamp)))


class DataPacket:
    header: DataPacketHeader
    payload: ctypes.Array

    def __init__(self, header: DataPacketHeader,
                 payload: typing.Union[ctypes.Array, PointUnionType]):
        self.header: DataPacketHeader = header
        if isinstance(payload, ctypes.Array):
            self.payload: ctypes.Array = payload
        else:
            ArrayType = type(payload[0]) * len(payload)
            self.payload: ctypes.Array = ArrayType()
            for i in range(len(payload)):
                self.payload[i] = payload[i]

    def __bytes__(self) -> bytes:
        return bytes(self.header) + bytes(self.payload)

    def __str__(self) -> str:
        return "DataPacket: {{{}, {} points}}".format(self.header, len(self.payload))

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "DataPacket":
        header = DataPacketHeader.from_buffer_copy(source, offset)
        offset += ctypes.sizeof(DataPacketHeader)
        PointType: typing.Type[PointUnionType] = point_type_from_enum(header.data_type)
        buffer_size = source.nbytes if isinstance(source, memoryview) else len(source)
        num_points = (buffer_size - ctypes.sizeof(DataPacketHeader)) // ctypes.sizeof(PointType)
        points = (PointType * num_points).from_buffer_copy(source, offset)
        return DataPacket(header, points)


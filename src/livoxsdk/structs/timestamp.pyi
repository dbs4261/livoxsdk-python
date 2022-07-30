import ctypes
import dataclasses
import datetime
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


@dataclasses.dataclass(init=True, repr=True, eq=True, order=True, unsafe_hash=True)
class PreciseTimestamp:
    date_time: datetime.datetime
    nanoseconds: int  # range(1000)

    def __str__(self) -> str:
        raise NotImplementedError


class TimestampPTP(StructureType):
    nanosecond: int  # ctypes.c_uint64

    @property
    def precise_timestamp(self) -> PreciseTimestamp:
        raise NotImplementedError

    @precise_timestamp.setter
    def precise_timestamp(self, timestamp: PreciseTimestamp) -> None:
        raise NotImplementedError


TimestampNoSync = typing.NewType("TimestampNoSync", TimestampPTP)
TimestampPps = typing.NewType("TimestampPps", TimestampPTP)


class TimestampUTC(StructureType):
    year: int  # ctypes.c_uint8
    month: int  # ctypes.c_uint8
    day: int  # ctypes.c_uint8
    hour: int  # ctypes.c_uint8
    microsecond: int  # ctypes.c_uint32

    @property
    def precise_timestamp(self) -> PreciseTimestamp:
        raise NotImplementedError

    @precise_timestamp.setter
    def precise_timestamp(self, timestamp: PreciseTimestamp) -> None:
        raise NotImplementedError


TimestampPpsGps = typing.TypeAlias = TimestampUTC

Timestamp: typing.TypeAlias = typing.Union[ctypes.c_uint64, TimestampNoSync, TimestampPTP, TimestampPps, TimestampUTC, TimestampPpsGps]


def timestamp_type(timestamp: Timestamp) -> livoxsdk.enums.TimestampType:
    raise NotImplementedError

def timestamp_type_from_enum(timestamp_enum: livoxsdk.enums.TimestampType) -> type:
    raise NotImplementedError
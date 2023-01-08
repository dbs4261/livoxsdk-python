import ctypes
import dataclasses
import datetime
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.utilities.annotations import LowerBound, UpperBound


@dataclasses.dataclass(repr=True, eq=True, order=True, unsafe_hash=True)
class PreciseTimestamp:
    date_time: datetime.datetime
    nanoseconds: typing.Annotated[int, LowerBound[int](0), UpperBound[int](1000, False)]

    def __init__(self, date_time: datetime.datetime, nanoseconds: int): ...

    def __str__(self) -> str: ...


class TimestampPTP(StructureType):
    nanosecond: typing.Annotated[int, ctypes.c_uint64]

    @typing.overload
    def __init__(self, nanosecond: int): ...

    @typing.overload
    def __init__(self, precise_timestamp: PreciseTimestamp): ...

    def precise_timestamp(self) -> PreciseTimestamp: ...


TimestampNoSync = typing.NewType("TimestampNoSync", TimestampPTP)
TimestampPps = typing.NewType("TimestampPps", TimestampPTP)


class TimestampUTC(StructureType):
    year: typing.Annotated[int, ctypes.c_uint8]
    month: typing.Annotated[int, ctypes.c_uint8]
    day: typing.Annotated[int, ctypes.c_uint8]
    hour: typing.Annotated[int, ctypes.c_uint8]
    microsecond: typing.Annotated[int, ctypes.c_uint32]

    @typing.overload
    def __init__(self, year: int = 0, month: int = 0, day: int = 0, hour: int = 0, microsecond: int = 0): ...

    @typing.overload
    def __init__(self, precise_timestamp: PreciseTimestamp): ...

    def precise_timestamp(self) -> PreciseTimestamp: ...


TimestampPpsGps = typing.TypeAlias = TimestampUTC

Timestamp: typing.TypeAlias = typing.Union[ctypes.c_uint64, TimestampNoSync, TimestampPTP, TimestampPps, TimestampUTC, TimestampPpsGps]


def timestamp_type(timestamp: Timestamp) -> livoxsdk.enums.TimestampType: ...

def timestamp_type_from_enum(timestamp_enum: livoxsdk.enums.TimestampType) -> typing.Type[Timestamp]: ...
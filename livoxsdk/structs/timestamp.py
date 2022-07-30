import ctypes
import dataclasses
import datetime
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType

logger = livoxsdk.logging_helpers.logger

_max_microseconds: typing.Final[int] = 60 * 60 * 1000 * 1000
_epoch: typing.Final[datetime.datetime] = datetime.datetime.utcfromtimestamp(0)


@dataclasses.dataclass(init=True, repr=True, eq=True, order=True, unsafe_hash=True)
class PreciseTimestamp:
    date_time: datetime.datetime
    nanoseconds: int

    def __str__(self) -> str:
        return self.date_time.strftime("%Y-%m-%d_%H:%M:%S.%f") + \
               f"{self.nanoseconds:03}"[-3:]


class TimestampPTP(StructureType):
    _pack_ = 1
    _fields_ = (
        ("nanosecond", ctypes.c_uint64),
    )

    @property
    def precise_timestamp(self) -> PreciseTimestamp:
        return PreciseTimestamp(_epoch + datetime.timedelta(microseconds=
            self.nanosecond // 1000), self.nanosecond % 1000)

    @precise_timestamp.setter
    def precise_timestamp(self, timestamp: PreciseTimestamp) -> None:
        delta = (timestamp.date_time - _epoch)
        self.nanosecond = timestamp.nanoseconds + 1000 * (delta.microseconds +
            1000 * 1000 * (delta.seconds + 60 * 60 * 24 * delta.days))


assert(ctypes.sizeof(TimestampPTP) == ctypes.sizeof(ctypes.c_uint64))

TimestampNoSync = typing.NewType("TimestampNoSync", TimestampPTP)
TimestampPps = typing.NewType("TimestampPps", TimestampPTP)


class TimestampUTC(StructureType):
    _pack_ = 1
    _fields_ = (
        ("year", ctypes.c_uint8),
        ("month", ctypes.c_uint8),
        ("day", ctypes.c_uint8),
        ("hour", ctypes.c_uint8),
        ("microsecond", ctypes.c_uint32),
    )

    @property
    def precise_timestamp(self) -> PreciseTimestamp:
        return PreciseTimestamp(datetime.datetime(year=self.year, month=self.month,
            day=self.day, hour=self.hour, microsecond=self.microsecond), 0)

    @precise_timestamp.setter
    def precise_timestamp(self, timestamp: precise_timestamp) -> None:
        if timestamp.nanoseconds != 0:
            livoxsdk.logging_helpers.logger.getChild("TimestampUTC").getChild("set_precise_timestamp").warning(
                "TimestampUTC doesnt support nanosecond precision")
        self.year = timestamp.date_time.year
        self.month = timestamp.date_time.month
        self.day = timestamp.date_time.day
        self.hour = timestamp.date_time.hour
        self.microsecond = timestamp.date_time.microsecond + 1000000 * \
                           (timestamp.second + 60 * timestamp.date_time.minute)


assert(ctypes.sizeof(TimestampUTC) == ctypes.sizeof(ctypes.c_uint64))

TimestampPpsGps = typing.TypeAlias = TimestampUTC

Timestamp: typing.TypeAlias = typing.Union[ctypes.c_uint64, TimestampNoSync, TimestampPTP, TimestampPps, TimestampUTC, TimestampPpsGps]


def timestamp_type(timestamp: Timestamp) -> livoxsdk.enums.TimestampType:
    if isinstance(timestamp, TimestampNoSync):
        return livoxsdk.enums.TimestampType.NoSync
    elif isinstance(timestamp, TimestampPTP):
        return livoxsdk.enums.TimestampType.Ptp
    elif isinstance(timestamp, TimestampPpsGps):
        return livoxsdk.enums.TimestampType.PpsGps
    elif isinstance(timestamp, TimestampPps):
        return livoxsdk.enums.TimestampType.Pps
    else:
        return livoxsdk.enums.TimestampType.Unknown


def timestamp_type_from_enum(timestamp_enum: livoxsdk.enums.TimestampType) -> type:
    if timestamp_enum == livoxsdk.enums.TimestampType.NoSync:
        return TimestampNoSync
    elif timestamp_enum == livoxsdk.enums.TimestampType.Ptp:
        return TimestampPTP
    elif timestamp_enum == livoxsdk.enums.TimestampType.PpsGps:
        return TimestampPpsGps
    elif timestamp_enum == livoxsdk.enums.TimestampType.Pps:
        return TimestampPps
    else:
        return ctypes.c_uint64

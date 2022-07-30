import enum
import typing


class CoordinateSystem(enum.IntEnum):
    Cartesian = enum.auto()
    Spherical = enum.auto()


class PointCloudReturnMode(enum.Enum):
    FirstReturn = enum.auto()
    StrongestReturn = enum.auto()
    DualReturn = enum.auto()
    TripleReturn = enum.auto()


class PointDataType(enum.Enum):
    Cartesian = enum.auto()
    Spherical = enum.auto()
    ExtendCartesian = enum.auto()
    ExtendSpherical = enum.auto()
    DualExtendCartesian = enum.auto()
    DualExtendSpherical = enum.auto()
    Imu = enum.auto()
    TripleExtendCartesian = enum.auto()
    TripleExtendSpherical = enum.auto()
    MaxPointDataType = enum.auto()

    @staticmethod
    def from_return_mode(coordinate_system: CoordinateSystem, return_mode: PointCloudReturnMode) -> "PointDataType":
        if coordinate_system not in CoordinateSystem:
            raise TypeError
        if return_mode not in PointCloudReturnMode:
            raise TypeError
        if return_mode == PointCloudReturnMode.FirstReturn or return_mode == PointCloudReturnMode.StrongestReturn:
            if coordinate_system == CoordinateSystem.Cartesian:
                return PointDataType.ExtendCartesian
            elif coordinate_system == CoordinateSystem.Spherical:
                return PointDataType.ExtendSpherical
        elif return_mode == PointCloudReturnMode.DualReturn:
            if coordinate_system == CoordinateSystem.Cartesian:
                return PointDataType.DualExtendCartesian
            elif coordinate_system == CoordinateSystem.Spherical:
                return PointDataType.DualExtendSpherical
        elif return_mode == PointCloudReturnMode.TripleReturn:
            if coordinate_system == CoordinateSystem.Cartesian:
                return PointDataType.TripleExtendCartesian
            elif coordinate_system == CoordinateSystem.Spherical:
                return PointDataType.TripleExtendSpherical
        raise NotImplementedError

    @property
    def coordinate_system(self) -> typing.Optional[CoordinateSystem]:
        if self in [PointDataType.Cartesian, PointDataType.ExtendCartesian, PointDataType.DualExtendCartesian, PointDataType.TripleExtendCartesian]:
            return CoordinateSystem.Cartesian
        elif self in [PointDataType.Spherical, PointDataType.ExtendSpherical, PointDataType.DualExtendSpherical, PointDataType.TripleExtendSpherical]:
            return CoordinateSystem.Spherical
        else:
            return None


class ImuFreq(enum.Enum):
    Freq0Hz = enum.auto()
    Freq200Hz = enum.auto()


class TimestampType(enum.IntEnum):
    NoSync = 0
    Ptp = 1
    Rsvd = 2
    PpsGps = 3
    Pps = 4
    Unknown = 5

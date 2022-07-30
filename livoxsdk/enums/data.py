import enum
import typing


class CoordinateSystem(enum.IntEnum):
    Cartesian = 0
    Spherical = 1


class PointCloudReturnMode(enum.IntEnum):
    FirstReturn = 0
    StrongestReturn = 1
    DualReturn = 2
    TripleReturn = 3


class PointDataType(enum.IntEnum):
    Cartesian = 0
    Spherical = 1
    ExtendCartesian = 2
    ExtendSpherical = 3
    DualExtendCartesian = 4
    DualExtendSpherical = 5
    Imu = 6
    TripleExtendCartesian = 7
    TripleExtendSpherical = 8
    MaxPointDataType = 9

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

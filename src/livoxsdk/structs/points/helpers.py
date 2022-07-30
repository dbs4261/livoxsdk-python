import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from .raw import RawPoint, SpherPoint
from .single import ExtendRawPoint, ExtendSpherPoint
from .dual import DualExtendRawPoint, DualExtendSpherPoint
from .triple import TripleExtendRawPoint, TripleExtendSpherPoint
from .imu import ImuPoint


_point_structs: typing.List[typing.Type[StructureType]] = [
    RawPoint,
    SpherPoint,
    ExtendRawPoint,
    ExtendSpherPoint,
    DualExtendRawPoint,
    DualExtendSpherPoint,
    TripleExtendRawPoint,
    TripleExtendSpherPoint,
    ImuPoint,
]

PointUnionType = typing.Union[
    typing.Type[RawPoint],
    typing.Type[SpherPoint],
    typing.Type[ExtendRawPoint],
    typing.Type[ExtendSpherPoint],
    typing.Type[DualExtendRawPoint],
    typing.Type[DualExtendSpherPoint],
    typing.Type[TripleExtendRawPoint],
    typing.Type[TripleExtendSpherPoint],
    typing.Type[ImuPoint],
]


PointUnionListType = typing.Union[tuple(typing.List[t] for t in PointUnionType.__args__)]


def point_type_from_enum(val: livoxsdk.enums.PointDataType) -> typing.Type[PointUnionType]:
    if val == livoxsdk.enums.PointDataType.Cartesian:
        return RawPoint
    elif val == livoxsdk.enums.PointDataType.Spherical:
        return SpherPoint
    elif val == livoxsdk.enums.PointDataType.ExtendCartesian:
        return ExtendRawPoint
    elif val == livoxsdk.enums.PointDataType.ExtendSpherical:
        return ExtendSpherPoint
    elif val == livoxsdk.enums.PointDataType.DualExtendCartesian:
        return DualExtendRawPoint
    elif val == livoxsdk.enums.PointDataType.DualExtendSpherical:
        return DualExtendSpherPoint
    elif val == livoxsdk.enums.PointDataType.Imu:
        return ImuPoint
    elif val == livoxsdk.enums.PointDataType.TripleExtendCartesian:
        return TripleExtendRawPoint
    elif val == livoxsdk.enums.PointDataType.TripleExtendSpherical:
        return TripleExtendSpherPoint
    else:
        raise ValueError


def point_enum_from_type(t: typing.Type[PointUnionType]) -> livoxsdk.enums.PointDataType:
    if t == RawPoint:
        return livoxsdk.enums.PointDataType.Cartesian
    elif t == SpherPoint:
        return livoxsdk.enums.PointDataType.Spherical
    elif t == ExtendRawPoint:
        return livoxsdk.enums.PointDataType.ExtendCartesian
    elif t == ExtendSpherPoint:
        return livoxsdk.enums.PointDataType.ExtendSpherical
    elif t == DualExtendRawPoint:
        return livoxsdk.enums.PointDataType.DualExtendCartesian
    elif t == DualExtendSpherPoint:
        return livoxsdk.enums.PointDataType.DualExtendSpherical
    elif t == ImuPoint:
        return livoxsdk.enums.PointDataType.Imu
    elif t == TripleExtendRawPoint:
        return livoxsdk.enums.PointDataType.TripleExtendCartesian
    elif t == TripleExtendSpherPoint:
        return livoxsdk.enums.PointDataType.TripleExtendSpherical
    else:
        raise TypeError


def point_enum_from_point(point: PointUnionType) -> livoxsdk.enums.PointDataType:
    return point_enum_from_type(type(point))

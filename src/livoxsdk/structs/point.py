import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class RawPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("x", ctypes.c_int32),
        ("y", ctypes.c_int32),
        ("z", ctypes.c_int32),
        ("reflectivity", ctypes.c_uint8)
    ]


Point: typing.TypeAlias = RawPoint
CartesianPoint: typing.TypeAlias = RawPoint


class SpherPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("depth", ctypes.c_uint32),
        ("theta", ctypes.c_uint16),
        ("phi", ctypes.c_uint16),
        ("reflectivity", ctypes.c_uint8)
    ]


SphericalPoint: typing.TypeAlias = SpherPoint


class ExtendRawPoint(StructureType):
    _fields_ = [
        ("x", ctypes.c_int32),
        ("y", ctypes.c_int32),
        ("z", ctypes.c_int32),
        ("reflectivity", ctypes.c_uint8),
        ("tag", ctypes.c_uint8)
    ]


ExtendCartesianPoint: typing.TypeAlias = ExtendRawPoint
ExtendedRawPoint: typing.TypeAlias = ExtendRawPoint
ExtendedCartesianPoint: typing.TypeAlias = ExtendedRawPoint


class ExtendSpherPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("depth", ctypes.c_uint32),
        ("theta", ctypes.c_uint16),
        ("phi", ctypes.c_uint16),
        ("reflectivity", ctypes.c_uint8),
        ("tag", ctypes.c_uint8)
    ]


ExtendSphericalPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSpherPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSphericalPoint: typing.TypeAlias = ExtendSpherPoint


class DualExtendRawPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("x1", ctypes.c_int32),
        ("y1", ctypes.c_int32),
        ("z1", ctypes.c_int32),
        ("reflectivity1", ctypes.c_uint8),
        ("tag1", ctypes.c_uint8),
        ("x2", ctypes.c_int32),
        ("y2", ctypes.c_int32),
        ("z2", ctypes.c_int32),
        ("reflectivity2", ctypes.c_uint8),
        ("tag2", ctypes.c_uint8)
    ]


DualExtendCartesianPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedRawPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedCartesianPoint: typing.TypeAlias = DualExtendRawPoint


class DualExtendSpherPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("theta", ctypes.c_uint16),
        ("phi", ctypes.c_uint16),
        ("depth1", ctypes.c_uint32),
        ("reflectivity1", ctypes.c_uint8),
        ("tag1", ctypes.c_uint8),
        ("depth2", ctypes.c_uint32),
        ("reflectivity2", ctypes.c_uint8),
        ("tag2", ctypes.c_uint8)
    ]


DualExtendSphericalPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSpherPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSphericalPoint: typing.TypeAlias = DualExtendSpherPoint


class TripleExtendRawPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("x1", ctypes.c_int32),
        ("y1", ctypes.c_int32),
        ("z1", ctypes.c_int32),
        ("reflectivity1", ctypes.c_uint8),
        ("tag1", ctypes.c_uint8),
        ("x2", ctypes.c_int32),
        ("y2", ctypes.c_int32),
        ("z2", ctypes.c_int32),
        ("reflectivity2", ctypes.c_uint8),
        ("tag2", ctypes.c_uint8),
        ("x3", ctypes.c_int32),
        ("y3", ctypes.c_int32),
        ("z3", ctypes.c_int32),
        ("reflectivity3", ctypes.c_uint8),
        ("tag3", ctypes.c_uint8)
    ]


TripleExtendCartesianPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedRawPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedCartesianPoint: typing.TypeAlias = TripleExtendRawPoint


class TripleExtendSpherPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("theta", ctypes.c_uint16),
        ("phi", ctypes.c_uint16),
        ("depth1", ctypes.c_uint32),
        ("reflectivity1", ctypes.c_uint8),
        ("tag1", ctypes.c_uint8),
        ("depth2", ctypes.c_uint32),
        ("reflectivity2", ctypes.c_uint8),
        ("tag2", ctypes.c_uint8),
        ("depth3", ctypes.c_uint32),
        ("reflectivity3", ctypes.c_uint8),
        ("tag3", ctypes.c_uint8)
    ]


TripleExtendSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSpherPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint


class ImuPoint(StructureType):
    _pack_ = 1
    _fields_ = [
        ("gyro_x", ctypes.c_float),
        ("gyro_y", ctypes.c_float),
        ("gyro_z", ctypes.c_float),
        ("acc_x", ctypes.c_float),
        ("acc_y", ctypes.c_float),
        ("acc_z", ctypes.c_float)
    ]


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

import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class RawPoint(StructureType):
    x: ctypes.c_int32
    y: ctypes.c_int32
    z: ctypes.c_int32
    reflectivity: ctypes.c_uint8


Point: typing.TypeAlias = RawPoint
CartesianPoint: typing.TypeAlias = RawPoint


class SpherPoint(StructureType):
    depth: ctypes.c_uint32
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    reflectivity: ctypes.c_uint8


SphericalPoint: typing.TypeAlias = SpherPoint


class ExtendRawPoint(StructureType):
    x: ctypes.c_int32
    y: ctypes.c_int32
    z: ctypes.c_int32
    reflectivity: ctypes.c_uint8
    tag: ctypes.c_uint8


ExtendCartesianPoint: typing.TypeAlias = ExtendRawPoint
ExtendedRawPoint: typing.TypeAlias = ExtendRawPoint
ExtendedCartesianPoint: typing.TypeAlias = ExtendedRawPoint


class ExtendSpherPoint(StructureType):
    depth: ctypes.c_uint32
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    reflectivity: ctypes.c_uint8
    tag: ctypes.c_uint8


ExtendSphericalPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSpherPoint: typing.TypeAlias = ExtendSpherPoint
ExtendedSphericalPoint: typing.TypeAlias = ExtendSpherPoint


class DualExtendRawPoint(StructureType):
    x1: ctypes.c_int32
    y1: ctypes.c_int32
    z1: ctypes.c_int32
    reflectivity1: ctypes.c_uint8
    tag1: ctypes.c_uint8
    x2: ctypes.c_int32
    y2: ctypes.c_int32
    z2: ctypes.c_int32
    reflectivity2: ctypes.c_uint8
    tag2: ctypes.c_uint8


DualExtendCartesianPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedRawPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedCartesianPoint: typing.TypeAlias = DualExtendRawPoint


class DualExtendSpherPoint(StructureType):
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    depth1: ctypes.c_uint32
    reflectivity1: ctypes.c_uint8
    tag1: ctypes.c_uint8
    depth2: ctypes.c_uint32
    reflectivity2: ctypes.c_uint8
    tag2: ctypes.c_uint8


DualExtendSphericalPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSpherPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSphericalPoint: typing.TypeAlias = DualExtendSpherPoint


class TripleExtendRawPoint(StructureType):
    x1: ctypes.c_int32
    y1: ctypes.c_int32
    z1: ctypes.c_int32
    reflectivity1: ctypes.c_uint8
    tag1: ctypes.c_uint8
    x2: ctypes.c_int32
    y2: ctypes.c_int32
    z2: ctypes.c_int32
    reflectivity2: ctypes.c_uint8
    tag2: ctypes.c_uint8
    x3: ctypes.c_int32
    y3: ctypes.c_int32
    z3: ctypes.c_int32
    reflectivity3: ctypes.c_uint8
    tag3: ctypes.c_uint8


TripleExtendCartesianPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedRawPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedCartesianPoint: typing.TypeAlias = TripleExtendRawPoint


class TripleExtendSpherPoint(StructureType):
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    depth1: ctypes.c_uint32
    reflectivity1: ctypes.c_uint8
    tag1: ctypes.c_uint8
    depth2: ctypes.c_uint32
    reflectivity2: ctypes.c_uint8
    tag2: ctypes.c_uint8
    depth3: ctypes.c_uint32
    reflectivity3: ctypes.c_uint8
    tag3: ctypes.c_uint8


TripleExtendSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSpherPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint


class ImuPoint(StructureType):
    gyro_x: ctypes.c_float
    gyro_y: ctypes.c_float
    gyro_z: ctypes.c_float
    acc_x: ctypes.c_float
    acc_y: ctypes.c_float
    acc_z: ctypes.c_float


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
    raise NotImplementedError


def point_enum_from_type(t: typing.Type[PointUnionType]) -> livoxsdk.enums.PointDataType:
    raise NotImplementedError


def point_enum_from_point(point: PointUnionType) -> livoxsdk.enums.PointDataType:
    raise NotImplementedError

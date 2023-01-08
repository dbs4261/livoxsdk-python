import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
# noinspection PyUnresolvedReferences
from livoxsdk.structs.points.return_tag import _add_return_tag_bitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


@_add_return_tag_bitfield
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
        ("tag2", ctypes.c_uint8),
    ]

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 2, True)


DualExtendCartesianPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedRawPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedCartesianPoint: typing.TypeAlias = DualExtendRawPoint


@_add_return_tag_bitfield
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
        ("tag2", ctypes.c_uint8),
    ]

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 2, False)


DualExtendSphericalPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSpherPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSphericalPoint: typing.TypeAlias = DualExtendSpherPoint

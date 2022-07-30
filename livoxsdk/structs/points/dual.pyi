import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_tag import ReturnTagBitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


class DualExtendRawPoint(StructureType):
    x1: ctypes.c_int32
    y1: ctypes.c_int32
    z1: ctypes.c_int32
    reflectivity1: ctypes.c_uint8
    tag1: ctypes.c_uint8
    tag1_bitfield: ReturnTagBitfield
    x2: ctypes.c_int32
    y2: ctypes.c_int32
    z2: ctypes.c_int32
    reflectivity2: ctypes.c_uint8
    tag2: ctypes.c_uint8
    tag2_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 2, True)


DualExtendCartesianPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedRawPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedCartesianPoint: typing.TypeAlias = DualExtendRawPoint


class DualExtendSpherPoint(StructureType):
    theta: ctypes.c_uint16
    phi: ctypes.c_uint16
    depth1: ctypes.c_uint32
    reflectivity1: ctypes.c_uint8
    tag1: ctypes.c_uint8
    tag1_bitfield: ReturnTagBitfield
    depth2: ctypes.c_uint32
    reflectivity2: ctypes.c_uint8
    tag2: ctypes.c_uint8
    tag2_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 2, False)


DualExtendSphericalPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSpherPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSphericalPoint: typing.TypeAlias = DualExtendSpherPoint

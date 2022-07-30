import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_tag import ReturnTagBitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


class TripleExtendRawPoint(StructureType):
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
    x3: ctypes.c_int32
    y3: ctypes.c_int32
    z3: ctypes.c_int32
    reflectivity3: ctypes.c_uint8
    tag3: ctypes.c_uint8
    tag3_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 3, True)


TripleExtendCartesianPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedRawPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedCartesianPoint: typing.TypeAlias = TripleExtendRawPoint


class TripleExtendSpherPoint(StructureType):
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
    depth3: ctypes.c_uint32
    reflectivity3: ctypes.c_uint8
    tag3: ctypes.c_uint8
    tag3_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator:
        return ReturnIterator(self, 3, False)


TripleExtendSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSpherPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint

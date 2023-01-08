import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_tag import ReturnTagBitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


class TripleExtendRawPoint(StructureType):
    x1: typing.Annotated[int, ctypes.c_int32]
    y1: typing.Annotated[int, ctypes.c_int32]
    z1: typing.Annotated[int, ctypes.c_int32]
    reflectivity1: typing.Annotated[int, ctypes.c_uint8]
    tag1: typing.Annotated[int, ctypes.c_uint8]
    tag1_bitfield: ReturnTagBitfield
    x2: typing.Annotated[int, ctypes.c_int32]
    y2: typing.Annotated[int, ctypes.c_int32]
    z2: typing.Annotated[int, ctypes.c_int32]
    reflectivity2: typing.Annotated[int, ctypes.c_uint8]
    tag2: typing.Annotated[int, ctypes.c_uint8]
    tag2_bitfield: ReturnTagBitfield
    x3: typing.Annotated[int, ctypes.c_int32]
    y3: typing.Annotated[int, ctypes.c_int32]
    z3: typing.Annotated[int, ctypes.c_int32]
    reflectivity3: typing.Annotated[int, ctypes.c_uint8]
    tag3: typing.Annotated[int, ctypes.c_uint8]
    tag3_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator: ...


TripleExtendCartesianPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedRawPoint: typing.TypeAlias = TripleExtendRawPoint
TripleExtendedCartesianPoint: typing.TypeAlias = TripleExtendRawPoint


class TripleExtendSpherPoint(StructureType):
    theta: typing.Annotated[int, ctypes.c_uint16]
    phi: typing.Annotated[int, ctypes.c_uint16]
    depth1: typing.Annotated[int, ctypes.c_uint32]
    reflectivity1: typing.Annotated[int, ctypes.c_uint8]
    tag1: typing.Annotated[int, ctypes.c_uint8]
    tag1_bitfield: ReturnTagBitfield
    depth2: typing.Annotated[int, ctypes.c_uint32]
    reflectivity2: typing.Annotated[int, ctypes.c_uint8]
    tag2: typing.Annotated[int, ctypes.c_uint8]
    tag2_bitfield: ReturnTagBitfield
    depth3: typing.Annotated[int, ctypes.c_uint32]
    reflectivity3: typing.Annotated[int, ctypes.c_uint8]
    tag3: typing.Annotated[int, ctypes.c_uint8]
    tag3_bitfield: ReturnTagBitfield

    def __iter__(self) -> ReturnIterator: ...


TripleExtendSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSpherPoint: typing.TypeAlias = TripleExtendSpherPoint
TripleExtendedSphericalPoint: typing.TypeAlias = TripleExtendSpherPoint

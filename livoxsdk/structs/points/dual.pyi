import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.points.return_tag import ReturnTagBitfield
from livoxsdk.structs.points.return_iterator import ReturnIterator


class DualExtendRawPoint(StructureType):
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

    def __iter__(self) -> ReturnIterator: ...


DualExtendCartesianPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedRawPoint: typing.TypeAlias = DualExtendRawPoint
DualExtendedCartesianPoint: typing.TypeAlias = DualExtendRawPoint


class DualExtendSpherPoint(StructureType):
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

    def __iter__(self) -> ReturnIterator: ...


DualExtendSphericalPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSpherPoint: typing.TypeAlias = DualExtendSpherPoint
DualExtendedSphericalPoint: typing.TypeAlias = DualExtendSpherPoint

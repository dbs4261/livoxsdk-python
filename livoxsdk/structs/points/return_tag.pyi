import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class ReturnTagBitfield(StructureType):
    # Note: ctypes.sizeof(ReturnTag) == ctypes.sizeof(ctypes.c_uint8)
    spatial_noise: typing.Annotated[int, ctypes.c_uint8, livoxsdk.annotations.BitField(2)]
    intensity_noise: typing.Annotated[int, ctypes.c_uint8, livoxsdk.annotations.BitField(2)]
    return_number: typing.Annotated[int, ctypes.c_uint8, livoxsdk.annotations.BitField(2)]
    reserved: typing.Annotated[int, ctypes.c_uint8, livoxsdk.annotations.BitField(2)]

    def is_noise(self) -> bool: ...

import ctypes

from livoxsdk.structs.structure_type import StructureType


class ReturnTagBitfield(StructureType):
    # In reality: ctypes.sizeof(ReturnTag) == ctypes.sizeof(ctypes.c_uint8)
    spatial_noise: ctypes.c_uint8
    intensity_noise: ctypes.c_uint8
    return_number: ctypes.c_uint8
    reserved: ctypes.c_uint8

    def is_noise(self) -> bool:
        raise NotImplementedError

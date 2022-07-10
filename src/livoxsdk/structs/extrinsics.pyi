import ctypes

from livoxsdk.structs.structure_type import StructureType


class Extrinsics(StructureType):
    x: ctypes.c_float = 0.0
    y: ctypes.c_float = 0.0
    z: ctypes.c_float = 0.0
    roll: ctypes.c_float = 0.0
    pitch: ctypes.c_float = 0.0
    yaw: ctypes.c_float = 0.0

import ctypes
import typing

from livoxsdk.structs.structure_type import StructureType


class ImuPoint(StructureType):
    gyro_x: typing.Annotated[int, ctypes.c_float]
    gyro_y: typing.Annotated[int, ctypes.c_float]
    gyro_z: typing.Annotated[int, ctypes.c_float]
    acc_x: typing.Annotated[int, ctypes.c_float]
    acc_y: typing.Annotated[int, ctypes.c_float]
    acc_z: typing.Annotated[int, ctypes.c_float]

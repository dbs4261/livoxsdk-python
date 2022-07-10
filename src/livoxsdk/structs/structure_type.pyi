import ctypes
import typing

import livoxsdk

BaseStructureType: typing.Type[typing.Union[ctypes.Structure, livoxsdk.BinarySerializable, typing.SupportsBytes]] =\
    ctypes.LittleEndianStructure if livoxsdk.endianness == "little" else ctypes.BigEndianStructure


class StructureType(BaseStructureType):
    def __str__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        raise NotImplementedError

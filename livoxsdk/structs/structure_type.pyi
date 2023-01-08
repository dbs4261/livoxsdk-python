import ctypes
import typing

import livoxsdk
from livoxsdk.binary_serializable import ReadableBuffer, WriteableBuffer

BaseStructureType: typing.Type[ctypes.Structure] =\
    ctypes.LittleEndianStructure if livoxsdk.endianness == "little" else ctypes.BigEndianStructure


class StructureType(BaseStructureType):
    def __init__(self, **kwargs): ...

    def __str__(self) -> str: ...

    def __eq__(self, other) -> bool: ...

    def __bytes__(self) -> bytes: ...

    @classmethod
    def from_buffer_copy(cls, source: ReadableBuffer, offset: int = ...) -> StructureType: ...

    @classmethod
    def from_buffer(cls, source: WriteableBuffer, offset: int = ...) -> StructureType: ...

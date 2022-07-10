import abc
import array
import ctypes
import mmap
import typing


T_co = typing.TypeVar("T_co", covariant=True)

ReadOnlyBuffer = bytes  # stable
# Anything that implements the read-write buffer interface.
# The buffer interface is defined purely on the C level, so we cannot define a normal Protocol
# for it. Instead we have to list the most common stdlib buffer classes in a Union.
WriteableBuffer = typing.Union[bytearray, memoryview, array.ArrayType, mmap.mmap, ctypes.c_byte]  # stable
# Same as _WriteableBuffer, but also includes read-only buffer types (like bytes).
ReadableBuffer = typing.Union[ReadOnlyBuffer, WriteableBuffer]  # stable


@typing.runtime_checkable
class BinarySerializable(typing.Protocol[T_co]):
    __slots__ = ()

    @classmethod
    @abc.abstractmethod
    def from_buffer_copy(cls, source: ReadableBuffer, offset: int = ...) -> T_co:
        raise NotImplementedError

    @abc.abstractmethod
    def __bytes__(self) -> bytes:
        raise NotImplementedError


@typing.runtime_checkable
class BinaryMappable(BinarySerializable[T_co], typing.Protocol[T_co]):
    __slots__ = ()

    @classmethod
    @abc.abstractmethod
    def from_buffer(cls, source: WriteableBuffer, offset: int = ...) -> T_co:
        raise NotImplementedError

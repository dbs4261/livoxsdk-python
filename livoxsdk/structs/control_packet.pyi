import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class ControlPacketHeader(StructureType):
    sof: typing.Annotated[int, ctypes.c_uint8] = 170
    version: typing.Annotated[int, ctypes.c_uint8] = 1
    seq_num: typing.Annotated[int, ctypes.c_uint16] = 0
    preamble_crc: typing.Annotated[int, ctypes.c_uint16]
    
    preamble: livoxsdk.structs.Preamble
    command_handler: livoxsdk.structs.CommandHeader

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType: ...

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None: ...

    @property
    def length(self) -> ctypes.c_uint16: ...

    @length.setter
    def length(self, val: ctypes.c_uint16) -> None: ...

    @property
    def command_set(self) -> livoxsdk.enums.CommandSet: ...

    @property
    def command_type(self) -> livoxsdk.enums.CommandId: ...

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None: ...


class ControlPacket:
    header: ControlPacketHeader
    raw_payload: bytearray

    def __init__(self, header: ControlPacketHeader,
                 payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes(),
                 crc: typing.Optional[int] = None): ...

    @staticmethod
    def CreateCommand(command_type: livoxsdk.enums.CommandId,
                      payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes()) -> "ControlPacket": ...

    def __bytes__(self) -> bytes: ...

    def __str__(self) -> str: ...

    @property
    def preamble(self) -> livoxsdk.structs.Preamble: ...

    @preamble.setter
    def preamble(self) -> livoxsdk.structs.Preamble: ...

    @property
    def command_handler(self) -> livoxsdk.structs.CommandHeader: ...

    @command_handler.setter
    def command_handler(self, val: livoxsdk.structs.CommandHeader) -> None: ...

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType: ...

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None: ...

    @property
    def command_set(self) -> livoxsdk.enums.CommandSet: ...

    @property
    def command_type(self) -> livoxsdk.enums.CommandId: ...

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None: ...

    @property
    def length(self) -> int: ...

    @property
    def packet_crc(self) -> int: ...

    @packet_crc.setter
    def packet_crc(self, val: int) -> None: ...

    def crc(self) -> int: ...

    def get_payload(self) -> typing.Union[bytes, livoxsdk.BinarySerializable, typing.Any]: ...

    def set_payload(self, val: typing.SupportsBytes) -> None: ...

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview],
                         offset: int = 0) -> "ControlPacket": ...

    def valid(self) -> typing.Tuple[bool, bool]: ...

    def validate(self) -> None:
        """:raises livoxsdk.crc.CrcChecksumError"""
        pass

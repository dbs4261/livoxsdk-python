import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class ControlPacketHeader(StructureType):
    sof: ctypes.c_uint8 = 170
    version: ctypes.c_uint8 = 1
    seq_num: ctypes.c_uint16 = 0
    preamble_crc: ctypes.c_uint16
    
    preamble: livoxsdk.structs.Preamble
    command_handler: livoxsdk.structs.CommandHeader

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType:
        raise NotImplementedError

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None:
        raise NotImplementedError

    @property
    def length(self) -> ctypes.c_uint16:
        raise NotImplementedError

    @length.setter
    def length(self, val: ctypes.c_uint16) -> None:
        raise NotImplementedError

    @property
    def command_set(self) -> livoxsdk.enums.CommandSet:
        raise NotImplementedError

    @property
    def command_type(self) -> livoxsdk.enums.CommandId:
        raise NotImplementedError

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None:
        raise NotImplementedError


class ControlPacket(livoxsdk.BinarySerializable):
    header: ControlPacketHeader
    raw_payload: bytearray

    def __init__(self, header: ControlPacketHeader,
                 payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes(),
                 crc: typing.Optional[int] = None):
        raise NotImplementedError

    @staticmethod
    def CreateCommand(command_type: livoxsdk.enums.CommandId,
                      payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes()) -> "ControlPacket":
        raise NotImplementedError

    def __bytes__(self) -> bytes:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    @property
    def preamble(self) -> livoxsdk.structs.Preamble:
        raise NotImplementedError

    @preamble.setter
    def preamble(self) -> livoxsdk.structs.Preamble:
        raise NotImplementedError

    @property
    def command_handler(self) -> livoxsdk.structs.CommandHeader:
        raise NotImplementedError

    @command_handler.setter
    def command_handler(self, val: livoxsdk.structs.CommandHeader) -> None:
        raise NotImplementedError

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType:
        raise NotImplementedError

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None:
        raise NotImplementedError

    @property
    def command_set(self) -> livoxsdk.enums.CommandSet:
        raise NotImplementedError

    @property
    def command_type(self) -> livoxsdk.enums.CommandId:
        raise NotImplementedError

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None:
        raise NotImplementedError

    @property
    def length(self) -> ctypes.c_uint16:
        raise NotImplementedError

    @property
    def packet_crc(self) -> int:
        raise NotImplementedError

    @packet_crc.setter
    def packet_crc(self, val: int) -> None:
        raise NotImplementedError

    def crc(self) -> int:
        raise NotImplementedError

    def get_payload(self) -> typing.Union[bytes, livoxsdk.BinarySerializable, typing.Any]:
        raise NotImplementedError

    def set_payload(self, val: typing.SupportsBytes) -> None:
        raise NotImplementedError

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview],
                         offset: int = 0) -> "ControlPacket":
        raise NotImplementedError

    def valid(self) -> typing.Tuple[bool, bool]:
        raise NotImplementedError

    def validate(self) -> None:
        """:raises livoxsdk.crc.CrcChecksumError"""
        raise NotImplementedError

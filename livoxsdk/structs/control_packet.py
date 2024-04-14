import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.preamble import Preamble
from livoxsdk.structs.command_header import CommandHeader


class ControlPacketHeader(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("packet_type_c", "packet_type"),
        ("command_set_c", "command_set"),
        ("command_type_c", "command_type"),
        ("_length", "length"),
    )
    _anonymous_ = (
        "preamble",
        "command_handler",
    )
    _fields_ = (
        ("preamble", Preamble),
        ("command_handler", CommandHeader),
    )
    _defaults_ = {
        **getattr(Preamble, "_defaults_", dict())
    }

    packet_type: property = Preamble.packet_type
    length: property = Preamble.length
    command_set: property = CommandHeader.command_set
    command_type: property = CommandHeader.command_type


class ControlPacket:
    _current_sequence_number: typing.ClassVar[livoxsdk.AtomicCounter] = \
        livoxsdk.AtomicCounter(max_val=(2 ** (ctypes.sizeof(ctypes.c_uint16) * 8 - 1)))
    header: ControlPacketHeader
    raw_payload: bytearray
    _packet_crc: ctypes.c_uint32

    def __init__(self, header: ControlPacketHeader,
                 payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes(),
                 crc: typing.Optional[int] = None):
        self.header: ControlPacketHeader = header
        self.raw_payload: bytearray = bytearray(bytes(payload))
        self._packet_crc: ctypes.c_uint32
        if crc is None:
            self.header.length = self.length
            self.header.preamble.preamble_crc = ctypes.c_uint16(self.header.preamble.crc())
            self._packet_crc = ctypes.c_uint32(self.crc())
        else:
            self._packet_crc = ctypes.c_uint32(crc)

    @staticmethod
    def CreateCommand(command_type: livoxsdk.enums.CommandId,
                      payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes()) -> "ControlPacket":
        # noinspection PyUnresolvedReferences
        return ControlPacket(header=ControlPacketHeader(packet_type=livoxsdk.enums.MessageType.CMD,
            command_type=command_type, seq_num=ControlPacket._current_sequence_number.postinc()), payload=payload)

    def __bytes__(self) -> bytes:
        # noinspection PyUnresolvedReferences
        return bytes(self.header) + self.raw_payload + bytes(self._packet_crc)

    def __str__(self) -> str:
        payload = self.get_payload()
        return "ControlPacket {{{}, payload<{}>: {}, packet_crc: {}}}".format(
            self.header, type(payload).__name__, payload, self.packet_crc)

    @property
    def preamble(self) -> Preamble:
        return self.header.preamble

    @preamble.setter
    def preamble(self, val: Preamble) -> None:
        self.header.preamble = val

    @property
    def command_handler(self) -> CommandHeader:
        return self.header.command_handler

    @command_handler.setter
    def command_handler(self, val: CommandHeader) -> None:
        self.header.command_handler = val

    @property
    def packet_type(self) -> livoxsdk.enums.MessageType:
        return self.header.packet_type

    @packet_type.setter
    def packet_type(self, val: livoxsdk.enums.MessageType) -> None:
        self.header.packet_type = val

    @property
    def command_set(self) -> livoxsdk.enums.CommandSet:
        return self.header.command_set

    @property
    def command_type(self) -> livoxsdk.enums.CommandId:
        return self.header.command_type

    @command_type.setter
    def command_type(self, val: livoxsdk.enums.CommandId) -> None:
        self.header.command_type = val

    @property
    def length(self) -> int:
        return ctypes.sizeof(self.header) + len(self.raw_payload) + ctypes.sizeof(ctypes.c_uint32)

    @property
    def packet_crc(self) -> int:
        # noinspection PyUnresolvedReferences
        return self._packet_crc.value

    @packet_crc.setter
    def packet_crc(self, val: int) -> None:
        self._packet_crc = ctypes.c_uint32(val)

    def crc(self) -> int:
        crc32_result = livoxsdk.crc.crc32Func(bytes(self.header) + self.raw_payload)
        return crc32_result

    def get_payload(self) -> typing.Union[bytes, livoxsdk.BinarySerializable, typing.Any]:
        if (self.packet_type, self.command_type) in livoxsdk.payloads.payload_mapping:
            PayloadType: typing.Optional[typing.Type[livoxsdk.BinarySerializable]] = \
                livoxsdk.payloads.payload_mapping[(self.packet_type, self.command_type)]
            if PayloadType is not None:
                return PayloadType.from_buffer_copy(self.raw_payload)
            else:
                return bytes(self.raw_payload)
        else:
            return bytes(self.raw_payload)

    def set_payload(self, val: typing.SupportsBytes) -> None:
        self.raw_payload = bytearray(bytes(val))
        self.packet_crc = ctypes.c_uint32(self.crc())

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "ControlPacket":
        header = ControlPacketHeader.from_buffer_copy(source, offset)
        offset += ctypes.sizeof(ControlPacketHeader)
        payload_size = header.length - ctypes.sizeof(ControlPacketHeader) - ctypes.sizeof(ctypes.c_uint32)
        payload = bytes(source[offset:offset+payload_size])
        offset += payload_size
        crc = int.from_bytes(source[offset:offset+ctypes.sizeof(ctypes.c_uint32)], livoxsdk.endianness)
        return ControlPacket(header, payload, crc)

    def valid(self) -> typing.Tuple[bool, bool]:
        return self.preamble.valid(), self.crc() == self.packet_crc

    def validate(self) -> None:
        expected_crc16 = self.preamble.preamble_crc
        calculated_crc16 = self.preamble.crc()
        expected_crc32 = self.packet_crc
        calculated_crc32 = self.crc()
        if expected_crc16 != calculated_crc16:
            raise livoxsdk.crc.CrcChecksumError(
                "CRC16 mismatch: calculated {} expected {}".format(calculated_crc16, expected_crc16))
        if expected_crc32 != calculated_crc32:
            raise livoxsdk.crc.CrcChecksumError(
                "CRC32 mismatch: calculated {} expected {}".format(calculated_crc32, expected_crc32))

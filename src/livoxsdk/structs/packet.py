import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.structs.preamble import Preamble
from livoxsdk.structs.command_header import CommandHeader


class PacketHeader(StructureType):
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


class Packet:
    header: PacketHeader
    raw_payload: bytearray
    _packet_crc: ctypes.c_uint32

    def __init__(self, header: PacketHeader,
                 payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes(),
                 crc: typing.Optional[int] = None):
        self.header: PacketHeader = header
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
                      payload: typing.Union[bytes, bytearray, typing.SupportsBytes] = bytes()) -> "Packet":
        return Packet(header=PacketHeader(packet_type=livoxsdk.enums.MessageType.CMD,
                                          command_type=command_type), payload=payload)

    def __bytes__(self) -> bytes:
        return bytes(self.header) + self.raw_payload + bytes(self._packet_crc)

    def __str__(self) -> str:
        payload = self.get_payload()
        return "Packet {{{}, payload<{}>: {}, packet_crc: {}}}".format(
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
    def length(self) -> ctypes.c_uint16:
        return ctypes.c_uint16(ctypes.sizeof(self.header) +
                len(self.raw_payload) + ctypes.sizeof(ctypes.c_uint32))

    @property
    def packet_crc(self) -> int:
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
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "Packet":
        header = PacketHeader.from_buffer_copy(source, offset)
        offset += ctypes.sizeof(PacketHeader)
        payload_size = header.length - ctypes.sizeof(PacketHeader) - ctypes.sizeof(ctypes.c_uint32)
        payload = bytes(source[offset:offset+payload_size])
        offset += payload_size
        crc = int.from_bytes(source[offset:offset+ctypes.sizeof(ctypes.c_uint32)], livoxsdk.endianness)
        return Packet(header, payload, crc)

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


if __name__ == "__main__":
    import copy
    heartbeat_command: bytearray = bytearray.fromhex("AA010F0000000004D7000338BA8D0C")
    powersave_command: bytearray = bytearray.fromhex("AA011000000000B809010002AB73F4FB")
    tmp = Packet.from_buffer_copy(powersave_command)
    print(tmp.valid())
    # tmp2 = PacketBase.from_buffer(powersave_command)
    tmp2 = tmp.from_buffer(powersave_command)
    print(powersave_command.hex(), bytes(tmp).hex(),
          "".join("1" if a == b else "0" for a, b in zip(powersave_command.hex(), bytes(tmp).hex())), sep="\n")
    print(powersave_command.hex(), bytes(tmp2).hex(),
          "".join("1" if a == b else "0" for a, b in zip(powersave_command.hex(), bytes(tmp2).hex())),sep="\n")
    print(bytes(tmp.preamble).hex(), bytes(tmp.command_header).hex(), bytes(ctypes.c_uint32(tmp.packet_crc)).hex())
    tmpp = copy.deepcopy(tmp.preamble)
    tmpp.sof = 169
    assert(tmp.preamble != tmpp)
    tmp.preamble = tmpp
    assert(tmp.preamble == tmpp)
    print(tmp)
    print(ctypes.sizeof(tmp), ctypes.sizeof(type(tmp)), powersave_command.hex(), bytes(tmp).hex())
    tmp.length = 19
    print(tmp, tmp.packet_crc)
    print(ctypes.sizeof(tmp), ctypes.sizeof(type(tmp)), bytes(tmp).hex())
    tmp.payload = "ticktock".encode("ascii")
    print(tmp)
    del tmp.payload
    print(tmp)

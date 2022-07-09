import ctypes
import typing

import livoxsdk.crc

if __name__ == "__main__":
    from livoxsdk.structs.StructureType import StructureType
    from livoxsdk.structs.Preamble import Preamble
    from livoxsdk.structs.CommandHeader import CommandHeader
else:
    from .StructureType import StructureType
    from .Preamble import Preamble
    from .CommandHeader import CommandHeader


class PacketHeader(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("packet_type_c", "packet_type"),
        ("command_set_c", "command_set"),
        ("command_type_c", "command_type"),
        ("_length", "length"),
    )
    _anonymous_ = (
        "_preamble",
        "_command_handler",
    )
    _fields_ = (
        ("_preamble", Preamble),
        ("_command_handler", CommandHeader),
    )
    _defaults_ = {
        **getattr(Preamble, "_defaults_", dict())
    }

    packet_type = Preamble.packet_type
    length = Preamble.length
    command_set = CommandHeader.command_set
    command_type = CommandHeader.command_type

    @property
    def preamble(self) -> Preamble:
        return Preamble.from_buffer_copy(self)

    @preamble.setter
    def preamble(self, val: Preamble) -> None:
        if not isinstance(val, Preamble):
            raise TypeError("Val must be {} but instead is {}".format(type(Preamble), type(val)))
        ctypes.memmove(ctypes.byref(self), ctypes.byref(val), ctypes.sizeof(Preamble))

    @property
    def command_header(self) -> CommandHeader:
        return CommandHeader.from_buffer_copy(self, ctypes.sizeof(Preamble))

    @command_header.setter
    def command_header(self, val: CommandHeader) -> None:
        if not isinstance(val, CommandHeader):
            raise TypeError("Val must be {} but instead is {}".format(type(CommandHeader), type(val)))
        ctypes.memmove(ctypes.byref(self, ctypes.sizeof(Preamble)), ctypes.byref(val), ctypes.sizeof(Preamble))


class Packet(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("packet_type_c", "packet_type"),
        ("command_set_c", "command_set"),
        ("command_type_c", "command_type"),
        ("_payload", "payload"),
        ("_packet_crc", "packet_crc"),
        ("_length", "length"),
    )
    _anonymous_ = (
        "_header",
    )
    _fields_ = (
        ("_header", PacketHeader),
        ("_payload", ctypes.c_byte * 0),
        ("_packet_crc", ctypes.c_uint32),
    )
    _defaults_ = {
        **getattr(PacketHeader, "_defaults_", dict())
    }

    packet_type = Preamble.packet_type
    command_set = CommandHeader.command_set
    command_type = CommandHeader.command_type
    preamble = PacketHeader.preamble
    command_header = PacketHeader.command_header

    def __init__(self, **kwargs):
        values = {}
        values["_length"] = ctypes.sizeof(self)
        values.update(kwargs)
        super().__init__(**values)
        setattr(self, "preamble_crc", Preamble.from_buffer(self).crc())
        self.packet_crc = self.crc()

    @property
    def length(self) -> ctypes.c_uint16:
        return self._length

    @length.setter
    def length(self, val: int) -> None:
        if val != ctypes.c_uint16(val).value:
            raise ValueError("Invalid length {} must be betwee {} and {}".format(
                val, 0, ctypes.c_uint16(-1).value))
        if val < ctypes.sizeof(type(self)):
            raise ValueError("Cannot shrink a Packet to have a smaller size than one without a payload")
        tmp_crc = self.packet_crc
        self._length = val
        ctypes.resize(self, val)
        self.packet_crc = tmp_crc

    @property
    def packet_crc(self) -> int:
        offset = ctypes.sizeof(self) - ctypes.sizeof(ctypes.c_uint32)
        return ctypes.c_uint32.from_buffer_copy(self, offset).value

    @packet_crc.setter
    def packet_crc(self, val: typing.Union[int, ctypes.c_uint32]) -> None:
        if isinstance(val, int):
            if val != ctypes.c_uint32(val).value:
                raise ValueError("Invalid packet_crc {} must be betwee {} and {}".format(
                    val, 0, ctypes.c_uint32(-1).value))
        if not isinstance(val, ctypes.c_uint32):
            self.packet_crc = ctypes.c_uint32(val)
            return
        offset = ctypes.sizeof(self) - ctypes.sizeof(ctypes.c_uint32)
        ctypes.memmove(ctypes.byref(self, offset), bytes(val), ctypes.sizeof(ctypes.c_uint32))

    def crc(self):
        return livoxsdk.crc.crc32Func(bytes(self)[:ctypes.sizeof(self) - ctypes.sizeof(ctypes.c_uint32)])

    @property
    def payload(self) -> bytes:
        payload_size = ctypes.sizeof(self) - ctypes.sizeof(type(self))
        return bytes((ctypes.c_byte * payload_size).from_buffer_copy(
            self, ctypes.sizeof(Preamble) + ctypes.sizeof(CommandHeader)))

    @payload.setter
    def payload(self, val: typing.SupportsBytes) -> None:
        payload_size = len(bytes(val))
        payload_offset = ctypes.sizeof(Preamble) + ctypes.sizeof(CommandHeader)
        self.length = ctypes.sizeof(type(self)) + payload_size
        ctypes.memmove(ctypes.byref(self, payload_offset), bytes(val), payload_size)

    @payload.deleter
    def payload(self):
        self.length = ctypes.sizeof(type(self))

    @classmethod
    def from_buffer_copy(cls, source: typing.Union[bytes, bytearray, memoryview], offset: int = 0) -> "Packet":
        preamble = Preamble.from_buffer_copy(source, offset)
        out = cls()
        ctypes.resize(out, preamble.length)
        raw_memory = (ctypes.c_byte * len(source)).from_buffer_copy(source, offset)
        ctypes.memmove(ctypes.byref(out), ctypes.byref(raw_memory, offset), ctypes.sizeof(out))
        return out

    @classmethod
    def from_buffer(cls, *args, **kwargs):
        raise NotImplementedError("From buffer does not work correctly because of the payload packet layout. "
                                  "Use the PacketHeader class to see a memory view of a packet")

    def valid(self) -> typing.Tuple[bool, bool]:
        return Preamble.from_buffer(self).crc() == getattr(self, "preamble_crc"), self.crc() == self.packet_crc


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

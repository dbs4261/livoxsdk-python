import crcmod
import typing


class CrcFuncProtocol(typing.Protocol):
    def __call__(self, data, crc=...) -> int: ...


crc16Func: CrcFuncProtocol = crcmod.mkCrcFun(0x11021, rev=True, initCrc=0x4C49)
crc32Func: CrcFuncProtocol = crcmod.mkCrcFun(0x104C11DB7, rev=True, initCrc=0x564F580A, xorOut=0xFFFFFFFF)


class CrcChecksumError(Exception):
    pass

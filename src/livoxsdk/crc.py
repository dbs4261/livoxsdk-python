import crcmod
import typing


crc16Func: typing.Callable[[bytes, int], int] = crcmod.mkCrcFun(
    0x11021, rev=True, initCrc=0x4C49)
crc32Func: typing.Callable[[bytes, int], int] = crcmod.mkCrcFun(
    0x104C11DB7, rev=True, initCrc=0x564F580A, xorOut=0xFFFFFFFF)


class CrcChecksumError(Exception):
    pass

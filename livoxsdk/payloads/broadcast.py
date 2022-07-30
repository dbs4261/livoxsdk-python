import ctypes
import typing

import livoxsdk
from livoxsdk.structs.structure_type import StructureType


class BroadcastPayload(StructureType):
    _pack_ = 1
    _mapped_ = (
        ("device_type_c", "device_type"),
        ("_reserved", None),
    )
    _anonymous_ = (
        "broadcast_code",
    )
    _fields_ = (
        ("broadcast_code", livoxsdk.structs.BroadcastCode),
        ("device_type_c", ctypes.c_uint8),
        ("_reserved", ctypes.c_uint16),
    )

    serial = livoxsdk.structs.BroadcastCode.serial
    range_code = livoxsdk.structs.BroadcastCode.range_code
    valid = livoxsdk.structs.BroadcastCode.valid

    @property
    def device_type(self) -> livoxsdk.enums.devices.DeviceType:
        return livoxsdk.enums.devices.DeviceType(getattr(self, "device_type_c"))

    @device_type.setter
    def device_type(self, val: livoxsdk.enums.devices.DeviceType) -> None:
        setattr(self, "device_type_c", ctypes.c_uint8(val.value))


if __name__ == "__main__":
    broadcast_payload = b'3JEDK1E001F6361\x00\x07\xe8\xfd'
    payload = BroadcastPayload.from_buffer_copy(broadcast_payload)
    print(broadcast_payload, bytes(payload), payload.valid(), payload)

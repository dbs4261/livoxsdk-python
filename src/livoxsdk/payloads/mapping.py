import ctypes
import typing

from livoxsdk import payloads
from livoxsdk.structs.structure_type import StructureType
from livoxsdk.enums.messages import MessageType, CommandId, GeneralCommandId, LidarCommandId

AllCLiterals: typing.Type = typing.Union[
    ctypes.c_ubyte,
    ctypes.c_uint8,
    ctypes.c_uint16,
    ctypes.c_uint32,
    ctypes.c_uint64,
    ctypes.c_byte,
    ctypes.c_int8,
    ctypes.c_int16,
    ctypes.c_int32,
    ctypes.c_int64,
    ctypes.c_bool,
    ctypes.c_float,
    ctypes.c_double,
]

PacketTypeEnum: typing.TypeAlias = typing.Tuple[MessageType, CommandId]

payload_mapping: typing.Dict[PacketTypeEnum, typing.Union[None, AllCLiterals, typing.Type[StructureType]]] = {
    (MessageType.MSG, GeneralCommandId.Broadcast): payloads.BroadcastPayload,
    (MessageType.CMD, GeneralCommandId.Handshake): payloads.ConnectionRequestPayload,
    (MessageType.ACK, GeneralCommandId.Handshake): ctypes.c_uint8,
    (MessageType.ACK, GeneralCommandId.Disconnect): ctypes.c_uint8,
    (MessageType.ACK, GeneralCommandId.Heartbeat): payloads.HeartbeatResponsePayload,
    (MessageType.ACK, GeneralCommandId.DeviceInfo): payloads.QueryResponsePayload,
    (MessageType.ACK, GeneralCommandId.ControlSample): ctypes.c_uint8,
    (MessageType.ACK, LidarCommandId): ctypes.c_uint8,
}

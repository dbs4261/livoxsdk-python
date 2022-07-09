import enum
import typing


class MessageType(enum.IntEnum):
    CMD = 0  # requires response from the receiver
    Request = CMD
    ACK = 1  # response of command type
    Response = ACK
    MSG = 2  # sent at a specified frequency
    Message = MSG


class CommandSet(enum.IntEnum):
    General = 0
    Lidar = 1
    Hub = 2


class GeneralCommandId(enum.IntEnum):
    Broadcast = 0
    Handshake = 1
    DeviceInfo = 2
    Heartbeat = 3
    ControlSample = 4
    CoordinateSystem = 5
    Disconnect = 6
    PushAbnormalState = 7
    ConfigureStaticDynamicIp = 8
    ConfigureIp = ConfigureStaticDynamicIp
    GetDeviceIpInformation = 9
    IpInformation = GetDeviceIpInformation
    RebootDevice = 10
    SetDeviceParam = 11
    GetDeviceParam = 12
    ResetDeviceParam = 13


class LidarCommandId(enum.IntEnum):
    SetMode = 0
    SetExtrinsicParameter = 1
    SetExtrinsics = SetExtrinsicParameter
    GetExtrinsicParameter = 2
    GetExtrinsics = GetExtrinsicParameter
    ControlRainFogSuppression = 3
    RainFogSuppression = ControlRainFogSuppression
    ControlFan = 4
    GetFanState = 5
    FanState = GetFanState
    SetPointCloudReturnMode = 6
    GetPointCloudReturnMode = 7
    SetImuPushFrequency = 8
    GetImuPushFrequency = 9
    SetSyncTime = 10


class HubCommandId(enum.IntEnum):
    QueryLidarInformation = 0
    SetMode = 1
    ControlSlotPower = 2
    SetExtrinsicParameter = 3
    GetExtrinsicParameter = 4
    QueryLidarDeviceStatus = 5
    QueryDeviceStatus = QueryLidarDeviceStatus
    DeviceStatus = QueryLidarDeviceStatus
    RainFogSuppression = 7
    QuerySlotPowerStatus = 8
    SlotPowerStatus = QuerySlotPowerStatus
    ControlFan = 9
    GetFanState = 10
    FanState = GetFanState
    SetPointCloudReturnMode = 11
    GetPointCloudReturnMode = 12
    SetImuPushFrequency = 13
    GetImuPushFrequency = 14


CommandId = typing.Union[GeneralCommandId, LidarCommandId, HubCommandId]

import enum


class DeviceType(enum.IntEnum):
    Hub = 0
    LidarMid40 = 1
    LidarTele = 2
    LidarHorizon = 3
    LidarMid70 = 6
    LidarAvia = 7

    def is_hub(self) -> bool:
        return self == DeviceType.Hub

    def is_lidar(self) -> bool:
        return self != DeviceType.Hub


class DeviceState(enum.IntEnum):
    Init = 0
    Normal = 1
    PowerSaving = 2
    StandBy = 3
    Error = 4
    Unknown = 5


class LidarMode(enum.IntEnum):
    Normal = 1
    PowerSaving = 2
    Standby = 3


class LidarFeature(enum.IntEnum):
    FeatureNone = 0
    RainFog = 1


class TimeSync(enum.IntEnum):
    Unsupported = 0
    PTP1588 = 1
    GPS = 2
    PPS = 3
    Abnormal = 4

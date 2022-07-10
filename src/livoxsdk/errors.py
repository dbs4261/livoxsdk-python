class LivoxError(RuntimeError):
    pass


class LivoxDeviceError(LivoxError):
    pass


class LivoxHubError(LivoxDeviceError):
    pass


class LivoxLidarError(LivoxDeviceError):
    pass


class LivoxConnectionError(LivoxError):
    pass


class LivoxAbnormalStatusError(LivoxDeviceError):
    pass


class LivoxBadRetError(LivoxDeviceError):
    pass

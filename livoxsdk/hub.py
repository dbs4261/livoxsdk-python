import livoxsdk


class Hub(livoxsdk.Device):
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError

import asyncio
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("DataProtocol")


class DataProtocol(asyncio.DatagramProtocol):
    def __init__(self, callback: typing.Callable[[livoxsdk.DataPacket], None]):
        self._transport: typing.Optional[asyncio.DatagramTransport] = None
        self._callback: typing.Callable[[livoxsdk.DataPacket], None] = callback

    @property
    def transport(self) -> typing.Optional[asyncio.DatagramTransport]:
        return self._transport

    @property
    def callback(self) -> typing.Callable[[livoxsdk.DataPacket], None]:
        return self._callback

    @callback.setter
    def callback(self, callback_func: typing.Callable[[livoxsdk.DataPacket], None]) -> None:
        self._callback = callback_func

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        logger.getChild("ConnectionMade").debug("Connected To: {}:{}".format(
            *transport.get_extra_info("sockname")))
        if self._transport is None:
            self._transport = transport
        else:
            raise NotImplementedError("Multiple connections not supported")

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        packet = livoxsdk.DataPacket.from_buffer_copy(data)
        asyncio.get_running_loop().call_soon(self._callback, packet)

    def connection_lost(self, exc: typing.Optional[Exception]) -> None:
        logger.getChild("ConnectionLost").debug("Closing transport")
        if exc is not None:
            raise exc
        self.close()

    def error_received(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc
        self.close()

    def close(self) -> None:
        self._transport.close()

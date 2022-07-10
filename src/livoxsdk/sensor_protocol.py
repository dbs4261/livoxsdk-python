import asyncio
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("SensorProtocol")


class SensorProtocol(asyncio.DatagramProtocol):
    def __init__(self, port: livoxsdk.Port):
        self.port = port
        self.transport: typing.Optional[asyncio.DatagramTransport] = None

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        logger.getChild("ConnectionMade").debug("Connected To: {}:{}".format(
            transport.get_extra_info("sockname"), transport.get_extra_info("peername")))
        if self.transport is None:
            self.transport = transport
        else:
            raise NotImplementedError("Multiple connections not supported")

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        logger.getChild("DatagramReceived").debug("{} {}".format(data.hex(), addr))
        if addr[1] == self.port:
            logger.getChild("DatagramReceived").debug("Received packet {} from {}:{}".format(data.hex(), *addr))
        else:
            logger.getChild("DatagramReceived").debug("Overheard packet {} from {}:{}".format(data.hex(), *addr))

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
        self.transport.close()

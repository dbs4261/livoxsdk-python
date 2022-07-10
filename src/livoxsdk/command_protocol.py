import asyncio
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("CommandProtocol")


class CommandProtocol(asyncio.DatagramProtocol):
    def __init__(self, port: livoxsdk.Port) -> None:
        self.port = port
        self.transport: typing.Optional[asyncio.DatagramTransport] = None
        self.response_future_table: typing.MutableMapping[livoxsdk.enums.CommandId,
            asyncio.Future[livoxsdk.structs.Packet]] = dict()
        self.message_callback_table: typing.MutableMapping[livoxsdk.enums.CommandId,
            typing.Callable[[livoxsdk.structs.Packet], typing.Coroutine]] = dict()

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        logger.getChild("ConnectionMade").debug("Connected To: {}:{}".format(
            transport.get_extra_info("sockname"), transport.get_extra_info("peername")))
        if self.transport is None:
            self.transport = transport
        else:
            raise NotImplementedError("Multiple connections not supported")

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        if addr[1] == livoxsdk.control_port:
            logger.getChild("DatagramReceived").debug("Received packet {} from {}:{}".format(data.hex(), *addr))
            packet = livoxsdk.structs.Packet.from_buffer_copy(data)
            packet.validate()
            if packet.packet_type == livoxsdk.enums.MessageType.Response \
                    and packet.command_type in self.response_future_table:
                self.response_future_table.pop(packet.command_type).set_result(packet)
            elif packet.packet_type == livoxsdk.enums.MessageType.Message \
                    and packet.command_type in self.message_callback_table:
                asyncio.get_running_loop().create_task(self.message_callback_table[packet.command_type](packet))
            elif packet.packet_type == livoxsdk.enums.MessageType.Response:
                logger.getChild("DatagamReceived").warning("Unregistered Response type: {}".format(packet.command_type))
            elif packet.packet_type == livoxsdk.enums.MessageType.Message:
                logger.getChild("DatagamReceived").warning("Unregistered Message type: {}".format(packet.command_type))
            else:
                logger.getChild("DatagramReceived").warning("Unknown packet: {}".format(packet))
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

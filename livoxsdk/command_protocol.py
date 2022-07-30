import asyncio
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("CommandProtocol")

AbnormalStatusHandler: typing.Type = typing.Callable[[typing.Tuple[str, int], livoxsdk.structs.ControlPacket], typing.Coroutine]


async def default_abnormal_status_handler(addr: typing.Tuple[str, int], packet: livoxsdk.structs.ControlPacket) -> None:
    logger.getChild("AbnormalStatusHandler").error("{}:{} raw_payload:\n{}".format(*addr, packet.raw_payload))
    raise livoxsdk.errors.LivoxAbnormalStatusError("{}:{} raw_payload:\n{}".format(*addr, packet.raw_payload))


class CommandProtocol(asyncio.DatagramProtocol):
    def __init__(self, port: livoxsdk.Port) -> None:
        self.port = port
        self.transport: typing.Optional[asyncio.DatagramTransport] = None
        self.response_future_table: typing.MutableMapping[livoxsdk.enums.CommandId,
            asyncio.Future[livoxsdk.structs.ControlPacket]] = dict()
        self.message_callback_table: typing.MutableMapping[livoxsdk.enums.CommandId, AbnormalStatusHandler] = dict()
        self.message_callback_table[livoxsdk.enums.GeneralCommandId.PushAbnormalState] = \
            default_abnormal_status_handler

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        logger.getChild("ConnectionMade").debug("Connected To: {}:{}".format(
            *transport.get_extra_info("sockname")))
        if self.transport is None:
            self.transport = transport
        else:
            raise NotImplementedError("Multiple connections not supported")

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        packet = livoxsdk.structs.ControlPacket.from_buffer_copy(data)
        logger.getChild("DatagramReceived").debug("Received packet {} from {}:{}".format(packet, *addr))
        packet.validate()
        if packet.packet_type == livoxsdk.enums.MessageType.Response \
                and packet.command_type in self.response_future_table:
            self.response_future_table.pop(packet.command_type).set_result(packet)
        elif packet.packet_type == livoxsdk.enums.MessageType.Message \
                and packet.command_type in self.message_callback_table:
            asyncio.get_running_loop().create_task(self.message_callback_table[packet.command_type](addr, packet))
        elif packet.packet_type == livoxsdk.enums.MessageType.Response:
            logger.getChild("DatagamReceived").warning("Unregistered Response type: {}".format(packet.command_type))
        elif packet.packet_type == livoxsdk.enums.MessageType.Message:
            logger.getChild("DatagamReceived").warning("Unregistered Message type: {}".format(packet.command_type))
        else:
            logger.getChild("DatagramReceived").warning("Unknown packet: {}".format(packet))

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

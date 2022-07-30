import asyncio
import ipaddress
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("BroadcastProtocol")


class BroadcastProtocol(asyncio.DatagramProtocol):
    def __init__(self, info_future: asyncio.Future, device_ip_address: ipaddress.IPv4Address):
        self.info_future: asyncio.Future = info_future
        self.device_ip_address: str = str(device_ip_address)

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        if self.device_ip_address == addr[0] and addr[1] == livoxsdk.control_receive_port:
            packet = livoxsdk.structs.ControlPacket.from_buffer_copy(data)
            packet.validate()
            if packet.packet_type == livoxsdk.enums.messages.MessageType.MSG and \
                    packet.command_set == livoxsdk.enums.messages.CommandSet.General and \
                    packet.command_type == livoxsdk.enums.messages.GeneralCommandId.Broadcast:
                broadcast_payload: livoxsdk.payloads.BroadcastPayload = packet.get_payload()
                self.info_future.set_result(broadcast_payload)
            else:
                logger.debug("Unexpected packet {}".format(packet))
        else:
            logger.debug("Received packet from unexpected source {}:{} | {}".format(*addr, data.hex()))

    def connection_lost(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc

    def error_received(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc

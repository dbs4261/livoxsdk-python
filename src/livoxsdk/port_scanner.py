import asyncio
import dataclasses
import datetime
import socket
import typing

import livoxsdk.enums.messages
import livoxsdk.enums.devices
import livoxsdk.structs.packet
import livoxsdk.crc
import livoxsdk.payloads
import livoxsdk.logging_helpers

import logging
logger = livoxsdk.logging_helpers.logger.getChild("PortScanner")


@dataclasses.dataclass(repr=True, eq=True, order=True, unsafe_hash=True)
class DeviceConnectionInfo:
    serial_number: str
    range_code: int
    device_type: livoxsdk.enums.devices.DeviceType
    ip_address: str
    port: int


class PortScanner(asyncio.DatagramProtocol):
    def __init__(self, devices_future: asyncio.Future, port: int = 65000):
        self.devices_future: asyncio.Future = devices_future
        self.port = port
        self.found_devices: typing.Set[DeviceConnectionInfo] = set()

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        logger.getChild("DatagramReceived").debug("{} {}".format(data.hex(), addr))
        if addr[1] == self.port:
            packet = livoxsdk.structs.Packet.Packet.from_buffer_copy(data)
            if not packet.valid():
                raise livoxsdk.crc.CrcChecksumError("Invalid packet encountered during port scan")
            if packet.packet_type == livoxsdk.enums.messages.MessageType.MSG and \
                    packet.command_set == livoxsdk.enums.messages.CommandSet.General and \
                    packet.command_type == livoxsdk.enums.messages.GeneralCommandId.Broadcast:
                broadcast_payload = livoxsdk.structs.Payloads.BroadcastPayload.from_buffer_copy(packet.payload)
                device = DeviceConnectionInfo(broadcast_payload.serial, broadcast_payload.range_code,
                                              broadcast_payload.device_type, addr[0], addr[1])
                self.found_devices.add(device)

    def connection_lost(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc
        else:
            self.devices_future.set_result(self.found_devices)

    def error_received(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc


async def scan_for_devices(scan_time: datetime.timedelta, command_port: int = 55000
                           ) -> typing.Set[DeviceConnectionInfo]:
    loop = asyncio.get_running_loop()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", command_port))

    devices_future = loop.create_future()
    logger.info("Scanning for Livox devices...")
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: PortScanner(devices_future), sock=server_socket)
    try:
        await asyncio.sleep(scan_time.total_seconds())
    finally:
        transport.close()
    found_devices = await devices_future
    logger.info("Device scan complete")
    return found_devices

if __name__ == '__main__':
    livoxsdk.logging_helpers.SetupDefaultLogger(None, logging.DEBUG, None, use_simple_console_format=True)
    scan_time = datetime.timedelta(seconds=10)
    found_devices = asyncio.run(scan_for_devices(scan_time))
    logger.info("Found Devices:\n" + "\n".join(str(d) for d in found_devices))
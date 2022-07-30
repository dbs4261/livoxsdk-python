import asyncio
import dataclasses
import datetime
import ipaddress
import socket
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("PortScanner")


class NoDevicesDetectedError(Exception):
    pass


@dataclasses.dataclass(repr=True, eq=True, order=True, unsafe_hash=True)
class DeviceConnectionInfo:
    serial_number: str
    range_code: int
    device_type: livoxsdk.enums.DeviceType
    ip_address: ipaddress.IPv4Address
    port: livoxsdk.Port


class PortScannerProtocol(asyncio.DatagramProtocol):
    def __init__(self, devices_future: asyncio.Future):
        self.devices_future: asyncio.Future = devices_future
        self.found_devices: typing.Set[DeviceConnectionInfo] = set()

    def datagram_received(self, data: bytes, addr: typing.Tuple[str, int]) -> None:
        logger.getChild("DatagramReceived").debug("{} {}".format(data.hex(), addr))
        if addr[1] == livoxsdk.control_receive_port:
            packet = livoxsdk.structs.ControlPacket.from_buffer_copy(data)
            if not packet.valid():
                raise livoxsdk.crc.CrcChecksumError("Invalid packet encountered during port scan")
            if packet.packet_type == livoxsdk.enums.messages.MessageType.MSG and \
                    packet.command_set == livoxsdk.enums.messages.CommandSet.General and \
                    packet.command_type == livoxsdk.enums.messages.GeneralCommandId.Broadcast:
                broadcast_payload: livoxsdk.payloads.BroadcastPayload = packet.get_payload()
                device = DeviceConnectionInfo(broadcast_payload.serial, broadcast_payload.range_code,
                                              broadcast_payload.device_type, ipaddress.IPv4Address(addr[0]),
                                              livoxsdk.Port(addr[1]))
                self.found_devices.add(device)
        else:
            logger.debug("Received packet from unexpected source {}:{} | {}".format(*addr, data.hex()))

    def connection_lost(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc
        else:
            self.devices_future.set_result(self.found_devices)

    def error_received(self, exc: typing.Optional[Exception]) -> None:
        if exc is not None:
            raise exc


async def scan_for_devices(scan_time: datetime.timedelta) -> typing.Set[DeviceConnectionInfo]:
    loop = asyncio.get_running_loop()
    devices_future = loop.create_future()
    logger.info("Scanning for Livox devices...")
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: PortScannerProtocol(devices_future), family=socket.AF_INET, allow_broadcast=True,
        reuse_port=True, local_addr=("0.0.0.0", livoxsdk.scan_port))
    try:
        await asyncio.sleep(scan_time.total_seconds())
    finally:
        transport.close()
    found_devices = await devices_future
    logger.info("Device scan complete")
    return found_devices


if __name__ == '__main__':
    import logging
    import sys
    livoxsdk.logging_helpers.SetupDefaultLogger(None, logging.DEBUG, None)
    if 'pdb' in sys.modules or 'pydevd' in sys.modules:
        debug = True
    else:
        debug = False
    livoxsdk.logging_helpers.SetupDefaultLogger(None, logging.DEBUG, None, use_simple_console_format=True)
    scan_time = datetime.timedelta(seconds=10)
    found_devices = asyncio.run(scan_for_devices(scan_time), debug=debug)
    logger.info("Found Devices:\n" + "\n".join(str(d) for d in found_devices))

import asyncio
import ctypes
import datetime
import ipaddress
import socket
import typing
from types import TracebackType

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("Device")


class Device:
    def __init__(self, device_ip_address: ipaddress.IPv4Address,
                 command_port: livoxsdk.Port, data_port: livoxsdk.Port,
                 event_loop: typing.Optional[asyncio.AbstractEventLoop] = None,
                 sensor_port: typing.Optional[livoxsdk.Port] = None,
                 host_ip_address: typing.Optional[ipaddress.IPv4Address] = None,
                 default_timeout: datetime.timedelta = datetime.timedelta(milliseconds=500)):
        self.device_ip_address: ipaddress.IPv4Address = device_ip_address
        self.host_ip_address: ipaddress.IPv4Address = host_ip_address
        if self.host_ip_address is None:
            self.host_ip_address = livoxsdk.utilities.HostIPForDeviceIp(self.device_ip_address)
        if self.host_ip_address is None:
            raise ValueError("Could not automatically determine host address "
                             "for communicating with {}".format(self.device_ip_address))
        self.default_timeout: datetime.timedelta = default_timeout
        self.command_port: livoxsdk.Port = command_port
        self.data_port: livoxsdk.Port = data_port
        self.sensor_port: livoxsdk.Port = sensor_port if sensor_port is not None else 0
        self._loop: typing.Optional[asyncio.AbstractEventLoop] = event_loop
        self._command_protocol: typing.Optional[livoxsdk.CommandProtocol] = None
        self._data_protocol: typing.Optional[livoxsdk.DataProtocol] = None
        self._sensor_protocol: typing.Optional[livoxsdk.SensorProtocol] = None
        self._heartbeat_task: typing.Optional[asyncio.Task] = None
        self._firmware_version: typing.Optional[livoxsdk.FirmwareVersion] = None

    async def __aenter__(self) -> "Device":
        if self._loop is None:
            self._loop = asyncio.get_running_loop()
        _, self._command_protocol = await self._loop.create_datagram_endpoint(
            lambda: livoxsdk.CommandProtocol(self.command_port), family=socket.AF_INET,
            reuse_port=True, local_addr=(str(self.host_ip_address), self.command_port)
        )
        _, self._data_protocol = await self._loop.create_datagram_endpoint(
            lambda: livoxsdk.DataProtocol(self.data_port), family=socket.AF_INET,
            reuse_port=True, local_addr=(str(self.host_ip_address), self.data_port)
        )
        if self.sensor_port != 0:
            _, self._sensor_protocol = await self._loop.create_datagram_endpoint(
                lambda: livoxsdk.SensorProtocol(self.sensor_port), family=socket.AF_INET,
                reuse_port=True, local_addr=(str(self.host_ip_address), self.sensor_port)
            )
        return self

    async def __aexit__(self, __exc_type: typing.Optional[typing.Type[BaseException]],
                        __exc_value: typing.Optional[BaseException],
                        __traceback: typing.Optional[TracebackType]) -> typing.Optional[bool]:
        logger.info("Disconnecting from demo")
        if self._command_protocol is not None:
            self._command_protocol.close()
        if self._data_protocol is not None:
            self._data_protocol.close()
        if self._sensor_protocol is not None:
            self._sensor_protocol.close()
        return None

    async def _send_message(self, packet: livoxsdk.structs.Packet, caller: str) -> asyncio.Future:
        if self._command_protocol is None or self._command_protocol.transport is None:
            raise RuntimeWarning("No transport!")
        packet.validate()
        future = self._loop.create_future()
        if packet.command_type in self._command_protocol.response_future_table:
            logger.getChild("send_{}".format(caller)).warning(
                "Receive future for {} already exists but will be canceled and replaced".format(packet.command_type))
            self._command_protocol.response_future_table[packet.command_type].cancel("Replaced")
        self._command_protocol.response_future_table[packet.command_type] = future
        logger.getChild("send_{}".format(caller)).debug("Sending {} to {}:{}".format(
            bytes(packet).hex(), self.device_ip_address, livoxsdk.control_port))
        self._command_protocol.transport.sendto(bytes(packet), (str(self.device_ip_address), livoxsdk.control_port))
        return future

    async def send_message(self, packet: livoxsdk.structs.Packet) -> asyncio.Future:
        return await self._send_message(packet, caller="send_message")

    async def _send_message_response(self, packet: livoxsdk.structs.Packet, caller: str,
                                    timeout: typing.Optional[datetime.timedelta] = None) -> livoxsdk.structs.Packet:
        if timeout is None:
            timeout = self.default_timeout
        future = await self._send_message(packet, caller=caller)
        response: livoxsdk.structs.Packet = await asyncio.wait_for(future, timeout=timeout.total_seconds())
        logger.getChild("receive_{}".format(caller)).debug("Received {}".format(response))
        return response

    async def send_message_response(self, packet: livoxsdk.structs.Packet,
                                     timeout: typing.Optional[datetime.timedelta] = None) -> livoxsdk.structs.Packet:
        return await self._send_message_response(packet, caller="send_message_response", timeout=timeout)

    async def _heartbeat_function(self, interval: datetime.timedelta = datetime.timedelta(seconds=1),
                                  timeout: typing.Optional[datetime.timedelta] = None):
        heartbeat_packet = livoxsdk.structs.Packet(
            header=livoxsdk.structs.PacketHeader(
                packet_type=livoxsdk.enums.messages.MessageType.CMD,
                command_type=livoxsdk.enums.messages.GeneralCommandId.Heartbeat
            )
        )
        logger.getChild("heartbeat").info("Beginning heartbeat...")
        while True:
            response = await self._send_message_response(heartbeat_packet, caller="heartbeat", timeout=timeout)

            payload: livoxsdk.payloads.HeartbeatResponsePayload = response.get_payload()
            if payload.ret_code != 0:
                logger.getChild("heartbeat").warning("{} responded incorrectly to heartbeat with ret_code: {}".format(
                    self.device_ip_address, payload))
            else:
                if payload.state == livoxsdk.enums.devices.DeviceState.Error:
                    raise livoxsdk.errors.LivoxAbnormalStatusError(
                        "Heartbeat error {} with state {} received from {}\n"
                        "Details: feature: {} progress: {}".format(payload.ret_code, payload.state,
                            self.device_ip_address, payload.feature, payload.error_union.progress))
            await asyncio.sleep(interval.total_seconds())

    async def query(self, timeout: typing.Optional[datetime.timedelta] = None) -> None:
        query_packet = livoxsdk.structs.Packet(
            header=livoxsdk.structs.PacketHeader(
                packet_type=livoxsdk.enums.MessageType.CMD,
                command_type=livoxsdk.enums.GeneralCommandId.DeviceInfo
            )
        )
        response = await self._send_message_response(query_packet, caller="query", timeout=timeout)
        payload: livoxsdk.payloads.QueryResponsePayload = response.get_payload()
        if payload.ret_code != 0:
            raise livoxsdk.errors.LivoxBadRetError("Invalid query result {}".format(payload.ret_code))
        self._firmware_version = payload.firmware_version

    async def connect(self, timeout: typing.Optional[datetime.timedelta] = None) -> ctypes.c_uint8:
        connection_packet = livoxsdk.structs.Packet(header=livoxsdk.structs.PacketHeader(
                packet_type=livoxsdk.enums.MessageType.CMD,
                command_type=livoxsdk.enums.GeneralCommandId.Handshake
            ), payload=livoxsdk.payloads.ConnectionRequestPayload(
                ip_address=self.host_ip_address, command_port=self.command_port,
                data_port=self.data_port, sensor_port=self.sensor_port,
            )
        )
        logger.getChild("connect").info("Sending connection request from {} to {}:{} | (cmd: {}, data: {}{})".format(
            self.host_ip_address, self.device_ip_address, livoxsdk.control_port, self.command_port, self.data_port,
            "" if self.sensor_port is None else ", sensor: {}".format(self.sensor_port)))
        response = await self._send_message_response(connection_packet, caller="connect", timeout=timeout)
        ret: ctypes.c_uint8 = response.get_payload()
        if ret.value != 0:
            raise livoxsdk.errors.LivoxConnectionError("Could not connect to {}".format(self.device_ip_address))
        else:
            logger.info("Successfully connected to {}".format(self.device_ip_address))
        self._heartbeat_task = asyncio.get_running_loop().create_task(
            self._heartbeat_function(), name="{} Heartbeat".format(self.device_ip_address))
        return ret

    async def disconnect(self, timeout: typing.Optional[datetime.timedelta] = None) -> ctypes.c_uint8:
        disconnect_packet = livoxsdk.structs.Packet(
            header=livoxsdk.structs.PacketHeader(
                packet_type=livoxsdk.enums.MessageType.CMD,
                command_type=livoxsdk.enums.GeneralCommandId.Disconnect
            )
        )
        response = await self._send_message_response(disconnect_packet, caller="disconnect", timeout=timeout)
        ret: ctypes.c_uint8 = response.get_payload()
        if ret.value != 0:
            raise livoxsdk.errors.LivoxConnectionError("Could not disconnect from {}".format(self.device_ip_address))
        else:
            logger.info("Successfully disconnect from {}".format(self.device_ip_address))
        return ret

    @property
    def firmware_version(self) -> typing.Optional[livoxsdk.FirmwareVersion]:
        return self._firmware_version

    @property
    def mode(self) -> livoxsdk.enums.devices.DeviceState: ...

    @mode.setter
    def mode(self, state: livoxsdk.enums.devices.LidarMode): ...

    @property
    def data(self) -> bool: ...

    @data.setter
    def data(self, state: bool): ...

    @property
    def coordinate_system(self) -> livoxsdk.enums.CoordinateSystem: ...

    @coordinate_system.setter
    def coordinate_system(self, val: livoxsdk.enums.CoordinateSystem): ...

    @property
    def extrinsics(self) -> livoxsdk.structs.Extrinsics: ...

    @extrinsics.setter
    def extrinsics(self, val: livoxsdk.structs.Extrinsics): ...

    @property
    def rain_fog_suppression(self) -> bool: ...

    @rain_fog_suppression.setter
    def rain_fog_suppresssion(self, val: bool): ...

    @property
    def sensor_rate(self): ...

    @sensor_rate.setter
    def sensor_rate(self, val): ...

    @property
    def broadcast_code(self) -> livoxsdk.BroadcastCode: ...

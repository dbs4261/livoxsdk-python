import asyncio
import ctypes
import datetime
import ipaddress
import socket
import typing
from types import TracebackType

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("Device")

_ProtocolT = typing.TypeVar("_ProtocolT", bound=asyncio.DatagramProtocol)
async def _FindDatagramEndpoint(loop: asyncio.AbstractEventLoop,
        protocol_factory: typing.Callable[[], _ProtocolT],
        local_addr: typing.Optional[typing.Tuple[str, int]] = None,
        find_available_port: bool = False, **kwargs) -> tuple[int, asyncio.DatagramTransport, _ProtocolT]:
    kwargs["local_addr"] = local_addr
    if not find_available_port or local_addr is None:
        transport, protocol = await loop.create_datagram_endpoint(protocol_factory, **kwargs)
    else:
        while True:
            try:
                transport, protocol = await loop.create_datagram_endpoint(protocol_factory, **kwargs)
            except OSError:
                logger.getChild("FindDatagramEndpoint").debug(
                    "Could not create port on {}:{}".format(*kwargs["local_addr"]))
                kwargs["local_addr"] = (kwargs["local_addr"][0], kwargs["local_addr"][1] + 1)
            break
        logger.getChild("FindDatagramEndpoint").debug(
            "Created endpoint at {}:{}".format(*kwargs["local_addr"]))
    port: int = transport.get_extra_info("sockname")[1]
    return port, transport, protocol


class Device:
    def __init__(self, device_ip_address: ipaddress.IPv4Address,
                 command_port: typing.Optional[livoxsdk.Port] = None,
                 data_port: typing.Optional[livoxsdk.Port] = None,
                 sensor_port: typing.Optional[livoxsdk.Port] = None,
                 gateway_ip_address: typing.Optional[ipaddress.IPv4Address] = None,
                 default_timeout: datetime.timedelta = datetime.timedelta(milliseconds=500),
                 event_loop: typing.Optional[asyncio.AbstractEventLoop] = None):
        self.default_timeout: datetime.timedelta = default_timeout
        self._device_ip_address: ipaddress.IPv4Address = device_ip_address
        self._gateway_ip_address: ipaddress.IPv4Address = gateway_ip_address
        if self._gateway_ip_address is None:
            self._gateway_ip_address = livoxsdk.utilities.HostIPForDeviceIp(self._device_ip_address)
        if self._gateway_ip_address is None:
            raise ValueError("Could not automatically determine host gateway address "
                             "for communicating with {}".format(self._device_ip_address))
        self._command_port: livoxsdk.Port = command_port if command_port is not None else livoxsdk._default_command_port
        self._data_port: livoxsdk.Port = data_port if data_port is not None else livoxsdk._default_data_port
        self._sensor_port: typing.Optional[livoxsdk.Port] = sensor_port
        self._loop: typing.Optional[asyncio.AbstractEventLoop] = event_loop

        self._command_protocol: typing.Optional[livoxsdk.CommandProtocol] = None
        self._data_protocol: typing.Optional[livoxsdk.DataProtocol] = None
        self._sensor_protocol: typing.Optional[livoxsdk.SensorProtocol] = None

        self._heartbeat_task: typing.Optional[asyncio.Task] = None
        self._state_update_future: typing.Optional[typing.Tuple[livoxsdk.enums.LidarState, asyncio.Future]] = None

        self._firmware_version: typing.Optional[livoxsdk.FirmwareVersion] = None
        self._device_state: livoxsdk.enums.LidarState = livoxsdk.enums.LidarState.Unknown
        self._device_type: typing.Optional[livoxsdk.enums.DeviceType] = None
        self._broadcast_code: livoxsdk.BroadcastCode = livoxsdk.BroadcastCode()
        self._coordinate_system: typing.Optional[livoxsdk.enums.CoordinateSystem] = None
        self._sampling: bool = False

    # <editor-fold desc="Properties">
    @property
    def device_ip_address(self) -> ipaddress.IPv4Address:
        return self._device_ip_address

    @property
    def gateway_ip_address(self) -> ipaddress.IPv4Address:
        return self._gateway_ip_address

    @property
    def command_port(self) -> livoxsdk.Port:
        return self._command_port

    @property
    def data_port(self) -> livoxsdk.Port:
        return self._data_port

    @property
    def sensor_port(self) -> typing.Optional[livoxsdk.Port]:
        return self._sensor_port

    @property
    def firmware_version(self) -> typing.Optional[livoxsdk.FirmwareVersion]:
        return self._firmware_version

    @property
    def state(self) -> livoxsdk.enums.LidarState:
        return self._device_state

    @property
    def coordinate_system(self) -> typing.Optional[livoxsdk.enums.CoordinateSystem]:
        return self._coordinate_system

    @property
    def broadcast_code(self) -> livoxsdk.BroadcastCode:
        return self._broadcast_code

    @property
    def device_type(self) -> livoxsdk.enums.DeviceType:
        if self._device_type is None:
            raise RuntimeError("Device is not yet initialized. Use async with `livoxsdk.Device() as _:`")
        return self._device_type

    # </editor-fold>

    async def _update_device_conn_info(self):
        broadcast_future = self._loop.create_future()
        transport, _ = await self._loop.create_datagram_endpoint(
            lambda: livoxsdk.BroadcastProtocol(broadcast_future, self.device_ip_address),
            family=socket.AF_INET, reuse_port=True, local_addr=("0.0.0.0", livoxsdk.scan_port))
        broadcast_payload: livoxsdk.payloads.BroadcastPayload = \
            await asyncio.wait_for(broadcast_future, 2 * self.default_timeout.total_seconds())
        transport.close()
        self._broadcast_code = broadcast_payload.broadcast_code
        self._device_type = broadcast_payload.device_type
        logger.info("Updated device info for {}: Broadcast Code: {} Device Type: {}".format(
            self.device_ip_address, self._broadcast_code, self._device_type))

    async def __aenter__(self) -> "Device":
        if self._loop is None:
            self._loop = asyncio.get_running_loop()
        device_info_future = self._loop.create_task(self._update_device_conn_info(), name="UpdateDeviceConnectionInfo")
        self._command_port, _, self._command_protocol = await _FindDatagramEndpoint(self._loop,
                lambda: livoxsdk.CommandProtocol(self.command_port), family=socket.AF_INET,
                reuse_port=False, local_addr=(str(self.gateway_ip_address), self._command_port)
        )
        self._data_port, _, self._data_protocol = await _FindDatagramEndpoint(self._loop,
                lambda: livoxsdk.DataProtocol(self.data_port), family=socket.AF_INET,
                reuse_port=False, local_addr=(str(self.gateway_ip_address), self._data_port)
        )
        await device_info_future
        if self.sensor_port is not None:
            if self._sensor_port <= 0:
                self._sensor_port = livoxsdk._default_sensor_port
            self._sensor_port, _, self._sensor_protocol = await _FindDatagramEndpoint(self._loop,
                    lambda: livoxsdk.SensorProtocol(self.sensor_port), family=socket.AF_INET,
                    reuse_port=False, local_addr=(str(self.gateway_ip_address), self.sensor_port)
            )
        return self

    async def __aexit__(self, __exc_type: typing.Optional[typing.Type[BaseException]],
                        __exc_value: typing.Optional[BaseException],
                        __traceback: typing.Optional[TracebackType]) -> typing.Optional[bool]:
        logger.info("Disconnecting from demo")
        try:
            await self.disconnect()
        except livoxsdk.errors.LivoxConnectionError:
            pass
        if self._command_protocol is not None:
            self._command_protocol.close()
        if self._data_protocol is not None:
            self._data_protocol.close()
        if self._sensor_protocol is not None:
            self._sensor_protocol.close()
        return None

    async def _send_message(self, packet: livoxsdk.structs.ControlPacket, caller: str) -> asyncio.Future:
        if self._command_protocol is None or self._command_protocol.transport is None:
            raise RuntimeWarning("No transport!")
        packet.validate()
        future = self._loop.create_future()
        if packet.command_type in self._command_protocol.response_future_table:
            logger.getChild("send_{}".format(caller)).warning(
                "Receive future for {} already exists but will be canceled and replaced".format(packet.command_type))
            self._command_protocol.response_future_table[packet.command_type].cancel("Replaced")
        self._command_protocol.response_future_table[packet.command_type] = future
        logger.getChild("send").getChild(caller).debug("Sending {} to {}:{}".format(
            bytes(packet).hex(), self.device_ip_address, livoxsdk.control_receive_port))
        self._command_protocol.transport.sendto(bytes(packet),
            (str(self.device_ip_address), livoxsdk.control_receive_port))
        return future

    async def send_message(self, packet: livoxsdk.structs.ControlPacket) -> asyncio.Future:
        return await self._send_message(packet, caller="send_message")

    async def _send_message_response(self, packet: livoxsdk.structs.ControlPacket, caller: str,
                                     timeout: typing.Optional[datetime.timedelta] = None
                                     ) -> livoxsdk.structs.ControlPacket:
        if timeout is None:
            timeout = self.default_timeout
        future = await self._send_message(packet, caller=caller)
        response: livoxsdk.structs.ControlPacket = await asyncio.wait_for(future, timeout=timeout.total_seconds())
        logger.getChild("receive").getChild(caller).debug("Received {}".format(response))
        return response

    async def send_message_response(self, packet: livoxsdk.structs.ControlPacket,
                                    timeout: typing.Optional[datetime.timedelta] = None
                                    ) -> livoxsdk.structs.ControlPacket:
        return await self._send_message_response(packet, caller="send_message_response", timeout=timeout)

    async def _heartbeat_function(self, interval: datetime.timedelta = datetime.timedelta(seconds=1),
                                  timeout: typing.Optional[datetime.timedelta] = None):
        logger.getChild("heartbeat").info("Beginning heartbeat...")
        prior_progress = 0
        while True:
            heartbeat_packet = livoxsdk.structs.ControlPacket.CreateCommand(
                livoxsdk.enums.messages.GeneralCommandId.Heartbeat)
            logger.getChild("heartbeat").debug("Sending heartbeat {}".format(heartbeat_packet))
            try:
                response = await self._send_message_response(heartbeat_packet, caller="heartbeat", timeout=timeout)
            except asyncio.TimeoutError as exc:
                raise livoxsdk.errors.LivoxHeartbeatLostError() from exc

            payload: livoxsdk.payloads.HeartbeatResponsePayload = response.get_payload()
            logger.getChild("heartbeat").debug("Heartbeat response: {}".format(payload))
            if payload.ret_code != 0:
                logger.getChild("heartbeat").warning("{} responded incorrectly to heartbeat with ret_code: {}".format(
                    self.device_ip_address, payload))
            else:
                if payload.state == livoxsdk.enums.devices.LidarState.Error:
                    raise livoxsdk.errors.LivoxAbnormalStatusError(
                        "Heartbeat error {} with state {} received from {}\n"
                        "Details: feature: {} progress: {}".format(payload.ret_code, payload.state,
                            self.device_ip_address, payload.feature, payload.error_union.progress))
                elif payload.state == livoxsdk.enums.devices.LidarState.Init:
                    if payload.error_union.progress != prior_progress:
                        prior_progress = payload.error_union.progress
                        logger.info("State change progress: {}%".format(prior_progress))
                else:
                    if prior_progress != 0:
                        logger.info("State change progress: {}%".format(100))
                        prior_progress = 0
                    if self._device_state != payload.state:
                        logger.getChild("heartbeat").info(
                            "Device at {} updated state to {}".format(self.device_ip_address, str(payload.state)))
                    self._device_state = payload.state
                    if self._state_update_future is not None:
                        if self._state_update_future[0] == payload.state or self._state_update_future[0] < 0:
                            self._state_update_future[1].set_result(True)
                            self._state_update_future = None
            await asyncio.sleep(interval.total_seconds())

    async def query(self, timeout: typing.Optional[datetime.timedelta] = None) -> None:
        query_packet = livoxsdk.structs.ControlPacket.CreateCommand(livoxsdk.enums.GeneralCommandId.DeviceInfo)
        response = await self._send_message_response(query_packet, caller="query", timeout=timeout)
        payload: livoxsdk.payloads.QueryResponsePayload = response.get_payload()
        if payload.ret_code != 0:
            raise livoxsdk.errors.LivoxBadRetError("Invalid query result {}".format(payload.ret_code))
        self._firmware_version = payload.firmware_version

    async def connect(self, timeout: typing.Optional[datetime.timedelta] = None) -> ctypes.c_uint8:
        connection_packet = livoxsdk.structs.ControlPacket.CreateCommand(
            livoxsdk.enums.GeneralCommandId.Handshake, livoxsdk.payloads.ConnectionRequestPayload(
                ip_address=self.gateway_ip_address, command_port=self.command_port,
                data_port=self.data_port, sensor_port=self.sensor_port,
            )
        )
        logger.getChild("connect").info("Sending connection request from {} to {}:{} | (cmd: {}, data: {}{})".format(
            self.gateway_ip_address, self.device_ip_address, livoxsdk.control_receive_port, self.command_port,
            self.data_port, "" if self.sensor_port is None else ", sensor: {}".format(self.sensor_port)))
        response = await self._send_message_response(connection_packet, caller="connect", timeout=timeout)
        ret: ctypes.c_uint8 = response.get_payload()
        if ret.value != 0:
            raise livoxsdk.errors.LivoxConnectionError("Could not connect to {}".format(self.device_ip_address))
        else:
            logger.info("Successfully connected to {}".format(self.device_ip_address))
        # Ensure the heartbeat is started before a device query is run
        mode_set_future = self._loop.create_future()
        self._state_update_future = (-1, mode_set_future)
        self._heartbeat_task = asyncio.get_running_loop().create_task(
            self._heartbeat_function(), name="{} Heartbeat".format(self.device_ip_address))
        await mode_set_future
        await self.query(timeout=timeout)
        return ret

    async def disconnect(self, timeout: typing.Optional[datetime.timedelta] = None) -> ctypes.c_uint8:
        disconnect_packet = livoxsdk.structs.ControlPacket.CreateCommand(livoxsdk.enums.GeneralCommandId.Disconnect)
        response = await self._send_message_response(disconnect_packet, caller="disconnect", timeout=timeout)
        ret: ctypes.c_uint8 = response.get_payload()
        if ret.value != 0:
            raise livoxsdk.errors.LivoxConnectionError("Could not disconnect from {}".format(self.device_ip_address))
        else:
            logger.info("Successfully disconnected from {}".format(self.device_ip_address))
        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
        return ret

    async def reboot(self, timeout: typing.Optional[datetime.timedelta] = None):
        reboot_packet = livoxsdk.structs.ControlPacket.CreateCommand(livoxsdk.enums.GeneralCommandId.RebootDevice)
        response = await self._send_message_response(reboot_packet, caller="reboot", timeout=timeout)
        # TODO
        return

    async def ip_info(self, timeout: typing.Optional[datetime.timedelta] = None):
        ip_info_packet = livoxsdk.structs.ControlPacket.CreateCommand(livoxsdk.enums.GeneralCommandId.RebootDevice)
        response = await self._send_message_response(ip_info_packet, caller="ip_info", timeout=timeout)
        # TODO
        return

    async def set_coordinate_system(self, coord: livoxsdk.enums.CoordinateSystem,
                                    timeout: typing.Optional[datetime.timedelta] = None):
        coordinate_system_packet = livoxsdk.structs.ControlPacket.CreateCommand(
            livoxsdk.enums.GeneralCommandId.CoordinateSystem)
        response = await self._send_message_response(
            coordinate_system_packet, caller="coordinate_system", timeout=timeout)
        # TODO
        self._coordinate_system = coord
        return

    async def sampling(self, sampling_state: bool, timeout: typing.Optional[datetime.timedelta] = None):
        sampling_packet = livoxsdk.structs.ControlPacket.CreateCommand(
            livoxsdk.enums.GeneralCommandId.ControlSample, payload=ctypes.c_uint8(int(sampling_state)))
        response = await self._send_message_response(sampling_packet, caller="sampling", timeout=timeout)
        # TODO
        self._sampling = sampling_state
        return

    def is_sampling(self) -> bool:
        return self._sampling

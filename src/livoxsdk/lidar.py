import asyncio
import ctypes
import datetime
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("Lidar")


class Lidar(livoxsdk.Device):
    async def set_mode(self, mode: livoxsdk.enums.LidarMode,
                       timeout: typing.Optional[datetime.timedelta] = None) -> asyncio.Future:
        set_mode_packet = livoxsdk.structs.ControlPacketPacket(
            header=livoxsdk.structs.ControlPacketPacketHeader(
                packet_type=livoxsdk.enums.MessageType.CMD,
                command_type=livoxsdk.enums.LidarCommandId.SetMode,
            ),
            payload=ctypes.c_uint8(mode.value),
        )
        response = await self._send_message_response(set_mode_packet, caller="set_mode", timeout=timeout)
        mode_set_future = self._loop.create_future()
        ret: ctypes.c_uint8 = response.get_payload()
        if ret == 0:
            logger.getChild("set_mode").info("Successfully set mode of {} to {}".format(self.device_ip_address, mode))
            mode_set_future.set_result(True)
        elif ret == 1:
            logger.getChild("set_mode").warning("Failed to set mode of {} to {}".format(self.device_ip_address, mode))
            mode_set_future.set_result(False)
        else:
            logger.getChild("set_mode").debug("SetMode on {} returned {}".format(self.device_ip_address, ret))
            self._state_update_future = (mode, mode_set_future)
        return mode_set_future

    async def make_ready(self, timeout: typing.Optional[datetime.timedelta] = None) -> asyncio.Future:
        return await self.set_mode(livoxsdk.enums.LidarMode.Normal, timeout=timeout)

    async def powersave(self, timeout: typing.Optional[datetime.timedelta] = None) -> asyncio.Future:
        return await self.set_mode(livoxsdk.enums.LidarMode.PowerSaving, timeout=timeout)

    async def standby(self, timeout: typing.Optional[datetime.timedelta] = None) -> asyncio.Future:
        return await self.set_mode(livoxsdk.enums.LidarMode.Standby, timeout=timeout)

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
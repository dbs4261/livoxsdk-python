import asyncio
import ctypes
import datetime
import typing

import livoxsdk


logger = livoxsdk.logging_helpers.logger.getChild("Lidar")


class Lidar(livoxsdk.Device):
    async def set_mode(self, mode: livoxsdk.enums.LidarMode,
                       timeout: typing.Optional[datetime.timedelta] = None) -> None:
        set_mode_packet = livoxsdk.structs.ControlPacket.CreateCommand(
            livoxsdk.enums.LidarCommandId.SetMode, ctypes.c_uint8(mode.value))
        response = await self._send_message_response(set_mode_packet, caller="set_mode", timeout=timeout)
        ret: ctypes.c_uint8 = response.get_payload()
        if ret.value == 0:
            logger.getChild("set_mode").info("Successfully set mode of {} to {}".format(self.device_ip_address, str(mode)))
        elif ret.value == 1:
            logger.getChild("set_mode").error("Failed to set mode of {} to {}".format(self.device_ip_address, str(mode)))
        else:
            logger.getChild("set_mode").debug("SetMode on {} returned {}".format(self.device_ip_address, ret))
            mode_set_future = self._loop.create_future()
            self._state_update_future = (mode, mode_set_future)
            await mode_set_future

    async def make_ready(self, timeout: typing.Optional[datetime.timedelta] = None) -> None:
        return await self.set_mode(livoxsdk.enums.LidarMode.Normal, timeout=timeout)

    async def powersave(self, timeout: typing.Optional[datetime.timedelta] = None) -> None:
        return await self.set_mode(livoxsdk.enums.LidarMode.PowerSaving, timeout=timeout)

    async def standby(self, timeout: typing.Optional[datetime.timedelta] = None) -> None:
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
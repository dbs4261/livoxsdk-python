import asyncio
import contextlib
import datetime
import logging
import typing

import livoxsdk


logger = logging.getLogger("DesiredUsage")

async def powersave(lidar: livoxsdk.Lidar):
    await lidar.connect()
    await lidar.powersave()
    await lidar.disconnect()

async def main(conn_infos: typing.List[livoxsdk.port_scanner.DeviceConnectionInfo]):
    async with contextlib.AsyncExitStack() as device_set:
        devices: typing.List[livoxsdk.Lidar] = \
            [await device_set.enter_async_context(livoxsdk.Lidar(conn_info.ip_address)) for conn_info in conn_infos]
        await asyncio.gather(*[powersave(lidar) for lidar in devices])
    logger.info("Closing demo...")



if __name__ == '__main__':
    import sys
    livoxsdk.logging_helpers.SetupDefaultLogger(None, logging.DEBUG, None)
    if 'pdb' in sys.modules or 'pydevd' in sys.modules:
        debug = True
    else:
        debug = False
    scan_time = datetime.timedelta(seconds=3)
    found_devices = asyncio.run(livoxsdk.port_scanner.scan_for_devices(scan_time), debug=debug)
    if len(found_devices) < 1:
        logger.warning("Didn't find any Livox devices")
    else:
        asyncio.run(main(list(found_devices)), debug=debug)

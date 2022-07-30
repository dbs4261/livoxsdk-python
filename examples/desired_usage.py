import asyncio
import datetime
import ipaddress
import logging
import socket
import typing

import livoxsdk


logger = logging.getLogger("DesiredUsage")


async def main(conn_info: livoxsdk.port_scanner.DeviceConnectionInfo):
    async with livoxsdk.Lidar(conn_info.ip_address) as lidar:
        await lidar.connect()
        logger.info("Query result: {}".format(lidar.firmware_version))
        await lidar.make_ready()
        await lidar.sampling(True)
        await asyncio.sleep(5)
        await lidar.sampling(False)
        await asyncio.sleep(1)
        await lidar.powersave()
        await lidar.disconnect()
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
        raise livoxsdk.port_scanner.NoDevicesDetectedError()
    else:
        asyncio.run(main(list(found_devices)[0]), debug=False)

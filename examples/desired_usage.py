import asyncio
import datetime
import ipaddress
import logging
import socket
import typing

import livoxsdk


logger = logging.getLogger("DesiredUsage")


async def main(conn_info: livoxsdk.port_scanner.DeviceConnectionInfo):
    async with livoxsdk.Device(conn_info.ip_address, livoxsdk.Port(55001), livoxsdk.Port(65001),
                               sensor_port=livoxsdk.Port(60001), event_loop=asyncio.get_running_loop()) as lidar:
        await lidar.connect()
        logger.info("Sleeping...")
        await asyncio.sleep(3)
        logger.info("Query result: {}".format(lidar.firmware_version))
        await asyncio.sleep(3)
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
        asyncio.run(main(list(found_devices)[0]), debug=debug)

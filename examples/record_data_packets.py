import asyncio
import datetime
import functools
import logging
import pathlib
import typing

import livoxsdk


logger = logging.getLogger("RecordXYZFile")


def data_callback(packet: livoxsdk.DataPacket, output_file: typing.BinaryIO, requested_packets: int,
                  completion_future: asyncio.Future) -> None:
    if not hasattr(data_callback, "found_packets"):
        data_callback.found_packets = 0
    if data_callback.found_packets < requested_packets:
        data_callback.found_packets += 1
        output_file.write(bytes(packet))
    else:
        if not completion_future.done():
            completion_future.set_result(True)


async def main(conn_info: livoxsdk.port_scanner.DeviceConnectionInfo,
               output_file: typing.BinaryIO, requested_packets: int):
    async with livoxsdk.Lidar(conn_info.ip_address) as lidar:
        completion_future = asyncio.get_event_loop().create_future()
        lidar.data_callback = functools.partial(data_callback, output_file=output_file,
            requested_packets=requested_packets, completion_future=completion_future)
        await lidar.connect()
        await lidar.set_coordinate_system(livoxsdk.enums.CoordinateSystem.Cartesian)
        await lidar.set_return_mode(livoxsdk.enums.PointCloudReturnMode.FirstReturn)
        logger.info("Query result: {}".format(lidar.firmware_version))
        await lidar.make_ready()
        await lidar.sampling(True)
        await completion_future
        await lidar.sampling(False)
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
    num_packets = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
    search_time = datetime.timedelta(seconds=3)
    found_devices = asyncio.run(livoxsdk.port_scanner.scan_for_devices(search_time), debug=debug)
    outpath = pathlib.Path.cwd().joinpath("livox.bin")
    outpath.unlink(missing_ok=True)
    if len(found_devices) < 1:
        raise livoxsdk.port_scanner.NoDevicesDetectedError()
    else:
        with open(outpath, "wb") as outfile:
            asyncio.run(main(list(found_devices)[0], outfile, num_packets), debug=False)

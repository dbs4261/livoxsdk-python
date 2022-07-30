import asyncio
import datetime
import logging
import math
import pathlib

import livoxsdk


logger = logging.getLogger("RecordXYZFile")


def data_callback(packet: livoxsdk.DataPacket) -> None:
    if packet.header.data_type.coordinate_system.value == livoxsdk.enums.CoordinateSystem.Cartesian:
        for point in packet.payload:
            for sample in point:
                if not sample.valid():
                    continue
                outfile.write("{} {} {}\n".format(
                    sample.x, sample.y, sample.z))
    else:
        for point in packet.payload:
            for sample in point:
                if not sample.valid():
                    continue
                sintheta = math.sin(float(sample.theta) * 0.01 * math.pi / 180.0)
                sinphi = math.sin(float(sample.phi) * 0.01 * math.pi / 180.0)
                costheta = math.cos(float(sample.theta) * 0.01 * math.pi / 180.0)
                cosphi = math.cos(float(sample.phi) * 0.01 * math.pi / 180.0)
                outfile.write("{} {} {}\n".format(
                    float(sample.depth) * cosphi * sintheta,
                    float(sample.depth) * sinphi * sintheta,
                    float(sample.depth) * costheta))


async def main(conn_info: livoxsdk.port_scanner.DeviceConnectionInfo, capture_time: datetime.timedelta):
    async with livoxsdk.Lidar(conn_info.ip_address) as lidar:
        lidar.data_callback = data_callback
        await lidar.connect()
        await lidar.set_coordinate_system(livoxsdk.enums.CoordinateSystem.Cartesian)
        await lidar.set_return_mode(livoxsdk.enums.PointCloudReturnMode.FirstReturn)
        logger.info("Query result: {}".format(lidar.firmware_version))
        await lidar.make_ready()
        await lidar.sampling(True)
        await asyncio.sleep(capture_time.total_seconds())
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
    capture_seconds = float(sys.argv[1]) if len(sys.argv) >= 2 else 5.0
    capture_time = datetime.timedelta(seconds=capture_seconds)
    search_time = datetime.timedelta(seconds=3)
    found_devices = asyncio.run(livoxsdk.port_scanner.scan_for_devices(search_time), debug=debug)
    outpath = pathlib.Path.cwd().joinpath("livox.xyz")
    outpath.unlink(missing_ok=True)
    if len(found_devices) < 1:
        raise livoxsdk.port_scanner.NoDevicesDetectedError()
    else:
        with open(outpath, "wt") as outfile:
            asyncio.run(main(list(found_devices)[0], capture_time), debug=False)

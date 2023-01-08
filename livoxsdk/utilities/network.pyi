import ipaddress
import netifaces
import typing


def compare_hex(a, b): ...

NetworkInterfaces: typing.Mapping[str, ipaddress.IPv4Interface]


# noinspection PyPep8Naming
def HostIPForDeviceIp(device_ip: ipaddress.IPv4Address) -> typing.Optional[ipaddress.IPv4Address]: ...


if __name__ == "__main__":
    print(NetworkInterfaces)

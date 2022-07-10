import ipaddress
import netifaces
import typing


def compare_hex(a, b):
    return a.hex(), b.hex(), "".join("1" if a == b else "0" for a, b in zip(a.hex(), b.hex()))


NetworkInterfaces = {iface: netifaces.ifaddresses(iface) for iface in netifaces.interfaces()}
NetworkInterfaces = {iface: addrs[netifaces.AF_INET] for iface, addrs in NetworkInterfaces.items() if netifaces.AF_INET in addrs}
NetworkInterfaces = {iface: addrs for iface, addrs in NetworkInterfaces.items() if len(addrs) > 0}
NetworkInterfaces = {iface: [ipaddress.ip_interface((addr.get("addr"), addr.get("netmask")))
                      for addr in addrs] for iface, addrs in NetworkInterfaces.items()}


def HostIPForDeviceIp(device_ip: ipaddress.IPv4Address) -> typing.Optional[ipaddress.IPv4Address]:
    if not isinstance(device_ip, ipaddress.IPv4Address):
        raise TypeError
    containing_interfaces = [iface for ifaces in NetworkInterfaces.values() for iface in ifaces
                             if device_ip in iface.network]
    if len(containing_interfaces) == 0:
        return None
    elif len(containing_interfaces) == 1:
        return containing_interfaces[0].ip
    else:
        raise NotImplementedError


if __name__ == "__main__":
    print(NetworkInterfaces)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from scapy.all import *
import ConfigParser


def dhcp_scan():
    conf.checkIPaddr = False
    fam, hw = get_if_raw_hwaddr(conf.iface)
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff") /\
            IP(src="0.0.0.0", dst="255.255.255.255") /\
            UDP(sport=68, dport=67) / BOOTP(chaddr=hw) /\
            DHCP(options=[("message-type", "discover"), "end"])
    ans, unans = srp(dhcp_discover, retry=1, timeout=2)
    mac, ip = (None, None)
    num = 0
    for p in ans:
        num += 1
        (mac, ip) = p[1][Ether].src, p[1][DHCP].options[1][1]
    if num == 0:
        return True
    else:
        return False


def subnet_scan(local, gateway):
    pkts = sniff(filter="arp", count=5, prn=lambda x: x.summary())
    for p in pkts:
        ipa = p.summary().split(" ")[7]
        if ipa != local and ipa != gateway:
            return False
    return True


def gateway_scan(gateway):
    ip, unans = sr(IP(dst=gateway, proto=(0, 255)) / "SCAPY", timeout=0.1)
    arp, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=gateway),
                     timeout=2)
    if len(ip) > 0 and len(arp) > 0:
        return True
    else:
        return False


def get_network_info_from_file():
    config = ConfigParser.ConfigParser()
    network_info = {}
    with open("/tmp/unitedstack.cfg", "rw") as cfgfile:
        config.readfp(cfgfile)
        network_info['subnet'] = config.get("network", "subnet")
        network_info['master'] = config.get("network", "master_ip")
        network_info['gateway'] = config.get("network", "gateway")
        network_info['netmask'] = config.get("network", "netmask")
    return network_info

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from scapy.all import *


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
        print p
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
    network_info = {}
    with open("/etc/sysconfig/network-scripts/ifcfg-master", "r") as cfgfile:
        dic = {}
        strs = cfgfile.read()
        lists = strs.split("\n")
        for li in lists:
            d = li.split("=")
            if len(d) >= 2:
                dic[d[0]] = d[1]
        network_info['subnet'] = dic['NETWORK']
        network_info['master'] = dic['IPADDR']
        network_info['gateway'] = dic['GATEWAY']
        length = 0
        netns = dic['NETMASK'].split('.')
        for netn in netns:
            length += bin(int(netn)).count("1")
        network_info['netmask'] = length
    return network_info

if __name__ == "__main__":
    print get_network_info_from_file()

import json
import logging
import httplib2
import netaddr
from oslo.config import cfg

from mimic.db import api

LOG = logging.getLogger(__name__)


def get_remote_data(url, method, **kwargs):
    h = httplib2.Http(".cache")
    LOG.debug("foreman access url is: %s, method is: %s" % (url, method))
    resp, content = h.request(url, method, **kwargs)
    data = json.loads(content)
    LOG.debug("now get data: %s" % data)
    return data


def operating_system():
    boot_from_local = "BootFromLocal"
    unitedstack_os = "UnitedStackOS"
    systems = get_remote_data("%s/api/operatingsystems" %
                              cfg.CONF.foreman_address, "GET")
    LOG.info("get operating_systems %s" % systems)
    for system in systems:
        if system['operatingsystem']['name'] == boot_from_local:
            boot_from_local_id = system['operatingsystem']['id']
        if system['operatingsystem']['name'] == unitedstack_os:
            unitedstack_os_id = system['operatingsystem']['id']
    return (boot_from_local_id, unitedstack_os_id)


def host_groups():
    hostgroups = get_remote_data("%s/api/hostgroups"
            % cfg.CONF.foreman_address, "GET")
    outgroups = {}
    LOG.info("get host_groups: %s" % host_groups)
    for hostg in hostgroups:
        outgroups[hostg['hostgroup']['name']] = hostg['hostgroup']['id']
    return outgroups


def hosts():
    hosts = get_remote_data("%s/api/hosts" %
                                    cfg.CONF.foreman_address, "GET")
    LOG.info("get hosts: %s" % hosts)
    return hosts


def build_pxe_default():
    data = get_remote_data("%s/api/config_templates/build_pxe_default"
                              % cfg.CONF.foreman_address, "GET")
    LOG.info("build_pxe_default: %s" % data)
    return data


def host_detail(id):
    host_detail = get_remote_data("%s/api/hosts/%s" %
                              (cfg.CONF.foreman_address, id), "GET")
    LOG.info("host detail: %s" % host_detail)
    return host_detail


def unused_ip(mac):
    dbapi = api.get_instance()
    result = dbapi.find_lookup_value_by_match("env=subnet")
    subnet = result[0].value
    ipdata = get_remote_data("%s/dhcp/%s/unused_ip?mac=%s" %
                              (cfg.CONF.foreman_proxy_address,
                               subnet, mac), "GET")
    LOG.info("unused_ip: %s" % ipdata)
    return ipdata['ip']


def create_host(host_info):
    data = {"host": host_info}
    LOG.info("Create Host Info: %s" % host_info)
    hostdata = get_remote_data("%s/api/hosts" % cfg.CONF.foreman_address,
            "POST", body=json.dumps(data),
            headers={'content-type': 'application/json'})
    LOG.info("create host data: %s" % hostdata)
    return hostdata


def update_subnet(net, gate, dhcp_range, master):
    ip = netaddr.IPNetwork(net)
    dhcp_from = dhcp_range.split(" ")[0]
    dhcp_to = dhcp_range.split(" ")[1]
    subnet = {
        "subnet": {
           "network": str(ip.network),
           "mask": str(ip.netmask),
           "gateway": gate,
           "from": dhcp_from,
           "to": dhcp_to,
           "dns_primary": master
        }
    }
    LOG.info("update subnet: %s" % subnet)
    data = get_remote_data("%s/api/subnets/2" %
                              cfg.CONF.foreman_address,
                              "PUT",
                              body=json.dumps(subnet),
                              headers={'content-type': 'application/json'})
    LOG.info("update result: %s" % data)
    return data

import json
import logging
import httplib2
from oslo.config import cfg

from mimic.db import api

LOG = logging.getLogger(__name__)


def operating_system():
    boot_from_local = "BootFromLocal"
    unitedstack_os = "UnitedStackOS"

    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/operatingsystems" %
                              cfg.CONF.foreman_address, "GET")
    systems = json.loads(content)
    for system in systems:
        if system['operatingsystem']['name'] == boot_from_local:
            boot_from_local_id = system['operatingsystem']['id']
        if system['operatingsystem']['name'] == unitedstack_os:
            unitedstack_os_id = system['operatingsystem']['id']
    return (boot_from_local_id, unitedstack_os_id)


def host_groups():
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/hostgroups"
            % cfg.CONF.foreman_address, "GET")
    hostgroups = json.loads(content)
    outgroups = {}
    for hostg in hostgroups:
        outgroups[hostg['hostgroup']['name']] = hostg['hostgroup']['id']
    return outgroups


def hosts():
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/hosts" % cfg.CONF.foreman_address, "GET")
    hosts = json.loads(content)
    return hosts


def build_pxe_default():
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/config_templates/build_pxe_default"
                              % cfg.CONF.foreman_address, "GET")
    return content


def host_detail(id):
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/hosts/%s" %
                              (cfg.CONF.foreman_address, id), "GET")
    host = json.loads(content)
    return host


def unused_ip(mac):
    dbapi = api.get_instance()
    result = dbapi.find_lookup_value_by_match("env=subnet")
    subnet = result[0].value
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/dhcp/%s/unused_ip?mac=%s" %
                              (cfg.CONF.foreman_proxy_address,
                               subnet, mac), "GET")
    ip = json.loads(content)['ip']
    return ip


def create_host(host_info):
    h = httplib2.Http(".cache")
    data = {"host": host_info}
    LOG.info("Create Host Info: %s" % host_info)
    resp, content = h.request("%s/api/hosts" % cfg.CONF.foreman_address,
            "POST", body=json.dumps(data),
            headers={'content-type': 'application/json'})
    return content

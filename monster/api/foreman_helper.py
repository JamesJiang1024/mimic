import json
import urllib
import httplib2

from monster.openstack.common import cfg


(boot_from_local_id, unitedstack_os_id) = find_operationg_system()

def inform_foreman(disks, mac):
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/hosts" % cfg.CONF.foreman_address, "GET")
    hosts = json.loads(content)
    origin_mac = mac
    change_id = 0
    for host in hosts:
        host_id = host['host']['id']
        resp, content = h.request("%s/api/hosts/%s" % (cfg.CONF.foreman_address, host_id), "GET")
        host_detail = json.loads(content)
        new_mac = host_detail['host']['mac']
        for origin_macd in origin_mac:
            if new_mac.upper() == origin_macd.upper():
                change_id = host_id
                put_data = {
                "host":{
                    "build": True,
                    "disk": disks,
                    "operatingsystem_id": "4"
                }
               }
                resp, content = h.request("http://192.168.1.2:3000/api/hosts/%s" % \
                change_id, "PUT", body=json.dumps(put_data), \
                headers={'content-type': 'application/json'} )
                return True
    return False

def build_host_to_foreman(operatingsystem, disk_info, hardware_info):
    h = httplib2.Http(".cache")
    foreman_address = cfg.CONF.foreman_address
    return "ok"

def find_operationg_system():
    boot_from_local = "CentOS-Live"
    unitedstack_os = "Ubuntu"

    h = httplib2.Http(".cache")
    resp, content = h.request("%s/api/operatingsystems" % cfg.CONF.foreman_address, "GET")
    systems = json.loads(content)
    for system in systems:
        if system['operatingsystem']['name'] == boot_from_local:
            boot_from_local_id = system['operatingsystem']['id']
        if system['operatingsystem']['name'] == unitedstack_os:
            unitedstack_os_id = system['operatingsystem']['id']
    return (boot_from_local_id, unitedstack_os_id)


if __name__ == "__main__":
    print find_operationg_system()



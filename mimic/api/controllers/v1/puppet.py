import commands
import subprocess
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import manager


puppet_status = [
    {'service': 'begin', 'status': False},
    {'service': 'nova-api', 'status': False},
    {'service': 'nova-scheduler', 'status': False},
    {'service': 'nova-conductor', 'status': False},
    {'service': 'nova-compute', 'status': False},
    {'service': 'ceilometer-api', 'status': False},
    {'service': 'messagebus', 'status': False},
    {'service': 'libvirt', 'status': False},
    {'service': 'finished', 'status': False}
 ]


class PuppetController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        result1, mac = commands.\
                getstatusoutput("ifconfig br100 | awk '/HWaddr/{ print $5 }'")
        result1, ip = commands.\
                getstatusoutput("ifconfig br100 | "
                                "awk '/inet addr:/{ print $2 }' "
                                "| awk -F: '{print $2 }'")
        data = manager.build_host_data(mac, "no", ip, build=False)
        subprocess.Popen("puppet agent -vt >> /tmp/master_puppet.log",
                         shell=True)
        return data

    @wsme_pecan.wsexpose(unicode)
    def get_all(self):
        return puppet_status

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def put(self, content):
        for puppet_s in puppet_status:
            if puppet_s['service'] == content['service']:
                puppet_s['status'] = True
        return puppet_status

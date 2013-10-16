import commands
import subprocess
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import manager


puppet_status = [
    {'service': 'uos-preinstall', 'status': False},
    {'service': 'messagebus', 'status': False},
    {'service': 'libvirt', 'status': False},
    {'service': 'tgtd', 'status': False},
    {'service': 'nova-api', 'status': False},
    {'service': 'nova-compute', 'status': False},
    {'service': 'nova-network', 'status': False},
    {'service': 'glance-api', 'status': False},
    {'service': 'glance-registry', 'status': False},
    {'service': 'cinder-api', 'status': False},
    {'service': 'cinder-volume', 'status': False},
    {'service': 'swift-container-rep', 'status': False},
    {'service': 'swift-account-auditor', 'status': False},
    {'service': 'swift-object', 'status': False},
    {'service': 'ceilometer-api', 'status': False},
    {'service': 'ceilometer-agent-central', 'status': False},
    {'service': 'ceilometer-collector', 'status': False},
    {'service': 'terminator-server', 'status': False},
    {'service': 'uos-cleanup', 'status': False}
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

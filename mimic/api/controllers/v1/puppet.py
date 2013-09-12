import commands
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import manager


puppet_status = [
    {'service': 'begin', 'status': True},
    {'service': 'nova-api', 'status': True},
    {'service': 'nova-scheduler', 'status': True},
    {'service': 'nova-conductor', 'status': True},
    {'service': 'nova-compute', 'status': True},
    {'service': 'ceilometer-api', 'status': True},
    {'service': 'ustack-mimic-api', 'status': True},
    {'service': 'ustack-placebo', 'status': True},
    {'service': 'messagebus', 'status': True},
    {'service': 'libvirt', 'status': True},
    {'service': 'finished', 'status': True}
 ]


class PuppetController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        result1, mac = commands.\
                getstatusoutput("ifconfig master | awk '/HWaddr/{ print $5 }'")
        result1, ip = commands.\
                getstatusoutput("ifconfig master | "
                                "awk '/inet addr:/{ print $2 }' "
                                "| awk -F: '{print $2 }'")
        data = manager.build_host_data(mac, "no", ip)
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

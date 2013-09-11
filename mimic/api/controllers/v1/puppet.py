import commands
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import manager


puppet_status = [
    {'begin': False},
    {'nova-api': False},
    {'nova-scheduler': False},
    {'nova-conductor': False},
    {'nova-compute': False},
    {'ceilometer-api': False},
    {'ustack-mimic-api': False},
    {'ustack-placebo': False},
    {'messagebus': False},
    {'libvirt': False},
    {'finished': False}
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
        result1, result2 = commands.\
                getstatusoutput('puppet agent -vt >> /tmp/master_puppet.log')
        return data

    @wsme_pecan.wsexpose(unicode)
    def get_all(self):
        return puppet_status

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def put(self, content):
        for puppet_s in puppet_status:
            if content['service'] in puppet_s:
                puppet_s[content['service']] = True
        return puppet_status

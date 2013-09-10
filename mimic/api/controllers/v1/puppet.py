import commands
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import manager


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

from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.openstack.common import log as logging
from mimic.engine import manager


LOG = logging.getLogger(__name__)


class NodeController(rest.RestController):
    """Version 1 API controller Node."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        mac = content['mac']
        if not mac:
            return False
        local = content['local']
        ip = None
        if content.has_key("ip"):
            ip = content['ip']
        return manager.build_host_data(mac, local, ip)

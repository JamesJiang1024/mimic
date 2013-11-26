from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.openstack.common import log as logging
from mimic.engine import manager


LOG = logging.getLogger(__name__)


class NodeController(rest.RestController):
    """Version 1 API controller Node."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        LOG.info("post data to create node, content is: %s" % content)
        mac = content['mac']
        if not mac:
            return False
        local = content['local']
        ip = None
        if "ip" in content:
            ip = content['ip']
        #TODO(wentian): judge if first node is created by puppet agent
        return manager.build_host_data(mac, local, ip)

from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import keystone_helper
from mimic.openstack.common import log as logging


LOG = logging.getLogger(__name__)


class UserController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        LOG.info("create user with username: %s" % content['username'])
        result = keystone_helper.\
                create_admin(content['username'], content['password'])
        LOG.info("create user result: %s" % result)
        return "{'result': 'ok'}"

from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import keystone_helper


class UserController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        resp, content = keystone_helper.\
                create_admin(content['username'], content['password'])
        return resp, content

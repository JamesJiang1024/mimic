import commands
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan


class PuppetController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        result1, result2 = commands.getstatusoutput('puppet agent -vt')
        return result2

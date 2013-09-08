import commands
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan


class SwitchController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def put(self, status):
        scanning = status['scanning']
        if scanning:
            commands.\
                getstatusoutput("cat /etc/mimic/pxe.template "
                                "> /var/lib/tftpboot/pxelinux.cfg/default")
        else:
            commands.\
                getstatusoutput("cat /etc/mimic/local.template "
                                "> /var/lib/tftpboot/pxelinux.cfg/default")
        return status

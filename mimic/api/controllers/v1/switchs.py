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

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_all(self):
        flag, answer_local = commands.\
                getstatusoutput("cat /etc/mimic/local.template")
        flag, answer_pxe = commands.\
                getstatusoutput("cat /etc/mimic/pxe.template")
        flag, answer_status = commands.\
                getstatusoutput("cat /var/lib/tftpboot/pxelinux.cfg/default")

        result = {}
        if answer_local == answer_status:
            result = {
                "lock": False
            }
        else:
            result = {
                "lock": True
            }

        return result

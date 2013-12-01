import commands
import subprocess
from pecan import rest
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.engine import manager

from mimic.openstack.common import log
from oslo.config import cfg

puppet_opts = [
    cfg.StrOpt('mimic_internal_interface',
               default='br100',
               help='mimic internal interface'),
    cfg.ListOpt('uos_status_modules',
                default=[
                      'tgtd',
                      'nova-api',
                      'nova-compute',
                      'nova-network',
                      'glance-api',
                      'glance-registry',
                      'cinder-api',
                      'cinder-volume',
                      'swift-account-auditor',
                      'swift-container-rep',
                      'swift-object',
                      'ceilometer-api',
                      'ceilometer-agent-central',
                      'ceilometer-collector'
     ])
]

LOG = log.getLogger(__name__)

CONF = cfg.CONF
CONF.register_opts(puppet_opts)


def merge_service_to_status(puppet_status):
    status_modules = CONF.uos_status_modules
    puppet_status.append({'service': 'uos-preinstall', 'status': False})

    for status in status_modules:
        puppet_status.append({'service': status, 'status': False})

    puppet_status.append({'service': 'uos-cleanup', 'status': False})
    return puppet_status

puppet_status = merge_service_to_status([])


class PuppetController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        mac_command = "ifconfig %s | awk '/HWaddr/{ print $5 }'" % \
                CONF.mimic_internal_interface
        ip_command = "ifconfig %s | awk '/inet addr:/{ print $2 }' | awk -F: '{print $2 }'" % CONF.mimic_internal_interface

        LOG.info("execute commands to get %s mac: %s" %
                 (CONF.mimic_internal_interface, mac_command))
        LOG.info("execute commands to get %s ip: %s" %
                 (CONF.mimic_internal_interface, ip_command))

        result1, mac = commands.getstatusoutput(mac_command)
        result1, ip = commands.getstatusoutput(ip_command)

        LOG.info("create first machine, mac: %s , ip: %s" % (mac, ip))
        data = manager.build_host_data(mac, "no", ip, build=False)

        LOG.info("create first machine finished begin to configuration")
        subprocess.Popen("puppet agent -vt >> %s" %
                         CONF.uos_install_stage2_log,
                         shell=True)
        return data

    @wsme_pecan.wsexpose(unicode)
    def get_all(self):
        LOG.info("now puppet status are: %s" % puppet_status)
        return puppet_status

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def put(self, content):
        LOG.info("now puppet status are: %s" % puppet_status)
        for puppet_s in puppet_status:
            if puppet_s['service'] == content['service']:
                puppet_s['status'] = True
        return puppet_status

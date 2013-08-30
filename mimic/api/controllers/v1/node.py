from pecan import rest
from oslo.config import cfg
from mimic.openstack.common import jsonutils

from mimic.engine import foreman_helper
from mimic.db import api
from mimic.engine import judgement
from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.openstack.common import log as logging
from mimic.engine.driver import base

LOG = logging.getLogger(__name__)
mc = {}

policy_opts = [
    cfg.StrOpt('policy',
               default='/etc/mimic/policy.json',
               help='make policy.json')
]
CONF = cfg.CONF
CONF.register_opts(policy_opts)


class NodeController(rest.RestController):
    """Version 1 API controller Node."""

    def _load_drivers(self):
        po = file(CONF.policy)
        policys = jsonutils.load(po)
        drivers = []
        for key in policys:
            lookup_key_id = policys[key]['key']
            format = policys[key]['format']
            driver = base.get_instance(policys[key]['driver'])
            drivers.append(driver.get_backend(lookup_key_id, format))
        return drivers

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        dbapi = api.get_instance()
        mac = content['mac']
        local = content['local']
        ip = None
        if content.has_key("ip"):
            ip = content['ip']
        hosts_num = foreman_helper.hosts() or {}
        if not ip:
            ipaddr = foreman_helper.unused_ip(mac)
        else:
            ipaddr = ip
        host_info = {
            'name': "us" + str(len(hosts_num) + 1),
            'ip': ipaddr,
            'mac': mac,
            'build': True
        }
        if local == "no":
            hostgroup_id = judgement.judge_hostgroup()
        else:
            hostgroup_id = foreman_helper.host_groups()['local']

        drivers = self._load_drivers()
        host_info['hostgroup_id'] = hostgroup_id
        for driver in drivers:
            driver.action(len(hosts_num) + 1, host_info['name'], ip=ipaddr)
        LOG.info("Server To Post: %s" % host_info)
        return jsonutils.loads(foreman_helper.create_host(host_info))

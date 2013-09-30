import logging

from oslo.config import cfg
from mimic.engine import foreman_helper
from mimic.engine import judgement
from mimic.openstack.common import jsonutils
from mimic.engine.driver import base

policy_opts = [
    cfg.StrOpt('policy',
               default='/etc/mimic/policy.json',
               help='make policy.json')
]
CONF = cfg.CONF
CONF.register_opts(policy_opts)

LOG = logging.getLogger(__name__)


def build_host_data(mac, local, ip, build=True):
    hosts_num = foreman_helper.hosts() or {}
    if not ip:
        ipaddr = foreman_helper.unused_ip(mac)
    else:
        ipaddr = ip

    if len(hosts_num) == 0:
        hostname = "master"
    else:
        hostname = "us" + str(len(hosts_num) + 1)

    host_info = {
        'name': hostname,
        'ip': ipaddr,
        'mac': mac,
        'build': build
    }
    hg = foreman_helper.host_groups()
    role = "master"
    if local == "no":
        hostgroup_id = judgement.judge_hostgroup()
    else:
        hostgroup_id = hg['local']
    for ro in hg:
        if hg[ro] == hostgroup_id:
            role = ro

    drivers = _load_drivers()
    host_info['hostgroup_id'] = hostgroup_id
    for driver in drivers:
        if role == driver.role:
            driver.action(len(hosts_num) + 1, host_info['name'], ip=ipaddr)
    LOG.info("Server To Post: %s" % host_info)
    return jsonutils.loads(foreman_helper.create_host(host_info))


def _load_drivers():
    po = file(CONF.policy)
    policys = jsonutils.load(po)
    drivers = []
    for key in policys:
        format = policys[key]['format']
        role = policys[key]['role']
        classes = policys[key]['class']
        driver = base.get_instance(policys[key]['driver'])
        drivers.append(driver.get_backend(key, format, classes, role))
    return drivers

import commands
from pecan import rest
from mimic.db import api
from mimic.engine import foreman_helper
from mimic.openstack.common import log as logging
from mimic.engine import network_scanning as network_scan
from mimic.common.wsmeext import pecan as wsme_pecan


LOG = logging.getLogger(__name__)


class NetworkController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        """
        post foreman information
        """
        result = {}
        param_list = ['dhcp_range', 'subnet', 'fixed_range']

        for param in param_list:
            self._update_env_key_value(param, content[param])
            result[param] = content[param]

        self._update_env_key_value("reserve_bottom",
                                   content['dhcp_range'].split(" ")[1])

        result['reserve_bottom'] = content['dhcp_range'].split(" ")[1]
        foreman_helper.build_pxe_default()

        return result

    def _update_network_info(self):
        network_info = network_scan.get_network_info_from_file()
        for ni in network_info:
            self._update_env_key_value(ni, network_info[ni])

    @wsme_pecan.wsexpose(unicode)
    def get(self):
        """
        get global infomation of unitedstack os from foreman db

        """
        self._update_network_info()
        dbapi = api.get_instance()
        networklist = {
            "dhcp_range": None,
            "subnet": None,
            "netmask": None,
            "gateway": None,
            "master": None
        }
        for network in networklist:
            value = dbapi.find_lookup_value_by_match("env=%s" % network)
            if len(value) > 0:
                if network != "netmask":
                    networklist[network] = value[0].value
                else:
                    networklist[network] = int(value[0].value)
        return networklist

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_one(self, status):
        """
        scanning network status

        scan if dhcp is exist, gateway is ok and subnet can be used
        """
        dbapi = api.get_instance()
        try:
            gateway = dbapi.find_lookup_value_by_match("env=gateway")[0].value
            master = dbapi.\
                    find_lookup_value_by_match("env=master")[0].value
        except:
            return {
                "error": "system error with no master and gateway"
            }
        LOG.info("Begin to scanning network")
        dhcp_status = network_scan.dhcp_scan()
        LOG.info("Scanning DHCP")
        gateway_status = network_scan.gateway_scan(gateway)
        LOG.info("Scanning Gateway")
        #subnet_status = network_scan.subnet_scan(gateway, master)
        LOG.info("Scanning Subnet")
        subnet_status = True
        result = {
            "dhcp_status": dhcp_status,
            "gateway_status": gateway_status,
            "subnet_status": subnet_status
        }
        return result

    def _update_env_key_value(self, key, value):
        """
        update the global parameter key and value

        key: global parameter key
        value: global parameter value
        """

        dbapi = api.get_instance()
        lookup_values = {
            "match": "env=%s" % key,
            "value": value,
            "lookup_key_id": 10000
        }
        result = dbapi.find_lookup_value_by_match("env=%s" % key)
        if len(result) > 0:
            dbapi.update_lookup_value(result[0].id, lookup_values)
        else:
            dbapi.create_lookup_value(lookup_values)
        return lookup_values

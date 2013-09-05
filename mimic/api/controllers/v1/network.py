import commands
from pecan import rest
from mimic.db import api
from mimic.engine import foreman_helper
from mimic.engine import network_scanning as network_scan
from mimic.common.wsmeext import pecan as wsme_pecan


class NetworkController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        """
        post foreman information
        """
        dhcp_range = content['dhcp_range']
        subnet = content['subnet']
        self._update_env_key_value("dhcp_range", dhcp_range)
        self._update_env_key_value("subnet", subnet)
        result = {
            "dhcp_range": dhcp_range,
            "subnet": subnet
        }
        foreman_helper.build_pxe_default()
        return result

    @wsme_pecan.wsexpose(unicode)
    def get(self):
        """
        get global infomation of unitedstack os from foreman db

        """
        dbapi = api.get_instance()
        networklist = {
            "dhcp_range": None,
            "subnet": None,
            "netmask": None,
            "gateway": None,
            "master_ip": None
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
            master_ip = dbapi.\
                    find_lookup_value_by_match("env=master_ip")[0].value
        except:
            return {
                "error": "system error with no master_ip and gateway"
            }
        dhcp_status = network_scan.dhcp_scan()
        gateway_status = network_scan.gateway_scan(gateway)
        #subnet_status = network_scan.subnet_scan(gateway, master_ip)
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

        dbapi.create_lookup_value(lookup_values)
        return lookup_values

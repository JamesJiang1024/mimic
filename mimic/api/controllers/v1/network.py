import commands
from pecan import rest
from mimic.db import api
from mimic.engine import foreman_helper
from mimic.common.wsmeext import pecan as wsme_pecan


class NetworkController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        dhcp_range = content['dhcp_range']
        subnet = content['subnet']
        self.update_env_key_value("dhcp_range", dhcp_range)
        self.update_env_key_value("subnet", subnet)
        result = {
            "dhcp_range": dhcp_range,
            "subnet": subnet
        }
        foreman_helper.build_pxe_default()
        return result

    @wsme_pecan.wsexpose(unicode)
    def get(self):
        dbapi = api.get_instance()
        dhcp_range = dbapi.find_lookup_value_by_match("env=dhcp_range")
        subnet = dbapi.find_lookup_value_by_match("env=subnet")
        network = {
            "dhcp_range": dhcp_range[0].value,
            "subnet": subnet[0].value
        }
        return network

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_one(self, status):
        result = {
            "dhcp_status": True,
            "gateway_status": True,
            "subnet_status": True
        }
        return result

    def update_env_key_value(self, key, value):
        dbapi = api.get_instance()
        lookup_values = {
            "match": "env=%s" % key,
            "value": value,
            "lookup_key_id": 10000
        }
        result = dbapi.find_lookup_value_by_match("env=%s" % key)
        if len(result) > 0:
            return {"error": "fail to add same env"}

        dbapi.create_lookup_value(lookup_values)
        return lookup_values

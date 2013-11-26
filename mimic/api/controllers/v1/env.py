from pecan import rest
from mimic.db import api
from mimic.openstack.common import log as logging
from mimic.common.wsmeext import pecan as wsme_pecan


LOG = logging.getLogger(__name__)


class EnvController(rest.RestController):
    """Version 1 API controller Node."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):

        key = content['key']
        value = content['value']
        LOG.info("new env parameter input, key: %s, value: %s" % (key, value))

        dbapi = api.get_instance()
        lookup_values = {
            "match": "env=%s" % key,
            "value": value,
            "lookup_key_id": 10000
        }
        result = dbapi.find_lookup_value_by_match("env=%s" % key)
        LOG.info("find env in database: %s" % result)

        if len(result) > 0:
            return {"error": "fail to add same env"}

        dbapi.create_lookup_value(lookup_values)
        LOG.info("env created: %s" % lookup_values)
        return lookup_values

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_one(self, match):
        dbapi = api.get_instance()
        result = dbapi.find_lookup_value_by_match("env=%s" % match)
        LOG.info("find env: %s" % result)
        if len(result) > 0:
            return result[0]["value"]

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def put(self, content):
        result = self._update_env_key_value(content['key'], content['value'])
        LOG.info("update env into database %s" % result)
        return True

    def _update_env_key_value(self, key, value):
        """
        update the global parameter key and value

        key: global parameter key
        value: global parameter value
        """
        LOG.debug("begin to update env")
        dbapi = api.get_instance()
        lookup_values = {
            "match": "env=%s" % key,
            "value": value,
            "lookup_key_id": 10000
        }
        result = dbapi.find_lookup_value_by_match("env=%s" % key)
        LOG.debug("find env in database: %s" % result)
        if len(result) > 0:
            dbapi.update_lookup_value(result[0].id, lookup_values)
        else:
            dbapi.create_lookup_value(lookup_values)
        return lookup_values

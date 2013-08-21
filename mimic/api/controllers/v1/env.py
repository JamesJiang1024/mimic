from pecan import rest
from mimic.db import api
from mimic.common.wsmeext import pecan as wsme_pecan


class EnvController(rest.RestController):
    """Version 1 API controller Node."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, content):
        key = content['key']
        value = content['value']
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

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_one(self, match):
        dbapi = api.get_instance()
        result = dbapi.find_lookup_value_by_match("env=%s" % match)
        return result[0]["value"]

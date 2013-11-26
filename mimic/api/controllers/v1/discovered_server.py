from pecan import rest

from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.openstack.common import log as logging
from wsme import types as wtypes
from mimic.api.controllers.v1 import base
from mimic.db import api as api


LOG = logging.getLogger(__name__)
mc = {}


class DiscoveredServer(base.APIBase):
    uuid = wtypes.text
    cpu = wtypes.text
    memory = wtypes.text
    harddisk = wtypes.text
    discovered_mac = wtypes.text


class DiscoveredServerController(rest.RestController):
    """Version 1 API controller DiscoveredServer."""

    def check_create_input(self, inputs):
        standard = {
                    'uuid': True,
                    'cpu': True,
                    'memory': True,
                    'harddisk': True,
                    'discovered_mac': True
                    }

        for ins in inputs:
            ri = standard.pop(ins)
            if ri is None:
                return False

        if standard != {}:
            return False
        return True

    @wsme_pecan.wsexpose(unicode, unicode, unicode)
    def get_one(self, server_id):
        LOG.info("find by serverid: %s" % str(server_id))
        server = mc.get(str(server_id))
        LOG.info("get discovered_server from cache: %s" % server)
        return {"data": server}

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_all(self):
        # info from cache
        discovered_cache = mc.get("discovered_new") or []

        LOG.info("get discovered server list from cache: %s"
                 % discovered_cache)
        for server in discovered_cache:
            server['status'] = "pendding"
            mc[str(server['uuid'])] = server

        LOG.info("now memory is: %s" % mc)

        # reset cache
        result = mc.get("discovered_new")
        mc["discovered_new"] = []

        if not result:
            result = []

        return {"data": result}

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def post(self, discovered_server):

        if not self.check_create_input(discovered_server):
            return False
        LOG.info("new server being discovered: %s" % discovered_server)

        #read data from cache
        discovered_cache = mc.get("discovered_new") or []

        LOG.debug("now cache are %s" % discovered_cache)
        #append server to cache
        name = "HD" + str(len(discovered_cache))
        discovered_server['name'] = name
        LOG.debug("now append new server to cache")
        discovered_cache.append(discovered_server)
        mc["discovered_new"] = discovered_cache
        LOG.info("now cache are: %s" % discovered_cache)

        return {"data": discovered_cache}

    @wsme_pecan.wsexpose(unicode, unicode, unicode, body=unicode)
    def put(self, server_id, delta):
        server = mc.get(str(server_id))
        LOG.info("update discovered server status before: %s" % server)

        server['status'] = delta['status']
        mc[str(server_id)] = server
        LOG.info("update discovered server status after: %s" % server)
        return {"data": server}

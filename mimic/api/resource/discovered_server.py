# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Sina Corporation
# All Rights Reserved.
# Author: jiangwt100 <jiangwt100@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from mimic.openstack.common import log as logging
from mimic.openstack.common import wsgi

from mimic.api import controller


LOG = logging.getLogger(__name__)
mc = {}


class Controller(controller.Controller):

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

    def index(self, req, **kwargs):
        # info from cache
        discovered_cache = mc.get("discovered_new") or []

        LOG.info("Get discovered Server Into Cache: %s" % discovered_cache)
        for server in discovered_cache:
            server['status'] = "pendding"
            mc[str(server['uuid'])] = server

        # reset cache
        result = mc.get("discovered_new")
        mc["discovered_new"] = {}
        return {"data": result}

    def create(self, req, **kwargs):
        #check if inputs is ok
        discovered_server = kwargs['body']
        if not self.check_create_input(discovered_server):
            return False
        LOG.info("New Server Being discovered: %s" % discovered_server)

        #discover new machine

        #read data from cache
        discovered_cache = mc.get("discovered_new") or []

        #append server to cache
        name = "HD" + str(len(discovered_cache))
        discovered_server['name'] = name
        discovered_cache.append(discovered_server)
        mc["discovered_new"] = discovered_cache
        LOG.info("Now Cached Servers: %s" % discovered_cache)

        return {"data": discovered_cache}

    def update(self, req, **kwargs):

        server_id = kwargs['id']
        server = mc.get(str(server_id))
        LOG.info("Update discovered Server Status Before: %s" % server)

        server['status'] = kwargs['body']['status']
        mc[str(server_id)] = server
        LOG.info("Update discovered Server Status After: %s" % server)

        return {"data": server}

    def show(self, req, **kwargs):
        server_id = kwargs['id']
        server = mc.get(str(server_id))
        return {"data": server}


def create_resource():
    return wsgi.Resource(Controller())

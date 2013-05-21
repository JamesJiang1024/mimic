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
import memcache

from monster.openstack.common import log as logging
from monster.openstack.common import wsgi
from monster.openstack.common import cfg

from monster.api import controller


LOG = logging.getLogger(__name__)


class Controller(controller.Controller):

    def check_create_input(self, inputs):
        standard = {
                    'cpu': True,
                    'memory': True,
                    'harddisk': True,
                    'discoveried_mac': True
                    }

        if inputs['uuid'] == None or inputs['detail'] == None:
            return False

        for ins in inputs['detail']:
            ri = standard.pop(ins)
            if ri == None:
                return False

        if standard != {}:
            return False
        return True


    def index(self, req, **kwargs):
        mc = memcache.Client([cfg.CONF.memcache_address])
        discoveried_cache = mc.get("discoveried_new") or {}

        LOG.info("Get Discoveried Server Into Cache: %s" % discoveried_cache)
        for server in discoveried_cache:
            discoveried_cache[str(server)]['status'] = "pendding"
            mc.set(str(server), discoveried_cache[str(server)])
        result = mc.get("discoveried_new")
        mc.set("discoveried_new", {})
        return result

    def create(self, req, **kwargs):
        discoveried_server = kwargs['body']
        if not self.check_create_input(discoveried_server):
            return False

        LOG.info("New Server Being Discoveried: %s" % discoveried_server)
        mc = memcache.Client([cfg.CONF.memcache_address])
        discoveried_cache = mc.get("discoveried_new")
        name = "HD" + str(len(discoveried_cache))
        if discoveried_cache == None:
            discoveried_cache = {}

        discoveried_server['detail']['name'] = name
        discoveried_cache[discoveried_server['uuid']] = discoveried_server['detail']
        mc.set("discoveried_new", discoveried_cache)
        LOG.info("Now Cached Servers: %s" % discoveried_cache)
        return discoveried_cache

    def update(self, req, **kwargs):
        mc = memcache.Client([cfg.CONF.memcache_address])

        server_id = kwargs['id']
        server = mc.get(str(server_id))
        LOG.info("Update Discoveried Server Status Before: %s" % server)

        server['status'] = kwargs['body']['status']
        mc.set(str(server_id), server)
        LOG.info("Update Discoveried Server Status After: %s" % server)

        return server

    def show(self, req, **kwargs):
        mc = memcache.Client([cfg.CONF.memcache_address])
        server_id = kwargs['id']
        server = mc.get(str(server_id))
        return server

def create_resource():
    return wsgi.Resource(Controller())
